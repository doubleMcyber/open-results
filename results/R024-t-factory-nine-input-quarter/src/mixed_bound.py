"""Upper bound on A(0) for commuting-path trees whose accepted leaves are full nine-qubit codes
(8 commuting generators, one logical qubit) at a valid syndrome. Exact rationals.

Facts used (each read from a committed result file, not typed in):
 1. A tree of single-Pauli commuting measurements has at most 2^8 = 256 leaves; a leaf accepts with
    probability q_s of its signed group (product of commuting projectors = the code projector).
 2. Orbit leaves (S9 x W^a images of C, q = 1/128 each, nvalid = 1): at most 32 in any tree
    (orbit tree DP: max V(G2) = 8 over all 1,032 dim-2 classes, V(root) <= 4 * 8; results/rec_dim2.txt).
    Non-orbit leaves do not change this count: V is a maximum over all subtrees.
 3. Any other valid leaf has q <= A0 of its unsigned group <= m, the largest A0 among valid codes
    outside the orbit over X-ranks 0..8 (exhaustive searches; values are A0 * 2^20 rounded, so we add 1/2).
Then A(0) <= n/128 + (256 - n) m with n <= 32, increasing in n since m < 1/128.
"""
import re, glob
from fractions import Fraction as F

def maxes(path, pat):
    return [int(v) for line in open(path) for v in re.findall(pat, line)]

src = {}
src["X-rank 8, a != 0"] = max(maxes("results/xrank8.txt", r"^DONE.*max A0\*2\^20 (\d+)"))
src["X-rank 8, a = 0"] = max(maxes("results/xrank8_a0.txt", r"^DONE.*max A0\*2\^20 (\d+)"))
src["X-rank 7"] = max(maxes("results/xrank7.txt", r"^DONE.*max A0\*2\^20 (\d+)"))
for r in range(6):
    src[f"X-rank {r}"] = max(maxes(f"results/xlow/xlow_r{r}.log", r"^DONE.*max A0\*2\^20 (\d+)"))
best6 = [v for v in maxes("results/xlow/xlow_r6.log", r"^BEST .* A0\*2\^20=(\d+)") if v < 8192]
src["X-rank 6, runs without orbit codes"] = max(best6)
src["X-rank 6, runs with orbit codes (second best)"] = max(maxes("results/xlow/xlow_second_r6.txt", r"^DONE.*= (\d+)"))
nin = maxes("results/xlow/orbit_check_r6.txt", r"^checked (\d+) codes")
nout = maxes("results/xlow/orbit_check_r6.txt", r"(\d+) outside")
assert nout == [0], "a code with A0 >= 1/128 lies outside the orbit"
for k, v in src.items():
    print(f"max A0*2^20 outside the orbit, {k}: {v}")
mi = max(src.values())
m = F(2 * mi + 1, 2 ** 21)
V2 = maxes("results/rec_dim2.txt", r"^DONE dim 2: 1032 classes, max V = (\d+)")
assert len(V2) == 1
V2 = V2[0]
nmax = 4 * V2
print(f"orbit codes with A0 >= 1/128 checked: {nin[0]}, outside the orbit: {nout[0]}")
print(f"max orbit leaves per tree: 4 * max V(G2) = {nmax}")
print(f"m <= {2*mi+1}/2^21 = {float(m):.6g} (< 1/128: {m < F(1,128)})")
B = F(nmax, 128) + (256 - nmax) * m
print(f"A(0) <= {nmax}/128 + {256 - nmax} m = {B} = {float(B):.6f}; below 1/2: {B < F(1,2)}; margin {float(F(1,2)-B):.6f}")
