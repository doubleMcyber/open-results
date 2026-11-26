"""Reproduce the jet determinants for two five-point orbits in the plane."""
import argparse
import os
from math import comb, isqrt

for key in ("OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
            "OMP_NUM_THREADS", "MKL_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[key] = "1"

import numpy as np

P = 1009
PANEL = 32
CASES = {1: 3, 6: 19, 12: 38, 55: 174}


def determinant(matrix):
    """Modular PLU with row pivoting. The input is overwritten."""
    n, size = matrix.shape
    assert n == size
    value = 1
    for start in range(0, n, PANEL):
        end = min(start + PANEL, n)
        for j in range(start, end):
            pivots = np.flatnonzero(matrix[j:, j])
            if not len(pivots):
                return 0
            row = j + pivots[0]
            if row != j:
                matrix[[j, row]] = matrix[[row, j]]
                value = -value
            pivot = int(matrix[j, j])
            value = (value * pivot) % P
            factors = matrix[j+1:, j]
            factors[:] = (factors * pow(pivot, -1, P)) % P
            sub = matrix[j+1:, j+1:end]
            sub[:] = (sub - factors[:, None] * matrix[j, j+1:end]) % P

        # Apply the panel eliminations to the remaining columns.
        top = matrix[start:end, end:]
        for i in range(1, end-start):
            top[i] = (top[i] - matrix[start+i, start:start+i] @ top[:i]) % P
        tail = matrix[end:, end:]
        tail[:] = (tail - matrix[end:, start:end] @ top) % P
    return value


def jet_matrix(m, d, residue):
    exponents = [(i, j) for i in range(d+1) for j in range(d+1-i)
                 if (i+2*j) % 5 == residue]
    jets = [(a, s-a) for s in range(m) for a in range(s+1)]
    assert len(exponents) == 2 * len(jets)
    ii, jj = np.array(exponents).T
    choose = np.array([[comb(i, a) % P for a in range(m)] for i in range(d+1)])
    weights = np.array([pow(2, i, P) * pow(7, j, P) % P for i, j in exponents])
    matrix = np.empty((len(exponents), len(exponents)), dtype=np.float64)
    for row, (a, b) in enumerate(jets):
        coeffs = choose[ii, a] * choose[jj, b] % P
        matrix[row] = coeffs
        matrix[row + len(jets)] = coeffs * weights % P
    return matrix


def check_algorithm():
    # Known determinant, forced row swaps straddling a panel, then rank loss.
    n = PANEL + 3
    lower = np.eye(n, dtype=np.int64)
    upper = np.zeros((n, n), dtype=np.int64)
    expected = 1
    for i in range(n):
        for j in range(i):
            if j > 0:
                lower[i, j] = (i*i + 11*j + 1) % P
            upper[j, i] = (3*i + j*j + 4) % P
        upper[i, i] = i + 2
        expected = expected * (i + 2) % P
    original = (lower @ upper) % P
    original[[0, -1]] = original[[-1, 0]]
    assert determinant(original.astype(np.float64)) == -expected % P
    original[0] = original[1]
    assert determinant(original.astype(np.float64)) == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=int, choices=CASES)
    parser.add_argument("--residue", type=int, choices=range(5))
    args = parser.parse_args()
    assert all(P % k for k in range(2, isqrt(P)+1))
    balanced = {m: d for m in range(1, 56) for d in range(175)
                if comb(d+2, 2) == 10*comb(m+1, 2)}
    assert balanced == CASES
    check_algorithm()
    for m in ([args.case] if args.case else CASES):
        d = CASES[m]
        for r in ([args.residue] if args.residue is not None else range(5)):
            det = determinant(jet_matrix(m, d, r))
            print(f"m={m} d={d} r={r} det={det}", flush=True)
            if det == 0:
                raise ArithmeticError("singular jet block")


if __name__ == "__main__":
    main()
