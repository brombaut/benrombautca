*A note on the charts: they come straight out of my own experiment
records, so their titles and labels carry numbering like "Experiment
020" and "Phase 3" that only means something inside my notes. Feel free
to ignore that part; the axes and the curves are what matter here.*

My last post was about adding a Mixture of Experts layer, and it ended on a
list of things I wanted to try next that had nothing to do with the
architecture at all: learning rate schedules, the difference between Adam and
AdamW, dropout, batch size, and reduced precision. The model was going to stay
exactly where it was. The only thing changing was how it got trained.

I expected this to be the tidy part. Every one of those decisions has a
standard recommendation attached to it, and I mostly wanted to watch the
recommendations come true on a model small enough to run the comparison in an
afternoon.

Six of the seven things I ran did not come out the way I expected, and they
were all wrong in the same shape. I would change one setting, get a result, and
find out later that the setting I changed had quietly dragged a second one
along with it. Two of the results reversed completely once I pinned that second
thing down. So this post is less about what learning rate schedules do than
about how hard it turned out to be to change exactly one thing.

## The Model That Would Not Overfit

Before comparing anything I needed a baseline that overfits. Half the decisions
on my list are regularizers, and a regularizer has nothing to show you on a
model that is still underfitting.

Two numbers carry the rest of this post. Training loss is how well the model
predicts the text it is being trained on. Validation loss is the same
measurement on a slice of text held back and never trained on. Overfitting is
when the first keeps improving while the second stops and starts getting
worse: the model is learning the specific text in front of it rather than the
language in it. The distance between the two is the generalization gap. A
regularizer is anything that makes memorizing harder — dropout and weight
decay are the two in this post.

My first attempt was a 1.7 million parameter model on an 8 MiB slice of
TinyStories. Training and validation loss tracked each other the whole run with
no gap at all. So I did the obvious thing and made the model bigger: 5.8
million parameters, a 10 MiB slice, three passes over the data. Validation loss
finished *below* training loss.

The thing that finally worked was making the dataset smaller. I swapped
TinyStories for Tiny Shakespeare, the same roughly one megabyte of text
Karpathy's char-rnn uses, and the same forty minutes of compute bought about
thirty passes over the data instead of three. The overfitting curve showed up
on the first try.

![Training loss keeps falling while validation loss bottoms out and climbs](images/learning-llms-4/020-baseline-overfitting.png)

Validation loss bottomed out at 1.5260 around step 8,250, about a quarter of
the way in, and then rose steadily to 1.9037 by the end while training loss
kept dropping from 1.2622 to 0.8090. That is a 25% degradation, and the
checkpoint sitting on disk at the end of the run is the worst one.

TinyStories is built to be easy for small models to generalize on. That is its
entire design goal, and it means a held-out story is nearly as predictable as
a memorized one, so the model has no reason to memorize. Tiny Shakespeare's
dialogue and proper nouns are structurally much richer, so repeated exposure
eventually pushed the model past learning the style and into learning specific
sequences of bytes.

The part I did not expect was the ordering. Two increases in model size did
nothing, and one change of dataset did it immediately. When a model will not
overfit, the data is worth checking before the parameter count.

One more thing from this run stuck with me: the generated text still looked
fine at the end. Correct speaker tags, plausible archaic phrasing, real words.
Overfitting was clearly visible in the loss for the second half of training
and never became visible in the samples at all.

## When the Learning Rate Moves, So Does the Weight Decay

Some vocabulary first, because the rest of this leans on it. The optimizer is
the piece that takes the gradients from a training step and decides how to
change each weight. The learning rate is how far it moves them, and a schedule
is a rule for changing that distance as training goes on. Cosine decay starts
at the full rate and eases down toward near zero along a cosine curve. Warmup
is the opposite at the beginning: ramp up from zero over the first few hundred
steps instead of starting at full speed. One step is one batch of text, and
every run in this post got exactly 29,410 of them, so nothing here wins by
training longer than anything else.

The first real experiment was a cosine learning rate schedule. The reasoning
seemed solid: my baseline overfits in the back half of training, a cosine
schedule takes smaller and smaller steps toward the end, so it should be doing
less damage exactly where the damage was happening.

It overfit worse. Final validation loss went from the constant schedule's
1.9037 to 2.1337. Adding warmup changed essentially nothing.

What I had missed is in how AdamW applies weight decay. Weight decay is a small
constant pull that shrinks every weight toward zero on every step, and the
strength of that pull is not the `weight_decay` setting by itself. It is
`learning_rate * weight_decay`. At my baseline's constant learning rate of
`3e-4` and decay of `0.1`, that is a steady `3e-5` shrink per weight for the
whole run.

A cosine schedule takes the learning rate from `3e-4` down to `3e-5`. The
`weight_decay` setting never moves; it is `0.1` the entire time. But the
product does, and by the end of training the actual pull is `3e-6` instead of
`3e-5`. The regularization had quietly decayed to a tenth of its original
strength, right at the point in training where I most needed it.

So I ran a third arm that scales `weight_decay` up as the learning rate comes
down, holding the product pinned at `3e-5` for the whole run. If both effects
mattered, this should land somewhere in the middle.

![Validation loss, learning rate, and the effective decay pull across three schedules](images/learning-llms-4/021-learning-rate-schedules.png)

It did not land in the middle. Final validation loss went to 1.7094, which is
not just better than the cosine run's 2.1337 but better than the constant
baseline I started from. Nearly all of the extra overfitting was the decay
following the learning rate down. Once that was held fixed, the smaller
late-training steps stopped looking harmful and started looking like a small
independent win.

The conclusion is not that cosine decay is bad. Both cosine runs matched the
constant baseline's *best* validation loss just fine; what they damaged was
everything after the point where I should have stopped training anyway. The
conclusion is that a schedule named after one hyperparameter changed two, and I
could not tell which one mattered by looking at the curve. It took a run
designed to hold one of them still.

## Two Optimizers, Two Different Failures

Next was the optimizer comparison: plain SGD, plain Adam, and the AdamW
baseline, all at the same learning rate.

Each is a line to describe. SGD moves every weight by a fixed fraction of its
gradient: same step size everywhere, no memory of previous steps. Adam keeps a
running average of each weight's recent gradients and divides by a running
estimate of how big they have been, so a weight with small but consistent
gradients still gets a real step, and a weight with erratic ones gets a
cautious one. AdamW is Adam with exactly one thing changed, and that one thing
is the subject of this section: where weight decay gets applied.

"AdamW uses decoupled weight decay" is the kind of sentence I had read a dozen
times and filed as a footnote. Here is what it means concretely, with both
update rules side by side:

![In plain Adam the decay term joins the gradient before Adam scales it; in AdamW it is applied separately afterwards](images/learning-llms-4/weight-decay-coupling.png)

`m` and `v` are Adam's running estimates of how big and how consistent a
parameter's recent gradients have been. They are a confidence estimate, used to
decide how large a step is safe to take. Coupled Adam mixes the decay force
into the gradient *before* that estimate gets built, so the decay is subject to
the same scaling as everything else. AdamW keeps it outside, as a separate flat
shrink applied after the step.

I expected the coupled version to be mildly worse, on the grounds that the
regularization would come out weaker than intended. Instead it fell apart in a
way I would not have predicted.

![Validation curves and early gradient norms for AdamW, SGD, and coupled Adam](images/learning-llms-4/022-optimizer-comparison.png)

For the first 500 steps it was *winning* — validation loss of 2.5914 against
the AdamW baseline's worse number at the same point. Then the gradient norm
spiked to 6.10 around step 1,750, validation loss climbed to 3.4512 by step
2,500, and the run spent the remaining 27,000 steps stuck around 2.79, never
getting back to where it had been at step 500.

The gradient norm there is one number for the size of an entire step's
gradients: stack every parameter's gradient into one long vector and take its
length. On my stable runs it sits around 1.3, so 6.10 is a step several times
larger than normal.

The lag between those two events is the interesting part. The gradient spike
was over by step 2,500, but validation loss kept climbing for another 750 steps
past that and then took 3,000 more to come back down. That is momentum: `m` is
weighted 90% toward its previous value each step, so the model keeps coasting
in a bad direction well after the thing that pushed it there has stopped.

Adam's confidence estimate starts at zero and is built from only a handful of
steps early on, which makes it naturally under-calibrated for the first few
hundred iterations. That is normal and self-correcting. Coupling glues the
decay onto the gradient during exactly that window, so the decay gets swept
into the shaky early calibration and amplified by it.

Plain SGD, meanwhile, just lost. Final validation loss of 2.9942, no spike, no
drama — the learning rate I had tuned for Adam is simply far too small a step
for SGD to make progress with. I deliberately left it untuned so the optimizer
would be the only thing changing, which makes this less a verdict on SGD than
a measurement of how much of Adam's value is in adapting the step size per
parameter.

By final loss alone those two runs look like the same result: both plateau
somewhere around 2.8 to 3.0. They are nothing alike. One was underpowered from
the first step and the other destabilized and never recovered, and the only way
to see the difference was to look at the early part of the curve instead of the
endpoint.

## Clipping the Wrong Quantity

A gradient norm spiked, so the obvious next move was gradient clipping. Cap the
total gradient norm at a threshold, rescale anything larger, carry on.

I picked a threshold of 2.0 off the baseline's own logged norms, where the
median is about 1.33 and the 99th percentile is about 2.03. That should leave
ordinary steps untouched and catch the norm-6 outliers from the coupled-Adam
run. Then I ran it two ways: on the stable AdamW baseline as a control, and on
the unstable coupled-Adam config as the actual test.

The control did nothing, which is what I wanted. It tracked the baseline within
about 0.01 validation loss at every checkpoint and fired on 17 of 1,178 logged
steps.

The test also did nothing, which is not what I wanted.

![Validation curves and pre-clip gradient norms for both clipped runs](images/learning-llms-4/023-gradient-clipping-comparison.png)

Clipping fired on 86 steps this time, concentrated exactly in the run-up to the
spike, with one raw norm as high as 11.50. Every one of those gradients got
capped. The validation loss peak happened anyway, at 3.4683 versus 3.4512
unclipped, at the same step, followed by the same plateau at the same level.

The one thing clipping did change was for the worse. That fast competitive
early descent — the best-in-class 2.5914 at step 500 — disappeared, because
a norm cap has no way to tell a large useful gradient from a large harmful
one.
It removed the good part of the run and left the bad part intact.

Reading the training loop afterwards explained why. My code calls `backward()`,
measures and clips the gradients, and then calls the optimizer step. But
PyTorch's coupled Adam adds `weight_decay * param` to the gradient *inside*
that optimizer step, after my clipping has already happened. So the cap applied
to the task gradient, and the quantity Adam actually built its moment estimates
from was never capped at all.

![The clip runs between backward() and the optimizer step, so the decay term the optimizer adds is never covered by it](images/learning-llms-4/clipping-placement.png)

What that run rules out is "the raw loss gradients by themselves are the whole
problem." What it cannot tell me is whether the remaining problem is a step
that is too big or a step pointed in a bad direction. The measurement I was
reading and the quantity that mattered were not the same thing, and nothing in
the plot would have told me that. Only the order of operations in the loop did.

## Dropout Buys Time, Not Immunity

Dropout randomly switches off a fraction of activations during training, so no
neuron can depend on one specific partner always being there. The textbook
framing is a dial with a bad end on each side: too little and the model
memorizes, too much and it cannot learn enough to begin with.

I swept five rates from 0.1 to 0.5 against the no-dropout baseline. Through 0.3
every step up beat the one before it — best validation loss fell from 1.5260
to 1.4835 to 1.4730 to 1.4689 — and the best checkpoint kept landing later in
the run, moving from step 8,250 to 15,250 to 22,000 to 28,750. At 0.4 the streak
turned into a tie. At 0.5 it finally broke: best validation loss rose, final
validation loss rose, and final *training* loss rose too, which is the part
that makes it real underfitting rather than a model just being more careful.
The samples picked up small disfluencies at that rate as well, phrases like
"this are not delight" that had not appeared at any lower rate.

So the sweet spot was 0.3 to 0.4 and the ceiling was somewhere just past it.
That was the finding, and it was wrong.

The problem is where 0.3's best checkpoint landed: step 28,750, out of a budget
of 29,410. Its curve had not turned. It had simply run out of room. So I reran
that exact configuration for twice as many steps.

![Validation loss keeps improving past the original budget, then turns](images/learning-llms-4/024-dropout-extended-budget.png)

Validation loss kept improving for another 9,000 steps past where I had stopped
it, reaching 1.4636 at step 38,750 — better than any rate in the original
sweep. Then it turned and climbed steadily while training loss kept falling,
which is the same overfitting signature the no-dropout baseline produced,
ending at 1.4997.

So dropout did not remove overfitting here. It postponed it, from step 8,250 to
about step 38,750, roughly a factor of 4.7. The flat region I had read as a
ceiling was the slow front edge of a curve that had not gotten around to
turning yet, and no amount of staring at the original plot would have
distinguished those two. A curve that stops improving at the edge of a fixed
budget is a fact about the budget until someone runs it longer.

Two smaller things from this sweep are worth keeping. The generalization gap —
the distance between training and validation loss — shrank monotonically
across all five rates, including the 0.5 run that was measurably worse at both
jobs.
It narrowed there because validation loss caught up to a degraded training
loss, not because anything improved. Read alone, it would have hidden the
regression completely.

And dropout is not free. The cleanest timing measurement in the sweep ran at
8,703 tokens per second against the baseline's 12,169, about 28.5% slower,
purely from sampling the masks. That is a substantial ongoing cost for
something usually described as a technique that costs nothing.

## Testing the Linear Scaling Rule

A batch is the group of sequences averaged together into a single update. Mine
was 16 sequences of 64 characters, so 1,024 characters of text went into
deciding each step.

The linear scaling rule says that when you double the batch size you should
double the learning rate: a bigger batch averages over more examples, so the
gradient direction is more reliable, so it is safe to move further along it.
That compensates for the fact that a fixed token budget now buys half as many
steps.

I ran it. Doubling the batch to 32 while holding the learning rate fixed cost
validation loss at every single checkpoint. Doubling the learning rate
alongside it recovered most of that gap, and by the final step it did better
than that: 1.8895 against the original baseline's 1.9037, from half as many
optimizer steps over the same data.

Which was the moment I should have been suspicious, and was, because of what
the schedule experiment had already taught me. AdamW's per-step shrink is
`learning_rate * weight_decay`. I had doubled the learning rate and left
`weight_decay` alone, so I had also doubled the regularization strength — and
I already had a result showing that this lever by itself can explain a
late-training improvement of about this size.

So I ran the arm that pins the shrink back to the baseline's `3e-5` while still
doubling the learning rate. That isolates the actual claim: bigger steps, same
total regularization.

![Validation curves for doubled batch size with and without scaled learning rate](images/learning-llms-4/025-batch-size-lr-scaling.png)

It came last. Final validation loss of 2.0429, worse than the run that left
the learning rate alone (1.9668) and worse than the original baseline's
1.9037. It also had the lowest final training loss of the three, at 0.7297,
and the widest generalization gap — the bigger steps moved the model toward
memorizing the one-megabyte corpus faster, and the decay pull counteracting
that had not grown to match.

The honest version of this result is close to the opposite of what I had after
two arms. At this scale, doubling the learning rate to match a doubled batch
size mostly worked because it happened to double the regularization too, not
because bigger well-scaled steps are as good as more small ones. The rule's
usual justification is about the reliability of the step *direction*, and it
says nothing at all about whether a fixed decay coefficient still regularizes
enough at the larger step size.

Separately, and not affected by any of this: all three batch-32 runs measured
around 14,000 tokens per second against the baseline's 12,169, about 15%
faster, from amortizing per-step overhead over more tokens. That part is real
regardless of what the loss did.

## One Result That Held Up

The last thing I tried was mixed precision. Run the forward pass in bfloat16,
keep the weights, the gradients, and the optimizer state in float32.

The split is the whole idea. bfloat16 stores each value much less precisely
than float32 — 7 bits of mantissa instead of 23 — but keeps the same 8-bit
exponent, so it covers the same range of magnitudes and does not need the
overflow handling float16 requires. The forward pass is a lot of large matrix
multiplications whose results are thrown away after one step, so a little
rounding there is harmless. The weights and the optimizer's running averages
are the opposite: they accumulate tiny changes over tens of thousands of steps,
and rounding error there could permanently bend the training trajectory.

The one thing I did before running it was check `lscpu` for `avx512_bf16`. On a
CPU without it, PyTorch runs the same code correctly through software
emulation, and I would have measured nothing or a slowdown and drawn the wrong
conclusion about the technique.

![bfloat16 and float32 validation curves tracking each other throughout](images/learning-llms-4/026-mixed-precision.png)

Throughput went from 12,169 to 18,074 tokens per second, a 48.5% improvement.
The validation curve is indistinguishable from the float32 run at every
checkpoint: 1.5296 best against 1.5260, 1.8890 final against 1.9037, both
differences smaller than the spread I was already seeing between the baseline
and its closest relatives elsewhere.

My favourite number in that run is the one from step 0, before a single
training step: 5.5612 against 5.5614. Same weights, same data, one forward
pass, two precisions. That is the size of what bfloat16 actually changes, and
it is the right scale for calling something rounding noise rather than a
behavioural difference.

After five experiments where the appealing headline number had something hiding
behind it, this one just worked the way it was advertised.

## Where I Ended Up

I can now say what a cosine schedule does to weight decay, why coupled and
decoupled decay are not two spellings of the same thing, what dropout buys and
what it costs per step, and why I check `lscpu` before believing a speedup. All
of that is worth having.

But the thing I actually took away is about the shape of the mistake, because
it was the same mistake every time. A schedule that changes the learning rate
also changes the regularization. A learning rate that doubles also doubles the
regularization. A clipping threshold applied before the optimizer step does not
cover what the optimizer step adds afterwards. A sweep that ends at a fixed
budget measures the budget as much as the setting. In each case I had changed
one named thing and something unnamed came with it, and in two of them the
result flipped sign once I held the passenger still.

What makes that hard is that none of those results looked broken. They looked
like findings. Cosine decay overfitting worse is a perfectly plausible story.
The linear scaling rule beating the baseline is the result you would hope for.
I only caught them because the numbers were slightly better than they had any
right to be, and the control run was cheap enough to just go and do.

So the habit I am keeping is to ask what else a setting is arithmetically
attached to before running the comparison, and to treat any pleasant surprise
as a hypothesis about a confound rather than a result. Both times I did that
here, there was one.

What I worked on next was training as a system rather than a set of settings:
where the time actually goes when you profile a step, whether a run can be
stopped and resumed without changing what it learns, what happens when the
numbers themselves go bad, where the memory goes, and how much throughput was
sitting in the CPU thread count all along.
