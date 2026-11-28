"""Rerun an exact distance search on the published matrices (data/H_X.txt, data/H_Z.txt).

usage: python3 run_exact.py mtx OUTDIR                    write H_X.mtx, H_Z.mtx for dist-m4ri (stdlib only)
       python3 run_exact.py engine_c  T [--all-starts]    in-house search C (numpy, numba)
       python3 run_exact.py cluster   T [--all-starts]    fresh re-derivation search (numpy, numba)

A result of 'none' at T = 16 in both sectors means d >= 17. Without --all-starts the search uses the
translation symmetry of the code (two start qubits, 0 and 81); the translations are checked first.
"""
import sys
import time
from pathlib import Path

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
DATA = SRC.parent / 'data'


def load(name):
    return [[int(c) for c in line] for line in (DATA / name).read_text().split()]


def write_mtx(rows, path):
    ones = [(i + 1, j + 1) for i, r in enumerate(rows) for j, v in enumerate(r) if v]
    with open(path, 'w') as f:
        f.write('%%MatrixMarket matrix coordinate integer general\n')
        f.write('%d %d %d\n' % (len(rows), len(rows[0]), len(ones)))
        f.writelines('%d %d 1\n' % p for p in ones)


def main():
    mode = sys.argv[1]
    HX, HZ = load('H_X.txt'), load('H_Z.txt')
    if mode == 'mtx':
        out = Path(sys.argv[2])
        out.mkdir(parents=True, exist_ok=True)
        write_mtx(HX, out / 'H_X.mtx')
        write_mtx(HZ, out / 'H_Z.mtx')
        return
    import numpy as np
    import code2b
    HX, HZ = np.array(HX, np.uint8), np.array(HZ, np.uint8)
    T, all_starts = int(sys.argv[2]), '--all-starts' in sys.argv[3:]
    G, _ = code2b.abelian_group([27, 3])
    for sector in 'XZ':
        t0 = time.time()
        if mode == 'engine_c':
            import engine_c
            if all_starts:
                starts, orbits = None, None
            else:
                orbits = engine_c.orbits_2bga(G, HX, HZ)   # checks each translation on H_X and H_Z
                starts = [min(o) for o in orbits]
            status, support, stats = engine_c.cc_lower(HX, HZ, sector, T, starts=starts, orbits=orbits)
            nodes = stats['nodes']
        elif mode == 'cluster':
            import cluster
            import rlib
            from engine_c import orbits_2bga
            if not all_starts:
                assert [len(o) for o in orbits_2bga(G, HX, HZ)] == [81, 81]
            LX, LZ = rlib.logical_basis(HX, HZ)
            checks, tests = (HZ, LZ) if sector == 'X' else (HX, LX)
            cq, ql, lg, maxcol = cluster.prep(checks, tests)
            seeds = range(162) if all_starts else (0, 81)
            nodes, best, support = 0, 10 ** 9, None
            for seed in seeds:       # logicals through `seed` that avoid the excluded qubits
                excl = np.arange(seed, dtype=np.int32)
                r = cluster.search(cq, ql, lg, maxcol, T, seed, excl, False)
                nodes += r[0]
                if r[1] < best:
                    best, support = r[1], sorted(int(q) for q in r[2][:r[3]])
            status = 'none' if support is None else 'found'
        else:
            raise SystemExit(__doc__)
        print('%s sector %s T=%d starts=%s -> %s nodes=%d wall=%.1fs %s' % (
            mode, sector, T, 'all' if all_starts else 'orbit', status, nodes, time.time() - t0,
            '' if support is None else 'support=%s' % support), flush=True)


if __name__ == '__main__':
    main()
