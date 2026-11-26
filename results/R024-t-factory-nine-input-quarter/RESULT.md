# Clifford correction applied to the nine-input T factory: ideal acceptance 1/4

## Summary

Balada Gaggioli and Marecek (arXiv:2610.31115, Proposition 7) give a stabilizer protocol that takes
nine noisy T states and returns one with error 27/2 p^2 + O(p^3). It is the smallest protocol with
quadratic error suppression for this state, but it accepts an ideal batch with probability only
1/128. Bravyi and Kitaev (2005) and Campbell, Anwar and Browne (2012) showed that a nontrivial
syndrome can be kept, rather than discarded, by applying an outcome-dependent Clifford correction.
We apply that step to Proposition 7. Measuring four of its checks first gives ideal acceptance
1/8, and a depth-five adaptive tree over symmetry images of the code gives 1/4, in both cases with
an output error identical, as a rational function of p, to the published one. At p = 0.01 the tree
accepts with probability 0.2323, or 38.7 inputs per output. We also give an argument (computer-assisted, one implementation, not independently reproduced, not formalised) that, for nine inputs with independent Z faults and ideal Clifford operations, no protocol
with quadratic suppression reaches ideal acceptance 1/2: the maximum lies between 1/4 and
32407/65536 = 0.4945. The argument is not formalised, and its status is stated part by part below.

## Setting

Each input is rho_T(p) = (1-p)|T><T| + p Z|T><T|Z with |T> = (|0> + e^{i pi/4}|1>)/sqrt2, and the
nine faults are independent. A protocol is any adaptive stabilizer circuit: ideal Clifford gates,
stabilizer ancillas, Pauli measurements, classical feedforward and random bits, postselection, one
output qubit. A(p) is the probability of acceptance and eps(p) the infidelity of the accepted
output with |T>. We ask for eps(p) <= 20 p^2 on 0 <= p <= 0.01.

The published protocol measures eight commuting stabilizer generators g1, ..., g8 of a nine-qubit
code C and accepts only the all +1 outcome. Summing over all 512 fault patterns gives
A(p) = D(p)/256 and eps(p) = N(p)/D(p) with

D(p) = 2 - 15p + 87p^2 - 256p^3 + 408p^4 - 336p^5 + 112p^6,
N(p) = 27p^2 - 141p^3 + 324p^4 - 384p^5 + 224p^6 - 48p^7.

These agree with Sec. S3 of the paper, as do the counts of harmful fault patterns.

## The adaptive idea

The single-qubit Clifford W = (X + Y)/sqrt2 fixes |T>, maps Z to -Z, and so maps a Z fault to a Z
fault. Applying W to a set a of qubits leaves the noisy input state rho_T(p)^(x)9 unchanged. If a
generator g has outcome -1 and W^a maps the group <earlier checks, -g> onto <earlier checks, +g>,
then the -1 branch is equivalent to the +1 branch after the correction W^a. Its fault statistics
are those of the +1 branch, so it can be kept instead of discarded.

This is the correction step of Bravyi and Kitaev [BK05, Sec. VI and Lemma 2]. Their operator
A = (sigma_x + sigma_y)/sqrt2 is our W, their |A0> is our |T>, and their 15-to-1 protocol applies
A(w) for the measured outcome and accepts on the remaining checks only. Campbell, Anwar and Browne
[CAB12, Sec. III E] state the step for general codes and note that it raises the success
probability. What follows is an application of that principle to the code of Proposition 7.

For the published generators this works for four of the eight checks if they are measured first,
in the order g7, g8, g1, g2 (paper numbering). After each one a -1 outcome is corrected by a W^a
(for example a = {2}, {3}, {2,7}, {3,6} in qubit numbering from 1). The remaining four checks are
then measured and only +1 is accepted. Sixteen outcome strings survive, each with probability
1/128, so A(0) = 1/8 and A(p) = 16 D(p)/256, with eps = N/D unchanged.

The 1/4 protocol extends this from the 512 W images of C to its full orbit under qubit permutations
and W on any subset (15,482,880 codes). It is a binary tree of depth five. Each node measures one
nine-qubit Pauli; both outcomes continue. Each of the 32 leaves then measures the rest of a code in
the orbit of C that contains the path's measurements, accepts only that code's one valid syndrome,
and decodes with a fixed Clifford. The first measurement is XZIIZIIIX. The leaves are mutually
orthogonal and each accepts with probability 1/128 at p = 0. Because every leaf is a symmetry
image of C under a map that preserves the input noise, its accepted weight and damage per fault
pattern sum to the same polynomials as for C. The full tree, with the eight signed generators of
every leaf, is in `results/tree_best.json`.

## Exact acceptance and error

Over all 512 fault patterns, in exact rational arithmetic:

- A(p) = D(p)/8, so A(0) = 1/4, 32 times the published value.
- H(p) = N(p)/8 (accepted damage), so eps(p) = H/A = N(p)/D(p), identical to the published error.
  eps(p)/p^2 tends to 27/2, and eps(0.01) = 1.3787e-3.
- 20 p^2 A(p) - H(p) = p^2 Q(p) with Q(0) = 13/8, and Q has no root in [0, 1/100] by an exact Sturm
  count. So eps(p) <= 20 p^2 on the whole interval.
- At p = 0 the protocol uses 9/A(0) = 36 inputs per accepted output, against 1,152 for the
  published schedule. At p = 0.001, A = 0.2481 (36.3 inputs per output, against 1,161); at
  p = 0.01, A = 0.2323 (38.7, against 1,240).

## An upper bound below 1/2

Status: computer-assisted, one implementation, not independently reproduced, not formalised.

Claim. Every protocol in the setting above with eps(p) <= 20 p^2 on [0, 0.01] has
A(0) <= 32407/65536 = 0.49449.

The argument has four parts. Parts 1 and 2 are written proofs; parts 3 and 4 rest on exact
computer searches.

1. Per-branch validity. The criterion forces the constant and linear terms of the accepted damage
   to vanish. Both are sums of nonnegative per-record terms, so every accepted record must output
   |T> exactly at p = 0 and for every single fault that reaches it.
2. Reduction to commuting trees on the data. Pulled back to the input frame, a measurement that
   anticommutes with the current stabilizer group, a measurement on an ancilla in that situation,
   or a random bit is a coin: the group stays the same, the outcome probabilities do not depend on
   the input, and only the Clifford frame changes (for anticommuting Hermitian Paulis A and B,
   Pi_B Pi_A = 2^{-1/2} V Pi_A with V = (A + B)/sqrt2 Clifford; this is the reduction lemma of
   Campbell and Browne [CB09], see also Theorem 1 of arXiv:2610.31115). Replacing a coin by the Clifford
   correction of its better child never lowers A(0) and keeps every accepted record valid.
   Protocols without a depth bound are handled by truncation. What remains is a tree of commuting
   Pauli measurements on the nine data qubits. A valid leaf that keeps more than one logical
   qubit holds |T> (x) |phi> for every pattern it must handle, so measuring a logical Pauli of a discarded qubit splits it into valid
   leaves of full rank with the same total probability.
3. Leaf values. Exhaustive searches over all nine-qubit stabilizer codes with one logical qubit
   (about 4.0e9 normal forms, X-rank 0 to 8) find that a valid branch worth 1/128 occurs only for
   codes in the orbit of C, and that every other valid branch is worth at most 1144/2^20.
4. Counting. Full-rank leaves of a commuting tree are orthogonal rank-2 projectors, so there are
   at most 256. An exact tree recursion over the orbit of C shows that at most 32 leaves can be
   orbit codes. Hence A(0) <= 32/128 + 224 * 2289/2^21 = 32407/65536.

How each part was checked. Parts 1 and 2 (the review notes are not included here) were reviewed by an independent
agent with its own simulator, which found them sound and pointed out three gaps in the wording
(unbounded depth, biased random bits, how a coin is removed); the fixed text has not been
re-reviewed. The leaf-splitting step of part 2 was tested numerically only on leaves that are
valid at p = 0, because no fully valid leaf with two logical qubits turned up. The searches of
part 3 were run by one implementation, tested against a slower reference function and reviewed
without being rerun. The cap of 32 orbit leaves in part 4 was computed by two independent
implementations. Nothing has been formalised in Lean.

The bound is crude in part 4 (every non-orbit leaf is charged the largest non-orbit value). It
leaves open whether some tree mixes the 32 orbit leaves with other leaves to exceed 1/4 slightly.
It covers only the setting above: nine inputs, independent Z faults on the inputs, ideal Clifford
operations, one output. It says nothing about noisy Clifford operations, other noise models or
larger factories.

## Verification and how to rerun it

Python 3 with numpy, sympy and numba; run with `OMP_NUM_THREADS=1`. From this folder:

| Check | Command | Time on an M2 Max |
|---|---|---|
| Published schedule 1/128 and adaptive 1/8, exact | `python src/positive_control.py` | about 20 s |
| The 1/4 tree, exact over 512 patterns, criterion E | `python src/verify_tree.py results/tree_best.json` | about 6 s |
| Independent dense-simulator check of the tree | `cd work/review_tree && python check.py` | about 60 s |
| The bound from the committed search outputs | `python src/mixed_bound.py` | under 1 s |
| Reduction lemmas on random protocols (quick form; full form `40 2`, 150 s) | `python src/check_reductions.py 3 1` | about 35 s |

The searches behind the bound take hours and are not part of the quick rerun; their outputs are
in `results/`. The search commands are not included in this folder. Which results have two
implementations: the 1/128 and 1/8 values (the exploratory script that found 1/8, and
`src/positive_control.py`, written without reading it); the 1/4 tree, the cap of 32 orbit leaves and
the reduction lemmas (the original code, and code written by a separate agent from a brief alone, of which `work/review_tree/check.py` is included). The exhaustive code searches of
part 3 have one implementation.

## Limits

- Larger factories remain more efficient per output. The ten-input, two-output protocol of Meier,
  Eastin and Knill accepts ideal inputs with probability 1 and uses 5 inputs per output, against 36
  here; the familiar 15-to-1 protocol also accepts ideal inputs with probability 1. The result
  improves the smallest factory; it does not make the smallest factory the cheapest.
- The cost of correction is not counted. The tree needs five sequential measurements with
  feed-forward and then an outcome-dependent leaf code and decode, so the leaf circuit is not
  fixed in hardware. This adds classical latency and Clifford depth. All results assume ideal
  Clifford operations; with noisy ones the gain may be smaller.
- The Lean formalisation (branch weights, output fidelity, retry cost) is not done. All proofs here
  are by exact computation and short written arguments, and the bound depends on searches that
  have run once.
- Prior art, checked 2026-11-25 (18 recorded searches plus
  citation databases). The correction principle is published [BK05, CAB12]; Hu, Liang and
  Calderbank (arXiv:2109.13481) and Heussen (arXiv:2504.17509) study syndrome correction where it
  lowers the suppression order, which it does not here. No source was found that applies the
  principle to Proposition 7 or reports an acceptance above 1/128 for a nine-input quadratic T
  factory. arXiv:2610.31115 has one citing paper, by the same authors. arXiv:2211.07535 was read in
  full: it bounds code length against acceptance for CSS code projections with depolarised |H>
  inputs, leaves intermediate Clifford corrections as an open question, and does not apply to the
  non-CSS code here or imply the bound below 1/2. No prior bound of that kind was found. Google
  Scholar, X and Zenodo were not searched directly.

## References

- [BK05] S. Bravyi and A. Kitaev, Universal quantum computation with ideal Clifford gates and noisy
  ancillas, Phys. Rev. A 71, 022316 (2005), arXiv:quant-ph/0403025.
- [CB09] E. T. Campbell and D. E. Browne, On the structure of protocols for magic state
  distillation, TQC 2009, arXiv:0908.0838.
- [CAB12] E. T. Campbell, H. Anwar and D. E. Browne, Magic-state distillation in all prime
  dimensions using quantum Reed-Muller codes, Phys. Rev. X 2, 041021 (2012), arXiv:1205.3104.
- L. Balada Gaggioli and J. Marecek, The limits of magic-state distillation, arXiv:2610.31115.

## Rerun record

Run on 2026-11-26 from this folder, Python with numpy, sympy and numba, `OMP_NUM_THREADS=1`, M2 Max under other load (wall times exceed the table above for the longer checks).

- `python src/positive_control.py` (126 s): published schedule A(0) = 1/128 with eps/p^2 = 27/2; adaptive schedule "ideal acceptance A(0) = 1/8", "16 branches surviving at p=0", "eps identical to published: True ; A_adaptive / A_published = 16".
- `python src/verify_tree.py results/tree_best.json` (7.8 s CPU, 198 s wall): "leaves = 32; A(0) = 1/4", "A / (D/256) = 32; H / (N/256) = 32", "eps/p^2 at 0 = 27/2", "criterion E: gap(0) = 13/8, roots in [0,1/100] = 0", "eps(0.01) = 0.00137867820859".
- `cd work/review_tree && python check.py` (204 s wall): "A==D/8 True  H==N/8 True", "Q(0)= 13/8", "real roots of Q in [0,0.01]: 0", "A(0.01) 0.232306005814".
- `python src/mixed_bound.py` (under 1 s): "orbit codes with A0 >= 1/128 checked: 48, outside the orbit: 0", "max orbit leaves per tree: 4 * max V(G2) = 32", "A(0) <= 32/128 + 224 m = 32407/65536 = 0.494492; below 1/2: True". This reads stored search outputs; it does not rerun the searches.
- `python src/check_reductions.py 3 1` (145 s wall): final line "ALL CHECKS PASSED"; the scrambled 1/4 tree gives A(0) = 0.25 in all three runs.
