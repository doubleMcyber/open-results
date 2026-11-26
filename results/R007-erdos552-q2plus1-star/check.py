"""Finite certificates for the C4 versus 26-leaf star Ramsey number (Python 3)."""
from collections import Counter
from itertools import combinations, product


def lower_bound():
    # First nonzero coordinate is 1. All arithmetic is over F_5.
    points = [p for p in product(range(5), repeat=3)
              if next((v for v in p if v), 0) == 1]
    neighbors = [{j for j, q in enumerate(points)
                  if i != j and sum(a*b for a, b in zip(p, q)) % 5 == 0}
                 for i, p in enumerate(points)]
    degrees = sorted(map(len, neighbors))
    assert degrees == [5]*6 + [6]*25
    assert max(len(a & b) for a, b in combinations(neighbors, 2)) == 1
    return len(points), degrees.count(5), degrees.count(6)


def quotients():
    # Vertex 0 is the root, 1..6 its neighbors in cyclic order.
    ring = range(1, 7)
    graph = [set() for _ in range(16)]
    graph[0] = set(ring)
    for i in ring:
        graph[i] = {0, i % 6 + 1, (i - 2) % 6 + 1}
    outside = list(range(7, 16))
    pairs = [pair for pair in combinations(ring, 2)
             if graph[pair[0]] & graph[pair[1]] == {0}]
    assert len(pairs) == len(outside)
    for x, (a, b) in zip(outside, pairs):
        graph[x] = {a, b}
        graph[a].add(x)
        graph[b].add(x)

    options = {}
    for x in outside:
        options[x] = []
        for rest in combinations([z for z in outside if z != x], 4):
            row = graph[x] | set(rest)
            if all(len(row & graph[i]) == 2 for i in ring):
                options[x].append(row)

    def extend(k):
        if k == len(outside):
            assert all(len(row) == 6 for row in graph)
            assert all(i not in row and all(i in graph[j] for j in row)
                       for i, row in enumerate(graph))
            assert all(len(a & b) == 2 for a, b in combinations(graph, 2))
            yield tuple(map(frozenset, graph))
            return
        x = outside[k]
        initial = graph[x]
        for row in options[x]:
            if all(((y in row) == (x in graph[y])) and len(row & graph[y]) == 2
                   for y in outside[:k]):
                graph[x] = row
                yield from extend(k + 1)
        graph[x] = initial

    yield from extend(0)


OBSTRUCTION = (
    (0, 2, 1, 6), (0, 2, 10, 3), (0, 3, 4, 5), (0, 1, 8, 4),
    (0, 4, 14, 5), (0, 1, 9, 6), (1, 6, 9, 8), (4, 5, 14, 8),
    (1, 2, 10, 9), (3, 4, 14, 10), (8, 9, 10, 14),
)


def verify_obstruction(graph):
    multiplicities = Counter()
    for cycle in OBSTRUCTION:
        assert len(set(cycle)) == 4
        for u, v in zip(cycle, cycle[1:] + cycle[:1]):
            assert v in graph[u]
            multiplicities[tuple(sorted((u, v)))] += 1
    assert len(OBSTRUCTION) % 2 == 1
    assert all(count % 2 == 0 for count in multiplicities.values())


def main():
    print("projective points, degree-5 count, degree-6 count:", lower_bound())
    completions = 0
    for graph in quotients():
        verify_obstruction(graph)
        # A square has two unordered pairs of opposite corners.
        diagonals = sum(len(a & b) * (len(a & b) - 1) // 2
                        for a, b in combinations(graph, 2))
        assert diagonals == 120
        print("distinct squares, obstruction size:", diagonals // 2, len(OBSTRUCTION))
        completions += 1
    assert completions == 1
    print("labeled completions:", completions)


if __name__ == "__main__":
    main()
