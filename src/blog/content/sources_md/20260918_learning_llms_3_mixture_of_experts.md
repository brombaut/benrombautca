My last post was about changing the transformer architecture one piece at a
time: context length, embedding size, head count, depth, activation function,
normalization placement, positional encoding, and attention structure. Those
were all changes to parts I had already built. Mixture of Experts was the
first thing I added that was genuinely new to the model.

It also had the biggest gap between its reputation and its actual size as an
idea. Several frontier models are built this way, and the descriptions I had
read made it sound like a fundamentally different kind of architecture.
Implementing it took about eighty lines.

What I did not expect was that the two most useful things I learned here would
have almost nothing to do with Mixture of Experts. Both were about how
convincingly a broken component can imitate a working one.

## Four MLPs Where There Was One

Each transformer block in my model ran attention, then a single MLP shared by
every token. A Mixture of Experts layer replaces that one MLP with several,
plus a small learned router that picks which one each token uses.

![A dense block runs its one MLP; a Mixture of Experts block stores four and runs the one its router picks](images/learning-llms-3/moe-block-explained.png)

I used four experts and picked one per token. The dense model stores one MLP
and uses one. The Mixture of Experts model stores four and still uses one. That
is the entire trade: a bigger model that costs about the same to run. The
analogy that made it stick for me was a hospital with four specialists instead
of one generalist. The building holds more expertise, but any one patient still
sees exactly one doctor, and the visit takes the same amount of time.

I had two details wrong before I implemented it. Routing happens per token
rather than per sequence, so in my configuration, where a batch is 64 sequences
of 16 characters, that is 1,024 independent routing decisions per batch and not
64. Routing also repeats in every block, with its own router and its own four
experts each time, so a character can go to expert 2 in the first block and
expert 0 in the second.

The router itself is deliberately tiny: a single linear layer with 32 inputs,
because 32 values is everything the model knows about a token at that point,
and four outputs, because there are four choices. That is 128 parameters out of
the model's 76,608. Compute is supposed to be spent processing a token, not
deciding where to send it.

Those 128 numbers are four rows of 32. Each row is a direction in the embedding
space that one expert claims, and a token's score for that expert is its dot
product with that direction. Training the router means learning four directions
that carve up the space the tokens live in.

## Turning the Dispatch Loop Inside Out

The one real implementation idea is in how tokens reach their experts.

The obvious version is to loop over tokens and look up each one's expert. That
is 1,024 separate calls per layer, each pushing a single token through a small
network. Hardware built for large matrix multiplications is almost entirely
wasted doing that.

So the loop gets turned inside out. Instead of looping over tokens and finding
their expert, loop over experts and gather their tokens. That is four calls per
layer instead of 1,024.

![Looping over tokens means 1,024 tiny calls; looping over experts gathers rows into four batched calls and scatters the results back](images/learning-llms-3/dispatch-loop-explained.png)

What shapes the rest of the code is that every result has to return to its
original row, because the next layer reads tokens in order. The layer allocates
a zero tensor as a blank canvas, builds a boolean mask of which rows chose the
current expert, gathers those rows into one contiguous stack, makes a single
batched call, and scatters the results back using the same mask that selected
them. Every token appears in exactly one mask, so every row gets filled exactly
once.

While I was writing it, the masking felt like bookkeeping around the real work.
Reading it as "loop over experts, gather their tokens" made it look less like
overhead and more like the only sensible way to batch the thing.

It is worth being precise about what sparse means here, because I had assumed
something slightly different. The tokens that did not choose an expert never
enter its matrix multiplication at all. This is not computing all four experts
and discarding three.

## A Router That Never Trained

My first working version trained fine. The loss fell. The routing distribution
moved for about 500 steps and then went flat, which I read as the router
settling into a stable partition. I wrote that interpretation down.

It was wrong. The router had not settled. It had never moved at all.

The dispatch computed the router's weight like this:

```python
top_k_weights, top_k_indices = torch.topk(router_logits, k, dim=-1)
top_k_weights = F.softmax(top_k_weights, dim=-1)
```

The softmax runs after the selection. When you select one expert, that softmax
receives a list of exactly one element, and a softmax over one element returns
1.0 no matter what the input is. It is a constant function, and constants have
zero derivative.

That mattered more than it looks, because `topk` is itself not
differentiable. The softmax was the router's only path to a gradient, and
turning it into a constant meant the router received nothing at all.

Printing the gradients directly settled it. On a single backward pass with one
expert selected, the router's largest absolute gradient was exactly zero, with
zero of its 128 entries nonzero. With two experts selected, the same code gave
a healthy 9.322e-03 across all 128. After the fix, one expert selected gave
2.771e-03 across all 128. The expert MLPs were training normally at around
5e-3 the entire time, which is why nothing about the loss curve ever looked
wrong.

The fix is to apply the softmax over all four scores before selecting, which is
the Switch Transformer formulation and precisely why Switch can train with one
expert per token:

```python
router_probs = F.softmax(self.router(flat), dim=-1)
top_k_weights, top_k_indices = torch.topk(router_probs, k, dim=-1)
```

![With softmax after the selection the gradient stops at a constant; with softmax before it, the gradient reaches the router](images/learning-llms-3/router-gradient-explained.png)

Chasing this also answered a question I had parked earlier: why the selected
weight is multiplied into the expert's output at all. With one expert it is a
multiplication by approximately 1.0, and it barely changes the numbers. Its job
is not numerical. Selecting an expert is a hard choice with no adjustable dial
attached to it, so that multiplication is the only place the router's own
output enters the computation, and therefore the only route a gradient has back
to it.

Turning the router on was worth 0.030 validation loss. The frozen-by-accident
version finished at 1.8048, the fixed version at 1.7745, same configuration and
seed. Real, but modest, and it suggests most of what Mixture of Experts bought
me at this size came from the extra expert capacity rather than from anything
clever about the routing.

What I keep coming back to is not the bug itself but how complete the story
around it was. The model trained. The loss fell to near the best of any run I
had done. The routing chart showed four experts with visibly different usage
rates, which is exactly what specialization is supposed to look like. I was
looking at the random initialization, unchanged after 5,000 steps. Even the
drift I saw in the first 500 steps had an explanation that was not the one I
gave it: the token representations were sliding around underneath a partition
that never moved.

Checking took one command. Print the gradient and see whether it is zero.

## Sparse Does Not Mean Fast

The other thing these experiments corrected was my sense of what Mixture of
Experts costs.

I had absorbed the idea that it gives you capacity for free, since each token
only activates one expert. Counting arithmetic operations supports that.
Measuring the clock does not. The dense run took 73.8 seconds for 5,000
training steps, and the one-expert Mixture of Experts run took 81.0, doing less
expert arithmetic than evaluating all four would and still more total work than
the dense model.

The memory cost is the obvious one. All four experts stay resident whether or
not they are used, so the model holds 76,608 parameters to perform the
arithmetic of roughly 27,200. That ratio is what shapes real deployments, where
Mixtral 8x7B loads around 47 billion parameters to compute about 13 billion
worth per token.

The cost I had not thought about is movement. Gathering scattered rows into
per-expert batches and scattering the results back is pure data movement with
no arithmetic attached, and splitting one 1,024-row matrix multiplication into
four roughly 250-row ones is less efficient than doing the single large one. At
my scale that is a handful of seconds. At real scale, where experts live on
different machines, the same shuffling becomes network traffic and turns into
the dominant engineering problem.

Moving to two experts per token made the distinction concrete. The parameter
count stayed at exactly 76,608, since the same stored experts are being used,
but each of the 1,024 tokens now passes through two of them, doubling the
expert-token assignments to 2,048 per block. Training time went from 81.0 to
123.5 seconds, a 52.5% increase, for a validation loss improvement of 0.0133.

So parameter count describes what is stored, and experts per token describes
what is actually run. I had been treating those as one number.

The runtime did not double either, because the model is more than its experts.
Attention, normalization, embeddings, loss calculation, and the optimizer all
cost what they cost before. When you double one part of a program and the whole
thing gets 52.5% slower, the gap tells you how much of the runtime that part
actually owned.

## Reading My Own Routing Chart Wrong

With two experts per token, my routing chart looked healthy. The first block's
four experts sat at roughly 0.24, 0.27, 0.27, and 0.22 of assignments, which is
about as even as four numbers get.

That evenness was partly manufactured by how I was measuring. The logger
divided each expert's count by the total number of assignments, and when two
experts are chosen from four, no single expert can exceed 0.50, because it
cannot be picked twice for the same token. The more misleading part is what the
remaining numbers translate to: an expert holding 0.35 of assignments was
actually being selected for around 70% of tokens.

Converting to the rate at which tokens select each expert, which is what I
should have been logging in the first place, the second block was badly
lopsided. Two of its experts were selected for 85.5% and 90.6% of tokens. One
was selected for 8.3%.

![The same expert reads as 0.35 of assignments or 70% of tokens, depending on the denominator](images/learning-llms-3/routing-metric-explained.png)

## Why Routers Collapse

The obvious reaction is that the router should have known better. It could not
have. Balance appears nowhere in the loss function.

The router is trained on one signal, which is whether the model predicted the
next character well. Nothing in that objective refers to how many tokens each
expert received. The router is not deciding to ignore balance; balance is not
among the things it can perceive. Expecting otherwise is expecting a quantity
nobody optimized to come out optimized.

There is also a feedback loop pushing in the wrong direction. An expert that
receives more tokens gets more gradient updates, improves faster, and attracts
more tokens for being better. Experts that start slightly ahead stay ahead, and
the ones that start behind fall further behind. My run did not begin with a
starved expert. The concentration built up over training.

The standard fix adds a second term to the objective so that balance becomes
something the router can see:

```text
balance loss = number of experts
             x sum(assignment share x mean router probability)

total loss = prediction loss + 0.01 x balance loss
```

The term needs both the hard assignment counts and the soft router
probabilities. The counts describe where tokens actually went, but you cannot
get an ordinary gradient through the selected indices, so the probabilities are
what carry the signal back to the router's weights.

For a weight of 0.01, the effect was larger than I expected. The second block's
starved expert went from being selected for 8.3% of tokens to 45.1%. Its two
dominant experts fell from a combined 88.0% of assignments to 54.5%. Runtime
increased by 1.7%.

Validation loss also improved rather than regressing, from 1.7610 to 1.7467,
with the best checkpoint going from 1.7456 to 1.7265. I had expected to pay
something: if the lopsided routing were genuinely better for prediction,
forcing it flatter should have hurt. It didn't, which points at the feedback
loop running away rather than the model having found a partition worth keeping.

![The rich-get-richer routing loop, and what a 0.01 balance term changed](images/learning-llms-3/load-balance-explained.png)

![Validation and training loss for normalized top-2 routing with and without the load-balancing term](images/learning-llms-3/moe-load-balance-loss-curves.png)

The curves are worth looking at precisely because they are so boring. Nearly
all of the visible difference is a slight separation over the last thousand
steps. Underneath, one expert went from nearly unused to carrying a normal
share of the traffic. The plot of the number I was ranking runs by shows
almost none of what the experiment was actually about.

Balanced does not mean identical, incidentally. After balancing, the second
block still selected one expert for 62.1% of tokens and the others for roughly
45 to 47%, so the router kept a preference without starving anything. And in a
model this small, load balancing is not doing the job it does in production. My
experts have unlimited capacity and run one after another, so spreading tokens
evenly does not improve throughput or stop tokens being dropped. Here it just
keeps neglected experts learning. In a real deployment, where experts run in
parallel on different devices and can only take so many tokens each, it is also
an operational requirement.

## What It Cost and What It Bought

The honest summary is that Mixture of Experts was not worth it at this scale.

My best Mixture of Experts run reached 1.7467 validation loss with 76,608
parameters. Earlier on, extending the context window from 16 to 32 characters
reached 1.7789 with 29,760. So this spent about 2.6 times the parameters to
gain roughly 0.004 over a much simpler change, and took longer per step to do
it.

That is not an argument against the technique. It says something about what was
limiting my particular model, which was context and not capacity. Giving more
capacity to a model that cannot see enough text buys very little, and something
that works at 47 billion parameters is under no obligation to help at 76
thousand.

I would rather have this result than a flattering one. It separates knowing how
a mechanism works from knowing when to reach for it, which are easy to confuse
when every description you read is written by someone for whom it worked.

## A Failure I Could Rule Out

Every run here generated text that was 100% newline characters. That is the
same degenerate behavior I ran into with rotary positional embeddings last
time and wrote about there, and improving the validation loss did nothing for
it, which fits what that failure turned out to be. Validation loss is measured
by handing the model real text and asking it to predict each next character,
so it never once asks the model to consume its own output.

The one new piece of evidence came from the bug. The broken-router run and the
fixed-router run produced byte-identical degenerate output, and since those two
models differ in whether the router trained at all, identical output rules
routing out as the cause and points back at the positional encoding. The bug I
introduced by accident ended up serving as a control for a different one.

## Where I Ended Up

I can now write a sparse Mixture of Experts layer, say why the selected weight
is multiplied in even though it barely changes the numbers, and explain why the
balancing term is necessary rather than a nice-to-have. I also have one case
where the technique did not pay off and a reason why it didn't.

The part I expect to keep is smaller than any of that. Twice now, something
was broken in a way that the validation loss could not show me: a router with
no gradient at all, and a routing chart whose apparent balance came from
dividing by the wrong number. Both looked fine for as long as I only looked at
the metric I was ranking runs by. Both took one command to expose once I
thought to look at the component itself instead.

So I have started asking whether a thing is running before asking how well it
ran, and logging the two things that would have caught these: the size of each
component's gradient, which would have shown a flat zero from the first step,
and the share of tokens choosing each expert rather than each expert's share of
assignments. Both are one line.

What I worked on next left the architecture alone and changed how the model
trains: learning rate schedules and how they interact with weight decay, why
Adam and AdamW are not the same optimizer, how dropout delays overfitting
without preventing it, and whether mixed precision can make training
meaningfully faster without changing what the model learns.
