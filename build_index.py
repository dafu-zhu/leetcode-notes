#!/usr/bin/env python3
"""Regenerate index.html from data/problems.json.

Deterministic: reads the manifest, sorts problems ascending by number, and emits
a minimal light-themed landing page.  Run after adding/updating a problem:

    python build_index.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
MANIFEST = ROOT / CONFIG["manifest"]
PROBLEMS_DIR = CONFIG["problemsDir"]
STYLE = CONFIG["styleHrefFromIndex"]
OUT = ROOT / CONFIG["index"]

ROW = """      <a class="row" href="{href}">
        <span class="num">{num}</span>
        <span class="title">{title}</span>
        <span class="diff {diffclass}">{difficulty}</span>
      </a>"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LeetCode Notes</title>
<link rel="stylesheet" href="{style}">
</head>
<body>
<div class="wrap">
  <header class="site-head">
    <h1>LeetCode Notes</h1>
    <p class="tagline">Idea-first solutions, taught from scratch. Each one pressure tested.</p>
    <p class="count">{count} problem{plural}</p>
  </header>
  <main class="plist">
{rows}
  </main>
</div>
</body>
</html>
"""


def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"problems": []}
    problems = sorted(data.get("problems", []), key=lambda p: p["num"])

    if problems:
        rows = "\n".join(
            ROW.format(
                href=f"{PROBLEMS_DIR}/{html.escape(p['folder'])}/{CONFIG['tutorialFile']}",
                num=p["num"],
                title=html.escape(p["title"]),
                difficulty=html.escape(p["difficulty"]),
                diffclass=p["difficulty"].lower(),
            )
            for p in problems
        )
    else:
        rows = '      <p class="empty">No problems yet.</p>'

    page = PAGE.format(
        style=STYLE,
        count=len(problems),
        plural="" if len(problems) == 1 else "s",
        rows=rows,
    )
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT}  ({len(problems)} problem(s))")


if __name__ == "__main__":
    main()
