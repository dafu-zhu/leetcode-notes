"""Shared test harness for LeetCode Notes.

Each problem lives in its own folder (problems/NNNN-slug/) with a solution.py
and an attempt.py.  Because many problems each define a module named `solution`,
we load them by path under a unique module name to avoid sys.modules collisions.
"""
import importlib.util
from pathlib import Path


def load(path):
    """Load a .py file by path as a uniquely-named module and return it."""
    path = Path(path)
    name = f"lc_{path.parent.name}_{path.stem}".replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_solution(test_file):
    """Load the solution.py sitting next to the given test file."""
    return load(Path(test_file).parent / "solution.py")


def load_attempt(test_file):
    """Load the attempt.py sitting next to the given test file (may be absent)."""
    p = Path(test_file).parent / "attempt.py"
    return load(p) if p.exists() else None
