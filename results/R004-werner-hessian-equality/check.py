"""Exact rank-two Hessian at the aligned Werner zero. Standard library only."""

from collections import Counter, defaultdict
from itertools import combinations_with_replacement, product
from math import comb, isqrt
import sys


def add_entry(matrix, i, j, value):
    matrix[min(i, j), max(i, j)] += value


def partial_trace_unit(row, col, traced):
    """Tr_S |row><col| is either zero or a matrix unit on surviving sites."""
    if any(row[k] != col[k] for k in traced):
        return None
    return (tuple(x for k, x in enumerate(row) if k not in traced),
            tuple(x for k, x in enumerate(col) if k not in traced))


def build_gram(d, n):
    words = list(product(range(d), repeat=n))
    support = [(a,) + (0,) * (n - 1) for a in range(2)]
    exterior = [x for x in words if x not in support]
    tangent = [(i, j) for i in words for j in words if i in support or j in support]
    position = {unit: i for i, unit in enumerate(tangent)}
    gram = Counter()
    normal_diagonal = Counter()

    # Each subset contributes 2^n (-1/2)^|S| times an integer Gram matrix.
    for mask in range(1 << n):
        traced = {k for k in range(n) if mask & (1 << k)}
        weight = (-1) ** len(traced) * 2 ** (n - len(traced))
        buckets = defaultdict(list)
        for i, (row, col) in enumerate(tangent):
            unit = partial_trace_unit(row, col, traced)
            if unit is not None:
                buckets[unit].append(i)
        for bucket in buckets.values():
            for i, j in combinations_with_replacement(bucket, 2):
                add_entry(gram, i, j, weight)

        # Pair the partial traces of X0 with those of each exterior diagonal unit.
        # An off-diagonal unit either traces to zero or stays off-diagonal.
        x0_trace = Counter(partial_trace_unit(a, a, traced) for a in support)
        for x in exterior:
            normal_diagonal[x] += weight * x0_trace[partial_trace_unit(x, x, traced)]

    real, imaginary = gram.copy(), gram.copy()
    # The chart contributes 2 Re <L^tensor n X0, CB>. Multiplication
    # of two imaginary units reverses its sign. Mixed real/imag terms vanish.
    for x in exterior:
        for a in support:
            i, j = position[x, a], position[a, x]
            add_entry(real, i, j, normal_diagonal[x])
            add_entry(imaginary, i, j, -normal_diagonal[x])
    return position, real, imaginary


def exact_spectrum(size, matrix):
    """Discover the blocks from nonzero entries and solve each characteristic polynomial."""
    neighbors = defaultdict(list)
    for (i, j), value in matrix.items():
        if i != j and value:
            neighbors[i].append(j)
            neighbors[j].append(i)
    assert all(len(js) == 1 for js in neighbors.values())
    eigenvalues = Counter()
    for i in range(size):
        if not neighbors[i]:
            eigenvalues[matrix[i, i]] += 1
            continue
        j = neighbors[i][0]
        if i > j:
            continue
        a, b, c = matrix[i, i], matrix[i, j], matrix[j, j]
        delta = (a - c) ** 2 + 4 * b * b
        root = isqrt(delta)
        assert root * root == delta
        for signed_root in (-root, root):
            numerator = a + c + signed_root
            assert numerator % 2 == 0
            eigenvalues[numerator // 2] += 1
    assert sum(eigenvalues.values()) == size
    return eigenvalues


def predicted_spectrum(d, n):
    # Eigenvalues here are in units of 2h for the Hessian.
    result = Counter({0: 2 + 4 * (d - 2), 1: 6, 2: 4 * (d - 2)})
    for w in range(1, n):
        b = 2 ** w
        count = comb(n - 1, w) * (d - 1) ** w
        for eig, mult in [(0, 4), (b, 12), (b - 1, 4 * (d - 2)), (b + 1, 4 * (d - 2))]:
            result[eig] += count * mult
    return result


def path_value(n, a, other, x, t, sign, use_imaginary):
    """Evaluate 2^n f on an actual rank-two path, without its Hessian."""
    # X(t) = |other><other| + (e_a + z e_x)(e_a^T + sign*z e_x^T).
    # z=t or i*t. Store the real and imaginary parts as separate integers.
    re, im = (0, t) if use_imaginary else (t, 0)
    entries = [(other, other, 1, 0), (a, a, 1, 0),
               (x, a, re, im), (a, x, sign * re, sign * im),
               (x, x, sign * (re * re - im * im), 0)]
    total = 0
    for mask in range(1 << n):
        traced = {k for k in range(n) if mask & (1 << k)}
        real_trace, imag_trace = Counter(), Counter()
        for row, col, real_part, imag_part in entries:
            unit = partial_trace_unit(row, col, traced)
            if unit is not None:
                real_trace[unit] += real_part
                imag_trace[unit] += imag_part
        norm = sum(v * v for trace in (real_trace, imag_trace) for v in trace.values())
        total += (-1) ** len(traced) * 2 ** (n - len(traced)) * norm
    return total


def check_path_curvatures(n, position, real, imaginary):
    a, other = (0,) * n, (1,) + (0,) * (n - 1)
    for w in range(n):
        x = (2,) + (1,) * w + (0,) * (n - 1 - w)
        i, j = sorted((position[x, a], position[a, x]))
        for use_imaginary, matrix in ((False, real), (True, imaginary)):
            for sign in (-1, 1):
                values = [path_value(n, a, other, x, t, sign, use_imaginary)
                          for t in (-2, -1, 0, 1, 2)]
                p, q, origin, r, s = values
                # Five exact values extract 24 times the quadratic coefficient.
                numerator = 16 * (q + r - 2 * origin) - (p + s - 2 * origin)
                predicted = matrix[i, i] + matrix[j, j] + 2 * sign * matrix[i, j]
                assert numerator == 24 * predicted


def check(d, n):
    position, real, imaginary = build_gram(d, n)
    size = len(position)
    check_path_curvatures(n, position, real, imaginary)
    computed = exact_spectrum(size, real) + exact_spectrum(size, imaginary)
    # The assembled matrices are 2^n Q, twice Q/h, where Q is half the Hessian.
    assert all(eig % 2 == 0 for eig in computed)
    normalized = Counter({eig // 2: count for eig, count in computed.items()})
    assert normalized == predicted_spectrum(d, n)
    assert sum(normalized.values()) == 8 * d ** n - 8
    assert normalized[0] == 4 * d + 4 * d ** (n - 1) - 10
    assert min(e for e in normalized if e) == 1
    print(f"d={d} n={n} eigenvalue in units of 2h -> multiplicity {dict(sorted(normalized.items()))}")


if __name__ == "__main__":
    if not __debug__:
        sys.exit("Run without -O so that all checks execute.")
    for dimension, copies in [(3, 1), (3, 2), (3, 3), (3, 4), (4, 4)]:
        check(dimension, copies)
