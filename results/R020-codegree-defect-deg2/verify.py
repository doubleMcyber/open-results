"""Necessary conditions for a nonzero codegree defect of maximum degree two."""

from collections import Counter
from itertools import combinations, product
from math import gcd


def partitions(budget, minimum=2):
    """Nondecreasing tuples of cycle half-lengths with sum at most budget."""
    yield ()
    for k in range(minimum, budget + 1):
        for tail in partitions(budget - k, k):
            yield (k,) + tail


def possible_cell_row(lengths, k):
    others = list(lengths)
    others.remove(k)
    isolates = 45 - 2 * sum(lengths)
    for d in range(k):
        if k * d % 2 or (k >= 5 and d in (0, k - 1)):
            continue
        target = 11 * k * (k - 1) + k * d
        # The paired cell is either completely joined or completely disjoint.
        own = k * d * (k - d)
        states = {(d, own), (d + k, own)}
        for h in others + others:
            g = gcd(k, h)
            choices = []
            for t in range(g + 1):
                forward, reverse = t * h // g, t * k // g
                choices.append((forward, h * reverse * (k - reverse)))
            states = {
                (degree + a, dist + b)
                for degree, dist in states
                for a, b in choices
                if degree + a <= 22 and dist + b <= target
            }
        if any((22 - s, target) in states for s in range(isolates + 1)):
            return True
    return False


def eligible_positions(lengths, k, step):
    # A size-h cell has period dividing gcd(k,h) in its k row indices.
    count = 2 * sum(h for h in lengths if step % gcd(k, h))
    return count - k  # the size-k paired cell is constant


def possible_steps(lengths):
    for k in set(lengths):
        for step in range(1, k):
            if eligible_positions(lengths, k, step) < 22:
                return False
    return True


def has_possible_isolate_degrees(lengths):
    """The sum of degrees in the graph induced by singleton cells must be even."""
    count = 45 - 2 * sum(lengths)
    cell_sums = {0}
    for k in lengths + lengths:
        cell_sums |= {s + k for s in cell_sums}
    parities = {d % 2 for d in range(count) if 22 - d in cell_sums}
    return bool(parities) and (0 in parities or count % 2 == 0)


def census():
    stages = Counter()
    candidates = []
    for lengths in partitions(22):
        if not lengths:
            continue
        stages["tuples"] += 1
        m, c = 2 * sum(lengths), len(lengths)
        if m * (m - 1) < 45 * (m - 2 * c):
            continue
        stages["trace"] += 1
        if sum(k % 2 == 0 for k in lengths) % 2:
            continue
        stages["eigenvalue"] += 1
        if not all(possible_cell_row(lengths, k) for k in set(lengths)):
            continue
        stages["rows"] += 1
        if not possible_steps(lengths):
            continue
        stages["distances"] += 1
        if not has_possible_isolate_degrees(lengths):
            continue
        stages["handshake"] += 1
        candidates.append(lengths)
    return stages, candidates


def product_matrix(a, b):
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) for col in zip(*b)) for row in a)


def small_block_checks():
    # Internal adjacency blocks of the four 8-cycles in the mixed case.
    edges = list(combinations(range(4), 2))
    blocks = []
    for values in product((0, 1), repeat=6):
        a = [[0] * 4 for _ in range(4)]
        for (i, j), v in zip(edges, values):
            a[i][j] = a[j][i] = v
        if len(set(map(sum, a))) == 1:
            blocks.append(tuple(map(tuple, a)))
    t = tuple(tuple(int(i == j) - int((i + 1) % 4 == j) for j in range(4)) for i in range(4))
    pairs = [
        (l, r) for l in blocks for r in blocks if product_matrix(l, t) == product_matrix(t, r)
    ]
    assert len(blocks) == 8 and len(pairs) == 4
    for l, r in pairs:
        assert l == r
        assert all(l[i][j] == l[0][(j - i) % 4] for i in range(4) for j in range(4))
        assert l[0][1] == l[0][3]

    # Off-diagonal heavy-entry supports between two matched pairs, modulo 2.
    z = ((0, 1), (1, 1))
    masks = []
    for values in product((0, 1), repeat=4):
        h = (values[:2], values[2:])
        left, right = product_matrix(z, h), product_matrix(h, z)
        if all((left[i][j] + right[i][j] + h[i][j]) % 2 == 0 for i in range(2) for j in range(2)):
            masks.append(sum(v << i for i, v in enumerate(values)))
    nonempty = [mask for mask in masks if mask]
    assert sorted(m.bit_count() for m in nonempty) == [2, 3, 3]
    assert all(a & b for a in nonempty for b in nonempty)
    print(
        "Regular four-vertex blocks, commuting pairs, parity masks:",
        len(blocks),
        len(pairs),
        masks,
    )


if __name__ == "__main__":
    stats, candidates = census()
    print("Counts after successive necessary conditions:", dict(stats))
    print("Surviving half-length tuples:", candidates)
    expected = {(2, 2, 4, 4, 4, 4), (2,) * 8, (2,) * 10}
    assert set(candidates) == expected
    small_block_checks()
