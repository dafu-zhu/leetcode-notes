# LeetCode Notes

Idea-first LeetCode solutions, taught from scratch — each one pressure-tested.

**Live site:** https://dafu-zhu.github.io/leetcode-notes/

Every problem is generated from a screenshot of an attempt via the `/lc-tutor`
skill. The skill judges the *idea* (not the code), rebuilds the solution from the
first read in an interview think-aloud voice, and ships a light-themed HTML
tutorial next to a LeetCode-style `pytest` suite.

## Layout

```
index.html                     generated landing page (ascending by problem #)
style.css                      shared light-minimal design system
problems/<NNNN-slug>/
    tutorial.html              the teaching page
    solution.py                the correct solution, importable
    attempt.py                 the original attempt, for the record
    test_solution.py           pytest pressure suite (examples/boundaries/fuzz/scale)
data/problems.json             manifest — source of truth for the index
config.json                    paths & naming for the skill
build_index.py                 regenerates index.html from the manifest
conftest.py / lc_harness.py    test harness (per-folder solution loading)
.claude/skills/lc-tutor/       the skill that generates all of the above
```

## Usage

From the repo root, in Claude Code:

```
/lc-tutor        (with a screenshot of your LeetCode attempt attached)
```

## Run the tests

```
pip install -r requirements.txt
pytest -q
```

CI runs the full suite on every push (`.github/workflows/test.yml`).
