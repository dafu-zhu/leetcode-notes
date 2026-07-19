"""50. Pow(x, n)
https://leetcode.com/problems/powx-n/

Binary exponentiation, recursive. Each call squares the base and halves the
exponent, so computing x^n takes about log2(n) multiplications instead of n.
Approach and code provided by the user.
"""


class Solution:
    def myPow(self, x: float, n: int) -> float:
        def helper(x, n):
            if x == 0:                     # 0 to any positive power is 0
                return 0
            if n == 0:                     # base case: anything to the power 0 is 1
                return 1
            res = helper(x * x, n // 2)    # square the base, halve the exponent
            return x * res if n % 2 else res   # odd n keeps one extra factor of x

        res = helper(x, abs(n))            # compute the magnitude with a non-negative power
        return res if n >= 0 else 1 / res  # reciprocal when the original power was negative
