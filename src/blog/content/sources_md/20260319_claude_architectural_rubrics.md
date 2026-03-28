# What Does Claude Think Is Architecturally Important?

I wanted to know what a frontier model actually values when it looks at code architecture. Not what it says in a generic prompt about "best practices," but what it reaches for when it's staring at a real codebase with a real problem to solve.

So I had Claude Code with Opus 4.6 generate 500 architectural rubrics, one for every instance in SWE-bench Verified. Each rubric required the model to explore a codebase, identify its architectural patterns, and decide which structural properties matter most for evaluating a patch. Then I had all 500 parsed and analyzed to see what came out.

## The Pipeline

The rubrics come from an architectural evaluation pipeline I've been building. It has three stages:

**Stage 1** looks at each SWE-bench Verified problem and judges how much codebase-specific architectural understanding you'd need to solve it. It outputs a complexity verdict from `trivial` to `expert`, based on things like structural depth, how many files you'd need to explore, and how many modules need to coordinate.

**Stage 2** is what we're analyzing here, and it's the most involved stage. For each SWE-bench Verified instance, Claude Code receives the problem statement and the full source repository. It then runs through a multi-step process to produce the rubric.

**Stage 3** takes a patch and evaluates it against the rubric, producing a categorical verdict on architectural conformance.

This article covers Stage 2.

All three stages run Opus 4.6 inside Docker containers, one per SWE-bench Verified instance. Everything is static structural analysis, no code execution.

### How Stage 2 Works

The rubric generation skill orchestrates four steps:

**Step 1: Read and classify.** The model reads the problem statement and scans the top-level project structure in parallel. It classifies the issue as a `bug_fix`, `feature_addition`, `refactoring`, or `architectural_change`, and identifies which components are likely affected. The classification matters because different issue types shift what's architecturally important: a bug fix should involve minimal structural change, a feature addition should demonstrate extensibility, a refactoring should measurably improve structure.

**Step 2: Deep exploration.** This is the expensive part. The model dispatches a subagent to perform what the skill calls an "evidence-based architecture review" of the codebase. The subagent is prompted as a senior software architect. It scans directories and config files to build a mental map, follows dependency chains from entry points to core logic, examines interfaces before implementations, and then reports back on: architectural styles (with confidence scores), design patterns (with evidence, scope, and confidence), cross-cutting conventions, critical boundaries (with instructions for how to detect violations), and code organization patterns. Every claim must cite specific files and imports. "Insufficient evidence" is an acceptable answer; guessing is not.

**Step 3: Determine axes and priority.** Based on what the exploration actually found (not a generic checklist), the model selects which structural properties to evaluate and assigns each a priority. The priorities are guided by a few questions: which patterns are most load-bearing for this issue type, which structural properties are most at risk, and where did the exploration reveal fragility? Only properties backed by evidence with confidence >= 0.6 make the cut.

**Step 4: Generate the YAML.** A second subagent writes the actual rubric file. This subagent has no memory of the conversation so far; it receives the issue context, the axis priorities, and the full exploration output as a single prompt. For each axis, it writes two prose anchors describing ideal and poor conformance. There's an important constraint here: the anchors must describe structural *properties*, not specific *mechanisms*. Instead of "the fix calls `rhs.bump_prefix()` before change_map construction," the rubric should say "newly generated aliases are guaranteed to not appear as keys in the change_map." This matters because multiple implementations might satisfy the same property, and the rubric shouldn't prescribe a particular one.

The subagent verifies the file against a checklist before finishing: all required keys present, at least one primary axis, anchors are substantive paragraphs (not single sentences), no numeric scoring anywhere, no implementation-correctness language. If anything fails the check, it fixes the file and re-verifies.

### What's in a Rubric

Each rubric is a YAML file with four main sections:

**Metadata** classifies the issue: `bug_fix` / `feature_addition` / `refactoring` / `architectural_change`, risk level (`low` / `medium` / `high`), and which components are affected.

**Architectural context** captures what the model discovered about the codebase: the dominant style (free-text, e.g. "Class-based view hierarchy with mixin composition"), named patterns with evidence and confidence scores, and critical boundaries the patch must respect.

**Axes** are the evaluation dimensions, typically 3-5 per rubric. Each axis has a priority (`primary` / `secondary` / `minor`), a description grounded in what the model found during exploration, and two prose anchors: `ideal_conformance` and `poor_conformance`. The anchors describe structural properties, not specific code mechanisms. No numbers anywhere.

**Evaluation guidance** tells the evaluator how to use the rubric: read each axis's anchors, write a prose assessment of where the patch falls, cite specific evidence, and weight primary axes more heavily than secondary or minor ones. It also scopes out non-architectural artifacts (debug scripts, reproduction files) from the assessment.

One design choice worth flagging: the rubric deliberately ignores implementation correctness. Bugs, syntax errors, edge cases, runtime behavior are all out of scope. A patch can be architecturally perfect and still have bugs. A patch can work flawlessly and still violate architecture. The rubric only measures the structural dimension.

Here's the skeleton of a rubric (prose fields trimmed for brevity):

```yaml
metadata:
  issue_file: "issue-report.md"
  issue_summary: "QuerySet.bulk_create() crashes when update_conflicts=True and unique_fields contains expressions"
  issue_type: "bug_fix"
  issue_type_rationale: "Restoring correct behavior for an existing API."
  risk_level: "medium"
  affected_components: ["db.models", "db.backends"]
  evaluation_scope: "architectural_conformance"
  evaluation_format: "prose"

architectural_context:
  primary_style: "Layered ORM with backend-specific SQL compilation"
  style_evidence: "django/db/models/ depends on django/db/backends/ through compiler interface"
  style_confidence: 0.92

  key_patterns:
    - name: "SQL Compiler Delegation"
      evidence: "SQLCompiler in django/db/models/sql/compiler.py delegates dialect-specific SQL to backend operations"
      scope: "system-wide"
      confidence: 0.90

  critical_boundaries:
    - boundary: "ORM layer must not embed backend-specific SQL syntax"
      evidence: "All SQL dialect differences are handled through backend compiler classes"
      violation_check: "Check whether the patch adds raw SQL strings in django/db/models/ rather than delegating to the backend layer"

axes:
  sql_compilation_delegation:
    priority: "primary"
    priority_rationale: "The compiler delegation chain is load-bearing for this bug fix. A patch that bypasses it would work for one backend but break others."
    description: "Whether the fix respects the separation between ORM-level query construction and backend-specific SQL compilation."
    baseline_context: "bulk_create currently delegates conflict handling to the backend compiler via on_conflict_suffix_sql()."

    ideal_conformance: |
      The fix preserves the property that all SQL dialect differences
      are resolved at the backend compiler layer. Expression resolution
      happens through the same resolve_expression path used by other
      queryset operations, so backend-specific type handling is applied
      uniformly. No new SQL string construction appears in the ORM layer.

    poor_conformance: |
      The fix inlines SQL generation for the conflict clause directly
      in the ORM layer, bypassing the backend compiler. Expression
      objects are converted to SQL strings before reaching the compiler,
      losing backend-specific type information and breaking the
      delegation boundary that allows multiple database backends to
      coexist.

  expression_resolution_consistency:
    priority: "secondary"
    priority_rationale: "Expressions in unique_fields should resolve through the same pipeline as expressions elsewhere in the ORM."
    description: "Whether expressions in unique_fields are resolved consistently with how the ORM resolves expressions in other contexts."
    baseline_context: "The ORM resolves expressions via resolve_expression() during query compilation."

    ideal_conformance: |
      Expressions passed in unique_fields go through the standard
      resolve_expression pipeline, gaining access to the query's
      alias map and compiler context. The resolution path is the same
      one used for expressions in filter(), annotate(), and other
      queryset methods.

    poor_conformance: |
      Expressions in unique_fields are special-cased with a separate
      resolution path, or are stringified before the compiler sees them.
      This creates a second way to resolve expressions that may diverge
      from the standard pipeline as the ORM evolves.

evaluation_guidance: |
  For each axis, read both anchors and assess where the patch falls.
  Cite specific file:line references. Primary axes are load-bearing;
  problems there are fundamental. Non-architectural artifacts (test
  scripts, debug files) are out of scope.
```

The key thing to notice is the prose anchors. They describe structural properties ("all SQL dialect differences are resolved at the backend compiler layer") rather than specific mechanisms ("the fix calls `on_conflict_suffix_sql()`"). This is what allows the rubric to evaluate multiple correct implementations against the same standard.

## The Dataset

![Dataset overview](images/claude-architectural-rubrics/section_a_overview.png)

500 rubrics across 12 repos. The left panel shows risk level distribution per repo (stacked bars), the right shows how many components each rubric identifies as affected (lollipop chart). Django dominates with 231 instances (46%). 89.6% are bug fixes, which is just SWE-bench Verified's composition, not a choice I made. Most instances touch 2-3 components, with a long tail out to 14.

## What the Model Considers Load-Bearing

This is the part I was most curious about. Every rubric has 3-5 evaluation axes, each tagged with a priority. Across all 2,176 axes, I had the keys clustered into semantic themes and looked at how the model assigns priority within each theme.

![Priority mix per theme](images/claude-architectural-rubrics/section_c_priority_mix.png)

Each bar shows the priority breakdown for one theme: what percentage of axes in that theme are tagged primary, secondary, or minor. Delegation/Responsibility and Contract/API are overwhelmingly primary. Test Infrastructure and Minimality/Scope are overwhelmingly minor.

The model has a coherent worldview here. Contracts and delegation chains are the things that make or break a patch in its eyes. "Don't break the API contract" and "respect the delegation chain" are structural concerns, and the model treats them as load-bearing. Minimality ("keep the diff small") is almost never primary (3%) and lands at minor 64% of the time. Test infrastructure is explicitly deprioritized at 72% minor. The model treats diff size and test conventions as things worth mentioning, never as things worth failing a patch over.

![Themes by priority](images/claude-architectural-rubrics/section_c_themes_by_priority.png)

The same data from the other direction: total axis count per theme, broken down by priority level. Contract/API and Consistency/Convention are the most *frequent* themes (404 and 353 axes respectively), but Delegation/Responsibility has the highest primary *rate* despite being rare in absolute terms (38 axes, 58% primary). The model doesn't create delegation axes often, but when it does, it almost always makes them the deciding factor.

![Primary vs minor](images/claude-architectural-rubrics/section_c_primary_vs_minor.png)

A butterfly chart showing primary axes (right) vs minor axes (left) for each theme. This is the clearest view of the model's priorities. Contract/API and Delegation skew heavily right. Minimality and Test Infrastructure skew heavily left. You could disagree with this ranking, but it's clearly a *position*, not randomness.

## The Model Invents Its Own Pattern Vocabulary

This one surprised me. Out of 2,034 total pattern identifications, 1,935 names are unique. "Template Method" appears 49 times, "Mixin Composition" 9 times, and after that it's basically all one-offs. Names like "Dimensional Bookkeeping via Index Arrays," "Precedence-Based Parenthesization," "Relaxed-mode Column Building."

The model isn't reaching for a GoF cheat sheet. It's coining terms for the structures it actually finds.

![Pattern families](images/claude-architectural-rubrics/section_b_pattern_families.png)

To make sense of this, I had the 1,935 names clustered into 14 canonical families via keyword matching. The bar chart shows how many patterns landed in each family. "Other / Domain-Specific" is the largest bucket at 32.5%, meaning a third of the model's pattern names didn't match any canonical family. Strategy/Dispatch, Template Method, and Decorator/Wrapper are the most common recognizable families.

![Pattern families by repo](images/claude-architectural-rubrics/section_b_family_repo_heatmap.png)

The heatmap shows how often each pattern family appears per instance, broken down by repo. Each repo gets a distinct fingerprint that reads like a reasonable architectural summary. sympy lights up on Strategy/Dispatch (0.63/inst), because it really is built around type dispatch for expression evaluation. Django lights up on Template Method (0.41/inst), the CBV hook/override hierarchy. scikit-learn lights up on Mixin/Composition (0.59/inst), the estimator mixin architecture. If you've worked in any of these codebases, the fingerprints probably look about right.

## Different Codebases, Different Concerns

The model doesn't just identify different patterns per repo, it worries about different things too.

![Axis themes by repo](images/claude-architectural-rubrics/section_e_theme_repo_heatmap.png)

Each cell shows how many axes of a given theme appear per instance in that repo. pytest's plugin architecture means Boundary Preservation shows up more often (1.11/inst) than in any other repo. scikit-learn's strict estimator API means Contract/API dominates (1.00/inst). These aren't generic, they reflect the actual architectural pressure points of each project.

## Harder Problems Get Richer Rubrics

![Risk vs complexity](images/claude-architectural-rubrics/section_f_risk_complexity.png)

Three panels showing how rubric complexity (patterns, axes, and boundaries per instance) scales with the model's own risk assessment. Each dot is one instance, diamonds mark the mean. The model generates richer rubrics for harder problems: high-risk instances average 4.9 axes vs 4.0 for low-risk, and 3.0 boundaries vs 2.4.

The biggest jump is in affected components (not shown in this chart but visible in the dataset overview): 1.6 for low-risk to 4.3 for high-risk. When a problem touches more of the codebase, the model responds with more evaluation dimensions and more primary axes. It's not just stamping out the same rubric every time.

## The Template Is Fixed, the Content Isn't

![Rubric complexity by repo](images/claude-architectural-rubrics/section_e_complexity.png)

Mean rubric complexity per repo across four metrics: patterns, axes, primary axes, and boundaries. Each metric is a separate dot per repo, connected by a horizontal line to show the spread.

The *structure* of the rubrics barely varies. Axes per rubric ranges from 3.8 to 4.5 across all repos. Patterns: 3.0 to 5.0. Boundaries: 2.0 to 3.0. The model applies a consistent template regardless of which codebase it's looking at. But the *content* varies a lot: which patterns, which themes, which boundaries, what the prose anchors describe. The model uses the same frame every time but fills it with genuinely different architectural content. I'm not sure if this is a strength (consistent evaluation format) or a limitation (the model can't break its own mold when a problem warrants it). Probably a bit of both.

## Boundaries: Layers and Delegation, Over and Over

![Boundary types](images/claude-architectural-rubrics/section_d_boundaries.png)

The left panel shows total boundary counts by type across all rubrics. The right panel is a heatmap of boundary types per instance by repo. Layer/module separation (24.8%) and delegation/responsibility (16.7%) are the most common types. Boundaries like "view classes must not embed model-layer logic" and "must delegate to ModelAdmin for model-specific operations" are what the model identifies most often.

This echoes the axis priority findings. The model's architectural worldview is centered on: who delegates to whom, and which layers are not allowed to reach across into each other.

## Confidence Is Always High (Not Useful)

Style confidence: mean 0.932, std 0.025, range [0.85, 0.95]. Pattern confidence: mean 0.918, std 0.033, range [0.80, 1.00].

The model is confident about everything. There's no discriminating signal here. It's more of an "I found evidence" flag than a calibrated uncertainty estimate. If you were hoping to use confidence to find instances where the model struggled to read the architecture, this isn't going to help.

## What I Take Away

The model has a real architectural perspective. It's not random, not generic, and not just parroting textbook patterns. It prioritizes contracts and delegation over diff size and test conventions. It adapts its pattern vocabulary per codebase. It generates richer rubrics for harder problems.

Whether this perspective is *correct* is a different question, and one that Stage 3 of the pipeline is designed to help answer. But as a window into what a frontier model thinks "good architecture" means, I found this more interesting than I expected.

## What I'd Change

**The "Other / Domain-Specific" bucket is too large.** A third of all pattern identifications and a quarter of all boundary types land in the catch-all category. The keyword-based clustering is too coarse. The model is generating genuinely specific pattern names, and the analysis can't distinguish between "the model identified a real pattern that doesn't fit canonical families" and "the model generated noise." A more sophisticated clustering approach (semantic similarity rather than keyword matching) would give a clearer picture of whether the long tail of unique pattern names contains real signal.

**Confidence scores carry no information.** Style confidence clusters in [0.85, 0.95] with a standard deviation of 0.025. Pattern confidence is similar. The model never expresses meaningful uncertainty. This could be a rubric design issue (the skill asks for confidence but doesn't give the model enough reason to be uncertain), or it could be that the model genuinely found clear evidence in every case. Either way, the confidence field adds nothing to the analysis and could be dropped or replaced with something that has more dynamic range, like asking the model to identify which of its findings it's *least* sure about rather than assigning a number.

**Rubric structure is suspiciously uniform.** Axes per rubric ranges from 3 to 5 across all 500 instances, with most repos averaging 4.0-4.5. Boundaries per instance ranges from 2.0 to 3.0. The model is clearly applying a template. The skill doesn't actually constrain the axis count to 3-5. It suggests "expect 1-2 primary, 1-3 secondary, 0-2 minor," which allows anywhere from 2 to 7 axes, but the model consistently lands in a narrow band. Whether the expected-count hints are anchoring the model or the model just gravitates to 4 on its own isn't clear. A follow-up experiment could remove the count guidance entirely and see whether the model produces 2-axis rubrics for simple problems and 8-axis rubrics for complex ones, or whether it gravitates to 4 regardless.

**No validation against human judgment.** The rubrics represent what the model *thinks* is architecturally important. Whether those judgments are correct, whether the patterns it identifies are real, whether the boundaries it flags actually matter, is untested. Stage 3 evaluates patches against these rubrics, which tells you whether the rubrics are internally consistent, but not whether they're right. Validating a subset against expert human judgment would be the most valuable next step, and the hardest to do.

