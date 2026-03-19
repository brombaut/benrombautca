# Inside 12 Coding Agents: Control Loops, Tools, and Tradeoffs

Coding agents are everywhere. SWE-agent, OpenHands, Aider, Codex CLI, Gemini CLI, Cline — the list keeps growing. They all promise to fix bugs, implement features, and navigate codebases autonomously. But how do they actually work under the hood? Are they all just "wrap an LLM in a ReAct loop"?

This article is based on reading the source code of 12 open-source coding agent repositories line by line. Not the READMEs, not the blog posts — the actual source code. Tracing control loops, cataloguing tools, mapping state management strategies, and documenting how each agent scaffolds an LLM into a coding system.

## The Agents

The corpus spans the spectrum: CLI tools (SWE-agent, Codex CLI, Gemini CLI, Aider), SWE-bench-oriented agents (Agentless, OpenHands, AutoCodeRover, Moatless Tools, DARS-Agent, Prometheus), a minimal baseline (mini-swe-agent), and an IDE-native agent (Cline). They range from 100 lines of Python to sprawling TypeScript monorepos. Some have papers at NeurIPS and ICSE; others are community-driven tools with tens of thousands of GitHub stars.

Each agent was analyzed across 9 architectural dimensions: control loop, tool set, tool discovery, state management, context retrieval, execution isolation, context compaction, multi-model routing, and persistent memory. Every claim is pinned to a specific file and line number in a specific commit.

## Where They Converge

Despite radically different origins and goals, coding agents agree on more than you'd expect.

### The Same Four Tool Categories

Every LLM-driven agent in the corpus needs the same core capabilities: **read** code, **search** for code, **edit** code, and **execute** commands. The surface area varies wildly — mini-swe-agent exposes a single `bash` tool while Moatless Tools registers 37 action classes — but the underlying capability categories are remarkably stable.

This isn't surprising in retrospect. A coding task requires understanding the codebase (read + search), making changes (edit), and verifying them (execute). What *is* surprising is how little agreement there is on the right granularity. Should you give the LLM one powerful `bash` tool and let it compose its own workflows? Or 37 specialized tools with constrained inputs and validated outputs? This is a genuine design tradeoff, and different agents make different bets.

### ReAct as the Universal Inner Loop

At the level of individual steps, nearly every agent follows the same pattern: the LLM generates a thought, selects a tool, receives an observation, and repeats. This is the ReAct pattern, and it appears in 10 of 12 agents. The two exceptions are Aider (where the user drives the loop, not the LLM) and Agentless (which is a pipeline, not a loop).

But calling these agents "ReAct agents" is like calling every web app a "request-response app." It's technically true and completely uninformative. The interesting differences are in what's *around* the ReAct loop.

### Edit Tool Convergence

There's unexpected convergence in how agents modify code. OpenHands and SWE-agent both use the Anthropic-style `str_replace_editor` with an identical interface: `view`, `create`, `str_replace`, `insert`, `undo_edit`. This isn't because they copied each other — it's because Anthropic's tool spec became a de facto standard. DARS-Agent and mini-swe-agent inherit this through SWE-agent's codebase. That's 4 of 12 agents sharing the same edit interface.

Meanwhile, Aider supports 13 different text-parsed edit formats (unified diffs, search/replace blocks, whole-file rewrites), optimized per model. This is the opposite bet: instead of one standard interface, adapt the edit format to each model's strengths.

## Where They Diverge

The convergence story is about capabilities. The divergence story is about *architecture* — how agents compose those capabilities into systems. This is where it gets interesting.

### Control Loop: Pipeline to Tree Search

The most fundamental architectural axis isn't "which tools does the agent have?" — it's "how does the agent decide what to do next?"

There's a clear spectrum:

**Fixed pipeline (Agentless):** No loop at all. Localize → repair → validate, each stage runs once. The LLM generates ~40 independent patch candidates via temperature sampling and selects the best through majority voting. No feedback, no iteration. The design bet: diversity of independent attempts can substitute for feedback loops.

**Sequential loop (SWE-agent, OpenHands, Codex CLI, Gemini CLI, Cline, mini-swe-agent):** The standard approach. The LLM picks a tool, sees the result, picks the next tool. Depth-first exploration of a single trajectory. If something goes wrong, the agent can course-correct but can't un-do its previous actions — it works with the state its past decisions created.

**Phased loop (AutoCodeRover, Prometheus):** The loop is divided into distinct stages with different tool access. AutoCodeRover enforces a strict search → patch phase separation *at the code level* — the PatchAgent literally cannot import the SearchBackend. Prometheus goes further: a LangGraph state machine where each node binds only 1-10 tools relevant to its task. The edit node gets editing tools; the verification node gets only `run_command`. This structurally constrains the action space at each decision point.

**Tree search (DARS-Agent, Moatless Tools):** Instead of committing to one trajectory, explore alternatives. This is where the most interesting gradient emerges:

- **DARS-Agent** implements depth-first tree search with dynamic resampling. At branch points (edits, appends, creates), it generates 3 alternative actions at higher temperature, uses an LLM critic to select the best, and continues down that branch. No rewards, no backpropagation — the critic makes local decisions.
- **Moatless Tools** implements full Monte Carlo Tree Search: select → expand → simulate → backpropagate, with numeric rewards (-100 to 100), visit counting, and pluggable value functions. This is textbook MCTS applied to code generation.

The tradeoff is clear: pipelines are cheap but rigid. Sequential loops are flexible but can get stuck. Tree search explores alternatives but is expensive. And that expense has a specific architectural root: **environment replay**.

### The Environment Replay Problem

Here's a tradeoff that isn't obvious until you read the code: tree search in coding agents is fundamentally constrained by execution environment state.

When DARS-Agent wants to explore an alternative branch at depth N, it must reset the Docker container and replay all N previous actions from scratch. At depth 20, that's 20 shell commands re-executed just to reach the branch point. This is why DARS limits branching to specific action types (edit, append, create, submit) — branching at every step would be prohibitively expensive.

Moatless Tools solves this differently: `shadow_mode` lets the agent reason about file modifications without writing to disk. Combined with a `FileContext` that tracks code spans and patches as data structures, Moatless can explore multiple edit strategies without touching the filesystem. The execution environment stays clean because edits are virtual until committed.

This is a deep architectural tradeoff. Stateful execution environments (Docker containers with real file modifications) give you ground truth but make branching expensive. Virtual execution (shadow mode, in-memory patches) makes branching cheap but requires you to trust the simulation.

### State Management: Destructive to Event-Sourced

How agents track conversation history is another axis with real consequences.

**Destructive (Aider):** When conversation gets too long, Aider summarizes older messages using a weak LLM model and overwrites them in place. The original messages are gone. Simple, but information is permanently lost — and the quality of the summary depends on the summarization model.

**Preserved with filtered views (SWE-agent, DARS-Agent):** The full conversation history is kept, but a `HistoryProcessor` creates a filtered view for each LLM call. SWE-agent's `Last5Observations` keeps all assistant messages but replaces old observations with "Old output omitted (N lines)." No information is destroyed, but the LLM only sees recent context.

**Event-sourced (OpenHands):** An immutable event stream records everything that happened. Condensation markers indicate where summaries begin and end, but raw events are preserved. Any view of history can be reconstructed from the event log.

**Tree-structured (Moatless Tools, DARS-Agent):** Each node in the tree stores its own state snapshot. Branching creates new nodes with copied state. This is the most memory-intensive but the only approach that supports tree search — you need to know the state at every branch point to explore alternatives.

The tradeoff: simpler state management is easier to implement and uses less memory, but limits what orchestration strategies are possible. You can't do tree search with destructive summarization — you'd lose the information needed to explore alternatives.

### Tool Count: 0 to 37

The raw numbers are striking:

| Agent | LLM-Callable Tools |
|-------|-------------------|
| Aider | 0 |
| Agentless | 0 (default) / 1 (Anthropic path) |
| mini-swe-agent | 1 (bash) |
| SWE-agent | 3 (default) / ~34 (all bundles) |
| AutoCodeRover | 8 (all read-only) |
| OpenHands | 9 + MCP |
| DARS-Agent | ~15 |
| Gemini CLI | 17 + MCP |
| Prometheus | 17 (1-10 per node) |
| Codex CLI | ~20 + MCP |
| Cline | 27 + MCP |
| Moatless Tools | 37 (~15 active) |

But the numbers alone are misleading. Aider has 0 LLM-callable tools because the *user* drives the loop — the LLM's job is to produce edit blocks, not to decide what to do next. AutoCodeRover has 8 tools, but they're all read-only search operations — the LLM can't modify code during its search phase. mini-swe-agent has 1 tool (`bash`) but that tool can do anything.

The real design decision is **how much agency to give the LLM**. More tools = more flexibility = more surface area for mistakes. Fewer tools = more constrained = more predictable behavior. AutoCodeRover's search-only tool set is a deliberate bet that constraining the LLM to read-only operations during localization produces better results than letting it modify code while it's still figuring out what's wrong.

### Context Compaction: Five Strategies

Long coding sessions generate more context than fits in a model's context window. Agents handle this in fundamentally different ways:

1. **No compaction (mini-swe-agent).** The message list grows until context overflow crashes the agent. Combined with cost and step limits, this actually works for bounded tasks. The simplest approach, and a useful reminder that not every problem needs a sophisticated solution.

2. **Rule-based truncation (SWE-agent, DARS-Agent).** Keep the first message and last N observations, placeholder everything else. No LLM calls, no information loss in the retained window, but hard cutoffs mean older context is either in or out.

3. **LLM summarization (Aider, OpenHands).** Use a (usually weaker, cheaper) model to summarize older messages. More flexible than rule-based, but lossy and the quality depends on the summarization model.

4. **Structural isolation (Prometheus).** The graph-based control flow means each LLM call only sees messages relevant to its current node. No explicit compaction needed — the structure prevents unbounded accumulation. An elegant solution, but only works if you have explicit control flow structure.

5. **LLM-initiated compaction (Cline).** The LLM itself has a `condense` tool and can proactively request context summarization when it judges its context is getting too long. The only agent where the LLM has agency over its own context window management.

And then there's Gemini CLI, which does something no one else does: after LLM-based summarization, it runs a **verification probe** — a self-correction turn that checks whether critical information was lost. No other agent validates its own compaction quality.

### Model Routing: From "Use One Model" to 7-Layer Decision Chains

Most agents use a single model for everything. But several have evolved more sophisticated approaches:

**Role-based routing (Aider):** Assigns different models to different subtasks — a main model for coding, a weak model for summarization, an editor model for applying changes. Clean and explicit.

**Per-attempt model cycling (SWE-agent):** On retry, can switch to a different model entirely. The hypothesis: different models have different failure modes, so cycling models on retry covers more of the solution space than retrying with the same model.

**Actor-critic routing (Moatless Tools):** In tree search mode, one model generates actions while a separate `BaseValueFunction` (potentially a different model) evaluates their quality with numeric rewards. This is the coding agent equivalent of actor-critic reinforcement learning.

**7-layer routing chain (Gemini CLI):** A cascade of fallback → override → approval mode → Gemma classifier → LLM classifier → numerical → default routing strategies. Includes an optional local Gemma model for client-side classification to decide which model to use for a given turn. This is model routing as a first-class architectural concern, not a config option.

**LLM-as-safety-monitor (Codex CLI):** Uses a separate, potentially more capable model as a "Guardian" to evaluate tool call risk before execution, with structured risk scoring and fail-closed behavior. This is multi-model routing for safety, not capability.

## The Bigger Picture

Three cross-cutting observations are worth calling out.

### "Agent" is a Spectrum, Not a Binary

The cleanest finding: there's a continuous spectrum from pure pipeline (Agentless) through user-driven loop (Aider) to fully autonomous agent (OpenHands). Agentless has 0 tools and no loop. Aider has 0 LLM-callable tools but has a lint/test reflection loop. SWE-agent has tools and a loop but the user sets it up and walks away. Codex CLI and Cline are interactive — the LLM and user collaborate in real time.

Calling some of these "agents" and others "not agents" misses the point. The interesting question is: where on the autonomy spectrum does a given design sit, and what tradeoffs does that position entail?

### The Scaffold Matters More Than You Think

These 12 agents can all use the same underlying LLMs. Yet their architectures are radically different: pipelines vs loops vs tree search, 0 tools vs 37 tools, destructive state vs event-sourced state, no isolation vs Docker vs shadow mode. These scaffold decisions determine what strategies are even *possible* for the LLM — a model inside Agentless literally cannot iterate on a failed attempt, while a model inside Moatless Tools can explore 50 alternative branches.

If you're building a coding agent, the scaffold design constrains your ceiling more than the model choice does.

### The Ecosystem Hasn't Stabilized

DARS-Agent forks SWE-agent's entire codebase to add tree search. mini-swe-agent imports SWE-agent as a dependency. Both extend the same base architecture, but one can track upstream improvements and the other can't. Moatless Tools, Prometheus, and OpenHands each build their own tool frameworks, state management, and execution environments from scratch.

There are no shared abstractions — no "agent framework" that multiple coding agents build on (despite what LangChain and CrewAI might claim). Each agent reinvents tool registration, command execution, history management, and context formatting. This is a sign of a field that's still figuring out its fundamental abstractions.

## Implications for Agent Builders

If you're building or extending a coding agent, here's what this analysis suggests:

**Start with the control loop decision.** Pipeline, sequential loop, or tree search? This choice cascades into everything else — your state management, context strategy, and isolation model all follow from how you orchestrate LLM calls.

**Be deliberate about tool granularity.** One `bash` tool (mini-swe-agent) and 37 specialized actions (Moatless Tools) are both viable. The question is how much you trust the LLM to compose complex operations vs how much you want to constrain its action space. AutoCodeRover's search-only tool set during localization is an underappreciated design pattern.

**Context compaction is an architectural decision, not an afterthought.** The agents that handle long sessions well (Prometheus, Gemini CLI) designed their context management into the architecture from the start. Bolting on summarization later is possible but lossy.

**If you're considering tree search, solve the environment state problem first.** DARS-Agent's environment replay and Moatless Tools' shadow mode represent two fundamentally different solutions. The right choice depends on whether you need ground-truth execution results at every branch point.

---

*This analysis is part of an ongoing research project studying the architectural design space of coding agent scaffolds. All findings are based on source code analysis of specific commits, not documentation or marketing materials. The agents analyzed are: Aider, OpenHands, SWE-agent, Agentless, AutoCodeRover, Codex CLI, Gemini CLI, Moatless Tools, DARS-Agent, Prometheus, mini-swe-agent, and Cline.*
