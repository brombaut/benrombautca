# Interview Notes: AI Tools in My Development Workflow - Q1 2026
# Issue: benrombautca-ssw
# Status: Interview in progress (paused)

---

## Questions Asked & Answers

**Q: Walk me through Q1 roughly month by month — what was January like, what shifted in February, what was March about?**

January and February were about deepening the Claude Code practice:
- Really started using tmux and parallel sessions — both within the same project (same git repo) and across different projects, leading to lots of context switching
- Constantly checking tmux sessions to see which were waiting for input/approval — this friction led to building the Claude Code Radar (CCR) app
- CCR is an observability tool that hooks into all Claude Code sessions, captures all events, and displays them in a session-timeline view frontend — so you can see at a glance which sessions are actively working and which are waiting on input
- Started reading and listening to Steve Yegge interviews — he created beads and Gastown, liked his vibe and ideas
- Started using beads for issue tracking with the goal: get all issues and dependencies set up early in a way agents can handle, so less manual monitoring/check-ins needed

March: briefly tried opencode and Codex but neither hooked in the way Claude Code did — kept coming back to Claude Code. Work got busy, so not much time to explore. Plans to try opencode and model-per-role routing (from the inetanel article) more seriously next quarter.

**Q: The Claude Code Radar sounds like the most technically interesting thing you built. Was it mostly a fun side project, or did it actually meaningfully change how you managed parallel sessions?**

Mostly a fun side project. It kept growing from the original timeline view of a session to also showing subagent sessions, tool calls, capturing input/output content, token tracking, failure rates, etc. It didn't really change how I managed day-to-day sessions — it was just something cool to look at to help watch agents work. Abandoned it towards the end of March, the habit of using it didn't stick.

**Q: Kintsugi — what is it exactly, and what was your experience with it?**

Kintsugi (https://events.sonarsource.com/kintsugi/) — first try at using an "agent command center" or "agent orchestrator". Mental model: a nice UI that sits on top of tmux, tries to organize sessions better. Very cool to work with at first, but same thing happened — didn't stick, went back to tmux.

**Q: Which Steve Yegge articles/interviews specifically stood out? What did they change about how you think or work?**

Articles on Gastown, Beads, the AI Vampire, The Anthropic Hive Mind (all on https://steve-yegge.medium.com/). Also watched interviews with him. "Smart crazy guy" — his excitement for these things is contagious. Started working with beads in some projects as a result.

**Q: Did you actually use beads meaningfully this quarter, or more of an experiment?**

Definitely still "trying it out" phase. Only used it artificially on smaller projects, which isn't really its wheelhouse. Wants to try it on a much larger project where the work pipeline can stay full for a while. Main issues: keeping the pipeline full, and tracking beads issues across different clones — but those are growing pains.

**Q: The inetanel article on Claude Code vs. opencode — what sparked the model-per-role routing interest?**

Mostly seeing the true cost of using Anthropic models. With opencode, you can define different models for different types of tasks and not be locked into high-cost models all the time. Didn't look into it too deeply, but an interesting idea to come back to in the coming months. (Link: https://inetanel.com/articles/claude-code-vs-opencode-cto-decision)

**Q: opencode and Codex honest take — what specifically didn't hook you?**

OpenCode: didn't give it much of a chance — already had a Claude Code subscription and naturally came back to it. Plans to spend a couple days getting familiar with OpenCode and trying the model-per-role idea soon.

Codex: genuinely tries it every once in a while (usually when the Claude Code quota runs out, which happens two or three times per week), but doesn't get the same results. Too often typing things like "WHY DID YOU DO THAT I TOLD YOU TO DO THIS THING" or stopping it as it goes down weird rabbit holes and having to correct it.

**Q: What tone/format is this article meant to be?**

Continuation of the first blog post about getting started with AI tools (20260305_learning_to_use_ai_coding_tools.md). Personal journal entry, plans to do these 3-4 times per year to document the journey.

**Q: Anything you're deliberately leaving out?**

No, covered most of it. End of March / beginning of April: still using tmux and Claude Code as main drivers, looking into different agent command centers to try in coming months, no longer writing any code, getting Claude to always write docs and handoff readmes so it can come back to them later. Working with agents is getting better.

**Q: Context management strategies — what changed? Claude Code skills — what clicked?**

More aware of context management now. Compacting prematurely at natural break points. Has a new handoff skill to keep a markdown record of the agent's work.

**Q: Did you use Gemini CLI at all this quarter?**

No, didn't come back to it. It's just sitting off to the sidelines.

---

## Terminal Setup (clarified during interview)
- **Windows work computer**: Tabby — easy to save and quickly connect to SSH profiles on different servers
- **Personal Mac**: Ghostty (not Tabby — correct the issue notes which say Tabby)
- VS Code role reduced to: looking at data and file systems only

---

## Interview Complete (2026-04-17)

## Key Themes / Threads for Article
- **Pattern of tools not sticking**: CCR, Kintsugi, paper summary workflows, quick-capture convos — all exciting at first, then abandoned. Honest about this.
- **Claude Code as the constant**: Everything else comes and goes, but Claude Code remains the primary tool.
- **Cost awareness emerging**: The inetanel article sparked interest in model-per-role routing for cost reasons.
- **Codex frustration**: Genuine, visceral frustration compared to Claude Code — good anecdote material.
- **Steve Yegge influence**: Cultural/mindset influence, not just technical.
- **Beads as aspirational**: Not yet proven at scale, but the vision is clear.
- **No longer writing code**: A significant milestone in the journey from the first article.
- **Context management maturing**: More deliberate about compaction, handoffs, agent continuity.
- **Gemini CLI sidelined**: Fully replaced by Claude Code.
- **Continuation of journey**: Same tone as first article, personal and honest.

## Article Topics from Issue (final status)
- Claude Code as primary tool ✅
- Gemini CLI usage ✅ (sidelined, not used this quarter)
- Shift toward working more in the terminal / terminal emulator switch ✅
- Increased use of tmux ✅
- Running multiple Claude Code sessions in parallel ✅
- Trying out Kintsugi ✅
- Building Claude Code Radar app for observability ✅
- Using VS Code mainly to look at data rather than write code ✅
- Claude Code skills (prompting, context management, workflows) ✅
- Context management strategies ✅
- Getting started with Beads issue tracker ✅
- Reading Steve Yegge / GasTown articles ✅
- March: experimenting with opencode, Codex, other models ✅
- model-per-role routing idea from inetanel article ✅
- Workflows that didn't stick (paper summaries, quick-capture convos with Claude) ✅
