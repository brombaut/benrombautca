*A note on the charts: they come straight out of my own experiment
records, so their titles and labels carry numbering like "Experiment
027" that only means something inside my notes. Feel free to ignore that
part; the axes and the curves are what matter here.*

My last post was about training decisions — schedules, optimizers,
dropout, batch size — and it ended by saying that the next thing I wanted
to look at was training as a system rather than as a set of settings. Not
what the model computes, which I had spent two posts changing, but the
process that runs it: where the time goes, whether a run can be stopped
and restarted without changing what it learns, what happens when the
numbers themselves go bad, where the memory goes, and how many CPU
threads I should have been using all along.

None of the five experiments here changes a single line of the model or
the training math. Every one of them adds an instrument, points it at the
loop, and reads what comes back.

What they had in common surprised me more than any individual result. In
four of the five, the thing that was wrong had been wrong for a while and
was completely invisible in the one number I was actually watching. A
mishandled restart keeps producing a falling loss. A memory estimate can
be off by a factor of 27 while every run completes normally. A thread
count can be wrong for four consecutive experiments without a single
symptom. The loss curve is a measurement of the model, and almost
everything in this post is a property of the process running it.

## Reading a Number the Operating System Already Had

The first item on the list was observability, and it turned out I had
most of it already. The training script had been logging step time,
tokens per second, gradient norm, and loss since the schedule
experiments, because those experiments needed them. The one real gap was
memory: nothing recorded how much RAM the training process was actually
using, or whether that number stayed put over a forty-minute run.

The fix is one line, and it is the cheapest instrumentation in this
entire post:

```python
def peak_memory_mb() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
```

`ru_maxrss` is the peak resident set size — the most physical memory the
process has actually had in use at any point since it started. It is a
high-water mark the operating system is already tracking whether anyone
reads it or not. There is no new measurement technique here. I just
finally looked at a number that had been sitting there the whole time.

![Peak memory over the full run, a zoom on the early one-time allocation, and the profiled operator breakdown](images/learning-llms-5/027-observability.png)

The curve has exactly the shape that "no leak" should produce. Almost all
of the growth — 1,704.8MB up to 2,555.7MB — happens by step 25, which is
the one-time allocation of parameters, gradients, and the optimizer's two
running-average buffers. The remaining 29,385 steps add 8.6MB between
them, three tenths of a percent. That is the difference between assuming
a fixed model at a fixed batch size cannot leak memory and watching the
number hold flat for forty minutes. If it had not held flat, that would
have been the finding.

The second instrument was PyTorch's profiler, which answers a different
kind of question: where does the CPU actually spend its time inside a
forward and backward pass? Here I need to be precise about one column,
because every percentage in this post leans on it. The profiler reports
both self time and total time for each operation. Self time is time spent
inside that operation's own code. Total time also includes time spent
inside other operations it called into. For a leaf operation like
`aten::mm`, a matrix multiply that does not call other PyTorch
operations, the two are nearly identical. For something like the fused
attention kernel, total is noticeably higher, because part of what it
reports is really time spent in the kernels underneath it. I read the
self column throughout, because it attributes time to whoever actually
burned the cycles instead of crediting a parent for work its children
already got credit for.

Matrix multiplies dominating was the expected answer — four attention
projections and two linear layers are very nearly the whole model. But
the percentage moved a lot between two runs: 81% in a short smoke test
and 59.85% in the real one. The main difference between them was the
thread count, 4 against 20. I had not set out to test that, and I left it
as a loose end. It turns into the last section of this post.

One thing this did not answer, and I want to be straight about it. The
Mixture of Experts post ended by asking how much of that model's runtime
was real expert matrix multiplies versus the masking and gathering around
them. This profiling pass ran against the dense baseline, not the MoE
model, so that question is still open.

The number that mattered most here was one I could not explain. Peak
memory came in around 2.56GB. Parameters, gradients, and optimizer state
for a 5,837,056-parameter model account for about 93MB of that. The
remaining factor of 27 was the reason the memory experiment further down
exists.

## A Model Checkpoint Is Not a Training Checkpoint

Saving a model and saving a training run are different problems, and the
gap between them is easy to miss because the first one looks complete.

Weights alone are enough to reproduce the model's output exactly. They
are not enough to keep training it identically, because the optimizer
carries state of its own that the next update depends on, and that state
is invisible unless you go looking for it. AdamW keeps two running
averages per parameter: `m`, an average of recent gradients, which is the
momentum term, and `v`, an average of recent squared gradients, which is
a per-parameter sense of how large and noisy gradients have been in that
direction. It also keeps its own internal step counter, `t`.

That counter is the part that matters. `m` and `v` both start at zero, so
for the first several steps they are biased toward zero, and AdamW
corrects for that by dividing through by `1 - beta^t`. Early in training
that correction is large; later it is nearly nothing. A freshly
constructed optimizer starts with `t` at zero, `m` and `v` empty —
regardless of what step the training loop itself believes it is on. Give
it the right weights and the right next batch and it will still compute a
different update, because it thinks it is at the beginning.

So the checkpoint has to hold more than weights:

```python
checkpoint = {
    "step": step,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "train_generator_state": train_generator.get_state(),
    "torch_rng_state": torch.get_rng_state(),
    "training_metrics": training_metrics,
    "evaluation_metrics": evaluation_metrics,
    "training_time": training_time,
}
```

Each field answers a question the next process has to be able to answer.
Which weights. What the optimizer was about to do. Which batch comes next
— my batch sampling runs off its own generator, separate from the global
one. What any random operation like dropout would draw next. And what to
report as the full run once it finishes.

![What a checkpoint has to contain for training to continue unchanged](images/learning-llms-5/checkpoint-contents.png)

I ran four arms. A control that runs 4,000 steps straight through with no
interruption, which is the ground truth. An identical run that stops and
checkpoints at step 2,000. A resume that restores everything from that
checkpoint and finishes. And a fourth that restores everything *except*
the optimizer state — a deliberate wrong answer, built so the mistake
would be a measurement instead of a description.

![Control, resume, and fresh-optimizer resume, with each arm's difference from the control below](images/learning-llms-5/028-resume-correctness.png)

The resumed run matched the control exactly. Not closely — identically,
to the full floating point representation, at all 161 logged training
steps and 17 evaluation checkpoints from step 2,001 to the end, and the
generated text at the end was byte for byte the same. That is the
hypothesis confirmed directly rather than by proxy.

The fresh-optimizer arm matched through the shared prefix, since all
three runs did the same work up to step 2,000, and then diverged at the
very first logged step afterwards: a 0.019 gap at step 2,025, the largest
single-step difference anywhere in the comparison. No ramp, no warm-up
into it. The first post-resume update already used the wrong `m`, `v`,
and `t`, exactly as the bias-correction argument says it must. I checked
the mechanism directly rather than trusting the symptom: the saved
optimizer state has its internal step field set to 2,000, and a fresh
optimizer's would be 0. That is the variable that changed.

What I got wrong was the shape of the divergence. I expected something
dramatic, an echo of the optimizer instability from the last post. What
actually happened was a persistent but bounded noisy gap, roughly 0.0005
to 0.02, sometimes shrinking for a few hundred steps before jumping
again, never running away and never producing a NaN. Which makes sense in
hindsight: a fresh Adam is not broken, it is just a less warmed-up
optimizer walking a similar landscape.

That is the more unsettling version of the result. Nothing about the loss
curve announces that the checkpoint was mishandled. The run looks
healthy, the loss goes down, nothing crashes. You would need a control
run beside it to notice, and in a real training run the control is the
one thing you do not have.

## The Last Good Checkpoint Was Already Ruined

A training run can fail in two structurally different ways, and I had
already seen one of them. The coupled weight decay run in the last post
climbed for about 1,500 steps, peaked, and settled onto a permanently
worse plateau — slow, bounded, ugly, and never once a non-finite number.
The other kind is a cliff: the loss or a gradient genuinely overflows
what float32 can represent and becomes `inf` or `nan`.

They need different handling. A slow instability is something you can
watch in a loss curve and decide about. A fast one can go from fine to
NaN in two or three steps, which is faster than a printed loss line will
tell you, and by then the corrupted update is already in the weights. So
the check has to run every step, automatically, between the backward pass
and the optimizer step:

```python
if not (math.isfinite(loss_value) and math.isfinite(grad_norm)):
    break  # never call optimizer.step() on this
```

Alongside it, a periodic safety checkpoint using the same contents as
above, overwritten in place rather than accumulated, so there is always a
recent state to go back to.

Finding a trigger took a real search rather than a guess. A learning rate
of 8.0 stayed finite for 500-plus steps, with an enormous and chaotic
loss but no overflow. Every value from 8.05 up through 10.0 overflowed by
step 3, every time, deterministically. That is not a gradual ramp into
instability, it is a sharp edge, and knowing which side of it I was on
made the rest of the design obvious: pick 9.0, expect a fast failure.

![The slow bounded instability from the optimizer experiment next to this one's overflow within three steps, on a log scale](images/learning-llms-5/029-failure-modes.png)

The detector did its job. The control ran 2,000 steps and 8 safety
checkpoint writes with no false positives, and the unstable run was
caught at step 3, the same step the failure actually happened, with a
readable diagnostic and a preserved checkpoint sitting on disk.

Then the part I had not staged. I resumed that preserved checkpoint at a
safe learning rate, and it failed again immediately — with a loss value
identical to the original failure's, down to the last digit,
2659.863525390625 both times. That is not a coincidence. It is proof that
by the time anything looked wrong, the weights themselves had already
absorbed two catastrophic updates, and they alone were enough to doom the
very next forward pass no matter what learning rate came after.

"Keep the last checkpoint from before things went wrong" sounds like a
complete safety story. It quietly assumes the failure was gradual, that
whatever step you caught it at was itself still healthy. Here the last
known-good checkpoint was already two bad updates deep. Detecting
non-finite values is the easy part. Knowing how far back you have to
rewind is not.

One smaller thing I had expected to help and did not. Gradient clipping
is the standard reach for instability, and it made no difference at all —
the clipped run still failed at step 3. Working out why meant checking
what `clip_grad_norm_` actually does to an infinite gradient rather than
reasoning about it from the name. It computes a scale factor of
`max_norm / total_norm`. With `total_norm` infinite, that scale is 0, and
0 times infinity is NaN. Clipping does not skip an overflowing gradient
or pass it through untouched; it converts an `inf` into a `nan`. There is
no value it could have produced that would have passed the finite check.
The tool bounds magnitude, and an overflowed gradient has no finite
magnitude left to bound.

## Where the Memory Actually Went

This is the experiment that pays off the factor of 27 from the first
section, and it starts by splitting one number into three that behave
completely differently.

Parameters, gradients, and optimizer state are fixed the moment the model
and optimizer exist. They do not care about batch size or context length,
and they can be computed exactly from the parameter count with
arithmetic, no run required.

Process overhead — the interpreter, the framework, the allocator, the
thread pools — is fixed the moment `import torch` runs, before a single
tensor belonging to my model exists.

Activation memory is the intermediate values the forward pass has to keep
around so the backward pass can compute gradients from them. It is the
only one of the three that depends on what you are actually training on,
and it is the one the standard estimate ignores completely.

To see where each piece gets claimed I took named readings of that same
`ru_maxrss` high-water mark at nine points, from process start through
the first optimizer step. Because the value only ever grows, reading
consecutive checkpoints in order shows where growth happens rather than
just that it did.

![The named-checkpoint waterfall for the control run, and the batch and context sweeps showing near-identical memory growth](images/learning-llms-5/030-memory-breakdown.png)

The fixed overhead is larger than I would have guessed and genuinely
fixed. At `process_start` — before the model, the data, or the optimizer
exist — the process was already at 215.67MB, which is 2.42 times the
entire 89.07MB estimate for parameters, gradients, and optimizer state
combined. By the time the optimizer was constructed, still before any
training step, it was at 324.11MB. Those numbers were the same across
every arm to within a third of a megabyte, regardless of batch size or
context length, which is exactly the behaviour the framing predicts.

The activation result is the one I got wrong out loud beforehand. I
predicted context length would scale worse than batch size, because the
attention score matrix is quadratic in context length and only linear in
batch size. The data says no. An eight-fold batch size increase produced
a forward-pass memory jump of 1,271.69MB, which is 8.008 times the
control's jump. An eight-fold context length increase produced
1,271.30MB, 8.006 times. The same multiplier, from a completely different
knob, matching to two decimal places.

What both sweeps have in common is that they multiply tokens per step by
eight, and that is what the memory tracks. Either the attention score
tensor is never materialized in full by the CPU kernel, or it is too
small next to everything else at this model's size to register. Either
way, at this scale, activation memory reduces to one number — tokens per
step — and not to two independent knobs. Quadratic compute and quadratic
memory are separate claims, and it is worth measuring which one you
actually have before assuming the FLOP story carries over to RAM.

There is a loose end I cannot close here. This experiment's own control
run, at the same batch size, context length, and thread count as the
observability run, peaked at 681.98MB against that run's 2,564MB. Two
real differences exist: the earlier run did the full 29,410 steps against
this one's 500, and it had the profiler attached. A profiler pass
plausibly has a memory cost of its own, and tens of thousands of extra
steps give allocator fragmentation far more room to accumulate than 500
do. I do not have the data to say how the gap divides between those two,
and I would rather say so than pick one.

## Twelve Threads, Not Twenty-Four

Which brings back the loose end from the first section. The share of time
going to matrix multiplies moved between two runs with different thread
counts, and I had never related that to what the machine actually has.
Worse, every experiment in this batch used 20 threads, a number nobody
had chosen deliberately and nobody had ever measured.

`torch.set_num_threads` controls the intraop thread pool — the threads
that a single operation like a matrix multiply splits its own work
across. More of them only helps if there is somewhere for them to run.
This machine has 12 physical cores, each split into 2 hardware threads,
for 24 logical CPUs. The two siblings on a core share that core's actual
arithmetic units; they do not double them. So 12 threads should give
every thread a core to itself, and 24 should put two threads in line for
the same execution hardware. That is a prediction about contention, not
just about diminishing returns.

![Mean tokens per second at 1, 12, and 24 threads, plus the idle rerun](images/learning-llms-5/031-thread-throughput.png)

Running the identical workload at 1, 12, and 24 threads:

```text
 1 thread     3,274.22 tokens/sec    1.00x
12 threads   14,528.50 tokens/sec    4.44x
24 threads    7,684.50 tokens/sec    2.35x
```

Twelve wins by a wide margin, and going past it does not plateau, it
regresses — 24 threads came in 1.89 times slower than 12 while doing the
identical 3,430 matrix multiplies with twice as many workers. The
matrix multiply's own absolute self time nearly doubled, from 0.862s to
1.564s. The extra threads made the same operation take longer.

![Twelve threads, one per physical core, against twenty-four sharing the same execution hardware](images/learning-llms-5/threads-and-cores.png)

There was a confound, and I want to include it rather than tidy it away,
because resolving it was the most useful part. I had other things running
on the machine during those three runs. That lands hardest on the
24-thread arm, which claims every logical CPU and leaves nothing spare.
So I reran that exact configuration with the machine otherwise idle.

Both candidate explanations turned out to be partly right. Going idle
recovered a real chunk of the loss, from 7,684.50 up to 11,540.09 tokens
per second, a factor of 1.50 — so the competing processes genuinely were
a factor. But it did not close the gap. The clean 24-thread run is still
1.259 times slower than 12 threads, with the matrix multiply's self time
still higher at 1.003s against 0.862s, on identical work with nothing
else on the machine. That residual is the architectural cost: two workers
per physical core still compete for the same execution units, load or no
load. A confounded result was worth rerunning cleanly rather than either
trusting it or throwing it out.

One trap in reading the profiler across these runs. The matrix multiply's
share of self time falls steadily as threads go up — 81.33%, then 56.62%,
then 44.96% — which continues the pattern that started this whole thread
of investigation. But a falling share is not the same claim as an
operation getting faster. At 24 threads it is a smaller slice of a slower
run. The share drops because thread management and other fixed costs grow
as a fraction of the pie, not because the multiply improved.

The practical upshot is a one-line change, `--threads 12` instead of
whatever the machine reports as its CPU count, worth about 4.44 times
serial throughput. The method generalizes — measure a few explicit thread
counts spanning the physical and logical core counts — but the number 12
is about this machine and nothing else.

## Where I Ended Up

The concrete things are worth having on their own. I know what a training
checkpoint has to contain and why the optimizer's internal step counter
is the load-bearing part. I know that gradient clipping cannot save an
overflowed gradient, and why. I know that the framework itself costs more
memory than my entire model does, that activation memory at this scale
tracks tokens per step rather than the shape they arrive in, and that the
right thread count for this machine is the physical core count.

But the pattern underneath them is what I actually took away, and it is a
different pattern from the last post's. There the problem was that
changing one setting quietly changed another. Here the problem is that
the signal I was watching had nothing to say about the thing that was
wrong.

A resumed run with a reinitialized optimizer produces a falling, healthy,
entirely plausible loss curve while computing a different trajectory from
its first step. A memory estimate that is off by a factor of 27 produces
no symptom at all until something runs out of RAM. A thread count that
halves throughput produces runs that complete normally, just slower than
they needed to be, for four experiments in a row. In each case the loop
was reporting on the model, and the fault was somewhere else in the
process.

What made all of them findable was cheap instrumentation pointed at
something other than the loss: one line reading a counter the operating
system already maintained, a control run to compare a resume against, a
profiler pass over ten steps, three runs at different thread counts. None
of it took long, and none of it required understanding the problem in
advance — which is fortunate, because in four cases out of five I did
not.

The next thing I want to do is read code I did not write. I have built
this thing twice now, once by hand and once in PyTorch, and instrumented
it enough to know how it behaves. The obvious next step is to open a real
training codebase and find out how much of what I did resembles how it is
actually done.
