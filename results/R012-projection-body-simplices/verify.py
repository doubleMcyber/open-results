"""Exact certificates for RESULT.md. Run with standard Python 3."""

from fractions import Fraction
from math import factorial


def simplex(d):
    return Fraction((d + 1) * d**d, factorial(d))


def balanced(n, k):
    a, b = divmod(n, k)
    return simplex(a) ** (k - b) * simplex(a + 1) ** b


def formula(n):
    lo = max(1, n // 13)
    hi = max(1, (n + 12) // 13)
    return max(balanced(n, lo), balanced(n, hi))


def residue_product(n):
    q, j = divmod(n, 13)
    if j <= 8:
        return simplex(14) ** j * simplex(13) ** (q - j)
    return simplex(12) ** (13 - j) * simplex(13) ** (q + j - 12)


def partition_optima(limit):
    """Unbounded-part DP. Count maximizing multisets, ignoring part order."""
    best = [Fraction(0)] * (limit + 1)
    count = [0] * (limit + 1)
    best[0], count[0] = Fraction(1), 1
    for d in range(1, limit + 1):
        value = simplex(d)
        for n in range(d, limit + 1):
            candidate = best[n - d] * value
            if candidate > best[n]:
                best[n], count[n] = candidate, count[n - d]
            elif candidate == best[n]:
                count[n] += count[n - d]
    return best, count


def verify():
    if not __debug__:
        raise RuntimeError("Run without -O so all checks execute.")
    for d in range(1, 14):
        left, right = simplex(d + 1) ** d, simplex(d) ** (d + 1)
        assert (left > right if d <= 12 else left < right), d
    print("Per-dimension value increases through 13; first decline at 14.")

    for n in range(2, 20):
        assert balanced(n, 2) < simplex(n), n
    crossover = balanced(20, 2) / simplex(20)
    assert crossover == Fraction(5588869, 5505024) > 1
    print("First winning pair: dimensions 10 and 10; ratio", crossover)

    r12, r13 = simplex(13) / simplex(12), simplex(14) / simplex(13)
    assert r13**8 * r12**5 > simplex(13) > r13**9 * r12**4
    print("Residue cutoff certified: H(8) > 1 > H(9).")

    limit = 240
    best, count = partition_optima(limit)
    for n in range(1, limit + 1):
        assert formula(n) == best[n] and count[n] == 1, n
        if n >= 100:
            assert residue_product(n) == best[n], n
        if n >= 113:
            assert best[n] == simplex(13) * best[n - 13], n
    assert best[99] == simplex(12) ** 5 * simplex(13) ** 3
    assert best[112] == simplex(14) ** 8 > best[99] * simplex(13)
    print("Independent partition DP agrees in dimensions 1 through", limit)
    print("Recurrence holds from n=100; certified failure at n=99.")


if __name__ == "__main__":
    verify()
