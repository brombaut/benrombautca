# What 13 Coding Agents Actually Look Like Inside

Coding agents are everywhere. SWE-agent, OpenHands, Aider, Codex CLI, Gemini CLI, Cline, OpenCode, and the list keeps growing. They all promise to fix bugs, implement features, and navigate codebases autonomously. But how do they actually work under the hood? Are they all just "wrap an LLM in a ReAct loop"?

To find out, this analysis cloned 13 open-source coding agent repositories and traced their architectures line by line. Not the READMEs, not the blog posts, the actual source code. Control loops, tool registrations, state management, context strategies, all pinned to specific files and commits.

The short answer: no, they're not all ReAct loops. The design space is far wider than it looks from the outside, and the architectural choices these agents make have real consequences that aren't obvious until you read the code.

## The Corpus

The 13 agents span the full range: CLI tools (SWE-agent, Codex CLI, Gemini CLI, Aider, OpenCode), SWE-bench-oriented agents (Agentless, OpenHands, AutoCodeRover, Moatless Tools, DARS-Agent, Prometheus), a minimal baseline (mini-swe-agent), and an IDE-native agent (Cline). They range from 100 lines of Python to sprawling TypeScript monorepos. Some have papers at NeurIPS and ICSE; others are community-driven tools with tens of thousands of GitHub stars.

Each agent was analyzed across 9 architectural dimensions: control loop, tool set, tool discovery, state management, context retrieval, execution isolation, context compaction, multi-model routing, and persistent memory.

## Where They Converge

Despite radically different origins, coding agents agree on more than expected.

Every LLM-driven agent needs the same four capability categories: **read** code, **search** for code, **edit** code, and **execute** commands. This holds whether the agent exposes a single `bash` tool (mini-swe-agent) or registers 37 action classes (Moatless Tools). A coding task requires understanding the codebase, making changes, and verifying them. The capability categories reflect that.

At the level of individual steps, 11 of 13 agents follow the ReAct pattern: the LLM generates a thought, selects a tool, receives an observation, repeats. The two exceptions are Aider (where the user drives the loop) and Agentless (which is a pipeline, not a loop). But calling these "ReAct agents" is like calling every web app a "request-response app." Technically true and completely uninformative. The interesting differences are in what's *around* the ReAct loop.

There's also unexpected convergence in edit interfaces. OpenHands, SWE-agent, DARS-Agent, mini-swe-agent, and OpenCode all use the Anthropic-style `str_replace_editor` (or its equivalent oldString/newString replacement), giving 5 of 13 agents the same tool interface. Not because they copied each other, but because Anthropic's tool spec became a de facto standard. Meanwhile, Aider takes the opposite approach: 13 different text-parsed edit formats, optimized per model. One standard interface vs. adapting the format to each model's strengths. A real design fork.

## Where They Diverge

The convergence story is about capabilities. The divergence story is about *architecture*, how agents compose those capabilities into systems.

### Control Loop: Pipeline to Tree Search

The most fundamental architectural axis isn't "which tools does the agent have?" but "how does the agent decide what to do next?"

There's a clear spectrum. To make the differences concrete, here's what each control flow pattern actually looks like as code.

**Fixed pipeline (Agentless).** No loop at all. Localize, repair, validate, each stage runs once:

```python
def run(issue):
    locations = localize(issue)           # LLM identifies relevant files/functions
    patches = []
    for i in range(num_samples):          # generate ~40 candidates independently
        patch = repair(issue, locations,  # each call is independent, high temperature
                       temperature=0.8)
        patches.append(patch)
    best = majority_vote(patches)         # pick most common fix via string matching
    return best
```

The LLM generates ~40 independent patch candidates via temperature sampling and picks the best through majority voting. No feedback, no iteration. The bet: diversity of independent attempts can substitute for feedback loops. It's cheap and parallelizable, but if the localization step points to the wrong file, every downstream patch is wasted.

**Sequential loop (SWE-agent, OpenHands, Codex CLI, Gemini CLI, Cline, OpenCode, mini-swe-agent).** The standard approach:

```python
def run(issue):
    messages = [system_prompt, issue]
    while step < max_steps:
        response = llm(messages)                  # LLM chooses action
        tool_name, tool_args = parse(response)    # extract tool call
        observation = execute(tool_name, tool_args)  # run in environment
        messages.append(response)
        messages.append(observation)
        if is_done(response):
            break
    return get_patch()
```

The LLM picks a tool, sees the result, picks the next tool. Depth-first exploration of a single trajectory. If something goes wrong, the agent can course-correct but can't undo its previous actions. It works with the state its past decisions created. Flexible, but a bad early decision compounds. The agent has to dig itself out of holes it made.

**Phased loop (AutoCodeRover, Prometheus).** The loop is divided into distinct stages with different tool access:

```python
def run(issue):
    # Phase 1: Search (read-only tools only)
    search_tools = [search_class, search_method, search_code, ...]
    context = search_loop(issue, tools=search_tools, max_steps=15)

    # Phase 2: Patch (write tools only, no search allowed)
    patch_tools = [write_patch]
    patch = patch_loop(issue, context, tools=patch_tools)

    # Phase 3: Validate
    result = run_tests(patch)
    if not result.passed:
        retry()  # go back through the graph's retry mechanism
    return patch
```

AutoCodeRover enforces this phase separation *at the code level*: the PatchAgent literally cannot import the SearchBackend. Prometheus goes further with a LangGraph state machine where each node binds only 1-10 tools relevant to its task. The edit node gets editing tools; the verification node gets only `run_command`. This structurally prevents the LLM from modifying code while it's still supposed to be figuring out what's wrong. The cost: no interleaving. If the agent realizes mid-patch that it needs more context, it can't just run a search. It has to go through the graph's retry mechanism.

**Tree search (DARS-Agent, Moatless Tools).** Instead of committing to one trajectory, explore alternatives. This is where the most interesting gradient appeared.

DARS-Agent does depth-first tree search with dynamic resampling:

```python
def run(issue):
    root = Node(action=issue)
    current = root
    while step < max_steps:
        response = llm(messages_from(current))
        current = current.add_child(response)

        if should_expand(current):            # only at edit/append/create actions
            candidates = []
            for i in range(num_samples):      # generate 3 alternatives
                alt = llm(messages_from(current.parent),
                          temperature=0.8)    # higher temperature for diversity
                candidates.append(alt)
            best = critic(current, candidates)  # LLM compares candidates pairwise
            current = best                      # continue down best branch

        if is_done(current):
            break
    return get_patch(root.leftmost_path())    # final answer: always leftmost path
```

At branch points (edits, appends, creates), DARS generates 3 alternative actions at higher temperature, uses an LLM critic to compare them, and continues down the best branch. No rewards, no backpropagation. The critic makes purely local decisions.

Moatless Tools does full Monte Carlo Tree Search:

```python
def run(issue):
    root = Node(state=initial_state(issue))
    while budget_remaining():
        leaf = select(root)                     # UCB1 traversal to promising leaf
        child = expand(leaf)                    # generate new action
        reward = simulate(child)                # evaluate with value function
        backpropagate(child, reward)            # update all ancestors' statistics

        # reward is numeric: -100 (broken) to +100 (tests pass)
        # each node tracks: visit_count, total_reward, avg_reward

    best_path = highest_reward_path(root)
    return get_patch(best_path)
```

Textbook MCTS applied to code generation: select, expand, simulate, backpropagate, with numeric rewards (-100 to 100), visit counting, and pluggable value functions.

The tradeoff across this spectrum is straightforward: pipelines are cheap but rigid. Sequential loops are flexible but can get stuck. Tree search explores alternatives but is expensive, and that expense has a specific, non-obvious architectural root.

### The Environment Replay Problem

Here's a tradeoff that isn't visible from documentation or blog posts. It only becomes clear in the source code.

Tree search in coding agents is fundamentally constrained by execution environment state. When DARS-Agent wants to explore an alternative branch at depth N, it must reset the Docker container and replay all N previous actions from scratch:

```python
def reset_env_to_node(target_node):
    docker.reset()                              # full container reset
    path = get_path_from_root(target_node)      # walk up parent pointers
    for ancestor in path:                       # replay every action in order
        execute(ancestor.action)                # re-run each shell command
    # now environment matches state at target_node
```

At depth 20, that's 20 shell commands re-executed just to reach the branch point. This is why DARS limits branching to only edit/append/create/submit actions. Branching at every step would be prohibitively expensive.

Moatless Tools solves this differently: `shadow_mode` lets the agent reason about file modifications without writing to disk:

```python
class FileContext:
    def apply_change(self, file_path, change):
        if self.shadow_mode:
            self.pending_patches[file_path].append(change)  # store in memory
            return self.reconstruct(file_path)              # return virtual state
        else:
            write_to_disk(file_path, change)                # real modification
            return read_from_disk(file_path)
```

A `FileContext` tracks code spans and patches as data structures. The execution environment stays clean because edits are virtual until committed.

This reveals a deep architectural tradeoff. Stateful execution environments (Docker containers with real file modifications) give ground truth but make branching expensive. Virtual execution (shadow mode, in-memory patches) makes branching cheap but requires trusting the simulation. The right choice depends on whether the value of exploring alternatives outweighs the cost of imperfect execution feedback.

### How Much Agency to Give the LLM

Tool count sounds like a simple metric. It's not:

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
| OpenCode | 18 + MCP + plugins |
| Codex CLI | ~20 + MCP |
| Cline | 27 + MCP |
| Moatless Tools | 37 (~15 active) |

The numbers alone are misleading. Aider has 0 LLM-callable tools because the *user* drives the loop. The LLM's job is to produce edit blocks, not to decide what to do next. AutoCodeRover has 8 tools, but they're all read-only search operations. The LLM can't modify code during its search phase. mini-swe-agent has 1 tool (`bash`) but that tool can do anything.

The real design decision is how much autonomy to give the LLM. More tools means more flexibility and more surface area for mistakes. Fewer tools means more constrained and more predictable behavior. AutoCodeRover's search-only tool set during localization is a deliberate architectural bet: constraining the LLM to read-only operations while it's still figuring out the problem produces better results than letting it modify code mid-investigation.

And then there's Agentless's strangest trick. Its Anthropic code path has a 10-iteration tool-use loop where the LLM calls `str_replace_editor` to make edits, but every tool call gets a hardcoded response:

```python
def tool_use_repair(issue, file_content):
    messages = [system_prompt, file_content]
    for i in range(10):
        response = llm(messages, tools=[str_replace_editor])
        if response.has_tool_calls():
            for call in response.tool_calls:
                edits.append(call.arguments)        # collect the edit
                messages.append(
                    tool_result="File is successfully edited."  # always this string
                )
        else:
            break
    return apply_edits(edits, file_content)         # apply all at once at the end
```

The LLM never sees actual file state. It's structured output extraction disguised as tool use. The expectation that tool use means tool *execution* doesn't always hold.

### Context Compaction: Five Strategies

Long coding sessions generate more context than fits in a model's context window. Five distinct strategies emerged:

**No compaction (mini-swe-agent).** The message list grows until context overflow crashes the agent. Combined with cost and step limits, this works for bounded tasks. Not every problem needs a sophisticated solution.

**Rule-based truncation (SWE-agent, DARS-Agent).** Keep the first message and last N observations, placeholder everything else:

```python
def truncate(history, n=5):
    result = []
    user_msgs = [m for m in history if m.role == "user" and not m.is_demo]
    total = len(user_msgs)
    idx = 0
    for msg in history:
        if msg.role != "user" or msg.is_demo:
            result.append(msg)
            continue
        idx += 1
        if idx == 1 or idx > total - n:             # keep first + last N
            result.append(msg)
        else:
            result.append(f"Old output omitted ({msg.line_count} lines)")
    return result
```

No LLM calls, deterministic behavior, but older context is either fully in or fully out.

**LLM summarization (Aider, OpenHands, OpenCode).** Use a cheaper model to summarize older messages. More flexible than rules, but lossy, and the quality depends on the summarization model. Aider's approach is destructive: the original messages are overwritten in place. OpenHands preserves raw events alongside summaries. OpenCode adds a twist: a two-phase approach that first prunes old tool outputs (keeping message structure but removing verbose content) before summarizing via a dedicated compaction agent, preserving more conversational context than either pure truncation or full summarization alone.

**Structural isolation (Prometheus).** The graph-based control flow means each LLM call only sees messages relevant to its current node. No explicit compaction needed because the structure prevents unbounded accumulation. Elegant, but only works if you have explicit control flow structure.

**LLM-initiated compaction (Cline).** The LLM itself has a `condense` tool and can proactively request context summarization when it judges its window is getting too full. The only agent where the LLM has agency over its own context management.

Gemini CLI adds a twist on top of LLM summarization: after summarizing, it runs a **verification probe**, a self-correction turn that checks whether critical information was lost. No other agent validates its own compaction quality.

The tradeoff here is subtle. Simpler compaction strategies are easier to reason about and don't cost extra LLM calls. But they can't distinguish between "this old observation is irrelevant" and "this old observation contains the key insight the agent needs." LLM-based approaches can make that distinction, at the cost of sometimes getting it wrong.

### Model Routing: When Does It Justify the Complexity?

Most agents use a single model for everything. The question is: when does multi-model routing earn its keep?

The clearest case is **role-based routing**. Aider assigns different models to different subtasks: a capable model for coding, a cheap model for summarization, a specialized model for applying edits. OpenCode takes a similar approach but enforces it structurally: different agent types (build, plan, explore, general) can each use a different model, with the scaffold controlling which agent handles which task. The roles are well-defined, the savings are concrete, and the complexity is minimal.

**Per-attempt model cycling** (SWE-agent) is a more speculative bet: on retry, switch to a different model entirely, on the hypothesis that different models have different failure modes. More of the solution space gets covered, but the agent has no signal about *which* model is better for a given problem.

At the sophisticated end, **Moatless Tools** uses actor-critic routing in tree search: one model generates actions, a separate value function (potentially a different model) evaluates them with numeric rewards. And **Gemini CLI** has a 7-layer routing chain including an optional local Gemma model for client-side classification. This is model routing treated as a first-class architectural concern, but it's fair to ask whether the complexity pays off. The answer isn't obvious from architecture alone.

The most surprising use of multi-model routing is for **safety**: Codex CLI's "Guardian" uses a separate, potentially more capable model to evaluate tool call risk before execution, with structured risk scoring and fail-closed behavior. Every other agent relies on static sandboxing or user approval.

## The Bigger Picture

Three cross-cutting patterns stood out.

### "Agent" is a Spectrum, Not a Binary

There's a continuous spectrum from pure pipeline (Agentless) through user-driven loop (Aider) to fully autonomous agent (OpenHands). Agentless has 0 tools and no loop. Aider has 0 LLM-callable tools but has a lint/test reflection loop. SWE-agent has tools and a loop but the user sets it up and walks away. Codex CLI and Cline are interactive, with the LLM and user collaborating in real time.

Calling some of these "agents" and others "not agents" misses the point. The interesting question is: where on the autonomy spectrum does a given design sit, and what does that position cost?

### The Scaffold Constrains What's Possible

These 13 agents can all use the same underlying LLMs. Yet their architectures are radically different: pipelines vs loops vs tree search, 0 tools vs 37 tools, destructive state vs event-sourced state, no isolation vs Docker vs shadow mode. These scaffold decisions determine what strategies are even *possible* for the LLM. A model inside Agentless literally cannot iterate on a failed attempt, while a model inside Moatless Tools can explore 50 alternative branches.

The scaffold doesn't just affect performance. It defines the ceiling.

### The Ecosystem Hasn't Stabilized

DARS-Agent forks SWE-agent's entire codebase to add tree search. mini-swe-agent imports SWE-agent as a dependency. Both extend the same base architecture, but one can track upstream improvements and the other can't. Moatless Tools, Prometheus, and OpenHands each build their own tool frameworks, state management, and execution environments from scratch.

There are no shared abstractions. Each agent reinvents tool registration, command execution, history management, and context formatting. OpenCode is a partial exception: it uses the Vercel AI SDK as an LLM abstraction layer and Drizzle ORM for state persistence, building on existing libraries rather than rolling its own. But the core scaffold logic (control loop, tool definitions, compaction strategy) is still bespoke. This is a field still figuring out its fundamental abstractions, which means the design space is wide open. Building a coding agent today is as much about choosing where to sit in that space as it is about prompt engineering.

---

*This analysis is part of an ongoing research project studying the architectural design space of coding agent scaffolds. All findings are based on source code analysis of specific commits, not documentation or marketing materials. The 13 agents analyzed: Aider, OpenHands, SWE-agent, Agentless, AutoCodeRover, Codex CLI, Gemini CLI, OpenCode, Moatless Tools, DARS-Agent, Prometheus, mini-swe-agent, and Cline.*
