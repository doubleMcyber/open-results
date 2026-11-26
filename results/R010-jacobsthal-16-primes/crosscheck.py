"""Separate checks of the 16-prime classification, using offset differences."""

from itertools import combinations
from math import gcd, prod


def can_cover(length, slots, forbidden):
    # A group of size >= 2 has a prime label dividing a positive difference.
    # Trial division here is intentionally independent of check.py.
    primes = [d for d in range(2, length) if d not in forbidden
              and all(d % i for i in range(2, d))]
    groups = {p: [frozenset(range(a, length, p)) for a in range(p)]
              for p in primes}

    def possible(left, available, slots):
        if len(left) <= slots:
            return True
        if not slots:
            return False
        # Match a pivot point to one exclusive prime or give it a singleton.
        # First handle any label forced by the total capacity of the others.
        candidates = []
        for p in available:
            hits = [g & left for g in groups[p]]
            multi = [g for g in hits if len(g) > 1]
            if multi:
                candidates.append((max(map(len, multi)), p, multi))
        candidates.sort(reverse=True)
        caps = [size for size, _, _ in candidates] + [1] * slots
        if sum(caps[:slots]) < len(left):
            return False
        if candidates and sum(caps[1:slots + 1]) < len(left):
            _, p, options = candidates[0]
            others = available - {p}
            return any(possible(left - hit, others, slots - 1)
                       for hit in options if len(hit) + sum(caps[1:slots]) >= len(left))

        pivot = min(left)
        if possible(left - {pivot}, available, slots - 1):
            return True
        return any(possible(left - hit, available - {p}, slots - 1)
                   for _, p, options in candidates for hit in options if pivot in hit)

    return possible(frozenset(range(length)), frozenset(primes), slots)


def check_impossible(length, slots, forbidden):
    if can_cover(length, slots, forbidden):
        raise ValueError((length, slots, forbidden))
    print(f"Excluded L={length} slots={slots} forbidden={sorted(forbidden)}", flush=True)


if __name__ == "__main__":
    core = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    witnesses = [
        ((31, 37), 4783380817184, [27, 47, 65, 99]),
        ((31, 43), 74651409074, [39, 47, 65, 75]),
        ((37, 43), 2095238757854, [39, 47, 53, 75]),
    ]
    for pair, start, expected in witnesses:
        modulus = prod(core + pair)
        survivors = [i for i in range(105) if gcd(start + i, modulus) == 1]
        if survivors != expected:
            raise ValueError((pair, survivors))
        print(f"Pair {pair} modulus={modulus} survivor offsets={survivors}", flush=True)

    check_impossible(105, 16, {2})
    # Removing the even numbers leaves a progression of step two.
    # Scaling by its inverse modulo every remaining prime gives consecutive offsets.
    check_impossible(53, 15, {2})
    check_impossible(52, 14, {2})
    for p in core[1:]:
        check_impossible(52, 15, {2, p})
    for pair in combinations([31, 37, 43], 2):
        check_impossible(52, 15, {2, *pair})
    # Permit exactly one witness pair and the forced odd primes as multi-hit
    # labels. Four fresh singleton primes may still fill the uncovered sites.
    for pair, _, _ in witnesses:
        forbidden = set(range(2, 52)) - set(core[1:]) - set(pair)
        if not can_cover(52, 15, forbidden):
            raise ValueError(f"Missed a feasible pair: {pair}")
        print(f"Confirmed a reduced cover for {pair}", flush=True)
