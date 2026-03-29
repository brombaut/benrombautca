# Most of SWE-bench Verified Doesn't Require Deep Architectural Understanding

I wanted to know how architecturally demanding SWE-bench Verified actually is. Not whether the problems are *hard* in general, but specifically: how much do you need to understand about a codebase's architecture to solve them?

So I had Claude Code with Opus 4.6 evaluate all 500 instances in SWE-bench Verified. For each one, the model explored the repository, examined the problem, and rendered a verdict: how much codebase-specific architectural understanding would a developer need to produce a correct fix? The verdicts range from `trivial` (fix is derivable from the changed file alone using general programming knowledge) to `expert` (requires comprehensive understanding of the system's architecture, both deep structural knowledge and wide exploration).

## The Pipeline

The verdicts come from an architectural evaluation pipeline I've been building. It has three stages:

**Stage 1** is what we're analyzing here. For each SWE-bench Verified instance, the model receives the problem statement, the gold patch, and full access to the source repository. It judges how much codebase-specific architectural understanding a developer would need to produce a correct fix, outputting a complexity verdict from `trivial` to `expert`.

**Stage 2** generates architectural rubrics. For each instance, the model explores the codebase, identifies its architectural patterns and critical boundaries, and produces a structured YAML rubric describing which structural properties matter most for evaluating a patch.

**Stage 3** takes a patch and evaluates it against the rubric, producing a categorical verdict on architectural conformance.

This article covers Stage 1.

All three stages run Opus 4.6 inside Docker containers, one per SWE-bench Verified instance. Everything is static structural analysis, no code execution.

### How Stage 1 Works

The evaluator receives three inputs: a problem statement, the gold patch (the known-correct fix), and the full source repository. The patch isn't being evaluated. It's used as a guide. The model uses it to know where to start exploring, then works outward to assess how much architectural context a cold-start engineer would need to arrive at that fix independently.

The core question: imagine a skilled engineer who knows Python, knows the relevant libraries, knows the domain, but has never seen this codebase before. How much would they need to learn about *this codebase's specific architecture* before they could produce the correct patch?

The evaluation proceeds in steps. First, the model reads the problem statement and patch to identify what changed and where. If the patch is purely cosmetic (comments, docs, formatting), it fast-paths to `trivial` without further exploration. Otherwise, it dispatches an exploration subagent.

The subagent starts from the files changed in the patch and explores outward. For each changed file, it traces callers and callees until it crosses an architectural boundary or the relevant context is clear, examines interfaces and contracts the changed code participates in, identifies shared state or invariants, and looks at sibling implementations that establish conventions a solver would need to follow. It also identifies rejected fix paths: plausible-but-wrong approaches that a cold-start engineer might try, and why each would fail due to codebase-specific architecture.

Based on the exploration, the model assesses five independent axes:

- **Scope of context**: How much of the codebase do you need to read? From `minimal` (just the changed file) to `system_spanning` (the overall system architecture).
- **Dependency chain depth**: How many architectural boundary crossings from the change site? Intra-file hops don't count. From `shallow` (0-1 hops) to `deep` (4+ layers of abstraction).
- **Implicit knowledge**: How much codebase-specific knowledge isn't obvious from the changed code? From `minimal` (locally understandable) to `deep_invariants` (system-wide implicit contracts emergent from structure).
- **Coordination complexity**: How many components need to work together? Assessed at two levels: *changes* coordination (do the edits themselves span boundaries?) and *reasoning* coordination (does understanding *why* the fix is correct require cross-boundary knowledge?). The final label takes the higher of the two.
- **Insight density**: How hard is it to extract the relevant architectural understanding, assuming you already know which files to read? From `low` (documented or directly visible) to `expert` (emergent from synthesizing multiple design decisions at runtime).

It also assesses structural depth (localized to system-wide) and exploration surface area (how many files need substantive reading), and synthesizes everything into a final verdict: `trivial`, `low`, `moderate`, `high`, or `expert`.

An important scope constraint runs through the entire evaluation: only codebase-specific knowledge counts. General language semantics, external library APIs, domain knowledge, and algorithmic complexity are all out of scope. "You need to understand how OAuth works" doesn't count. "You need to understand how *this codebase* routes authentication through its middleware stack" does.

The output for each instance is a YAML file with this structure (prose fields trimmed for brevity):

```yaml
metadata:
  instance_id: "django__django-16139"
  evaluator: "architectural-understanding-evaluation-v4"
  fast_path: false
  multi_change_patch: false

structural_depth:
  label: "component_scoped"  # localized | component_scoped | cross_component | system_wide
  rationale: |
    Why this structural depth was assigned, grounded in exploration findings.
  nearest_alternatives:
    localized: "Why localized was ruled out."
    cross_component: "Why cross_component was ruled out."

exploration_surface_area:
  label: "moderate"  # low | moderate | high | extensive
  file_count: 5
  area_count: 2
  rationale: |
    How much of the codebase needed to be navigated and why.

final_verdict:
  label: "moderate"  # trivial | low | moderate | high | expert
  rationale: |
    How structural depth, surface area, and insight density combine
    to produce this verdict.

rejected_fix_paths:
  - path: "Description of a plausible-but-wrong approach"
    why_wrong: "Why it fails due to codebase-specific architecture"

axes:
  scope_of_context:
    level: "single_component"  # minimal | single_component | multiple_components | system_spanning
    assessment: "Prose assessment referencing specific modules and components."
    key_evidence:
      - "path/to/file.py — why this was relevant"

  dependency_chain_depth:
    level: "moderate"  # shallow | moderate | deep
    assessment: "Prose assessment describing the chains traced."

  implicit_knowledge:
    level: "some_conventions"  # minimal | some_conventions | architectural_conventions | deep_invariants
    assessment: "Prose assessment of non-obvious codebase-specific knowledge required."

  coordination_complexity:
    level: "cross_boundary"  # independent | locally_coordinated | cross_boundary | system_wide
    changes_coordination: "locally_coordinated"
    reasoning_coordination: "cross_boundary"
    assessment: |
      Prose assessment addressing both levels. The edits are local to one
      component, but understanding why they're correct requires reading
      across the boundary into the calling code.

  insight_density:
    level: "moderate"  # low | moderate | high | expert
    assessment: "Prose assessment of how hard it is to extract the relevant understanding."

files_explored:
  - "path/to/file1.py"
  - "path/to/file2.py"
  - "path/to/file3.py"
```

Each axis includes its own scale definitions and key evidence in the full output. The coordination axis is the only one assessed at two sub-levels (changes vs reasoning), which is where the divergence analysis later in this article comes from.

### How the Evaluation Was Developed

The skill described above is the result of several iterations, and the design choices reflect specific problems I encountered along the way.

The earliest versions didn't use the gold patch at all. The model explored blind from just the problem statement, which meant it had to figure out where in the codebase the problem lived before it could assess architectural complexity. This worked but was expensive. Giving it the gold patch as a starting reference, just to know which files are involved, cut exploration costs significantly without changing the thing being measured. The model still has to explore outward to assess how much architectural context surrounds the change; it just doesn't have to spend tokens finding the change site.

The biggest conceptual shift came early. Initial versions were measuring something closer to "how hard is this problem" than "how much codebase-specific architectural understanding does it require." The model would rate an XSS-related issue as highly architecturally complex because XSS involves understanding multiple technology layers (browsers, HTTP, encoding, injection vectors). But actually fixing the issue in the codebase was straightforward, a localized change in one file. The problem was hard in a domain-knowledge sense, not in a codebase-architecture sense. This is what led to the cold-start engineer framing and the repeated scope constraint that only codebase-specific knowledge counts. General domain knowledge, external library APIs, language semantics: all explicitly excluded.

The five axes evolved significantly across iterations. Early versions tried to be too specific about what counts as architecturally important, which ended up biasing the model toward my own thinking about architecture. That's not what I wanted. The goal was to let the model assess architectural complexity on its own terms, based on what it found during exploration, not to have it confirm my priors about what "good architecture" looks like. So I iterated toward more general axes that ask open-ended questions (how much context? how much implicit knowledge? how much coordination?) rather than prescribing specific architectural concerns.

The skill includes an unusually long "Common Mistakes to Avoid" table (19 entries) and a "Red Flags" section listing assessment smells. Some of these were anticipated during design, but many were added reactively after watching the model get things wrong on real instances. The scope-creep guards (don't count Python's GIL as architectural knowledge, don't count external library APIs) came directly from seeing the model inflate scores by treating general technical knowledge as codebase-specific understanding. The "small patch does not equal low understanding" guard came from watching the model assume one-line fixes were trivial without exploring.

The trivial fast-path (skip exploration entirely if the patch only touches comments, docs, or formatting) is a cost optimization. Running full exploration on a patch that changes a docstring is a waste of compute. This is a pragmatic shortcut, and as discussed in "What I'd Change," it comes with a tradeoff: we never actually verify those instances on the axes.

## 62% Trivial or Low

![Verdict distribution](images/swebench-architectural-complexity/verdict_distribution.png)

The model considers most SWE-bench Verified problems architecturally simple. 62% of instances land at trivial (20%) or low (42%), problems where you could produce a correct fix by reading the problem statement and at most one component. Only 35% reach moderate, and just 13 instances (2.6%) hit high. Zero instances received an expert verdict.

The model never once judged that a SWE-bench Verified problem required deep understanding of undocumented invariants across multiple subsystems. This is a statement about the benchmark, not about real-world software engineering. SWE-bench Verified selects for issues with clear problem statements and known fixes. The kind of architectural reasoning that makes senior engineers valuable (understanding implicit contracts, anticipating ripple effects, recognizing when a "simple" fix will break something subtle) is mostly not what this benchmark tests.

## Two Dimensions Determine the Verdict

![Depth x surface area](images/swebench-architectural-complexity/depth_surface_verdict.png)

Each cell shows the dominant verdict and instance count for a given combination of structural depth and exploration surface area. The mapping is nearly deterministic: if the fix is localized and touches few files, the verdict is trivial or low; if it spans components, it's moderate or higher.

The five detailed axes refine the picture, but these two coarse dimensions carry most of the signal. You could predict the final verdict from this 3x3 grid alone and be right almost every time.

## The Axes Aren't Really Independent

![Correlation heatmap](images/swebench-architectural-complexity/correlation_heatmap.png)

![Axis correlation with verdict](images/swebench-architectural-complexity/axis_verdict_correlation.png)

The evaluation schema presents five axes as independent dimensions. The correlation matrix shows they're not. Every axis correlates with every other at r >= 0.58. The lollipop chart ranks each axis by how well it predicts the final verdict.

The most striking finding: **structural depth and scope of context have a perfect correlation of r = 1.00**. They encode identical information and should have been one axis. Implicit knowledge is the strongest predictor of the verdict (r = 0.85). Dependency chain depth is the weakest (r = 0.67), partly because the model barely uses it: 74% of instances get "shallow." It's almost a constant.

## Trivial Is a Floor, Not a Grade

![Axes by verdict](images/swebench-architectural-complexity/axes_by_verdict.png)

Mean axis values grouped by verdict level. Trivial instances have *every axis at literally zero*: minimal scope, shallow dependencies, minimal implicit knowledge, independent coordination, low insight density. The model isn't grading them on a curve; it's making a binary call: "this problem is self-evident, nothing to evaluate."

The real action is in the jump from low to moderate. That's where implicit knowledge doubles (0.83 to 1.64) and coordination jumps sixfold (0.25 to 1.56). The model's threshold for "this requires architectural understanding" is driven by implicit knowledge and coordination, not by how deep the dependency chain goes.

## You Need to Understand More Than You Need to Change

![Coordination divergence](images/swebench-architectural-complexity/coordination_divergence.png)

The coordination axis is assessed at two levels: *changes* coordination (how many components your fix actually touches) and *reasoning* coordination (how many components you need to understand to know the fix is correct). This chart shows how many instances fall at each level for each sub-dimension.

In 28% of instances the two diverge, and the direction is almost always the same: 132 out of 141 divergent cases have reasoning > changes. Most bugs live in one place but understanding *why* they're bugs requires reading more widely. You touch one function but you need to understand three call sites to know your fix doesn't break something.

## scikit-learn Is the Easiest, matplotlib the Hardest

![Verdict by repo](images/swebench-architectural-complexity/verdict_by_repo.png)

Verdict distribution per repository, sorted by mean verdict. The stacked bars show what percentage of each repo's instances fall at each verdict level.

scikit-learn stands out at the bottom. 84% of its instances are trivial or low. Its strict estimator API means most fixes are localized: you know exactly which method to change, and the interface contract tells you what the fix should do. matplotlib sits at the other end. Its rendering pipeline crosses more boundaries, and bugs tend to involve understanding how state flows through the artist/renderer/backend hierarchy. The differences aren't huge in absolute terms (0.88 to 1.40 on a 0-4 scale), but they're consistent with what you'd expect from working in these codebases.

## The Model Barely Uses the Top of Its Scales

![Axis utilization](images/swebench-architectural-complexity/axis_utilization.png)

Distribution of levels within each axis across all 500 instances. Every axis has 3-4 possible levels; the model clusters at the bottom of each one.

The scales were designed for a wider range of software engineering problems than SWE-bench Verified contains. Or the model is conservative about using high levels. Probably both. Either way, the effective range of most axes is 2-3 levels out of 4, which limits how much discriminating power the evaluation can have. Dependency chain depth is the most extreme case: 74% shallow, 26% moderate, and exactly one instance rated deep.

## Harder Problems Have More Rejected Fix Paths

Every instance includes rejected fix paths: plausible-but-wrong approaches the model identified during exploration. Trivial instances average 1.1 rejected paths. Moderate instances average 2.8. High instances average 3.0.

Problems that require architectural understanding are exactly the ones where naive approaches break something subtle. A trivial bug has one obvious fix. A moderate bug has two or three reasonable-looking approaches that fail for different architectural reasons.

## Harder Problems Require More File Exploration

![Files by verdict](images/swebench-architectural-complexity/files_by_verdict.png)

Number of files the model explored during evaluation, grouped by verdict. The vertical bar marks the median; each dot is one instance.

The scaling is clean: trivial instances average 1.9 files, low averages 2.9, moderate 4.3, and high 6.5. This is reassuring as a sanity check. The model explores more code for problems it considers more architecturally complex. The outliers are interesting too: one moderate instance required 14 files, suggesting a problem that was sprawling in footprint but not deeply architectural.

## What I Take Away

SWE-bench Verified, through the lens of architectural complexity, is mostly a test of localized bug fixing. 62% of problems require understanding at most one component. The benchmark's value is real, these are genuine bugs from real projects, but it's not testing the kind of architectural reasoning that distinguishes senior engineers. If you built an AI system that was great at understanding cross-component interactions and implicit codebase conventions, SWE-bench Verified would only exercise that capability on about a third of its instances.

The evaluation schema itself has some redundancy. Structural depth and scope of context are the same axis. Dependency chain depth is nearly constant. The five "independent" axes all correlate above r = 0.58. A simpler schema with three dimensions (structural depth, implicit knowledge, and coordination) would capture most of the signal.

The most interesting finding, to me, is the coordination divergence. The consistent pattern that reasoning coordination exceeds changes coordination captures something real about software engineering: the hardest part of fixing a bug is often not writing the fix, but knowing the fix is correct. That requires understanding more of the system than you actually touch.

## What I'd Change

Some of these are clear rubric design issues. Others might just be SWE-bench Verified not containing enough architecturally complex problems to exercise the full evaluation range, and it's hard to tell from one dataset.

**Merge structural depth and scope of context.** This one is unambiguously a rubric problem. They're perfectly correlated at r = 1.00. The model answers them identically every time. They ask the same question in different words ("how deep in the system?" vs "how much of the system?"). One axis with a clearer name, something like *structural reach*, would capture the same information.

**Dependency chain depth is nearly constant, but that might be the benchmark.** 74% of instances land at "shallow" and only a single instance reaches "deep." This could mean the axis is poorly defined, or it could mean SWE-bench Verified problems genuinely don't involve deep dependency chains. Most SWE-bench Verified issues have clear problem statements that point you close to the fix, so you rarely need to traverse four layers of abstraction to understand what's going on. I'd want to test on a harder dataset before concluding the axis itself is broken. If it's still flat on problems that clearly involve deep dependency chains, then the definition of "hop" needs rethinking.

**The unused top of every scale might be correctly unused.** Zero `system_wide` verdicts, zero `extensive` surface areas, zero `expert` insight densities. My first instinct was that the scales are miscalibrated, but the more honest read is that SWE-bench Verified probably just doesn't contain system-wide architectural problems. It selects for issues with clear problem statements and known fixes, which filters out the kind of sprawling, ambiguous problems where you'd genuinely need to understand an entire system's architecture. A finer-grained scale at the low end would give more resolution on the problems we actually have, but that's an adaptation to the dataset, not a fix to the rubric.

**Separate the trivial fast-path from the axis assessment.** Right now, trivial instances get all axes set to zero by fiat because they're fast-pathed before exploration even runs. This means "trivial" is a process shortcut, not a measured verdict. It might be right, but we can't know because the model never actually assessed those instances on the axes. In the next version, I'd run full exploration on everything and let trivial emerge naturally from the axis values, even if it's slower.

**Address the lack of inter-rater reliability.** Each instance is evaluated once by one model. There's no way to know how stable the verdicts are. If you ran the same instance twice, would you get the same verdict? The high axis correlations suggest the model is applying a consistent template, which is encouraging, but it could also mean the model has a systematic bias (e.g., always conservative) that would be invisible without a second evaluation. Running a subset twice with different random seeds, or with a different model, would give some signal on this.

**The gold patch biases which architecture gets explored.** The skill explicitly treats the patch as a guide, not the subject of evaluation. It measures the architectural understanding needed to solve the *problem*, not to produce the specific patch. But the exploration still starts from the files the patch changed and works outward. A different correct fix might touch different files, cross different boundaries, and require different architectural context. The evaluation captures the architectural complexity surrounding one particular solution path, which may not represent the full landscape of what the problem demands. For SWE-bench, where there's typically one canonical fix, this is probably fine. For a more general evaluation, it would be a real limitation.

