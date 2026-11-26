"""Exact coefficient checks for the sparse-bias equal-row calculation."""

from itertools import combinations, combinations_with_replacement
from math import comb, factorial


def block_sizes(n):
    """Visit every labelled set partition once in least-element block order."""
    sizes = []

    def visit(placed):
        if placed == n:
            yield tuple(sizes)
            return
        for block in range(len(sizes)):
            sizes[block] += 1
            yield from visit(placed + 1)
            sizes[block] -= 1
        sizes.append(1)
        yield from visit(placed + 1)
        sizes.pop()

    yield from visit(0)


def formula(n, base):
    """Use weights 1 and base for plus and minus. No division is needed."""
    entries = n * (n + 1) // 2
    no_duplicate = 0
    for sizes in block_sizes(n):
        term = 1
        for i, size in enumerate(sizes):
            term *= (-1) ** (size - 1) * factorial(size - 1)
            term *= 1 + base ** (size * (size + 1) // 2)
            for other in sizes[:i]:
                term *= 1 + base ** (size * other)
        no_duplicate += term
    at_most_one = 0
    for j in range(n + 1):
        free = (n - j) * (n - j + 1) // 2
        at_most_one += (-1) ** j * (1 - j) * comb(n, j) * (1 + base) ** free
    cherries = 0
    if n >= 3:
        cherries = comb(n, 2) * (n - 2) * base**2 * (1 + base) ** (entries - 2*n + 1)
    return no_duplicate, at_most_one - no_duplicate, cherries


def enumerate_histograms(n):
    slots = list(combinations_with_replacement(range(n), 2))
    histograms = [[0] * (len(slots) + 1) for _ in range(3)]
    for mask in range(1 << len(slots)):
        rows = [0] * n
        for index, (i, j) in enumerate(slots):
            if mask & (1 << index):
                rows[i] |= 1 << j
                rows[j] |= 1 << i
        distinct = len(set(rows)) == n
        cherries = 0
        for i, j in combinations(range(n), 2):
            if rows[i] == rows[j] and rows[i].bit_count() == 1:
                if not rows[i] & ((1 << i) | (1 << j)):
                    cherries += 1
        weight = mask.bit_count()
        histograms[0][weight] += distinct
        histograms[1][weight] += not distinct and rows.count(0) <= 1
        histograms[2][weight] += cherries
    return histograms


def check(n):
    entries = n * (n + 1) // 2
    # Every coefficient is at most the number of matrices times the
    # maximum number of pairs per matrix. Thus base digits do not carry.
    base = (1 + comb(n, 2)) * (1 << entries) + 1
    counts = enumerate_histograms(n)
    for calculated, histogram in zip(formula(n, base), counts):
        for expected in histogram:
            calculated, digit = divmod(calculated, base)
            if digit != expected:
                raise ValueError((n, digit, expected))
        if calculated:
            raise ValueError("unexpected higher coefficient")
    print(f"n={n}: {1 << entries} matrices, excess histogram {counts[1]}")


if __name__ == "__main__":
    for order in range(1, 6):
        check(order)
