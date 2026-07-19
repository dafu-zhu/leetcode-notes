"""Pressure test for 50. Pow(x, n), LeetCode style.

Four layers hit the CORRECT solution and must all pass:
  1. examples      : the cases printed in the problem statement
  2. boundaries    : pulled from the stated constraints
  3. fuzz          : 500 seeded-random inputs vs. Python's float ** oracle
  4. scale/perf    : max-constraint n returns fast (O(log n), no timeout)

A final section documents that the original attempt.py is broken as the
tutorial claims, so the teaching example can't silently rot.
"""
import math
import random
import time

import pytest

from lc_harness import load_solution, load_attempt

solve = load_solution(__file__).Solution().myPow
attempt = load_attempt(__file__).Solution().myPow

REL = 1e-9
ABS = 1e-12


def close(a, b):
    return math.isclose(a, b, rel_tol=REL, abs_tol=ABS)


# ---------- 1. examples ----------
@pytest.mark.parametrize("x, n, expected", [
    (2.0, 10, 1024.0),
    (2.1, 3, 9.261),
    (2.0, -2, 0.25),
])
def test_examples(x, n, expected):
    assert close(solve(x, n), expected)


# ---------- 2. boundaries ----------
@pytest.mark.parametrize("x, n, expected", [
    (5.0, 0, 1.0),          # anything ^ 0 == 1
    (-3.0, 0, 1.0),
    (0.5, 0, 1.0),
    (7.0, 1, 7.0),          # ^1 == x
    (7.0, -1, 1 / 7.0),     # ^-1 == 1/x
    (1.0, 2**31 - 1, 1.0),  # 1 ^ INT_MAX
    (1.0, -2**31, 1.0),     # 1 ^ INT_MIN
    (-1.0, 2**31 - 1, -1.0),  # (-1) ^ odd  == -1
    (-1.0, -2**31, 1.0),      # (-1) ^ even == 1
    (0.01, 2, 1e-4),        # small base, still within x^n bounds
    (100.0, 2, 1e4),        # large base
])
def test_boundaries(x, n, expected):
    assert close(solve(x, n), expected)


# ---------- 3. fuzz vs oracle ----------
def test_fuzz_against_builtin_pow():
    rng = random.Random(0xC0FFEE)
    for _ in range(500):
        x = rng.choice((-1, 1)) * rng.uniform(0.1, 10.0)  # |x| in [0.1, 10] -> no overflow
        n = rng.randint(-40, 40)
        got = solve(x, n)
        ref = x ** n
        assert close(got, ref), f"x={x!r} n={n}: got {got!r}, expected {ref!r}"


# ---------- 4. scale / perf ----------
def test_scale_is_logarithmic():
    start = time.perf_counter()
    assert solve(1.0, 2**31 - 1) == 1.0            # exact, huge exponent
    solve(2.0, 2**31 - 1)                          # overflows to inf but must NOT loop 2^31 times
    elapsed = time.perf_counter() - start
    assert elapsed < 0.5, f"too slow ({elapsed:.3f}s), not O(log n)?"


# ---------- documentation: attempt.py is broken as claimed ----------
@pytest.mark.parametrize("x, n", [
    (2.0, 5),    # -> 64, should be 32
    (2.0, 6),    # -> 32, should be 64
    (2.0, 15),   # -> 16384, should be 32768
    (3.0, 5),    # -> 729, should be 243
    (2.0, -3),   # -> 0.25, should be 0.125
])
def test_attempt_is_broken_as_documented(x, n):
    """Locks in the tutorial's autopsy: the old attempt disagrees with truth here."""
    assert not close(attempt(x, n), solve(x, n))
