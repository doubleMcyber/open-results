"""Two exact enumerations of the fifth Craig lattice's minimum shell."""

from collections import Counter
from itertools import combinations
from math import comb, isqrt


def quintic_histogram(p):
    """Count distinct five-point fibers of depressed quintics."""
    squares = {u * u % p for u in range(1, p)}
    nonsquare = next(a for a in range(1, p) if a not in squares)
    histogram = Counter()
    for a, a_weight in ((0, 1), (1, len(squares)), (nonsquare, len(squares))):
        high = [(x**5 + a * x**3) % p for x in range(p)]
        for b in range((p + 1) // 2):
            weight = a_weight * (1 if b == 0 else 2)
            base = [(v + b * x * x) % p for x, v in enumerate(high)]
            for c in range(p):
                fibers = [0] * p
                for x, v in enumerate(base):
                    fibers[(v + c * x) % p] += 1
                histogram[fibers.count(5)] += weight
    return histogram


def moment_orbits(p):
    """Lookup for scaling centered power sums with weights 2, 3, 4."""
    powers = [(u**2 % p, u**3 % p, u**4 % p) for u in range(1, p)]
    lookup = [[None] * p for _ in range(p)]
    stabilizers = []
    for a in range(p):
        for b in range(p):
            if lookup[a][b] is not None:
                continue
            fixed = [u4 for u2, u3, u4 in powers
                     if a * u2 % p == a and b * u3 % p == b]
            # Keep repeated fourth powers: each represents a distinct scalar.
            representatives = [min(c * u4 % p for u4 in fixed) for c in range(p)]
            offset = len(stabilizers)
            for c, rep in enumerate(representatives):
                stabilizers.append(sum(c * u4 % p == c for u4 in fixed)
                                   if rep == c else 0)
            for u2, u3, u4 in powers:
                lookup[a * u2 % p][b * u3 % p] = (
                    offset, pow(u4, -1, p), representatives
                )
    return lookup, stabilizers


def anchored_histogram(p):
    """Enumerate five-subsets containing 0 and 1 by centered moments."""
    lookup, stabilizers = moment_orbits(p)
    anchored = [0] * len(stabilizers)
    sq = [x**2 % p for x in range(p)]
    cube = [x**3 % p for x in range(p)]
    fourth = [x**4 % p for x in range(p)]
    inverse_five = pow(5, -1, p)
    means = [total * inverse_five % p for total in range(3 * p)]
    for a, b in combinations(range(2, p), 2):
        t1 = 1 + a + b
        t2 = 1 + sq[a] + sq[b]
        t3 = 1 + cube[a] + cube[b]
        t4 = 1 + fourth[a] + fourth[b]
        for c in range(b + 1, p):
            mean = means[t1 + c]
            s2 = t2 + sq[c]
            s3 = t3 + cube[c]
            m2 = (s2 - 5 * sq[mean]) % p
            m3 = (s3 - 3 * mean * s2 + 10 * cube[mean]) % p
            m4 = (t4 + fourth[c] - 4 * mean * s3
                  + 6 * sq[mean] * s2 - 15 * fourth[mean]) % p
            offset, scale, representatives = lookup[m2][m3]
            anchored[offset + representatives[m4 * scale % p]] += 1

    assert sum(anchored) == comb(p - 2, 3)
    histogram = Counter()
    for h, stabilizer in zip(anchored, stabilizers):
        if stabilizer:
            multiplicity, remainder = divmod(h * stabilizer, 20)
            assert remainder == 0
            histogram[multiplicity] += (p - 1) // stabilizer
        else:
            assert h == 0
    return histogram


def check(p):
    assert p > 5 and all(p % d for d in range(2, isqrt(p) + 1))
    histogram = quintic_histogram(p)
    assert histogram == anchored_histogram(p)
    assert sum(histogram.values()) == p**3
    centered = sum(n * h for n, h in histogram.items())
    assert centered * p == comb(p, 5)
    pairs = sum(n * (n - 1) * h for n, h in histogram.items())
    result = p * pairs
    if p < 20:
        direct = Counter(
            tuple(sum(x**j for x in subset) % p for j in (1, 2, 3, 4))
            for subset in combinations(range(p), 5)
        )
        assert result == sum(n * (n - 1) for n in direct.values())
    print(f"p={p}  centered subsets={centered}  centered ordered pairs={pairs}"
          f"  norm-10 vectors={result}", flush=True)
    return result


if __name__ == "__main__":
    for prime in (7, 11, 13, 17, 19):
        check(prime)
    result = check(523)
    assert result == 1_323_456_100_308
