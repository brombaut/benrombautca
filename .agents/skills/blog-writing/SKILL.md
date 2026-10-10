---
name: blog-writing
description: House writing style and content pipeline for benrombaut.ca blog posts. Use when outlining, drafting, editing or reviewing a blog post, writing diagram labels or image alt text for one, or adding, converting or syncing a post and its images.
---

# Blog writing

Moved out of `AGENTS.md` so it only loads when a post is being worked on. The
hard prohibitions (never hand-edit `blog_posts_content.json`, never reconvert
the archived posts) stay in `AGENTS.md`, because a task that has nothing to do
with the blog can still break them.

## Writing style

Agreed with Ben by interview under #550, replacing a section that had accreted
from corrections given in passing. Where he said he does not care, that is
recorded as such below rather than left to be guessed at again.

**Scope.** These rules govern blog posts and the text in blog diagrams. They do
*not* govern commit messages or issue bodies, which were previously being
written to them by default. Within a diagram, the labels inside the figure get
only the phrase bans (no jargon, no coined labels), since the prose rules cannot
apply to a noun phrase; alt text is prose that ships on the page and gets read
aloud, so it follows every rule here.

**Two kinds of post.** The AI Experience series is a personal experience report
and reads as narrative. Everything else reports on an experiment or surveys a
landscape and reads as technical reporting. Rules below that apply to only one
kind say so; the rest apply to both.

### Voice and Tone

- First person. These are accounts of real experience, not guides or tutorials
- **Do not turn an observation into a general law with "you".** "When I'm
  running multiple agents" rather than "When you're running multiple agents".
  Describing what a tool lets anyone do is ordinary idiom and is fine ("a yolo
  mode where you could let it do whatever it needed to")
- **Use contractions.** "didn't", "I'm", "it's". Expanded forms throughout read
  stiff, which is what made the Q2 2026 post more formal than the Q1 one next to it
- Measured and direct, not flowery or over-written
- **No feeling words about a finding.** Not "surprised", "striking",
  "fascinating", "genuinely interesting", "remarkable", "magical", "dramatic",
  "what stands out". Naming a feeling reads as trying to make the post
  entertaining, and nothing here warrants it. A failed prediction stated flatly
  is a fact rather than a feeling, so it stays: "I expected the ordering to go
  the other way; it did not"
- **No borrowed-metaphor jargon.** Not "workflow gravity", "daily driver",
  "center of gravity", "highest-leverage", "paradigm shift", "brought to the
  table", "move the needle", "unlock", "deep dive", "game-changer". Domain terms
  that name a specific thing in the work are fine and should be used:
  "structural depth", "exploration surface area", "blast radius", "holistic
  scoring", "comprehension debt"
- **No "not just X, it's Y" contrast setup.** State the positive claim instead.
  "The useful part was having a workflow that knew what I was thinking about",
  not "the useful part wasn't just retrieval, it was having a workflow that..."
- **No coined labels for an idea.** A phrase like "a know vs do gap" is the
  writing trying to be snappy. Say the thing in a sentence
- Hedge when the uncertainty is genuine ("SWE-bench Verified probably just
  doesn't contain system-wide architectural problems"). Do not hedge a claim you
  are actually confident about
- When tools or automation did the work, say so: "I had Claude Code
  generate..." not "I generated...". Don't claim personal credit for automated work

### Content Decisions

- Cut implementation noise that doesn't serve the reader: internal version
  numbers, zero-count stats, details only a developer would care about. If a
  number or fact isn't interesting, don't report it
- Go deep on methodology. Readers want enough process detail to judge whether
  the approach is sound. Explain the "how" thoroughly, especially when the
  method is novel or non-obvious
- Organize around insights, not analysis structure. Each section heading should
  promise something interesting, not describe a data processing step. "The Model
  Invents Its Own Pattern Vocabulary" over "Section B: Pattern Analysis"
- **Mark the most important finding with a flat bolded label**, not a hyped one:
  `**The main finding:**` rather than "the most striking finding" or "the
  biggest surprise of the whole project". When several findings compete, carry
  it structurally instead, by putting the important one first or giving it its
  own section
- When a post is part of a larger system or pipeline, explain the pipeline
  briefly before the piece being analyzed. **A prose recap of the earlier posts
  in a series is the convention and should stay**; every AI Experience post
  opens with one. What is actually banned is requiring the reader to go read
  another post to follow this one
- Every plot needs two things: a brief sentence explaining what the chart shows
  (axes, colors, groupings), then the insight or takeaway, stated flatly. Don't
  drop a plot and jump straight to analysis, and don't just describe the data
  without drawing a conclusion
- **Alt text stays descriptive.** It says what the picture shows; the argument
  lives in the prose
- Don't duplicate a chart's data in a table. If the plot shows it, the prose
  should highlight the insight, not restate the numbers in a different format
- When discussing limitations, be honest about whether the issue is with the
  method or with the dataset. "The scale goes unused" could mean the scale is
  miscalibrated or it could mean the data doesn't have hard enough problems.
  Name the ambiguity instead of defaulting to self-criticism

### Length

Aim for a **10 minute read at most, and preferably shorter**. The site counts
reading time at 225 wpm (`WORDS_PER_MINUTE` in `src/_data/blog.js`), so that is
about 2,250 words. Going over is fine when the post genuinely covers that much
ground, but length is the guard against over-explaining: if a post is long
because it is spelling out things the reader can infer, cut rather than justify.

This applies to new posts. The five published posts already over the budget (the
three SWE-bench Architecture posts at 13 to 18 minutes, Learning LLMs 4 at 15,
and Inside 13 Coding Agents at 14) were deliberately left alone.

### Punctuation and Formatting

- **No em dashes in prose.** Use a comma, a colon, or restructure
- **An em dash as a heading separator is fine**, and is the house style:
  `## April — Building Personal Workflows on Top of Agents`. A colon is equally
  correct in that position; a plain hyphen is not, and was fixed in the Q2 post
- The three characters do three different jobs: a **hyphen** joins words into
  one compound ("day-to-day", "pre-AI"), an **en dash** spans a range
  ("January–February", "2023–2025"), and an **em dash** separates a label from a
  title or sets off a clause
- Italics are fine for internal thoughts or emphasis (e.g. *I need to learn how
  to use this thing*)
- Keep sentences clear and relatively short
- **Always specify a language on markdown code blocks** for syntax highlighting
  (e.g. ```python, ```bash, ```typescript). If writing pseudocode, use ```python
  since its highlighting is the closest match

### Structure

- Personal narrative posts open with a brief framing paragraph before the main
  content: what series this belongs to, what period it covers
- Section headers use the `## Heading` format with a date or phase label where relevant

### Working on a post with Ben

- **Outline first.** Get the outline agreed before writing prose, rather than
  handing over a full draft to react to
- **Don't add conclusions he didn't draw.** If there is an insight sitting in the
  data that the draft doesn't state, say so and let him decide. Do not write it
  into the post

### Deliberately unspecified

Ben was asked about these and does not want a rule, so do not infer one and do
not raise them again: when a bulleted list is right rather than prose (case by
case), the bracketed series prefixes in post titles, how much external evidence
a post should cite, and the wording of the series framing paragraph.

## Pipeline

### Adding a New Blog Post

Run steps 2 and 3 from the pinned venv (`npm run sync-articles` does both, and
recreates the venv first), or the converter will exit rather than fall back to
whatever pandoc is on the machine.

1. Write post in Markdown: `src/blog/content/sources_md/post-name.md`
2. Run conversion script from `src/blog/content/`: `python 01_md_to_html_converter.py`
3. Run sync script from `src/blog/content/`: `python 02_existing_html_articles_syncer.py`
   - This adds a blank stub entry to `blog_posts_meta.json` and populates `blog_posts_content.json` with the HTML body
   - **Important**: The syncer appends a blank meta entry (`_title: ""`, `_show: false`) for any HTML file not already in the content JSON. You must manually fill in the metadata after running it — do not run the syncer again after editing the meta or it will append another blank stub.
4. Edit the stub entry in `src/blog/blog_posts_meta.json` with the correct values:
   ```json
   {
     "_id": "YYYYMMDD_post_slug",
     "_title": "Post Title",
     "_createdAt": "YYYY-MM-DDT00:00:00.000Z",
     "_description": "One-sentence description.",
     "_show": true,
     "_archived": false
   }
   ```
5. Commit changes

**IMPORTANT**: Never directly edit `blog_posts_content.json`. To change blog post content, always edit the source markdown file in `src/blog/content/sources_md/`, then re-run the conversion and sync scripts (steps 2 and 3). The content JSON is a generated artifact and will be overwritten by the syncer.

### Blog Post Images
Images are served via Eleventy passthrough copy, which copies `src/blog/content/images/` to `dist/blog-images/` at build time. The MD-to-HTML converter rewrites `src="images/` to `src="blog-images/"` during conversion.

**To add images to a post:**
1. Create a directory: `src/blog/content/images/<post-slug>/`
2. Place image files in that directory
3. Reference them in your markdown as: `![Alt text](images/<post-slug>/image.png)`
4. The converter handles path rewriting automatically — no manual HTML editing needed

**When copying a post from an external source (e.g. a README from another repo):**
- Image paths must be rewritten from bare filenames (e.g. `![](image.png)`) to the `images/<post-slug>/` convention
- Remove any repo-specific sections (e.g. `## Files` listing notebook/data files) that don't belong on the blog
- Copy all referenced images into the corresponding `src/blog/content/images/<post-slug>/` directory

**To update an existing post's content:**
1. Overwrite the markdown source in `sources_md/`
2. Rewrite image paths to use the `images/<post-slug>/` prefix
3. Remove any repo-specific sections
4. Re-run `01_md_to_html_converter.py` and `02_existing_html_articles_syncer.py`
5. The syncer will update the content JSON without creating a duplicate meta entry

### The pandoc version is pinned

`requirements.txt` pins `pypandoc_binary==1.17`, whose wheel bundles pandoc 3.9,
and `01_md_to_html_converter.py` points `PYPANDOC_PANDOC` at that bundled binary
before converting anything. Both halves are needed: pypandoc searches `PATH`,
`~/bin` and its own bundle and uses the **highest** version it finds, so the pin
alone would lose to any newer pandoc installed on the machine. Without this the
committed HTML was a function of the machine rather than of the markdown (#548).
There is no `download_pandoc()` fallback; a missing bundled binary is a hard error.

The converter writes a `.html` only when the generated content differs, so
editing one post produces a one-post diff instead of rewriting every file.
