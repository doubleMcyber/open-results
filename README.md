# Open results

A running ledger of small, exact mathematical results: values, extremal cases, sharp constants and finite cases of open problems. Each entry has a statement, a proof and an exact computation that anyone can rerun with standard Python.

Most entries were produced with AI agents and are listed here so that people can check them. Read the status columns before citing anything.

## Status words

- **Certified**: an exact certificate exists and an independent check reproduced it.
- **Settled, unreviewed**: the entry contains a full proof and an exact check that passed, but no human expert has reviewed it yet.
- **No prior found (two passes)**: two independent searches (arXiv, Google Scholar, OEIS, MathOverflow, the source paper's full text, and for Erdős problems the erdosproblems.com page and the community database at github.com/teorth/erdosproblems) found no earlier statement.
- **Unclear**: a close earlier paper exists and has not been fully read.
- **Novelty pending**: searches for prior work have not finished. The statement may already be in the literature. Pending entries will be marked KNOWN (with the reference) or NEW AS FAR AS FOUND as the checks come in.

Corrections, counterexamples and prior references are welcome as issues.

## Results

| ID | Statement | Status | Novelty |
|---|---|---|---|
| [R001](results/R001-rk-order9/) | An explicit 13-stage Runge–Kutta method of order 9 exists, so a(9) ≤ 13 in OEIS A187102 (with Butcher's bound, 12 ≤ a(9) ≤ 13). All 486 order conditions vanish exactly over a degree-16 totally real number field | Certified | Paper and Zenodo record |
| [R002](results/R002-craig-lattice-min-vectors/) | The fourth Craig lattice in dimension 522 has 65,121,213,204 minimal vectors (squared norm 8); the fifth has 1,323,456,100,308 (squared norm 10) | Settled, unreviewed | k = 4 count is an evaluation of Bacher's exact formula; the k = 5 count: no prior found (two passes) |
| [R003](results/R003-k33-free-tripartite-5/) | The maximum number of edges in a K₃,₃-free tripartite graph with five vertices per part is 49 | Settled, unreviewed | no prior found (two passes) |
| [R004](results/R004-werner-hessian-equality/) | Hessian of the Werner endpoint inequality at aligned product zeros, every copy count: all nearby equality cases identified; for four qutrit copies, 110 zero directions and smallest positive eigenvalue 1/4 | Settled, unreviewed (local statement only) | unclear: arXiv:2607.24479 studies the same endpoint form |
| [R008](results/R008-erdos857-diagonal/) | Erdős problem 857, diagonal case: the least family size forcing an n-sunflower on n points is 2ⁿ − ⌊n/2⌋ − 1 for n ≥ 3, with the extremal families classified | Settled, unreviewed | no prior found (two passes) |
| [R009](results/R009-ame-8-4-gf4-graph/) | Among GF(4) graph states on eight ququarts, at most 34 of the 35 balanced cuts can be maximally mixed, and 34 is attained | Settled, unreviewed | unclear: may follow from a GF(4) AME(8,4) exclusion |
| [R013](results/R013-greedy-superstring-three/) | For three substring-free words of length at most L over at least three letters, with first greedy overlap ahead by k, the sharp greedy-superstring ratio is 1 + max(0, L−1−2k)/(L+k+2) | Settled, unreviewed | no prior found (two passes) |
| [R014](results/R014-sum-product-colouring-396/) | The least N such that every two-colouring of [1, N] has two distinct monochromatic sum-product pairs is 396 | Settled, unreviewed | no prior found (two passes) |
| [R015](results/R015-triangle-removal-k18/) | Random triangle removal on K₁₈ ends with the maximum 81 edges with probability about 6.40356903 × 10⁻²⁶ (exact fraction given) | Settled, unreviewed | no prior found (two passes) |
| [R016](results/R016-sparse-sign-equal-rows/) | With minus signs of probability (log n + t)/n, the probability that two rows are equal tends to 1 − (1+λ)e^(−λ), λ = e^(−t) | Settled, unreviewed | no prior found (two passes) |
| [R017](results/R017-magnon-order-7-2/) | For ideal magnons with given quadratic and quartic dispersion terms, the normalized order-7/2 coefficient ranges exactly over [(37−2R²)/128, 29/128]; range R = 5 is the first allowing both signs | Settled, unreviewed | unclear: physics literature not fully searched |
| [R019](results/R019-crouzeix-weighted-shift/) | For a finite positive weighted shift with numerical radius 1, the complete Crouzeix constant equals the largest consecutive weight product, with a sharp stability bound | Settled, unreviewed | formula known (Crouzeix and Greenbaum, arXiv:2508.12768); stability bound: unclear |
| [R020](results/R020-codegree-defect-deg2/) | Maximum-degree-two case of a codegree-defect question: every nonzero defect has a vertex in at least three defective pairs | Settled, unreviewed (one case) | no prior found (two passes) |
| [R021](results/R021-exoo-k43-five-cliques/) | Flipping exactly three blue edges of Exoo's cyclic colouring of K₄₃ (and any red edges) leaves at least 11 monochromatic K₅, and 11 is attained | Settled, unreviewed | no prior found (two passes). Applies only to this restricted family; Exoo reports a colouring of K₄₃ with 2 monochromatic K₅ |
| [R022](results/R022-symmetric-sign-fewest-minus/) | For n ≥ 3, a nonsingular symmetric ±1 matrix has at least ⌊n/2⌋ entries −1 on or above the diagonal, and exactly (2⌊n/2⌋+1)!! matrices attain this | Settled, unreviewed | no prior found (two passes) |
| [R023](results/R023-erdos639-extremal-colourings/) | Erdős problem 639 for n = 6, 7, 8: the colourings of K_n with the most edges in no monochromatic triangle number 360, 5,950 and 14,630, in 1, 5 and 5 classes; for n = 8 those edges always form K₄,₄ | Settled, unreviewed (exhaustive computation, two independent enumerations) | maxima known (Keevash and Sudakov 2004); counts and classes: no prior found (two passes) |

## Known results reproduced

These were proved here before the literature search found them. They stay as worked checks, not as new results.

| ID | Statement | Prior source |
|---|---|---|
| [R005](results/R005-six-vertex-ghz-colours/) | A six-vertex colouring statement reduces to the three-colour theorem it cites; two colours are attainable | Same reduction and witness in the six-vertex explainer at krenngufun.org (July 2026) |
| [R006](results/R006-ame-11-3-transitive/) | Every 11-qutrit stabilizer state with transitive site symmetry has at least 33 of 462 five-site reductions not maximally mixed; a graph state attains 33 | Follows from Danielsen, arXiv:1106.2428, §VI and Table VIII |
| [R007](results/R007-erdos552-q2plus1-star/) | Erdős problem 552, the q²+1 leaf case: R(C₄, K₁,q²₊₁) = q²+q+2 for every prime power q | T. D. Parsons, 1975 (JSTOR 1997368); credited on erdosproblems.com/552 |
| [R010](results/R010-jacobsthal-16-primes/) | For moduli with at most 16 distinct prime factors, the longest run of integers each sharing a factor with n is 105; the equality cases are classified | Hajdu and Saradha (105 and the primes through 29); the two-of-{31, 37, 43} rule follows from Ziller and Morack, arXiv:1611.03310 |
| [R011](results/R011-curve-ten-points-mult55/) | The least degree of a plane curve through ten very general points with multiplicity at least 55 at each is 175 | Ciliberto and Miranda, homogeneous interpolation on ten points, §10.1 |
| [R012](results/R012-projection-body-simplices/) | Among products of simplices, a unique multiset of factor dimensions maximizes normalized projection-body volume in every dimension; dimension 20 is the first where a product beats a single simplex | Towell, Zenodo record 23647750 (25 October 2026) |
| [R018](results/R018-wreath-subnormal-chain/) | The shortest subnormal chain with cyclic quotients from C_{p^k} to C_{p^a} ≀ C_{p^k} has length p^(k−1)(a(p−1)+1) | Clark and Schauz, arXiv:2201.02763, Theorem 4.7 |

More entries are in progress. Results that belong to ongoing research projects are added once those projects have reviewed them.

## Layout

Each folder under `results/` has `SUMMARY.md` (the short statement), `RESULT.md` (proof, construction and checks) and the scripts that verify it. Scripts use the Python standard library unless stated; run them from inside the folder. References to `INDEX.tsv` or `mine_20261125/out/INDEX.tsv` mean [`sources/INDEX.tsv`](sources/INDEX.tsv), the list of public problems and papers the entries follow up on (line numbers count the header as line 1).

## How these were made

Statements were chosen as finite follow-ups to recent papers and problem lists. AI agents wrote the proofs and the checking scripts. A summary line saying "the lead should..." is a note to the reviewer who has not yet done that check. Nothing here has been peer reviewed.

## Licence

Text under CC BY 4.0, code under MIT.
