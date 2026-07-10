# AIware Observability: Monitoring and Understanding AI Systems

The evolution of software development has brought us from measuring code quality by "WTFs per minute" during code review to a new era where AI agents make decisions on the fly. That shift changes what it means to observe a system.

This post is based on my paper [Watson: A Cognitive Observability Framework for the Reasoning of LLM-Powered Agents](https://www.arxiv.org/abs/2411.03455) and the related [AIware Observability slides](publications/202411_aiware_bootcamp_observability_for_pdf.pdf) from the AIware Leadership Bootcamp 2024 and Mini Bootcamp 2025. The goal here is to turn that material into a more accessible blog-form explanation of why AIware needs observability beyond ordinary logs, traces, and metrics.

Traditional observability is still necessary. We still care about latency, cost, errors, throughput, and resource usage. But AI-powered systems, or AIware, also need a different layer of observability: one that helps us understand not only what happened, but why an agent made a decision and how that decision moved through the system.

## What Is Observability?

Observability is the ability to understand a system's capabilities and behavior by analyzing the data it produces.

After deploying an application, we usually want to answer four questions:

- What is happening?
- Where are potential problems?
- Why is it happening?
- How is the system performing?

![Observability questions](images/aiware-observability/slide_05_observability.webp)

Traditional software answers these questions through assertions, metrics, logs, and traces. These methods work well because there is usually direct traceability between system behavior and executed code. Developers can instrument the code, track execution flows, identify bottlenecks, and trace issues back to their source.

AIware changes the shape of the problem. Operational metrics remain valuable, but they are not enough. If an AI agent takes an unexpected action, the failure may not live in a specific branch, condition, or function. It may emerge from the model's interpretation of context, its intermediate reasoning, a prompt ambiguity, or a cascade of decisions across multiple agents.

That means AIware observability needs to include both operational observability and cognitive observability.

## Operational Observability for AIware

Operational observability extends traditional monitoring to foundation-model-powered systems. Beyond basic API monitoring, we need to track how models and agentic components behave inside the larger application.

Useful operational signals include:

**Volume metrics.** How many calls are made to each foundation model, route, agent, or tool?

**Latency metrics.** Where do delays occur across AIware components, and which model or tool interactions dominate user-facing response time?

**Token metrics.** How much prompt and completion traffic is the system producing, and how does that affect cost, latency, and context-window pressure?

**Resource utilization.** How efficiently are compute, memory, storage, vector indexes, retrieval systems, and model calls being used?

**Tool monitoring.** Which tools do agents call, how often do they call them, what arguments do they pass, and how successful are those calls?

![Operational observability metrics](images/aiware-observability/slide_11_operational_metrics.webp)

Modern observability platforms such as LangSmith, Langfuse, and Dynatrace have started adding AIware-specific features. OpenLLMetry provides instrumentation standards for LLM providers and vector databases, tracking traces and runs made up of prompts, model calls, responses, and associated metrics.

This layer matters. Without it, you cannot answer basic production questions about cost, reliability, latency, and failure rates. But it still leaves a harder question unresolved: why did the agent behave that way?

![AIware observability moves to higher levels of abstraction](images/aiware-observability/slide_15_abstraction_shift.webp)

## Why AIware Is Harder to Observe

As foundation models become more capable and AIware becomes more complex, observability requirements move to a higher level of abstraction. Three challenges stand out.

![AIware observability challenges](images/aiware-observability/slide_17_aiware_challenges.webp)

### Abstract Behaviors

In traditional software, errors can often be traced back to code that can be reviewed, tested, and debugged. A condition was wrong. A function mishandled input. A database query returned unexpected data.

In agentic systems, errors can stem from abstract behavior that has no explicit code representation. Many decisions are generated on the fly from model responses. The behavior exists in the interaction between prompt, context, model, tools, and output, not in a fixed implementation that can be inspected line by line.

That makes traditional debugging techniques less direct. You can inspect the prompt and the output, but the path between them is opaque.

### Reasoning Chains

Consider a fraud detection system.

In a rule-based approach, if a transaction is wrongly flagged as fraudulent, you can trace the decision back to specific conditions. Maybe the transaction amount crossed a threshold. Maybe a geolocation rule fired. The rule can be inspected and adjusted.

In an agent-based approach, the same wrong flag may not have a clear logic path. The decision may arise from complex interactions among learned features, contextual cues, and prompt framing. The model may be using latent knowledge that is difficult to inspect directly.

The issue is not just that the system made a wrong decision. The issue is that the reasoning chain is hard to recover.

### Cascading Actions

The problem becomes even harder in multi-agent systems. An error introduced by an early agent may only become visible later in the workflow.

Imagine a code generation workflow with three agents:

- A conversational agent gathers requirements from the user.
- A system design agent proposes an architecture.
- A code generation agent implements the design.

If the conversational agent makes a wrong assumption about resource constraints, the system design agent may produce a poor architecture. The code generation agent may then implement that architecture faithfully. By the time the developer sees incorrect storage allocation in the generated code, the visible failure is far downstream from the original mistake.

Operational traces can show the sequence of events. They may not explain the reasoning error that caused the sequence to go wrong.

## Cognitive Observability

Cognitive observability shifts the focus from technical metrics alone to the cognitive and linguistic behavior of AI systems. It asks how foundation models appear to think, communicate, and decide.

This does not replace operational observability. It sits above it. Operational observability tells us what happened in the system. Cognitive observability helps us understand why the AIware produced a particular response or action.

There are three useful pillars.

![Cognitive observability pillars](images/aiware-observability/slide_22_cognitive_observability.webp)

## Output Integrity

Output integrity focuses on the quality and trustworthiness of prompts and responses.

This includes signals such as:

- hallucination risk
- prompt injection attempts
- toxicity
- sentiment
- readability
- complexity
- text quality
- output drift

Tools such as WhyLabs LangKit use natural language processing techniques to extract signals from prompts and responses. These signals help developers identify quality issues, security threats, and behavioral drift.

Output integrity is the easiest cognitive layer to make concrete because it treats prompts and completions as observable artifacts. The model produced text, and that text can be analyzed.

But output quality is not the same as reasoning quality. A response can look fluent and still be based on the wrong reasoning path.

## Semantic Feedback

Semantic feedback collects and interprets feedback about agent outputs.

There are several forms:

**Explicit feedback.** Direct user ratings, such as thumbs up or thumbs down.

**Implicit feedback.** Signals inferred from user behavior, such as whether a suggestion was copied, saved, dismissed, edited, or retained. GitHub Copilot's suggestion-retention metrics are an example of this kind of signal.

**Free-form feedback.** Corrections, explanations, or comments provided by users. Evaluation systems such as Humanloop can collect this kind of feedback and use it to assess model behavior.

Semantic feedback helps estimate whether AIware outputs are useful in practice. It can also inform model training, prompt design, retrieval configuration, and workflow changes.

However, feedback becomes harder to interpret in multi-agent systems. If the final output is bad, which agent should receive the blame? The one that gathered the requirement? The one that planned? The one that executed? The one that summarized? Cognitive observability needs to preserve enough context to answer that attribution question.

## Reasoning Path

The most difficult pillar is reasoning path observability: understanding how a model reached a conclusion.

For developers, reasoning paths are essential. If an agent makes a mistake, we do not only want to know that the output was wrong. We want to know what assumption, interpretation, or intermediate step led to the wrong output. Without that, prompt improvement becomes guesswork.

The challenge is that reasoning is not directly exposed. We can ask a model to explain itself, but the explanation may not be faithful to the process that produced the answer. We can ask the model to reason step by step, but that changes the completion itself.

That is the motivation behind Watson.

## Watson: A Framework for Reasoning Path Observability

Watson is a framework for observing the reasoning of foundation-model-powered agents without requiring the primary agent to expose its reasoning directly.

### The Problem

We cannot simply instruct every agent to output its reasoning alongside its answer.

First, asking for reasoning changes the completion. The system is no longer observing the original behavior; it is observing behavior under an additional instruction. That creates an observer effect.

Second, downstream systems in Agentware are often tightly coupled to agent outputs. They may require strict JSON schemas, exact labels, tool-call formats, or other structured outputs. Adding a long explanation can break the contract.

So the question becomes: how can we observe reasoning without interfering with the agent's primary behavior?

### The Surrogate Agent

Watson uses a surrogate agent that operates alongside the primary agent.

The primary agent receives its prompt and produces its answer normally. The surrogate agent receives the same configuration, the original prompt, and the final answer. Its job is not to change the answer. Its job is to generate plausible reasoning paths that connect the prompt to the answer.

In other words, the surrogate "reasons out loud" about how the primary agent may have reached the observed output.

### How Watson Works

Watson has four core steps.

**1. Mirror configuration.** The surrogate agent mirrors the primary agent's configuration so that its reasoning is generated under a similar setup.

**2. Fill-in-the-middle reasoning generation.** Watson treats the primary agent's input prompt as the prefix and the primary agent's answer as the suffix. The surrogate then generates reasoning that fills in the middle, connecting prompt to answer.

**3. Multiple reasoning paths.** The surrogate generates multiple reasoning samples. Watson then extracts common threads and recurring ideas across those samples. This captures patterns in the implicit reasoning paths that may explain the primary agent's output.

**4. Attribution-based verification.** Watson checks whether ideas represented by high-attribution prompt components are emphasized in the generated reasoning. This helps validate whether the generated reasoning aligns with the influential parts of the prompt.

![How Watson operates](images/aiware-observability/slide_29_watson_operates.webp)

The goal is not to claim perfect access to the model's hidden cognition. The goal is to make the reasoning path more observable and useful for debugging.

## Example: Debugging Moral Reasoning

Suppose an agent is asked whether two scenarios are morally wrong. The correct answer is:

```text
Not wrong, Wrong
```

But the primary agent responds:

```text
Wrong, Not wrong
```

The raw output tells us that the answer is incorrect, but not why.

Watson's surrogate analysis generates multiple reasoning paths and identifies a common thread: the agent is not considering the order of the "wrong" and "not wrong" options when analyzing the scenarios.

![Watson surrogate agent debugging example](images/aiware-observability/slide_31_watson_example.webp)

That gives the developer a more useful diagnosis. The model may not be misunderstanding the scenarios themselves. It may be mishandling the ordering of the options. The developer can then add explicit instructions about preserving option order in the prompt.

This is the value of reasoning path observability. It turns "the model got it wrong" into a more actionable debugging hypothesis.

## Why This Matters

Cognitive observability gives developers a way to work with AIware behavior at the right level of abstraction.

For developers, it helps identify and correct reasoning errors, refine prompts, improve agent interactions, and debug failures that do not map cleanly to a line of code.

For agents, it creates the possibility of observing and improving their own behavior. An agent that can inspect reasoning paths may be better able to adjust future decisions.

For multi-agent systems, it supports collaboration. Agents can observe and reflect on each other's reasoning, making it easier to identify where a workflow drifted off course.

The larger point is that AIware observability cannot stop at traces and metrics. Those tell us what happened. But when decisions are generated dynamically, we also need tools that help us reason about the reasoning.

## Conclusion

Observability for AI systems is evolving from operational metrics focused on what happened toward cognitive observability focused on why and how decisions are made.

Understanding reasoning paths is crucial for building trustworthy, accountable, and transparent AI systems. Frameworks like Watson represent one approach to making opaque agent behavior more observable without compromising the primary agent's functionality.

As AI systems become more complex and autonomous, this cognitive layer of observability will become essential for debugging, improving, and trusting AI-powered applications.

## References

- Rombaut et al. "[Watson: A Cognitive Observability Framework for the Reasoning of LLM-Powered Agents](https://www.arxiv.org/abs/2411.03455)" ([ASE 2025 page](https://conf.researchr.org/details/ase-2025/ase-2025-papers/148/Watson-A-Cognitive-Observability-Framework-for-the-Reasoning-of-LLM-Powered-Agents), [PDF](publications/202505_agent_observability_ase2025.pdf))
- Rombaut. "[AIware Observability](publications/202411_aiware_bootcamp_observability_for_pdf.pdf)" ([AIware Leadership Bootcamp 2024](https://www.aiwarebootcamp.io/), [AIware Mini Bootcamp 2025](https://www.aiwarebootcamp.io/mini.html), [video](https://www.youtube.com/watch?v=gXsZgtyJ3s8))
- Hassan et al. "Rethinking Software Engineering in the Foundation Model Era"
- Wei et al. "Chain-of-thought prompting elicits reasoning in large language models"
- Bavarian et al. "Efficient Training of Language Models to Fill in the Middle"
