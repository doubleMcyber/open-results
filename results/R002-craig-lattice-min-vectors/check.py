"""Exact kissing count for the fourth Craig lattice at p = 523."""

from collections import Counter
from itertools import combinations
from math import comb, isqrt


def centered_histogram(p):
    """Group four-subsets of F_p with sum zero by power sums 2 and 3."""
    counts = [0] * (p * p)
    sq = [x**2 % p for x in range(p)]
    cube = [x**3 % p for x in range(p)]
    for a, b in combinations(range(p), 2):
        pair_sq = sq[a] + sq[b]
        pair_cube = cube[a] + cube[b]
        for total in (p, 2 * p, 3 * p):
            cd = total - a - b
            # d = cd - c, with b < c < d < p.
            for c in range(max(b + 1, cd - p + 1), (cd - 1) // 2 + 1):
                d = cd - c
                s2 = (pair_sq + sq[c] + sq[d]) % p
                s3 = (pair_cube + cube[c] + cube[d]) % p
                counts[s2 * p + s3] += 1
    return Counter(counts)


def quartic_histogram(p):
    """Count split quartics x^4 + A*x^2 + B*x + C by (A, B)."""
    histogram = Counter()
    seen = bytearray(p * p)
    powers = [(u**2 % p, u**3 % p) for u in range(1, p)]
    fourth = [x**4 % p for x in range(p)]
    for a in range(p):
        base = [(v + a * x * x) % p for x, v in enumerate(fourth)]
        for b in range(p):
            if seen[a * p + b]:
                continue
            orbit = {(a * u2 % p) * p + b * u3 % p for u2, u3 in powers}
            for index in orbit:
                seen[index] = 1
            roots = [0] * p
            for x, v in enumerate(base):
                roots[(v + b * x) % p] += 1
            histogram[roots.count(4)] += len(orbit)
    return histogram


def all_subsets_count(p):
    """Tiny-prime reference count with no centering or polynomial orbit."""
    fibers = Counter(
        tuple(sum(x**j for x in subset) % p for j in (1, 2, 3))
        for subset in combinations(range(p), 4)
    )
    return sum(n * (n - 1) for n in fibers.values())


def check(p):
    assert p > 3 and all(p % d for d in range(2, isqrt(p) + 1))
    histogram = centered_histogram(p)
    assert histogram == quartic_histogram(p)
    assert sum(histogram.values()) == p**2
    centered = sum(n * h for n, h in histogram.items())
    assert centered * p == comb(p, 4)
    pairs = sum(n * (n - 1) * h for n, h in histogram.items())
    result = p * pairs
    if p < 20:
        assert result == all_subsets_count(p)
    print(f"p={p}  centered subsets={centered}  centered ordered pairs={pairs}"
          f"  norm-8 vectors={result}")
    return result


if __name__ == "__main__":
    for prime in (5, 7, 11, 13, 17, 19):
        check(prime)
    result = check(523)
    assert result == 65_121_213_204
