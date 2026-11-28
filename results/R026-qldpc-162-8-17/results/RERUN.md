# Rerunning the checks

Run all commands from the entry folder unless a step says otherwise. Times are for one thread on an Apple M2 Max.

## 1. Everything except the lower bound

```
python3 -I verify.py
```

Standard library only, under a second. It checks the matrices in `data/`, n, k, the check weights, H_X H_Z^T = 0 and the four weight-17 witnesses, and writes `results/verify.txt`. A nonzero exit status means a check failed.

## 2. d >= 17 with the two in-house searches

Needs numpy and numba. The runs of 2026-11-27 used Python 3.11.9, numpy 2.4.6 and numba 0.68.1.

```
python3 src/run_exact.py engine_c 16
python3 src/run_exact.py cluster 16
```

Each prints one line per sector, and `-> none` in both sectors means d >= 17. Each command took about a minute. With translation symmetry (start qubits 0 and 81) both searches visit 389,261,066 nodes in sector X and 521,097,876 in sector Z on the published matrices. Logs: `results/exact/rerun_engine_c_orbit_W16.log` and `results/exact/rerun_cluster_orbit_W16.log`.

Adding `--all-starts` drops the symmetry assumption and takes several times longer. That form was last run during the fresh re-derivation, on the original labelling (292 s and 381 s of CPU time), and was not repeated on the published matrices.

numba writes a cache next to the sources. Set `NUMBA_CACHE_DIR` to put it elsewhere.

## 3. d >= 17 with dist-m4ri

dist-m4ri 0.16.1 is by Pryadko and coauthors (github.com/QEC-pages/dist-m4ri, commit 4cc9c126e314d1e36bdefbb5e68b77c274e3065e). It was built against libm4ri 20260122 (github.com/malb/m4ri) with, from its `src/` folder and with `M` set to the libm4ri install prefix:

```
make dist_m4ri CC=clang OPT="-g -O3 -mcpu=native -I$M/include -L$M/lib -Wl,-rpath,$M/lib"
```

Write the matrices in MatrixMarket form to an empty folder, then run the program from that folder:

```
python3 src/run_exact.py mtx /path/to/empty-folder
cd /path/to/empty-folder
dist_m4ri method=2 finH=H_Z.mtx finG=H_X.mtx threads=1 timeout=0 debug=1 wmax=16    # sector X
dist_m4ri method=2 finH=H_X.mtx finG=H_Z.mtx threads=1 timeout=0 debug=1 wmax=16    # sector Z
```

No `start=` option is given, so every column is a start column. The expected output line is `17 0 0`: lower bound 17, no codeword found. The runs took 49 s (X) and 55 s (Z). Logs: `results/exact/rerun_distm4ri_allstarts_W16_X.log` and `..._Z.log`.

## Log index

`results/exact/`

| File | Contents | Run |
|---|---|---|
| `original_record1.json` | First certification of the code: weight-17 witnesses; in-house search C finds nothing at weight <= 16 (X 22.9 s, 377,500,588 nodes; Z 35.0 s, 542,663,168 nodes); dist-m4ri with start columns 0 and 81, `wmax=16`, prints `17 0 0` (9.5 s, 12.0 s) | 2026-11-25 |
| `original_round1_certification.log` | One line for each of the 73 search survivors, all the same code up to a permutation of qubits | 2026-11-25 |
| `fresh_search_W15_17.out` | Fresh re-derivation, symmetry-reduced: nothing at weight 15 or 16, weight 17 found, both sectors | 2026-11-25 |
| `fresh_search_allseeds_W16_X.out`, `..._Z.out` | Fresh re-derivation with all 162 start qubits and no symmetry: nothing at weight <= 16 | 2026-11-25 |
| `rerun_*.log` | The runs of sections 2 and 3, on the published matrices | 2026-11-27 |

`results/controls/` holds the positive controls and `results/side/` the logs for the three published codes. Both are described in `RESULT.md`.

## Labelling of the older logs

The logs dated 2026-11-25 number the group elements by a group table from the Bicycle Race database (SmallGroup(81,5)). There the code is a = [0, 74, 50], b = [0, 64, 32, 36], and x and y are elements 50 and 9. The published matrices use index 3i + j for x^i y^j. `data/log_labelling.json` gives, for each published column, the column used in those logs. `verify.py` maps the witnesses of the first certification through it. At packaging time the published matrices, relabelled this way, were equal entry for entry to the matrices saved by the original run (those saved matrices are not included). Node counts differ between the two labellings because the search breaks ties by index.

## Edits to copied files

In copied logs, shell timing lines that contained local paths were removed, and folder prefixes were removed from the dist-m4ri program and matrix file names. Two files in `results/exact/` were renamed. In `src/`, comments and docstrings of `engine_c.py` and `rlib.py` were reworded, and an unused line and one default file path in `rlib.py` were changed. `code2b.py` and `cluster.py` are unchanged. No number in any log was edited.
