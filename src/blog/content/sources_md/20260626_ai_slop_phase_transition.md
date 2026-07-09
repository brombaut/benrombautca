# When Code Is Cheaper to Produce Than to Justify

I've spent the last few months researching how AI-generated code fails. Not the obvious stuff, like syntax errors or hallucinated APIs, but the subtler patterns that accumulate in codebases where AI agents do most of the writing. This post covers what I think is the most important finding: the problem isn't mainly about new kinds of defects. A follow-up post catalogs what slop actually looks like across eleven families.

## Three Tiers of AI Code Quality

The instinct is to think of "AI slop" as a new category of defect. And there is a genuinely new category: narrator comments that explain what the model just did, hallucinated imports of packages that don't exist, cross-language contamination where Python idioms leak into JavaScript, fake-done stubs where a function claims to enforce a rate limit but just returns `True`. These are real, and they're distinctive to AI.

But they're not the whole story. When I scanned AI-generated repositories against human-written reference solutions for the same tasks, several old patterns showed up at elevated rates in the AI output: unused imports at 2.8x the reference rate, broad exception handlers at 2.1x. A survey of 70+ AI code quality tools reinforced the same picture. Of the 575 individual rules I cataloged across 42 tools, 109 fell into a gray zone: patterns that predate AI but appear disproportionately in AI output. Swallowed exceptions flagged by 18 tools, unused declarations by 12, broad/bare except by 10. These are AI-focused tools that bundle traditional smell detection alongside their AI-specific rules because practitioners found AI makes those old problems worse.

AI code quality has three tiers: traditional smells (the same ones we've always had), gray smells (old patterns at elevated rates), and AI-specific slop (genuinely new defects). A useful quality tool can't only target the new stuff.

The AI-specific tier is the strange one because the code can look like progress while quietly changing the truth of the system:

```python
def enforce_rate_limit(user_id: str, action: str) -> bool:
    """Return whether the user is allowed to perform this action."""
    # TODO: integrate with Redis-backed limiter
    return True
```

That is not just an incomplete TODO. It is an executable success path. Everything downstream can now behave as if rate limiting exists, while every request is actually permitted.

## Boredom Was a Quality Control

The deeper question is *why* AI produces these patterns. The answer comes down to economics.

Clean code was a scarcity discipline. Everything about the pre-AI quality movement was engineered against the failure modes of a specific producer: a human working under human economics. Think about what we brought to the table that we never recognized as quality mechanisms. Typing cost made verbosity self-limiting. Boredom was a built-in repetition detector ("I'm sick of writing this, I'll extract a helper"). Fatigue was a stopping rule. Shame was a pre-commit hook. Knowing the codebase was the deduplicator. Consequence ownership made gaming your own tests self-harm. And critically, in humans the ability to produce large volumes of code correlated with the seniority to know better. Juniors with poor judgment were slow, which capped their blast radius.

When we replaced the human producer with an LLM agent, we lost all of these limiters at once. The quality mechanisms were bundled with the producer, and we automated away both.

The result is a producer whose characteristic failures are the opposite of human failures. Humans fail by omission: too few tests, missing documentation, copy-paste instead of careful abstraction. AI fails by commission: too much code, too many tests, too many comments, the same logic written from scratch because the model doesn't remember it exists, hedging compiled into control flow because the model doesn't know the correct type, and code that looks correct but silently does nothing.

The hedging often shows up as "careful" code that has no relationship to the actual contract:

```typescript
const customerId =
  request?.body?.customer?.id ??
  request?.query?.customerId ??
  request?.headers?.["x-customer-id"] ??
  "unknown";
```

If the route contract says `customer.id` is required, this fallback chain is not robustness. It is uncertainty compiled into production behavior.

## Chesterton's Fence Falls

There's a classical principle that says you shouldn't remove something until you understand why it was put there, because its existence is evidence that someone had a reason. This works when building is expensive. If building a fence required effort, finding one standing was genuine evidence of intent.

When building the fence is nearly free, the principle breaks. The model produces abstractions, guard clauses, helper functions, and entire modules at no cost to itself, with no memory of why and no stake in whether they serve a purpose. Existence no longer carries evidence of intent. The presumption reverses: instead of "justify why you want to remove this," the default becomes "justify why this should stay."

For the first time in the history of the discipline, code is cheaper to produce than to justify.

## When Good Metrics Go Bad

One consequence of this shift is that signals traditionally used to measure code quality now point in the wrong direction. This one genuinely caught me off guard.

Comment density was a positive signal when humans were too lazy to document. Under model overproduction, dense comments signal noise: restating comments, narrator comments, step-by-step annotations that add nothing beyond what the code already says.

```python
# Check if the user is active
if user.is_active:
    # Send the welcome email
    send_welcome_email(user.email)
```

There is nothing to preserve here. The comments are not design intent, business context, or a warning about a non-obvious edge case. They are a transcript of the next line.

Code coverage was positive when humans skipped writing tests. Under model overproduction, high coverage can mean tests that verify the type system, the framework, or mock behavior rather than business logic. nWave documents ten patterns of fake tests, including a circular verification pattern where the test recomputes the expected value using the same formula as the production code, making failure impossible.

```python
def test_calculate_tax():
    amount = 100
    rate = 0.15
    expected = amount * rate

    assert calculate_tax(amount, rate) == expected
```

This test raises coverage, but it does not protect behavior. If the production implementation uses the same wrong formula, the test stays green.

Clone detection shows the same inversion. Traditional detectors look for copy-paste duplication: textual similarity. But models don't copy-paste. When a model needs a helper that already exists, it writes a new one from scratch. Same logic, different names, different structure, different file. Traditional clone detectors catch the shrinking fraction (human-style copy-paste) and miss the growing fraction (model-style regeneration).

```typescript
export function formatDuration(ms: number): string {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  return `${minutes}m ${seconds % 60}s`;
}
```

```typescript
export function humanizeElapsedTime(milliseconds: number): string {
  const totalSeconds = Math.trunc(milliseconds / 1000);
  const mins = Math.trunc(totalSeconds / 60);
  const secs = totalSeconds - mins * 60;
  return `${mins}m ${secs}s`;
}
```

Textually, these are different enough to evade simple clone detection. Semantically, the second function probably should not exist.

## What Real Teams Are Seeing

The theoretical argument is interesting on its own. What makes it concrete is that teams are already dealing with this at scale.

**OpenClaw** (378K stars, roughly 150 commits per day from AI agents). One maintainer deleted 11,903 lines of dead code in a single cleanup pass: orphaned provider integrations, duplicate barrel files, dead extension subsystems. All of it less than 7 months old. He then spent 34 hours over two days on 50+ dedup commits, consolidating local helpers agents had regenerated instead of reusing. The `r: too-many-prs` label has been applied to 1,892 PRs.

> "We've been hit with waves of spammy PRs: AI slop posted across dozens of PRs, duplicates of the same change, and low-effort noise that burns reviewer time."

**OpenAI Harness** (internal, zero manually-written code, roughly 1M lines). The team spent every Friday, 20% of the week, cleaning up AI slop. The primary pain was architectural drift: agents building on guessed shapes instead of reusing shared utilities.

> "Our team used to spend every Friday (20% of the week) cleaning up 'AI slop.' Unsurprisingly, that didn't scale."

**GitLab Orbit** (135K-line Rust codebase, roughly 95% AI-generated). Pain escalated over 5 months from "use this skill to clean up" to "do not write in the first place." A cleanup found 41 identical test blocks, a wildcard check duplicated 4 times, and 21 unused dependencies, in a codebase only 4 months old.

**Superpowers** (229K stars). The maintainer audited the last 100 closed PRs and found a 94% rejection rate. Open issues document agents fabricating entire subagent dialogues instead of dispatching real tool calls.

> "About every other day we get somebody submitting a pull request that is 60,000 lines of diff."

Industry-scale data supports the pattern. LinearB's study of 8.1 million PRs found AI PRs accepted at 32.7% versus 84.4% for human PRs, with agentic PRs waiting 5.3x longer for pickup. GitClear found copy-pasted lines rising while moved/refactored lines dropped. Google's DORA report estimated that for every 25% increase in AI adoption, delivery stability drops 7.2%, even as reported code quality increases 3.4%.

## What Teams Are Converging On

The most interesting finding wasn't the problem but how teams independently arrive at the same solutions.

**Prompt-only approaches don't work.** A SciPy maintainer tested an AGENTS.md with soft guidelines against a stripped version. The agent completed the work under both. Soft guidelines had zero deterrent effect. Another project found that negative instructions ("don't do X") degraded overall quality: the model became hesitant about everything.

**Two focused agents beat one constrained agent.** Multiple teams independently converged on cleanup as a pipeline stage, not a prompt constraint. Generate first, then clean in a separate pass with a separate agent.

**Deterministic plus LLM is the production architecture.** Every team that gets serious about slop arrives at deterministic pre-filtering (AST analysis, module graphs, regex patterns) combined with LLM judgment as a later stage. Pure-prompt approaches are absent from the top of every ranking.

Cleanup needs to be a recurring development phase, not a post-hoc report. The question isn't whether to clean, but when and how often.

## References

- <https://github.com/nWave-ai/nWave>
- <https://github.com/openclaw/openclaw/issues/38283>
- <https://github.com/openclaw/openclaw/pull/91020>
- <https://openai.com/index/harness-engineering/>
- <https://gitlab.com/gitlab-org/orbit/knowledge-graph/-/blob/main/AGENTS.md>
- <https://blog.fsck.com/2026/03/31/slop-prs/>
- <https://github.com/obra/superpowers/issues/1749>
- <https://github.com/obra/superpowers/issues/1701>
- <https://linearb.io/resources/engineering-benchmarks>
- <https://www.gitclear.com/ai_assistant_code_quality_2025_research>
- <https://dora.dev/research/2024/dora-report/>
- <https://discuss.scientific-python.org/t/agents-md-and-claude-md-addition-to-scipy-repository/2233>
