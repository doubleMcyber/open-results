"""Exact probability of a maximum leave for triangle removal on K_(2v)."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb, prod


def labeled_systems(v):
    """Enumerate Steiner triple systems with the link of vertex zero fixed."""
    triples = list(combinations(range(v), 3))
    edges = list(combinations(range(v), 2))
    edge_bits = {edge: 1 << i for i, edge in enumerate(edges)}
    masks = {t: sum(edge_bits[e] for e in combinations(t, 2)) for t in triples}
    by_edge = [[t for t in triples if masks[t] & edge_bits[e]] for e in edges]
    link = tuple((0, i, i + 1) for i in range(1, v, 2))
    solutions = []

    def cover(free, chosen):
        if not free:
            solutions.append(frozenset(chosen))
            return
        first = (free & -free).bit_length() - 1
        for t in by_edge[first]:
            if free & masks[t] == masks[t]:
                cover(free ^ masks[t], chosen + (t,))

    cover(((1 << len(edges)) - 1) ^ sum(masks[t] for t in link), link)
    reference = solutions[0]
    pairs = [t[1:] for t in link]
    orbit = set()
    for order in permutations(pairs):
        for flips in product((False, True), repeat=len(order)):
            image = [0]
            for pair, flip in zip(order, flips):
                image.extend(reversed(pair) if flip else pair)
            orbit.add(frozenset(tuple(sorted(image[x] for x in t)) for t in reference))
    assert orbit == set(solutions)
    matchings = prod(range(1, v - 1, 2))
    return [sorted(system) for system in solutions], matchings


def one_side(v, blocks):
    """Compute the one-list recurrence on actual edge sets, without grouping."""
    edges = list(combinations(range(v), 2))
    bit = {e: 1 << i for i, e in enumerate(edges)}

    def edge_mask(triple):
        return sum(bit[e] for e in combinations(triple, 2))

    triangles = [edge_mask(t) for t in combinations(range(v), 3)]
    block_edges = [edge_mask(t) for t in blocks]
    living_edges = [0]
    probabilities = [Fraction(1)]
    for subset in range(1, 1 << len(blocks)):
        low = subset & -subset
        live = living_edges[subset ^ low] | block_edges[low.bit_length() - 1]
        living_edges.append(live)
        internal = sum(live & mask == mask for mask in triangles)
        numerator = sum(probabilities[subset ^ (1 << j)] for j in range(len(blocks))
                        if subset >> j & 1)
        probabilities.append(numerator / (internal + v * live.bit_count()))
    return probabilities[-1]


def side_types(v, blocks):
    """Group live-block subsets by triangle count and one-deletion successors."""
    b = len(blocks)
    owner = {e: i for i, block in enumerate(blocks) for e in combinations(block, 2)}
    requirements = []
    for triple in combinations(range(v), 3):
        support = {owner[e] for e in combinations(triple, 2)}
        requirements.append(sum(1 << i for i in support))
    types = []
    lookup = {}
    subset_type = []
    for live in range(1 << b):
        triangles = sum(live & req == req for req in requirements)
        children = Counter(subset_type[live ^ (1 << i)] for i in range(b) if live >> i & 1)
        key = (live.bit_count(), triangles, tuple(sorted(children.items())))
        if key not in lookup:
            lookup[key] = len(types)
            types.append(key)
        subset_type.append(lookup[key])
    return types, subset_type[-1]


def fixed_system_pair(v, types, full):
    """Both sides have the same design up to relabeling."""
    probabilities = {}
    for i, (size_i, tri_i, kids_i) in enumerate(types):
        for j in range(i + 1):
            size_j, tri_j, kids_j = types[j]
            if size_i + size_j == 0:
                probabilities[i, j] = Fraction(1)
                continue
            total = tri_i + tri_j + 3 * v * (size_i + size_j)
            weight = sum(n * probabilities[max(k, j), min(k, j)] for k, n in kids_i)
            weight += sum(n * probabilities[i, k] for k, n in kids_j)
            probabilities[i, j] = weight / total
    return probabilities[full, full]


def maximum_leave(v):
    systems, matchings = labeled_systems(v)
    system_count = len(systems) * matchings
    types, full = side_types(v, systems[0])
    p = fixed_system_pair(v, types, full)
    one_list = matchings * sum(one_side(v, blocks) for blocks in systems)
    assert one_list**2 == system_count**2 * p
    partitions = comb(2 * v, v) // 2
    return len(systems), system_count, len(types), one_list, partitions * system_count**2 * p


if __name__ == "__main__":
    for v in (3, 7, 9):
        link_count, systems, types, one_list, probability = maximum_leave(v)
        if v == 3:
            assert probability == Fraction(1, 10)
        print(f"K_{2*v}: fixed link {link_count}, labeled systems {systems}, side types {types}")
        print(f"F({v},{v}) = {one_list}")
        print(f"P({v*v} terminal edges) = {probability}")
