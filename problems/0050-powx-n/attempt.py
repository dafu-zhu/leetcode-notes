"""Original attempt (kept for the record). This is the BROKEN version.

Idea was binary exponentiation, but the odd-bit "remainder" was tracked as an
integer `count` and then re-injected as x0**count at every level of the
recursion. That correction both compounds (positive n) and ignores sign
(negative n), so it computes x0**(something) that equals n only for certain
bit patterns. See tutorial.html for the full autopsy. Passed 220/307 on LeetCode.
"""


class Solution:
    def myPow(self, x: float, n: int) -> float:
        ans = 1
        def helper(x0, x, n, count):
            if n == 1:
                return x
            elif n == 0:
                return 1
            elif n == -1:
                return 1 / x
            else:
                if n % 2:
                    count += 1
                x *= x
                n //= 2
                return helper(x0, x0, count, 0) * helper(x0, x, n, count)
        return helper(x, x, n, 0)
