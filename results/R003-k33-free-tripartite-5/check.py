"""Check the 49-edge certificate using only Python's standard library."""

from collections import Counter
from itertools import combinations
from math import comb

# Rows index the first part, columns the second, in the order AB, BC, CA.
BLOCKS = (
    ("10101", "11011", "01110", "11100", "00111"),
    ("10101", "10110", "11010", "01111", "10011"),
    ("10101", "11100", "01111", "11011", "10110"),
)


def main():
    n = 5
    graph = [set() for _ in range(3 * n)]
    counts = []
    for part, rows in enumerate(BLOCKS):
        assert len(rows) == n
        count = 0
        for i, row in enumerate(rows):
            assert len(row) == n and set(row) <= {"0", "1"}
            for j, bit in enumerate(row):
                if bit == "1":
                    u = part * n + i
                    v = ((part + 1) % 3) * n + j
                    graph[u].add(v)
                    graph[v].add(u)
                    count += 1
        counts.append(count)
    edges = sum(map(len, graph)) // 2
    assert counts == [16, 16, 17] and edges == sum(counts) == 49

    # Test every possible first side of a K_{3,3}, across all 15 vertices.
    histogram = Counter(
        len(graph[i] & graph[j] & graph[k])
        for i, j, k in combinations(range(3 * n), 3)
    )
    assert sum(histogram.values()) == comb(3 * n, 3)
    assert max(histogram) == 2

    assert all(comb(d, 3) >= 3 * d - 8 for d in range(n + 1))
    degree_cap = (2 * comb(n, 3) + 8 * (2 * n)) // 3
    upper = (3 * degree_cap) // 2
    assert upper == edges
    print(f"Block edge counts {counts}, witness edges {edges}, upper bound {upper}")
    print(f"Triple common-neighbor histogram {dict(sorted(histogram.items()))}")


if __name__ == "__main__":
    main()
