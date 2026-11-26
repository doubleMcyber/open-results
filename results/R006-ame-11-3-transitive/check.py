"""Enumerate cyclic Lagrangians on 11 qutrits and count deficient five-site cuts."""
from collections import Counter
from itertools import combinations, product

N = 11
SITES = tuple(range(N))
ZERO = (0,) * N
ONES = (1,) * N
G = (2, 0, 1, 2, 1, 1)
H = (2, 2, 1, 2, 0, 1)


def multiply(left, right):
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return tuple(x % 3 for x in result)


def cyclic_product(left, right):
    result = [0] * N
    for i, x in enumerate(multiply(left, right)):
        result[i % N] += x
    return tuple(x % 3 for x in result)


def reciprocal(vector):
    return vector[:1] + vector[:0:-1]


def rotate(vector, steps):
    return vector[-steps:] + vector[:-steps] if steps else vector


def line_rows(x, z):
    return [rotate(x, i) + rotate(z, i) for i in range(5)]


def cyclic_spaces():
    # a and b generate the two five-dimensional minimal ideals.
    factor = (2, 1)
    assert multiply(factor, multiply(G, H)) == (2,) + (0,) * 10 + (1,)
    a = cyclic_product(factor, G)
    b = cyclic_product(factor, H)
    constants = [ONES + (s,) * N for s in range(3)] + [ZERO + ONES]
    for slope in product(range(3), repeat=5):
        t = slope + (0,) * 6
        rows = line_rows(a, cyclic_product(t, a))
        rows += line_rows(b, cyclic_product(reciprocal(t), b))
        for constant in constants:
            yield "line", rows + [constant]
    vertical = line_rows(ZERO, a) + line_rows(ZERO, b)
    for constant in constants:
        yield "line", vertical + [constant]
    for ideal in (a, b):
        rows = line_rows(ideal, ZERO) + line_rows(ZERO, ideal)
        for constant in constants:
            yield "plane", rows + [constant]


def echelon_basis(rows):
    basis = {}
    for row in rows:
        for i in range(len(row)):
            if row[i] == 0:
                continue
            if i not in basis:
                scale = row[i]  # Either nonzero scalar is its own inverse.
                basis[i] = [(x * scale) % 3 for x in row]
                break
            scale = row[i]
            row = [(x - scale * y) % 3 for x, y in zip(row, basis[i])]
    return basis


def space_key(rows):
    """Canonical reduced row echelon form, to check that spaces are distinct."""
    basis = echelon_basis(rows)
    for j in sorted(basis, reverse=True):
        for i in basis:
            if i < j and basis[i][j]:
                scale = basis[i][j]
                basis[i] = [(x - scale * y) % 3 for x, y in zip(basis[i], basis[j])]
    return tuple(tuple(basis[i]) for i in sorted(basis))


def cut_representatives(size):
    remaining = set(combinations(SITES, size))
    cuts = []
    while remaining:
        subset = min(remaining)
        orbit = {tuple(sorted((i + j) % N for i in subset)) for j in SITES}
        assert len(orbit) == N and orbit <= remaining
        remaining.difference_update(orbit)
        outside = [i for i in SITES if i not in subset]
        cuts.append(outside + [i + N for i in outside])
    return cuts


def deficient_count(rows, cuts):
    failures = 0
    for cols in cuts:
        rank = len(echelon_basis([[r[j] for j in cols] for r in rows]))
        failures += rank < N
    return N * failures


def verify_space(rows):
    assert len(rows) == len(echelon_basis(rows)) == N
    for i, u in enumerate(rows):
        for v in rows[:i]:
            assert sum(u[k]*v[k+N] - u[k+N]*v[k] for k in SITES) % 3 == 0


def small_graph_supports(first):
    """Enumerate graph labels of weight <= 5, modulo nonzero global scaling."""
    rows = [rotate(first, i) for i in SITES]
    supports = Counter()
    for weight in range(1, 6):
        for sites in combinations(SITES, weight):
            for tail in product((1, 2), repeat=weight - 1):
                # The first nonzero X coordinate can be normalized to 1.
                terms = list(zip(sites, (1,) + tail))
                support = set(sites)
                for j in SITES:
                    if sum(a * rows[i][j] for i, a in terms) % 3:
                        support.add(j)
                    if len(support) > 5:
                        break
                else:
                    supports[tuple(sorted(support))] += 1
    return supports


def main():
    cuts5 = cut_representatives(5)
    assert len(cuts5) == 42
    histogram = Counter()
    spaces = set()
    for kind, rows in cyclic_spaces():
        verify_space(rows)
        key = space_key(rows)
        shifted = [rotate(r[:N], 1) + rotate(r[N:], 1) for r in rows]
        assert key not in spaces and space_key(shifted) == key
        spaces.add(key)
        histogram[deficient_count(rows, cuts5), kind] += 1
    assert sum(histogram.values()) == len(spaces) == 984
    print("bad 5-cuts | line family | plane family")
    for bad in sorted({k for k, _ in histogram}):
        print(bad, histogram[bad, "line"], histogram[bad, "plane"], sep=" | ")

    # Explicit graph state attaining the minimum number of deficient cuts.
    first = (0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0)
    rows = [tuple(int(i == j) for j in SITES) + rotate(first, i) for i in SITES]
    verify_space(rows)
    print("graph witness bad 4-cuts:", deficient_count(rows, cut_representatives(4)))
    bad5 = deficient_count(rows, cuts5)
    print("graph witness bad 5-cuts:", bad5)
    supports = small_graph_supports(first)
    assert all(len(s) == 5 and n == 1 for s, n in supports.items())
    assert len(supports) == bad5 == min(bad for bad, _ in histogram)
    orbits = {min(tuple(sorted((i + j) % N for i in s)) for j in SITES)
              for s in supports}
    print("minimal supports up to cyclic translation:", sorted(orbits))


if __name__ == "__main__":
    main()
