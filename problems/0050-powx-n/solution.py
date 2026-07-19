"""50. Pow(x, n) — https://leetcode.com/problems/powx-n/

Binary (fast) exponentiation. Read n in binary from the low bit up: whenever
the current bit is 1, the running answer owes a factor of the *current* base;
every step squares the base and shifts n right. O(log n) time, O(1) space.
"""


class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:              # x^(-n) == (1/x)^n — handle the sign once, up front
            x, n = 1 / x, -n
        result = 1.0
        while n:
            if n & 1:          # low bit set -> multiply in the base at this position
                result *= x
            x *= x             # square the base for the next binary position
            n >>= 1            # drop the consumed bit
        return result
