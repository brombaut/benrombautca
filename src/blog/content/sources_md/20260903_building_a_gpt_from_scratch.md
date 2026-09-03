# [Learning LLMs 1] Learning How GPTs Work by Building One from Scratch

I've wanted to properly understand how GPTs work for a while. I knew most of
the words that come up when people explain transformers: embeddings, attention,
softmax, residual connections, and so on. I had used PyTorch before and built a
small neural network from scratch a few years ago. But if I tried to follow the
full path from some input text to the model updating one of its weights, my
understanding would get hand-wavy pretty quickly.

So I decided to go back through it from the beginning. I worked through Ian
Bull's [LLMs, the Hard Way](https://llms.ianbull.com/), which builds a small GPT
in TypeScript without using a machine learning framework. I followed the same
general path in Python, first with a version where every value in the model was
an individual scalar, and then with a more normal PyTorch implementation. That
PyTorch baseline was the final part of Phase 1, rather than the start of the
later architecture experiments.

The model I ended up with was very small and generated simple sentences like
`the sheep is by the tent`. That obviously isn't useful on its own, but model
quality wasn't really what I was after. I wanted to be able to look at a GPT
implementation and understand why each part was there and what happened during
training.

## Starting with Individual Numbers

The first few steps were intentionally basic. I made a simple word-level
tokenizer that split the training sentences on spaces, built a vocabulary, and
assigned a number to each word. It also added a special token to mark the start
and end of a sentence.

I had always thought of tokenization as a preprocessing step that happens before
the interesting model work starts. Working through the later fine-tuning section
made me realize that this isn't quite right. The tokenizer is tied directly to
what the model learns.

If `cat` is assigned token 89, then row 89 in the embedding table learns the
representation for `cat`. The model's output at position 89 also represents its
score for generating `cat`. If I rebuild the tokenizer and token 89 now means
`where`, the model hasn't adapted; I've just scrambled the meaning of its input
and output. This is obvious once it is laid out, but I hadn't thought through
that relationship before.

From there I implemented a small `Value` class. Each `Value` held one number,
its gradient, and enough information to remember how it had been calculated.
Operations like addition, multiplication, powers, exponentials, and ReLU all
returned another `Value`.

This made the code slow, but it also meant I could inspect every calculation
the model made. There were no tensors at this point. A vector was just a list of
`Value` objects, and a matrix was a list of those lists.

## Finally Understanding What `backward()` Does

Autograd was probably the first part that really changed my understanding.
Before this, I knew what backpropagation was doing at a high level. The model
makes a prediction, calculates a loss, and works backward to determine how the
weights should change. What I didn't understand as well was how something like
PyTorch could keep track of all of that automatically.

In the scalar version, every operation recorded a small function describing how
to pass a gradient back to its inputs. Addition passes the incoming gradient to
both values. Multiplication scales the gradient for each input by the value of
the other input. ReLU either passes the gradient through or blocks it depending
on whether its input was positive.

This is the multiplication implementation, with some type details removed to
make the important part easier to see:

```python
def __mul__(self, other):
    output = Value(self.data * other.data)
    output._parents = (self, other)

    def backward():
        self.grad += other.data * output.grad
        other.grad += self.data * output.grad

    output._backward = backward
    return output
```

The forward calculation multiplies the two numbers. The nested `backward`
function records how a later gradient should be distributed back to them.

Calling `backward()` starts at the loss and walks through those recorded
operations in reverse order. Each operation only needs to know its own small
derivative rule. Chaining all of those rules together is what gets the gradient
back to every weight in the model.

The part I struggled with was why the code always added to a gradient instead
of replacing it. The small example that helped was:

```text
loss = x * x
```

The same `x` affects the result through both sides of the multiplication. If
`x` is 3, the left side contributes 3 to the gradient and the right side also
contributes 3. Those contributions have to be added together, giving the
expected derivative of 6.

That was the missing piece for me. In a neural network, one weight can affect
the final loss through many different calculations. Its gradient is the sum of
all of those paths. PyTorch does this with entire tensors and a much larger set
of operations, but the basic process is the same as the small Python class I
had just written.

After that, `loss.backward()` felt a lot less magical.

![The two paths through x times x both contribute to the gradient for x](images/building-a-gpt-from-scratch/autograd-gradient-accumulation.png)

## Putting the Transformer Together

The next step was implementing the smaller pieces used throughout the model:
linear layers, softmax, and RMSNorm. Then I could start combining them into the
actual GPT.

What surprised me here was how little new machinery had to be added. A linear
layer was mostly multiplication and addition. Softmax used exponentials,
addition, and division. RMSNorm used squares, an average, and a square root.
All of those operations were already supported by the autograd code, so the
larger model automatically built one much bigger calculation graph.

At a high level, the model looked like this:

```text
token and position embeddings
  -> attention
  -> MLP
  -> attention
  -> MLP
  -> scores for the next word
```

There are normalization and residual connections around those pieces, but this
was the simple picture I kept coming back to. Attention lets token positions
share information with one another. The MLP then does some additional
processing on each position separately.

I found residual connections easier to understand once I stopped thinking of a
layer as replacing the current representation. The layer calculates an update,
and that update is added to what was already there. If the layer has nothing
useful to add yet, the original values still have a direct path through the
model. The same shortcut also gives gradients a cleaner path backward.

## Attention Took the Longest

Attention was the main thing I wanted to understand during this phase, and it
was also the part I spent the most time going back over.

I had seen queries, keys, and values explained a number of times before. The
names are memorable, but I still found it difficult to picture what was
actually being calculated. What helped was separating attention into two
questions.

First, the query and key vectors decide how much attention one token position
should give to another. Then those attention weights decide how much of each
value vector to bring back.

So the queries and keys answer something like "where should I look?", while the
values contain the information that gets collected. These vectors are
recalculated for each occurrence of a token, based on its current
representation. The model isn't learning one fixed relationship that says
`bank` should always pay attention to `river`. It learns the matrices that
produce useful query and key matches depending on the surrounding text.

The causal mask was more straightforward. Since the model is learning to
predict the next word, a position can look at itself and anything before it,
but it can't look at later words. Otherwise it would be able to see the answer
during training.

The scalar attention code made the order of operations fairly easy to follow:

```python
query = linear(hidden, attention.query)
key = linear(hidden, attention.key)
value = linear(hidden, attention.value)

cache_keys.append(key)
cache_values.append(value)

scores = [
    dot(head_query, head_key) / sqrt(head_dim)
    for head_key in head_keys
]
weights = softmax(scores)
attended = weighted_sum(weights, head_values)
```

The actual implementation spells out `dot` and `weighted_sum` using the scalar
`Value` operations. This shortened version is the part I would want to come
back to: make the three projections, compare the query with the stored keys,
turn the scores into weights, and use those weights to combine the values.

![A query is compared with allowed keys, then the resulting weights combine the value vectors](images/building-a-gpt-from-scratch/attention-from-scores-to-context.png)

Multi-head attention took a bit longer. I initially pictured each head as a
more independent thing than it really is. In this model, the 32 numbers used to
represent a token are split across four heads, with eight numbers per head.
Each head runs attention over its own smaller slice, and then the results are
joined back together and mixed with another linear layer.

I don't think I came away with an intuitive explanation for exactly what each
head learns, and that is probably the wrong thing to expect from such a small
model anyway. What I did understand was how the calculation is divided up and
put back together, which was the part I needed before moving on.

## Getting the First Model to Learn Anything

Once the pieces were connected, I trained the scalar model on 20 simple
sentences. It had 1,744 parameters, one attention head, one transformer layer,
and could look at up to eight words at a time.

An untrained model choosing between 57 possible tokens should start with a loss
of roughly `4.04`. After 100 training steps, the loss was down to `2.36`.

Some of its generated sentences looked surprisingly reasonable:

```text
the seed is shy
the brave bell is scared
the gray house
```

Others looked more like what I expected from such a tiny model:

```text
the am drums is the seed
the egg child dog i
```

I kept both kinds of output because they showed more than the loss did. The
model had picked up patterns like `the ... is ...`, even though it didn't have
enough data or capacity to use them consistently.

Originally, I thought I should reproduce the much larger scalar training run
from the book. Once I saw how slowly all of the individual `Value` objects ran
in Python, I reconsidered what I was actually trying to prove. The small run
showed that the loss went down, the saved model could be loaded again, and the
model could generate valid words. That was enough to show that I had connected
everything correctly.

The slowness was also a pretty good introduction to why tensor libraries exist.

## Training and Generating Are Almost the Same Loop

Another thing that became clearer was the relationship between training and
generation. In both cases, the model predicts what should come next.

During training, the real next word is already known. The loss measures how far
the model's prediction was from that answer, and then the weights are updated.
During generation, there is no known answer. The code chooses one of the model's
predicted words, adds it to the input, and runs the model again.

This also made temperature, top-k, and top-p feel less mysterious. They don't
change what the model knows. They only change how the next word is selected
from the scores the model already produced.

Fine-tuning was similar. I had expected there might be a different training
process involved, but it was mostly the same loop with a saved model, a smaller
specialized dataset, and gentler updates. The tricky parts were keeping the
original tokenizer and making sure the model didn't overwrite too much of what
it had already learned.

## Rebuilding It in PyTorch

The last part of this phase was moving the model to PyTorch. This is where all
of the scalar work started to feel worthwhile. I wasn't looking at a completely
different implementation anymore. I could recognize the same operations, just
applied to many values at once.

The part I struggled with now was tensor shapes. The PyTorch model trained on
64 sequences at a time, with 16 token positions in each sequence. Each token
position had 32 features, split into four attention heads:

```text
hidden values:    [64, 16, 32]
attention heads:  [64, 4, 16, 8]
attention scores: [64, 4, 16, 16]
```

The last `[16, 16]` was useful to focus on. For each of the 16 token positions,
there is a score for each position it could pay attention to. The other two
dimensions mean that PyTorch is doing this for all 64 sequences and all four
heads at the same time.

In PyTorch, most of that attention calculation became a few tensor operations:

```python
query = self._split_heads(self.query(hidden), self.config.n_head)
key = self._split_heads(self.key(hidden), self.config.n_head)
value = self._split_heads(self.value(hidden), self.config.n_head)

scores = query @ key.transpose(-2, -1)
scores = scores / sqrt(self.config.head_dim)
allowed = self.causal_mask[:sequence_length, :sequence_length]
scores = scores.masked_fill(~allowed, float("-inf"))
weights = F.softmax(scores, dim=-1)
attended = weights @ value
```

This is the same sequence as the scalar version. Matrix multiplication performs
all of the query-key comparisons together, and another matrix multiplication
combines all of the values using the resulting weights.

Batching had seemed like another layer of complexity when I first looked at
PyTorch language-model code. It eventually clicked that the learning problem
hadn't changed. The model was still looking at some tokens and predicting the
next ones. A batch just packed many of those examples into one tensor operation
so the computer could process them efficiently.

![Scalar Python exposes each attention operation while PyTorch performs the same calculation across batches and heads](images/building-a-gpt-from-scratch/scalar-to-pytorch.png)

The PyTorch version handled 64 windows of 16 tokens in every training step,
which worked out to 1,024 next-token predictions at once. Its loss changed like
this over 5,000 steps:

```text
step     0 | train 6.46 | validation 6.45
step  2500 | train 2.29 | validation 2.44
step  4999 | train 2.19 | validation 2.44
```

The model generated `the sheep is by the tent`. It was still trained on a small
set of simple sentences, so I wasn't expecting much more than that. The
important difference was that this version trained quickly enough to become the
baseline for later experiments.

I could also see the training loss continuing to improve while validation loss
had mostly stopped. That gave me something concrete to call overfitting rather
than just knowing its definition.

The training step itself ended up being the familiar PyTorch pattern:

```python
inputs, targets = get_batch(...)
_, loss = model(inputs, targets)

optimizer.zero_grad()
loss.backward()
optimizer.step()
```

By this point I could connect each line back to the scalar version: build the
calculation graph during the forward pass, clear gradients left over from the
previous step, walk the graph backward, and then update the weights.

## Where I Ended Up

By the end of this phase, I still wouldn't claim to understand every detail of
transformers. There were plenty of smaller things I had to revisit, especially
around tensor dimensions, normalization, and how the attention heads were
arranged in memory.

But I could now follow a token through the model. I understood how its ID chose
an embedding, how attention mixed information from earlier positions, how the
model produced a score for every possible next word, how that became one loss,
and how the gradient found its way back to the weights.

Moving to PyTorch also felt less like handing everything back to a black box.
`loss.backward()` was the larger, tensor-based version of the graph traversal I
had already implemented. Batching was many copies of the same prediction task.
The optimizer was taking the gradients stored on the parameters and turning
them into small updates.

The final model wasn't interesting because of what it could generate. It was
interesting because I understood enough of it to start changing things and have
some idea of what those changes meant. That became the goal of the next phase:
varying the model's size and architecture one part at a time and seeing what
actually happened.
