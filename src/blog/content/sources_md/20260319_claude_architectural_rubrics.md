# What Does Claude Think Is Architecturally Important?

I wanted to know what a frontier model actually values when it looks at code architecture. Not what it says in a generic prompt about "best practices," but what it reaches for when it's staring at a real codebase with a real problem to solve.

So I had Claude Code with Opus 4.6 generate 500 architectural rubrics, one for every instance in SWE-bench Verified. Each rubric required the model to explore a codebase, identify its architectural patterns, and decide which structural properties matter most for evaluating a patch. Then I had all 500 parsed and analyzed to see what came out.

## How the Rubrics Get Made

The rubrics come from an architectural evaluation pipeline I've been building. It has three stages:

**Stage 1** looks at each SWE-bench problem and judges how much codebase-specific architectural understanding you'd need to solve it. It outputs a complexity verdict from `trivial` to `expert`, based on things like structural depth, how many files you'd need to explore, and how many modules need to coordinate.

**Stage 2** is what we're analyzing here, and it's the most involved stage. For each SWE-bench instance, Claude Code receives the problem statement and the full source repository. It then runs through a multi-step process to produce the rubric.

**Stage 3** takes a patch and evaluates it against the rubric, producing a verdict. We're not looking at Stage 3 output here.

All three stages run Opus 4.6 inside Docker containers, one per SWE-bench instance. Everything is static structural analysis, no code execution.

### How Stage 2 Works

The rubric generation skill orchestrates four steps:

**Step 1: Read and classify.** The model reads the problem statement and scans the top-level project structure in parallel. It classifies the issue as a `bug_fix`, `feature_addition`, `refactoring`, or `architectural_change`, and identifies which components are likely affected. The classification matters because different issue types shift what's architecturally important: a bug fix should involve minimal structural change, a feature addition should demonstrate extensibility, a refactoring should measurably improve structure.

**Step 2: Deep exploration.** This is the expensive part. The model dispatches a subagent to perform what the skill calls an "evidence-based architecture review" of the codebase. The subagent is prompted as a senior software architect. It scans directories and config files to build a mental map, follows dependency chains from entry points to core logic, examines interfaces before implementations, and then reports back on: architectural styles (with confidence scores), design patterns (with evidence, scope, and confidence), cross-cutting conventions, critical boundaries (with instructions for how to detect violations), and code organization patterns. Every claim must cite specific files and imports. "Insufficient evidence" is an acceptable answer; guessing is not.

**Step 3: Determine axes and priority.** Based on what the exploration actually found (not a generic checklist), the model selects which structural properties to evaluate and assigns each a priority. The priorities are guided by a few questions: which patterns are most load-bearing for this issue type, which structural properties are most at risk, and where did the exploration reveal fragility? Only properties backed by evidence with confidence >= 0.6 make the cut.

**Step 4: Generate the YAML.** A second subagent writes the actual rubric file. This subagent has no memory of the conversation so far; it receives the issue context, the axis priorities, and the full exploration output as a single prompt. For each axis, it writes two prose anchors describing ideal and poor conformance. There's an important constraint here: the anchors must describe structural *properties*, not specific *mechanisms*. Instead of "the fix calls `rhs.bump_prefix()` before change_map construction," the rubric should say "newly generated aliases are guaranteed to not appear as keys in the change_map." This matters because multiple implementations might satisfy the same property, and the rubric shouldn't prescribe a particular one.

The subagent verifies the file against a checklist before finishing: all required keys present, at least one primary axis, anchors are substantive paragraphs (not single sentences), no numeric scoring anywhere, no implementation-correctness language. If anything fails the check, it fixes the file and re-verifies.

### What's in a Rubric

Each rubric is a YAML file with three main sections:

**Metadata** classifies the issue: `bug_fix` / `feature_addition` / `refactoring`, risk level (`low` / `medium` / `high`), and which files are affected.

**Architectural context** captures what the model discovered about the codebase: the dominant style (free-text, e.g. "Class-based view hierarchy with mixin composition"), named patterns with evidence and confidence scores, and critical boundaries the patch must respect.

**Axes** are the evaluation dimensions, typically 3-5 per rubric. Each axis has a priority (`primary` / `secondary` / `minor`), a description grounded in what the model found during exploration, and two prose anchors: `ideal_conformance` and `poor_conformance`. The anchors describe structural properties, not specific code mechanisms. No numbers anywhere.

One design choice worth flagging: the rubric deliberately ignores implementation correctness. Bugs, syntax errors, edge cases, runtime behavior are all out of scope. A patch can be architecturally perfect and still have bugs. A patch can work flawlessly and still violate architecture. The rubric only measures the structural dimension.

## The Dataset

500 rubrics across 12 repos. Django dominates with 231 instances (46%). 89.6% are bug fixes, which is just SWE-bench's composition, not a choice I made. 63.6% medium risk, 33.8% low, 2.6% high.

![Dataset overview](images/claude-architectural-rubrics/section_a_overview.png)

## What the Model Considers Load-Bearing

This is the part I was most curious about. Every rubric has 3-5 evaluation axes, each tagged with a priority. Across all 2,176 axes, I had the keys clustered into semantic themes and looked at how the model assigns priority within each theme.

It turns out the model has opinions, and they're remarkably consistent:

| Theme | % Primary | % Secondary | % Minor |
|---|---|---|---|
| Delegation / Responsibility | 58% | 39% | 3% |
| Contract / API | 52% | 33% | 15% |
| Pattern Conformance | 44% | 47% | 9% |
| Boundary Preservation | 34% | 51% | 15% |
| Hierarchy / Inheritance | 33% | 55% | 12% |
| Consistency / Convention | 30% | 41% | 29% |
| Minimality / Scope | 3% | 34% | **64%** |
| Test Infrastructure | 2% | 26% | **72%** |

The headline: the model cares deeply about contracts and delegation chains. "Don't break the API contract" and "respect the delegation chain" are the things that make or break a patch in its eyes. Boundary preservation matters but is rarely the deciding factor on its own, it tends to sit at secondary.

The bottom of the table is just as telling. Minimality ("keep the diff small") is almost never primary (3%) and lands at minor 64% of the time. Test infrastructure is explicitly deprioritized at 72% minor. The model treats diff size and test conventions as things worth mentioning, never as things worth failing a patch over.

I find this interesting because it's a coherent worldview, not just noise. Contracts and delegation are structural. Diff size is cosmetic. You could disagree with this ranking, but it's clearly a *position*, not randomness.

![Priority mix per theme](images/claude-architectural-rubrics/section_c_priority_mix.png)

![Themes by priority](images/claude-architectural-rubrics/section_c_themes_by_priority.png)

![Primary vs minor](images/claude-architectural-rubrics/section_c_primary_vs_minor.png)

## The Model Invents Its Own Pattern Vocabulary

This one surprised me. Out of 2,034 total pattern identifications, 1,935 names are unique. "Template Method" appears 49 times, "Mixin Composition" 9 times, and after that it's basically all one-offs. Names like "Dimensional Bookkeeping via Index Arrays," "Precedence-Based Parenthesization," "Relaxed-mode Column Building."

The model isn't reaching for a GoF cheat sheet. It's coining terms for the structures it actually finds.

To make sense of this, I had the 1,935 names clustered into 14 canonical families via keyword matching. After clustering, each repo gets a distinct fingerprint that, honestly, reads like a reasonable architectural summary:

| Repo | Top Pattern Families |
|---|---|
| **sympy** | Strategy/Dispatch (0.63/inst), expression evaluation via type dispatch |
| **django** | Template Method (0.41/inst), the CBV hook/override hierarchy |
| **scikit-learn** | Mixin/Composition (0.59/inst), the estimator mixin architecture |
| **pylint** | Convention/Config (0.70/inst), Registry (0.50/inst), plugin/checker registration |
| **requests** | Decorator/Wrapper, Layer Separation, Strategy all at 0.62, the transport adapter stack |
| **sphinx** | Template Method (0.55/inst), Registry (0.45/inst), documenter hierarchy + extensions |

If you've worked in any of these codebases, this probably looks about right. sympy really is built around type dispatch. Django really is Template Method all the way down. scikit-learn really is mixins.

![Pattern families](images/claude-architectural-rubrics/section_b_pattern_families.png)

![Pattern families by repo](images/claude-architectural-rubrics/section_b_family_repo_heatmap.png)

## Different Codebases, Different Concerns

The model doesn't just identify different patterns per repo, it worries about different things too:

| Repo | Top Axis Theme (per instance) |
|---|---|
| **pytest** | Boundary Preservation (1.11), plugin isolation matters most |
| **scikit-learn** | Contract/API (1.00), the estimator API contract is paramount |
| **matplotlib** | Consistency/Convention (0.88), visual consistency across backends |
| **xarray** | Contract/API (0.86), DataArray/Dataset interface contracts |
| **django** | Contract/API (0.81), ORM and view API stability |

pytest's plugin architecture means boundary preservation shows up more often than in any other repo. scikit-learn's strict estimator API means contract preservation dominates. These aren't generic, they reflect the actual architectural pressure points of each project.

![Axis themes by repo](images/claude-architectural-rubrics/section_e_theme_repo_heatmap.png)

## Harder Problems Get Richer Rubrics

Risk level correlates cleanly with rubric complexity across every metric:

| Risk | Patterns | Axes | Primary Axes | Boundaries | Components |
|---|---|---|---|---|---|
| Low | 3.9 | 4.0 | 1.5 | 2.4 | 1.6 |
| Medium | 4.1 | 4.5 | 1.7 | 2.7 | 2.6 |
| High | 4.4 | 4.9 | 2.0 | 3.0 | 4.3 |

The biggest jump is affected components: 1.6 to 4.3. When a problem touches more of the codebase, the model responds by generating more evaluation dimensions and more primary axes. It's not just stamping out the same rubric every time.

![Risk vs complexity](images/claude-architectural-rubrics/section_f_risk_complexity.png)

## The Template Is Fixed, the Content Isn't

One thing that's worth calling out: the *structure* of the rubrics barely varies. Axes per rubric ranges from 3.8 to 4.5 across all repos. Patterns: 3.0 to 5.0. Boundaries: 2.0 to 3.0. The model applies a consistent template regardless of which codebase it's looking at.

But the *content* varies a lot. Which patterns, which themes, which boundaries, what the prose anchors describe. The model uses the same frame every time but fills it with genuinely different architectural content. I'm not sure if this is a strength (consistent evaluation format) or a limitation (the model can't break its own mold when a problem warrants it). Probably a bit of both.

![Rubric complexity by repo](images/claude-architectural-rubrics/section_e_complexity.png)

## Boundaries: Layers and Delegation, Over and Over

Across 1,311 critical boundaries, layer/module separation (24.8%) and delegation/responsibility (16.7%) are the most common types. Boundaries like "view classes must not embed model-layer logic" and "must delegate to ModelAdmin for model-specific operations" are what the model identifies most often.

This echoes the axis priority findings. The model's architectural worldview is centered on: who delegates to whom, and which layers are not allowed to reach across into each other.

![Boundary types](images/claude-architectural-rubrics/section_d_boundaries.png)

## Confidence Is Always High (Not Useful)

Style confidence: mean 0.932, std 0.025, range [0.85, 0.95]. Pattern confidence: mean 0.918, std 0.033, range [0.80, 1.00].

The model is confident about everything. There's no discriminating signal here. It's more of an "I found evidence" flag than a calibrated uncertainty estimate. If you were hoping to use confidence to find instances where the model struggled to read the architecture, this isn't going to help.

## What I Take Away

The model has a real architectural perspective. It's not random, not generic, and not just parroting textbook patterns. It prioritizes contracts and delegation over diff size and test conventions. It adapts its pattern vocabulary per codebase. It generates richer rubrics for harder problems.

Whether this perspective is *correct* is a different question, and one that Stage 3 of the pipeline is designed to help answer. But as a window into what a frontier model thinks "good architecture" means, I found this more interesting than I expected.

