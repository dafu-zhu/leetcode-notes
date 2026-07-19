"""Root conftest: put the repo root on sys.path so tests can `import lc_harness`."""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
