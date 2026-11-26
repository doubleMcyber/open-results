"""Exact checks for the relative cyclic length of a cyclic wreath product."""

from collections import deque
from itertools import product
from math import comb


def predicted_length(p, a, k):
    n = p**k
    return n + (a - 1) * (n - n // p)


def check_ring(p, a, k):
    """Multiply by t-1 in the coordinate basis until the predicted boundary."""
    n = p**k
    modulus = p**a
    length = predicted_length(p, a, k)
    vector = [1] + [0] * (n - 1)
    coefficient = pow(-comb(n, n // p), a - 1, modulus)
    for exponent in range(length):
        if exponent == n - 1:
            last_expected = [(coefficient * entry) % modulus for entry in vector]
        if exponent == length - 1:
            assert any(vector) and vector == last_expected, (p, a, k, vector)
        vector = [(vector[i - 1] - vector[i]) % modulus for i in range(n)]
    assert not any(vector), (p, a, k, vector)


def shortest_chain(p, a, k):
    """Breadth-first search using just the semidirect-product multiplication."""
    n = p**k
    modulus = p**a
    elements = list(product(product(range(modulus), repeat=n), range(n)))
    number = {g: i for i, g in enumerate(elements)}
    table = []
    for v, r in elements:
        row = []
        for w, s in elements:
            summed = tuple((v[i] + w[(i - r) % n]) % modulus for i in range(n))
            row.append(number[summed, (r + s) % n])
        table.append(row)

    complement = frozenset(number[(0,) * n, r] for r in range(n))
    queue = deque([(complement, 0)])
    visited = {complement}
    while queue:
        subgroup, distance = queue.popleft()
        if len(subgroup) == len(elements):
            return distance
        # Every generator in a left coset yields the same extension.
        remaining = set(range(len(elements))).difference(subgroup)
        while remaining:
            g = next(iter(remaining))
            coset = {table[g][h] for h in subgroup}
            remaining.difference_update(coset)
            if coset != {table[h][g] for h in subgroup}:
                continue
            # g normalizes the subgroup, so adjoining g gives a cyclic quotient.
            extension = set(subgroup)
            power = g
            while power not in subgroup:
                extension.update(table[power][h] for h in subgroup)
                power = table[power][g]
            next_subgroup = frozenset(extension)
            if next_subgroup not in visited:
                visited.add(next_subgroup)
                queue.append((next_subgroup, distance + 1))
    raise AssertionError("No chain from the complement to the whole group")


def main():
    if not __debug__:
        raise RuntimeError("Run without -O so the checks execute")
    count = 0
    for p in (2, 3, 5, 7):
        for k in range(1, 5):
            if p**k <= 128:
                for a in range(1, 6):
                    check_ring(p, a, k)
                    count += 1
    print(f"Coordinate-ring boundary and last nonzero vector verified: {count} cases")

    cases = [(2, 1, 1), (2, 2, 1), (2, 3, 1), (2, 1, 2), (3, 1, 1), (2, 2, 2)]
    for p, a, k in cases:
        length = shortest_chain(p, a, k)
        assert length == predicted_length(p, a, k), (p, a, k, length)
        print(f"Group search (p,a,k)=({p},{a},{k}): length {length}")


if __name__ == "__main__":
    main()
