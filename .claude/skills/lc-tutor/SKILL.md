---
name: lc-tutor
description: Use when the user shares a screenshot (or code) of a LeetCode attempt and wants to be taught the pattern rather than nitpicked. Judges the IDEA (not the code), teaches the solution from scratch in an interview think-aloud voice, writes a light-themed HTML tutorial plus a pytest pressure suite into this repo, regenerates the index, and pushes. Run from the leetcode-notes repo root.
---

# lc-tutor

Turn one LeetCode attempt into a permanent, pressure-tested teaching page on the
`leetcode-notes` site. The output is idea-first: keep what's salvageable about the
user's thinking, throw the code away, and rebuild the solution from the first read.

## When to use
- The user attaches a screenshot of a LeetCode problem + their solution (usually a
  Wrong Answer / TLE) and asks to be taught, corrected, or shown "the pattern."
- Trigger phrases: "teach me", "dismantle the pattern", "correct me", "/lc-tutor".

## Prerequisites
- Run with cwd = the `leetcode-notes` repo root (this file lives in it).
- `python` + `pytest` available; `gh` authenticated; remote already set.
- Read `config.json` at the repo root for all paths and naming. Never hardcode.

## Voice & pedagogy (the whole point)
1. **Limit the criticism.** Diagnose the idea in a short verdict, then move on. Do
   not walk through every bug in their code. One or two crisp sentences on the
   single root flaw is the ceiling.
2. **Judge the IDEA, not the code.** Decide one of three verdicts:
   - `sound`   — the core approach is correct; only execution was off.
   - `partial` — the right instinct is in there but the key mechanism is wrong.
   - `wrong`   — the approach can't work; explain *why* in one clear paragraph.
3. **Throw the code away.** After the verdict, explicitly drop their code and
   rebuild. Never iterate on their broken structure.
4. **Teach from scratch, thinking out loud.** First person, present tense, as if
   whiteboarding in an interview. Start at the moment you read the problem:
   what's it really asking → where's the leverage / entry point → develop the
   approach step by step → edge cases → write it. Name the *trigger* that should
   fire next time ("exponent + must be sub-linear → square-and-halve").
5. **End with the transferable pattern**, plus a one-sentence invariant/principle
   and where else the shape shows up.

## Workflow

### 1. Extract from the screenshot
Read every attached image. Pull out: problem **number**, **title**, **difficulty**,
**language**, the user's **full code** (transcribe exactly), and any visible
**failing case / expected output**. Derive the LeetCode **slug** from the title
(lowercase, spaces→`-`, drop punctuation; e.g. `Pow(x, n)` → `powx-n`). Confirm the
slug against the real leetcode.com URL if unsure.

### 2. Resolve paths from config.json
- `folder   = "{num4}-{slug}"` (zero-pad number to 4 digits, e.g. `0050-powx-n`).
- `dir      = problemsDir + "/" + folder`.
- Files: `solution.py`, `attempt.py`, `test_solution.py`, `tutorial.html`.
- If the folder already exists, this is a **re-run**: overwrite in place and update
  (don't duplicate) the manifest entry.

### 3. Verify by execution (always try)
- Write the correct `solution.py` (LeetCode class signature) and the user's verbatim
  code as `attempt.py`.
- Build the strongest oracle available: brute force, a trusted library call, or
  known closed forms. Use it to find the *exact* inputs where the attempt fails —
  cite those real failures in the verdict, never hand-wave.
- If genuinely not runnable (e.g. needs LeetCode's internal types), fall back to
  static reasoning and say so in the page.

### 4. Write the pytest pressure suite  (`test_solution.py`)
LeetCode-style, four layers, all green against `solution.py`:
1. **examples** — the exact cases from the statement.
2. **boundaries** — derived from the problem's constraints (min/max n, empty, 1
   element, extreme values, sign edges…).
3. **fuzz** — a few hundred **seeded-random** inputs vs. the oracle (deterministic;
   pick input ranges that stay inside the stated constraints so nothing over/underflows).
4. **scale/perf** — a max-constraint input returns within a loose time budget and
   doesn't blow the recursion limit.
Import solution/attempt via `from lc_harness import load_solution, load_attempt`
(handles path loading; keeps modules collision-free). Add a final documentation
test asserting `attempt.py` disagrees with truth on its known-bad inputs, so the
teaching example can't silently rot.
Run `python -m pytest problems/<folder> -q` and confirm green before continuing.

### 5. Write the tutorial  (`tutorial.html`)
Copy `.claude/skills/lc-tutor/template.html` and fill every `{{PLACEHOLDER}}`.
Link `../../style.css` (never inline CSS). Sections, in order:
- crumb back to `../../index.html`
- header: kicker `LeetCode <num>`, `<h1>` title, difficulty dot, leetcode link
- **verdict** div with class `sound|partial|wrong` + 2–4 sentence idea judgement +
  the "keeping the idea, dropping the code" line
- **From scratch — thinking out loud**: a `.think` block of `.beat`-labelled
  paragraphs (the monologue)
- a `.callout` with the algorithm in one sentence
- **The full solution**: highlighted `<pre>` (spans `c-kw c-fn c-num c-str c-com c-op`)
  + a complexity line
- **Takeaway**: `.takeaway` box with the principle, then where the pattern recurs
Keep prose tight and concrete. Match the tone of `problems/0050-powx-n/tutorial.html`.

### 6. Update the manifest & rebuild the index
Upsert into `data/problems.json` (replace if the number already exists):
```json
{ "num": <int>, "title": "<str>", "slug": "<str>", "difficulty": "Easy|Medium|Hard",
  "folder": "<num4-slug>", "verdict": "sound|partial|wrong",
  "date": "<YYYY-MM-DD>", "leetcodeUrl": "<url>" }
```
Then run `python build_index.py` (deterministic; sorts ascending by number).

### 7. Commit & push, then report
- `git add -A && git commit -m "add <num>. <title>"` then `git push`.
- Print the two live URLs (from `config.json` baseUrl):
  - tutorial: `<baseUrl>problems/<folder>/tutorial.html`
  - index:    `<baseUrl>`
- Note Pages can take ~1 minute to update on first push.

## Idempotency
Re-running a problem overwrites its four files and its manifest entry, and rebuilds
the index — never creates a duplicate row or folder.
