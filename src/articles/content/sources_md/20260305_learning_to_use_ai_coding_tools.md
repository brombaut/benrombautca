Over the past few years I've been meaning to write about my experience learning to use AI tools, both for software development and for work more generally. This is the first of what I expect will be a few articles on the topic, covering the timeline from early 2023 through the end of 2025.

This is a rough timeline of how I went from casually experimenting with AI chat tools to making them a core part of how I build software. It's not a guide or a set of recommendations, just an honest account of how my habits and thinking shifted over the past couple of years as AI has really started to take off.

## Early 2023 — First Experiments with ChatGPT

I started using ChatGPT seriously around early 2023, when I was finishing up my master's degree. At the time it was mostly curiosity, asking it simple questions that popped into my head, copy-pasting stack traces and error messages to see if it could help me debug something, or asking it to write a simple function. I remember being genuinely impressed, but I wasn't using it heavily. Google was still my default for anything I needed to look up.

## Building the Habit

Through 2023 I found myself using ChatGPT more and more, but the real shift was a deliberate one. I told myself: *I need to learn how to use this thing well, and the only way to do that is to keep using it.* So I started forcing myself to go to ChatGPT first, even before opening a Google search. For a while I'd actually run both in parallel, Googling an issue I was stuck on while also asking ChatGPT about it in another window, just to compare the processes and get more practice.

That parallel approach helped me build intuition for where ChatGPT was useful and where it fell short. Gradually, my trust in it grew. I started using it for more than just coding, using it for research, writing, understanding concepts, and the coding problems I brought to it got more complex.

## June 2024 — GitHub Copilot and the "Tab Tab Tab" Phase

In June 2024 I got a GitHub Copilot subscription and started using it directly in VS Code. This introduced a completely different interaction model. Instead of context-switching to a chat window, suggestions were appearing right where I was writing code. I quickly settled into what I think of as the "tab tab tab" pattern, watching completions appear and just accepting them in a rhythm. It felt like a much faster autocomplete, and at first, that's basically all it was to me.

Over time I started exploring the other features: the chat panel on the side where I could give it more explicit instructions, manually adding files to the context so it understood what I was working with, and the inline chat for quick targeted edits. These were genuinely useful, but I made a point of reading through every change it made. There were definitely times it produced something off or subtly wrong, and that kept me in the habit of not just blindly accepting output.

## Through Early 2025 — Steady Progress, No Dramatic Leaps

The second half of 2024 and into early 2025 was more of the same, just more comfortable and more frequent. Copilot for autocomplete in the editor, a ChatGPT window always open in the background for when I needed to paste in a problem or talk through something. It was a good setup, but I was still operating with a fairly close eye on everything the tools produced.

I tried out Copilot's agent mode when it was released, hoping it would be a step up. It wasn't, at least not for me at the time. It would spin, get stuck, or produce something completely unexpected. I couldn't get it to work consistently and didn't have a good mental model for how to direct it effectively. I didn't go back to it.

## Summer 2025 — Gemini CLI and a Shift in Mindset

Around the summer of 2025 I started using the Gemini CLI, and this felt like a genuine paradigm shift. The results were substantially better, but more than that, it changed what the tool asked of me mentally.

Everything happened in the terminal. The agent was working on the codebase directly, and I wasn't approving individual diffs in a familiar editor interface. There was a "yolo mode" where you could essentially let it do whatever it needed to do without interruption. I found that uncomfortable at first. I kept VS Code open beside the terminal, watching the files change in real time, still needing that visual anchor to feel in control. But I was getting used to a new way of working, one where I was directing rather than writing.

## End of Summer 2025 — Claude Code, and Things Clicking

I started using Claude Code at the end of summer 2025, and this is where things really clicked into place. I'm not sure I can articulate exactly why it felt better than Gemini CLI, it just did. I had read that Claude Code was considered one of the best agent environments for coding, and that matched my experience.

I became less focused on watching every individual change, and more focused on describing what I wanted and reviewing the overall result. My trust in the agent went up, and I started routing almost all of my development work through it. Around the same time I also started branching out more with LLM chat tools in general, using Claude and Gemini alongside ChatGPT rather than defaulting to ChatGPT for everything.

In November 2025 I attended the Automated Software Engineering conference in Seoul. At dinner one evening, I got talking with someone from the Anthropic team, who showed me a browser-based version of Claude Code where you could give it a task, and it would clone your repository, do the work, commit and push the changes, and open a pull request, all without you touching your local environment. Seeing that in person made the direction things were heading feel very concrete.

## Where Things Stand Now

What's changed most is the activation energy required to start working on something. I used to talk myself out of picking up a project because I knew how much upfront cognitive effort it would take, understanding the current state of the code, figuring out where to start, holding the whole context in my head. Now I just start a conversation. I ask Claude Code about the codebase, describe what I want to do, and we're off. The cognitive barrier to entry is much lower.

It's made software development fun again, even if what I'm doing now barely resembles what I'd have called coding a few years ago.
