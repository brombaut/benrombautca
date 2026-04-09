# From Checklists to Prose Verdicts: Building an Architectural Evaluation Pipeline

This is the development story behind the architectural evaluation pipeline I've written about in two previous articles, one analyzing what Claude thinks is architecturally important, and another measuring how architecturally demanding SWE-bench Verified actually is. Those articles describe the pipeline's outputs. This one describes how the pipeline got built, what broke along the way, and what I learned from 12 experiments of pressure-testing assumptions about how to evaluate code architecture with AI.

The core question stayed the same throughout: can an AI agent look at an issue, explore a codebase, infer what "architecturally good" looks like for that context, and then evaluate candidate patches against that standard?

What changed from experiment to experiment was the answer to a harder question: what kind of rubric actually holds up once you start comparing many patches, many issues, and many evaluators?

## What I Was Trying to Build

I was not trying to build a general "is this patch good?" grader.

The target was narrower and more architectural. Ignore implementation correctness. Focus on whether a patch fits the codebase's existing structural logic. Reward extending existing mechanisms over introducing parallel ones. Penalize boundary violations, wrong-layer fixes, structural duplication, and unnecessary blast radius. Make the evaluation robust enough that scores mean something across multiple patches for the same issue.

That sounds straightforward until you try to operationalize it. The hard part is not generating a rubric once. The hard part is generating a rubric that remains coherent when the patch uses a different but equally valid mechanism, when the evaluator has to make threshold calls near boundaries, when two similar patches are judged by different runs, and when the codebase doesn't match the architectural assumptions baked into the rubric template.

Most of the 12 experiments were responses to one of those problems.

## Getting a Rubric to Exist at All

The earliest work was just getting the loop off the ground. Build a rubric-generation skill. Build a patch-evaluation skill that can use those rubrics. Try them on a small set of SymPy and RefactorBench-style examples.

At this stage I wasn't aiming for high-confidence evaluation quality. I was proving the workflow was even possible: explore a codebase, infer architectural expectations, write them down as a rubric, score a patch against that rubric.

It worked, in the sense that Claude Code could produce structurally meaningful observations rather than just style comments, and it was possible to push evaluation away from "did tests pass?" toward "did this preserve the codebase's design logic?" But the rubric structure was primitive, the evaluations weren't battle-tested, and too much of the rubric logic was implicit in the prompt rather than committed into outputs that later evaluators could reuse.

The real lesson from these first experiments: generation was feasible, but calibration and repeatability would be the actual problems.

## Separating Architecture from Correctness

The next experiments made what turned out to be the most important conceptual correction in the whole project: architectural evaluation is not the same thing as correctness evaluation.

That seems obvious in hindsight, but it matters a lot. If a rubric quietly mixes "architecturally clean" with "functionally right," it becomes impossible to tell what's being measured. So I explicitly excluded implementation correctness from the rubric's scope and reframed evaluation around architectural conformance only, using continuous 0-1 scoring with multiple rubric items per axis.

The evaluation target became much cleaner. It was easier to ask focused questions like "did this preserve the existing mechanism?" instead of blurring that with "does this fully solve the bug?" The rubric became more useful for comparing different patches that all "worked" functionally but took different structural approaches.

But the itemized, continuous scoring setup was too checklist-shaped. Here's what a rubric axis looked like at this stage, from a Django admin ordering issue:

```yaml
boundary_preservation:
  weight: 0.35
  rubrics:
    - id: "BP1"
      description: "Respects admin-to-ORM boundary by using field.get_choices(ordering=...)
        API rather than direct model queries"
      metric: "All choice retrieval uses field.get_choices() method, zero direct
        queries to field.remote_field.model"
      threshold: "No new direct queries to related model"
      weight: 3

    - id: "BP2"
      description: "Maintains encapsulation of ordering logic within admin layer"
      metric: "Ordering decisions made in admin code, not leaked into ORM queries"
      threshold: "No ordering-related changes to model or queryset layer"
      weight: 2
```

Each item gets a binary pass/fail against its threshold, weighted and summed into a 0-1 score. The problem is that a patch could satisfy BP1 and BP2 and still be architecturally off, because the checklist can't express "this patch introduces a parallel mechanism that duplicates existing logic." It rewarded local compliance while missing larger structural problems. A checklist rubric can catch individual violations but miss the overall structural fit, which is the thing you actually care about.

## The First Real Test

The first production-style run used 6 medium-difficulty SWE-bench Verified issues, evaluating official resolved patches alongside Claude Code-generated patches.

The headline result was strong. Claude Code ranked near the top and looked competitive against the resolved submissions. Architectural evaluation clearly separated stronger and weaker patch strategies. But the rubric still behaved like a well-organized checklist, sometimes under-penalizing bigger architectural violations, and the continuous 0-1 scheme created an illusion of precision.

## Holistic Scoring Changes Everything

The next experiment kept the same dataset and changed the rubric itself. This was the first major scoring redesign: move from continuous 0-1 item scoring to discrete 0-5 axis scoring. Evaluate each axis holistically by level descriptions. Treat architecture more like a structural judgment than a checklist tally.

This turned out to be one of the most useful shifts in the whole sequence.

The same axis now looked like this, from an Astropy WCS wrapper issue:

```yaml
architectural_alignment:
  weight: 0.30
  rubric:
    5:
      label: "Excellent"
      criteria: |
        Perfectly maintains Wrapper pattern in SlicedLowLevelWCS. All changes
        within world_to_pixel_values or helper methods, preserving delegation
        model. Does not modify self._wcs. Maintains abstract method contract
        signatures. No new architectural styles introduced.

    3:
      label: "Acceptable"
      criteria: |
        Follows Wrapper pattern in most changes but introduces inconsistencies.
        Adds public method that doesn't follow delegation pattern, or modifies
        multiple methods beyond world_to_pixel_values without clear justification.

    1:
      label: "Poor"
      criteria: |
        Minimal adherence to Wrapper pattern. Uses different approach: direct WCS
        manipulation instead of wrapping. Introduces 4+ new dependencies.
```

Instead of checking individual items against thresholds, the evaluator reads the level descriptions and makes a holistic judgment about where the patch falls on the spectrum. The question shifts from "did this pass each check?" to "how well does this preserve the system's structural logic?"

The new rubric was stricter in the right way. It caught issues the old version had softened or missed, including layer violations, parallel mechanisms, and architectural compromises hidden by partial item compliance. Claude Code's relative standing actually improved under the stricter rubric, which suggested its patches had genuinely better structural integrity rather than just better checklist coverage. That was a reassuring signal.

Running both rubric versions on the same 6 issues made the difference concrete:

| Model | Checklist Score | Holistic Score | Change |
|-------|----------------|----------------|--------|
| Claude Code | 96.8% | 93.1% | -3.7% |
| Gold Standard | 99.5% | 92.1% | -7.4% |
| OpenHands Claude 4 | 96.4% | 87.0% | -9.4% |
| SWE-Exp DeepSeek-V3 | 96.3% | 85.6% | -10.7% |

Every model scored lower under the holistic rubric, but the drops weren't uniform. Models that had been gaming the checklist (high item compliance, weaker structural integrity) fell further. Claude Code had the smallest drop and moved from #2 to #1, which suggested the checklist had been flattering patches that looked locally clean but had broader structural issues.

But holistic scoring also increased room for evaluator discretion. As soon as you have level boundaries, you have threshold ambiguities. The rubric became better at architectural judgment and more vulnerable to inconsistency between runs.

## Scaling Up Reveals the Cracks

Scaling from 6 issues to 9 was when the problems got concrete. A lot of evaluation systems look good on a small sample and then start wobbling as diversity increases.

Claude Code still performed well. The evaluation still produced plausible top-level results. But scaling exposed three specific failure modes that I hadn't seen clearly before.

**Baseline variance.** Different evaluations were sometimes comparing patches against different baseline measurements for the same issue. That meant scores were no longer fully comparable.

**Missing removal verification.** Evaluations were good at checking what a patch added. They were worse at checking whether the old problematic structure had actually been removed. That let structurally incomplete patches look cleaner than they were.

**Thoroughness variance.** Some evaluations explored the codebase deeply, others did a shallower pass. Those differences in exploration depth leaked directly into score quality.

This was a pivotal experiment because it moved the project out of the vague zone of "maybe the rubric is inconsistent" into the concrete zone of "here are specific mechanisms producing inconsistency." A plausible rubric is not enough. If the baseline, exploration depth, and deletion checks aren't standardized, the scores aren't trustworthy.

## Making Evaluation Mechanically Comparable

The next version was less about inventing a new theory of architectural quality and more about making evaluation mechanically comparable.

Three targeted fixes. First, baselines were calculated once during rubric generation, with the measurement methodology committed into the rubric so that patch evaluators would reuse it rather than silently re-deriving it. Second, evaluation now explicitly checked what code was removed, not just what was added. Third, evaluation depth was made explicit and expected to stay uniform across patches for a given issue.

The evaluation became meaningfully more stable. Several concrete inconsistencies from the previous experiment were directly addressed. The rubric started behaving more like an instrument and less like a loosely guided essay.

But even with better mechanics, there were still small ranking anomalies. Some score differences were clearly noise rather than genuine quality separation. The system had become more disciplined, but not fully calibrated. Consistency problems don't end once you fix obvious process variance. They reappear at the level of interpretation.

## The Scoring Consistency Audit

This is where the work became more self-critical in a useful way. I expanded the comparison across multiple models and then performed a post-hoc scoring consistency audit. That audit was one of the most important pieces of the whole project because it separated three things that are easy to conflate: real architectural differences between patches, harmless noise near score boundaries, and systematic evaluator inconsistency.

Three recurring failure modes showed up.

**Threshold boundary calls.** Evaluators made different decisions when a metric sat near a threshold. Small judgment differences became visible as score differences that looked more meaningful than they really were.

**Inconsistent severity language.** Similar violations were described as "minor" in one run and "moderate" in another. Once severity language drifts, the numeric score tends to drift with it.

**Cross-evaluator calibration.** Within a single evaluation, scores were often coherent. Across different evaluations of different patches, the threshold interpretation changed subtly.

The audit also surfaced a subtler problem: the skills themselves were getting overfit to the experiment history. Over time, the prompts had accumulated a fixed six-axis template, an issue-type weight table, and a hardcoded exception-handler check. Each had a good local reason for being added. Together, they were pushing the system toward Django/Astropy-shaped evaluation rather than codebase-specific architectural reasoning.

I responded by improving methodological commitment: explicit definitions for metrics, instructions to use committed baselines, a weight floor to discourage low-weight noisy axes. It helped. But some of that prescription was solving yesterday's problems by hardcoding yesterday's examples.

This is the fundamental tension in prompt engineering: you can reduce inconsistency by specifying more, but over-specification biases the rubric toward the datasets that taught you those rules.

## Letting the Codebase Drive the Evaluation

The corrective swing against accumulated prompt bias was one of the most important experiments. The core change was philosophical: stop assuming every codebase needs the same fixed architectural axes. Let the codebase exploration determine what axes matter. Remove hardcoded checks unless the exploration justifies them.

Concretely, I removed the fixed six-axis template, the issue-type weight table, and the hardcoded exception-handler check. I added a cross-axis calibration pass and explicit boundary-call documentation so threshold discretion had to be surfaced rather than hidden.

This was an important maturation step. Instead of asking the evaluator to fill in a pre-labeled scorecard, it asked the evaluator to infer the scorecard from the system under study.

The skills became more codebase-driven and less obviously biased by prior experiments. But this experiment also produced the biggest surprise of the whole project.

Even when Claude Code generated both the rubrics and the patches, the patches did not reliably match the architectural ideal described by the rubrics.

The rubric-generation workflow naturally involved deep architectural reconnaissance. The patch-generation workflow could still lapse into implementation search. So the system could often *describe* the right architectural move without actually *taking* it when writing the patch.

I found this genuinely interesting. It's not just a patch-generation bug. It says something broader: architectural understanding and architectural execution are related, but they're not identical capabilities. The model can articulate what the right structural approach looks like and then not follow it. A "know vs do" gap.

The response was practical. I updated the patch-generation prompt with a simple but strategically important instruction: before implementing, understand the patterns in the affected area and prefer extending existing mechanisms over building new ones. That sentence tries to import the reconnaissance behavior from rubric generation into patch generation. I also restructured the rubric-generation workflow operationally, delegating YAML generation and validation to subagents with isolated context to reduce contamination from the main conversation.

Some problems aren't rubric-theory problems. They're workflow problems.

## Numeric Scores Reach Their Limits

The final major experiment is where the project stopped trying to squeeze everything into a weighted 0-5 framework.

By this point, the numeric system had shown both its value and its limits. It offered finer-grained ranking, it was easy to aggregate and compare, and it imposed useful structure on the evaluation. But it encouraged false precision, it sometimes rewarded mechanism matching instead of property satisfaction, and it could miss semantic architectural failures if those failures weren't cleanly represented in axis criteria.

So I replaced numeric 0-5 scoring with prose-based evaluation and categorical verdicts like High, Acceptable, and Low. Here's what an evaluation looked like in the new format, for the same Astropy WCS issue:

```yaml
verdict:
  classification: "High"
  rationale: |
    Both primary axes show exemplary conformance. The WCS API contract is fully
    preserved: method signature, dimensional semantics, and caller-visible
    behavior are unchanged. The wrapper delegation pattern is maintained
    precisely: only the expansion step is modified, using the existing
    _pixel_to_world_values_all helper, while the delegation call and output
    contraction remain untouched. No new state is introduced, and the structural
    asymmetry that was the root cause of the bug is cleanly resolved.

  scope_clarification: |
    This verdict is based on ARCHITECTURAL QUALITY only. A verdict of "High"
    does not guarantee the patch is bug-free or functionally correct.
```

And the per-axis assessments became prose paragraphs rather than numbers:

| Axis | Priority | Assessment |
|------|----------|------------|
| WCS API Contract Conformance | Primary | Fully preserves the BaseLowLevelWCS interface contract. Method signature, input/output dimensionality, and delegation semantics are unchanged. |
| Wrapper Delegation Integrity | Primary | Maintains the three-step delegation pattern (expand, delegate, contract). Only the expansion step is modified; the delegation call and output contraction are untouched. |
| Dimension Tracking Consistency | Secondary | No new instance attributes introduced. Computes dropped-dimension values on the fly using existing helpers. |
| Inverse Operation Symmetry | Secondary | Resolves the structural asymmetry between pixel_to_world_values and world_to_pixel_values. Both methods now use actual coordinate values for dropped dimensions. |

Prose evaluation was genuinely better at catching semantic architectural errors, tracing a mechanism's blast radius beyond the immediate patch, recognizing that two different mechanisms can be architecturally equivalent, and calling out dead code and structural noise that numeric axes had sometimes let through.

But it was worse at fine-grained separation within the top tier, producing neat aggregate statistics, and constraining evaluator judgment in a reproducible way.

The tradeoff is clear. Numeric scoring gives you precision, but some of it is false. Prose verdicts give you better reasoning depth, but some of the nuance collapses into broad categories. The right system probably combines prose judgment with better anchors, not pure numbers or pure freeform narrative.

## What Held Up Across All 12 Experiments

A few ideas kept proving themselves.

**Separating architecture from correctness.** This was one of the earliest decisions and it held up the whole way through. When the rubric focuses on architecture, structural fit becomes visible, parallel mechanisms become visible, wrong-layer fixes become visible. If correctness is mixed in, those signals get blurred.

**Holistic judgment over itemized checklists.** The shift from continuous item scoring to holistic axis scoring was the first major quality jump. Checklist rubrics feel objective, but they're often objective about the wrong thing. Architecture is about whether the patch preserves or extends the system's existing structural logic, not about how many local boxes it checked.

**Committed methodology.** Whenever baselines, counting rules, or definitions were left implicit, evaluator variance filled the gap. The project improved substantially once rubrics started committing how metrics were measured, what the baseline was, what counted as blast radius, and what counting scope applied. If those details aren't committed, they get silently reinvented at evaluation time.

**Codebase-derived evaluation.** The fixed-axis phase was useful, but it eventually became clear that it was imposing a worldview onto the codebase instead of reading the codebase on its own terms. Letting axes emerge from exploration was the right move, even if it increased the burden on the evaluation pipeline.

## What Didn't Work, or Only Worked Temporarily

**Fine-grained numeric scores created false confidence.** Scores like 4.10, 4.35, and 4.90 look precise. Often they weren't. Sometimes they represented real distinctions, sometimes threshold ambiguity dressed up as measurement.

**Hardcoding yesterday's failure mode into tomorrow's rubric.** This happened repeatedly and understandably. One experiment reveals a miss, a new prompt rule gets added to catch that exact miss, the next version is more robust locally and more biased globally. That's a natural path in prompt engineering, but it doesn't generalize indefinitely.

**Evaluating the right thing didn't guarantee generating the right thing.** This may be the most interesting failure in the project. The model could generate a strong rubric describing the right architectural move, yet still generate a patch that failed to follow that move.

**Pure prose wasn't a complete answer either.** Prose verdicts fixed some of the numeric system's weaknesses, especially around semantic reasoning and mechanism equivalence. But they also flattened distinctions that were sometimes worth preserving.

## What I'd Compress the Whole Project Into

If I had to distill 12 experiments into a handful of durable lessons:

**The hard part is not generating a rubric, it's generating one that survives comparison.** A single rubric can look impressive in isolation. The real test is whether it still makes sense when multiple patches are compared on the same issue, similar patches are judged similarly, and different evaluators don't quietly change the measurement rules.

**Architectural evaluation needs both exploration and commitment.** Exploration is how the system discovers what matters in this codebase. Commitment is how it stops later evaluators from reinterpreting what was discovered. Exploration without commitment drifts. Commitment without exploration calcifies.

**A rubric should describe architectural properties, not prescribe specific mechanisms.** If the rubric says "the correct patch calls this specific function," it stops evaluating architecture and starts evaluating imitation. A stronger rubric asks whether the patch preserves the relevant structural property, even if it reaches that property by a different but architecturally sound route.

**The evaluation stack itself needs architecture.** By the later experiments, the work was not just about patch architecture. It was also about evaluation architecture: when do subagents help, what context should be isolated, what gets committed into the rubric, what gets recalculated, where does calibration happen. The quality of the evaluation depended heavily on the structure of the evaluation process.

## Where It's Heading

The project started with fixed axes, checklist scoring, numeric precision, and implicit evaluator judgment. It moved toward codebase-derived axes, holistic judgment, committed measurement methodology, explicit calibration, and prose-based reasoning about architectural properties.

The next step is probably a hybrid: property-based rubrics derived from exploration, prose axis judgments with explicit conformance anchors, stronger verdict-boundary rules, required gap reporting, explicit blast-radius tracing, and enough categorical structure to preserve comparability without pretending to have more precision than the evaluator actually has.

What I like about this project is that it records the real shape of prompt-and-evaluation research. The progress was not linear. Most improvements came from finding out that something apparently sensible failed under pressure. A checklist missed structural violations. A metric wasn't measured consistently. A rubric overfit to the examples that inspired it. A model could articulate the right architecture without implementing it. A numeric score implied more certainty than the process could honestly support.

That's why the experiments are useful as a sequence rather than just as a latest version. The value is not only in where the rubric ended up. It's in seeing how each failure forced a better question.
