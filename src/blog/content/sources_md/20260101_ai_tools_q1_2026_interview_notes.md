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

*[Answer pending — interview was cut short here]*

---

## Terminal Setup (clarified during interview)
- **Windows work computer**: Tabby — easy to save and quickly connect to SSH profiles on different servers
- **Personal Mac**: Ghostty (not Tabby — correct the issue notes which say Tabby)
- VS Code role reduced to: looking at data and file systems only

---

## Remaining Questions (planned but not yet asked)

1. The Claude Code Radar — did it actually meaningfully change how you managed parallel sessions day-to-day, or mostly a fun project?
2. Kintsugi — what is it exactly, and what was your experience with it? Did it solve what you hoped?
3. Which Steve Yegge articles/interviews specifically? What did they change about how you think or work?
4. Beads in practice — did you actually use it meaningfully this quarter, or more of an experiment? (Note: beads setup had issues transferring to this machine)
5. The inetanel article on Claude Code vs. opencode — what was the specific idea that sparked the model-per-role routing interest? (Link to include in post)
6. opencode and Codex honest take — did trying them make you more or less confident in Claude Code?
7. Is this article meant to be a personal journal entry, an opinionated take, or somewhere in between?
8. Anything that happened this quarter you're deliberately leaving out, and why?
9. Context management strategies — what specifically changed or improved in how you manage context in Claude Code sessions?
10. Claude Code skills generally — what are you doing now that you weren't doing in January? What clicked?

---

## Article Topics from Issue (for reference)
- Claude Code as primary tool
- Gemini CLI usage *(not discussed yet)*
- Shift toward working more in the terminal / terminal emulator switch
- Increased use of tmux
- Running multiple Claude Code sessions in parallel
- Trying out Kintsugi *(not discussed yet)*
- Building Claude Code Radar app for observability
- Using VS Code mainly to look at data rather than write code
- Claude Code skills (prompting, context management, workflows) *(not discussed yet)*
- Context management strategies *(not discussed yet)*
- Getting started with Beads issue tracker
- Reading Steve Yegge / GasTown articles
- March: experimenting with opencode, Codex, other models
- model-per-role routing idea from inetanel article *(link to include)*
- Workflows that didn't stick (paper summaries, quick-capture convos with Claude)
