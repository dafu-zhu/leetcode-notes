---
name: lc-tutor
description: Use when the user shares a LeetCode problem together with a target solution they want explained clearly. Read and understand the provided solution, then write a light-themed HTML tutorial that follows that solution's idea faithfully and explains it clearly, expanding wherever the given explanation is brief. Do NOT invent or substitute your own solution. Ship a pytest pressure suite that validates the provided solution, update the index, and push. Run from the leetcode-notes repo root.
---

# lc-tutor

Turn a LeetCode solution the user gives you into a clear, permanent, pressure
tested teaching page on the `leetcode-notes` site. You explain the user's chosen
approach. You do not design your own.

## When to use
- The user shares a LeetCode problem and a solution they want explained. The
  solution usually comes with a short intuition or algorithm that reads too briefly.
- Trigger phrases: "explain this solution", "write this up", "teach me this",
  "/lc-tutor". Screenshots or pasted code and text are all fine.

## Prerequisites
- Run with cwd = the `leetcode-notes` repo root (this file lives in it).
- `python` + `pytest` available; `gh` authenticated; remote already set.
- Read `config.json` at the repo root for all paths and naming. Never hardcode.

## The core rule (read this first)
**Do not generate or substitute your own solution.** The user provides the target
solution. Your job is to explain that exact solution well.
- Transcribe the provided code into `solution.py` faithfully. Keep its logic
  unchanged. You may add short clarifying comments, but do not rewrite it, and do
  not "improve" it or swap the approach (for example, do not turn a recursive
  solution into an iterative one).
- Follow the given idea. If the user's approach is recursive, teach it recursively.
- The only time you write code of your own is the pytest suite that checks the
  provided solution, and small clarifying comments.
- If the user explicitly asks you to write or fix a solution, then you may. Default
  is that you do not.

## Voice & pedagogy
1. **Explain clearly, expand where brief.** The provided intuition is usually terse.
   Make it clear: fill in the missing steps, define terms, and state why each step
   is correct. Follow the user's structure when they give one (for example an
   Intuition section then an Algorithm section).
2. **Show, don't assert, with a diagram.** Any step that is not obvious, such as a
   recurrence, a bitwise trick, or a reindexing, must be shown on a concrete
   example, never just stated. Use a Mermaid diagram, not a text table. Choose the
   diagram type that fits the solution:
   - a **recursion tree** or **call graph** for a recursive solution (trace one
     concrete input, solid arrows going down, dashed arrows returning values up),
   - a **flowchart** for branch heavy control flow,
   - a **mindmap** when a concept overview helps.
   Put it in `<figure class="diagram"><pre class="mermaid">...</pre></figure>`. See the
   "Watch it run" section of `problems/0050-powx-n/tutorial.html` for the reference
   shape, and the Mermaid setup note below.
3. **Write plainly.** This is the most important style rule.
   - No em dashes and no en dashes. Use a period, a comma, or parentheses instead.
   - No invented words or forced coinages. If a term is not standard English or
     standard CS vocabulary, define it in plain words or do not use it.
   - No slogans and no clever one liners. If a sentence sounds like an ad, rewrite it.
   - Short, direct sentences. Common words. Say the thing, then stop.
   - Read each sentence aloud. If a normal person would not say it that way, rewrite.
4. **Keep it focused.** The deliverable is a clear explanation of the provided
   solution. Do not critique the user's earlier attempts unless they share one and
   ask why it failed. In that case, keep the note short.

## Workflow

### 1. Extract the inputs
Read every attachment. Pull out: problem **number**, **title**, **difficulty**, the
**target solution code**, and any **intuition or algorithm** text the user gave.
Derive the LeetCode **slug** from the title (lowercase, spaces to `-`, drop
punctuation; for example `Pow(x, n)` becomes `powx-n`).

### 2. Resolve paths from config.json
- `folder = "{num4}-{slug}"` (zero pad the number to 4 digits, e.g. `0050-powx-n`).
- `dir = problemsDir + "/" + folder`.
- Files: `solution.py`, `test_solution.py`, `tutorial.html` (and `attempt.py` only
  if the user shared their own attempt).
- If the folder already exists, this is a re-run: overwrite in place and update the
  manifest entry rather than adding a duplicate.

### 3. Place the provided solution
Write the user's solution verbatim into `solution.py` (LeetCode class signature,
short clarifying comments allowed, logic unchanged).

### 4. Write the pytest pressure suite (`test_solution.py`)
LeetCode style, four layers, all green against `solution.py`:
1. **examples**: the exact cases from the statement.
2. **boundaries**: derived from the problem's constraints (min/max n, empty, one
   element, extreme values, sign edges).
3. **fuzz**: a few hundred seeded random inputs compared against an oracle (brute
   force, a trusted library call, or a known closed form). Keep it deterministic,
   and pick input ranges that stay inside the stated constraints.
4. **scale/perf**: a max constraint input returns within a loose time budget and
   does not blow the recursion limit.
Import the solution via `from lc_harness import load_solution` (and `load_attempt`
only if an attempt exists). Run `python -m pytest problems/<folder> -q`.
**If the provided solution fails any test, do not fix it silently.** Report the
failing inputs to the user and ask how to proceed.

### 5. Write the tutorial (`tutorial.html`)
Copy `.claude/skills/lc-tutor/template.html` and fill every `{{PLACEHOLDER}}`. Link
`../../style.css` (never inline CSS). Default sections, in order:
- crumb back to `../../index.html`
- header: kicker `LeetCode <num>`, `<h1>` title, difficulty dot, leetcode link
- a one line `.lede` naming the approach
- **Intuition**: the core idea, clear and complete. Put a key formula or recurrence
  in a `.callout` if there is one.
- **Watch it run**: a `.example` figure that traces one concrete input through the
  solution (this is the show-don't-assert step).
- **Algorithm**: the step list, cleaned and clear (an `<ol>`).
- **The full solution**: the provided code in a highlighted `<pre>` (spans
  `c-kw c-fn c-num c-str c-com c-op`) plus a complexity line.
- **Takeaway**: a `.takeaway` box with the transferable pattern, then where it recurs.
Match the structure and tone of `problems/0050-powx-n/tutorial.html`.

### 6. Update the manifest and rebuild the index
Upsert into `data/problems.json` (replace if the number already exists):
```json
{ "num": <int>, "title": "<str>", "slug": "<str>", "difficulty": "Easy|Medium|Hard",
  "folder": "<num4-slug>", "date": "<YYYY-MM-DD>",
  "leetcodeUrl": "<url>" }
```
Then run `python build_index.py` (sorts ascending by number).

### 7. Commit, push, and report
- `git add -A && git commit -m "add <num>. <title>"` then `git push`.
- Print the two live URLs from `config.json` baseUrl:
  - tutorial: `<baseUrl>problems/<folder>/tutorial.html`
  - index: `<baseUrl>`
- Note that Pages can take about a minute to update.

## Mermaid diagrams
Diagrams render with Mermaid, vendored at `assets/mermaid.min.js` (the UMD build, so
diagrams work when the page is opened locally with `file://` as well as on Pages).
Every tutorial ends with the two script tags from `template.html`: the vendored
`<script src="../../assets/mermaid.min.js">` and a `mermaid.initialize(...)` call
with the light theme. Do not use the CDN and do not use the ES module build, since
browsers block ES modules under `file://`.

Authoring rules that avoid parser errors:
- Wrap each diagram in `<figure class="diagram"><pre class="mermaid"> ... </pre></figure>`.
- Quote every flowchart node label, for example `A["helper(x, n)"]`, because labels
  contain parentheses and commas.
- Write special characters as HTML entities inside the `<pre>` (`&middot;`, `&times;`,
  `&rarr;`). The browser decodes them before Mermaid reads the text.
- In a mindmap, node text cannot be quoted, so avoid parentheses and other symbols;
  use plain words.
- Keep labels short. Put longer explanation in the `figcaption`, not in nodes.

## Idempotency
Re-running a problem overwrites its files and its manifest entry, and rebuilds the
index. It never creates a duplicate row or folder.
