"""Classify prime supports covering a consecutive interval, with free singletons."""

from math import isqrt
from itertools import combinations


def primes_below(limit):
    return [p for p in range(2, limit)
            if all(p % d for d in range(2, isqrt(p) + 1))]


def kernels(length, budget):
    """Return inclusion-minimal sufficient sets, with one residue per prime."""
    primes = primes_below(length)
    classes = [[sum(1 << j for j in range(r, length, p)) for r in range(p)]
               for p in primes]
    answers = set()

    def visit(i, uncovered, used):
        slots = budget - len(used)
        count = uncovered.bit_count()
        if count <= slots:
            answers.add(used)
            return
        if slots == 0 or i == len(primes):
            return
        # A prime can save at most its largest intersection minus one,
        # compared with using its slot for one arbitrary position.
        savings = [max((uncovered & m).bit_count() for m in masks) - 1
                   for masks in classes[i:]]
        if slots + sum(sorted(savings, reverse=True)[:slots]) < count:
            return
        for mask in classes[i]:
            hit = uncovered & mask
            if hit.bit_count() >= 2:
                visit(i + 1, uncovered ^ hit, used + (primes[i],))
        visit(i + 1, uncovered, used)

    visit(0, (1 << length) - 1, ())
    return sorted(s for s in answers
                  if not any(set(t) < set(s) for t in answers))


if __name__ == "__main__":
    # Candidate values specify just the two adjacent lengths to test.
    lengths = [1, 3, 5, 9, 13, 21, 25, 33, 39, 45, 57, 65, 73, 89, 99, 105]
    prime_list = primes_below(44)
    initial_segments = [0, 1, 1, 2, 3, 4, 5, 6, 6, 8, 9, 9, 11]
    expected = [[tuple(prime_list[:n])] for n in initial_segments]
    expected.append([tuple(prime_list[:9] + [31])])
    expected.append([tuple(prime_list[:12])])
    expected.append([tuple(prime_list[:10]) + pair
                     for pair in combinations([31, 37, 43], 2)])
    for k, length in enumerate(lengths, 1):
        sufficient = kernels(length, k)
        longer = kernels(length + 1, k)
        print(f"k={k} L={length} minimal={sufficient} at L+1={longer}", flush=True)
        if sufficient != expected[k - 1] or longer:
            raise ValueError(f"Classification mismatch for k={k}")
