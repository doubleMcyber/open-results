# A [[162,8,17]] two-block group-algebra code with check weight 7

## Summary

Over G = C27 x C3 = <x> x <y>, the two-block group-algebra CSS code with A = 1 + x + x^5 and
B = 1 + xy + x^4 y^2 + x^15 y has parameters [[162,8,17]] and check weight 7, so
k d^2 / n = 1156/81 = 14.27. The largest value at check weight at most 7 and length at most 162 in a
frozen table of published CSS codes is 96/7 = 13.71. The parameters n and k, the check weight and the
bound d <= 17 are checked by a standard-library script. The bound d >= 17 is an exhaustive computer
search. The code was found and checked by AI agents. No human expert has reviewed it.

## Construction

Write the element x^i y^j as the index 3i + j. For a set P of group elements let M(P) be the
81 x 81 matrix with M(P)[s g, g] = 1 for each s in P. Then

    H_X = ( M(A) | M(B) ),        H_Z = ( M(B)^T | M(A)^T ).

Qubits 0 to 80 form the left block and 81 to 161 the right block. G is abelian, so M(A) and M(B)
commute and H_X H_Z^T = M(A)M(B) + M(B)M(A) = 0 over GF(2). The construction is the two-block
group-algebra family of Lin and Pryadko (arXiv:2306.16400).

H_X and H_Z are 81 x 162, each of GF(2) rank 77, so k = 162 - 154 = 8. Every row has weight 3 + 4 = 7.
In each matrix 81 columns have weight 3 and 81 have weight 4. The matrices are in `data/H_X.txt` and
`data/H_Z.txt`, one row per line.

The code came out of a random-sampling search over 155 groups of order 65 to 83 at check weight 7,
about 43.3 million pairs (A, B) and about 29.4 CPU-hours. Its 73 survivors above the comparison value
were all this one code up to a permutation of qubits. The search did not enumerate those groups, so it
says nothing about which other codes exist.

## Upper bound d <= 17

`data/witnesses.json` lists four logical operators of weight 17, an X and a Z one from the first
certification and an X and a Z one from a fresh re-derivation. `verify.py` checks that each has weight
17, commutes with all checks of the other type and lies outside the row space of its own type.

## Lower bound d >= 17

### Why an empty search is a proof

Take X-type logicals (the Z case is the same with the matrices exchanged). A logical is a set c of
qubits with H_Z c = 0 that is not in the row space of H_X. Suppose one of weight at most W exists and
let c have minimum weight among them.

1. No nonempty proper subset s of c has H_Z s = 0. If it did and s were a stabilizer, c + s would be a
   logical lighter than c. If s were not a stabilizer, s itself would be a lighter logical.
2. A depth-first search starts from a qubit of c and keeps a chosen set s and an excluded set E, with
   s inside c and E disjoint from c. While s is not all of c, some check r has odd overlap with s.
   It has even overlap with c, so r contains a qubit of c outside s. The search takes the allowed
   qubits q_1, ..., q_m of r and, in branch i, adds q_i and excludes q_1, ..., q_(i-1). In the branch
   for the first q_i that belongs to c, s stays inside c and E stays disjoint from c. By induction the
   search reaches c.
3. Each added qubit changes at most D checks, where D is the largest column weight. A set with u
   unsatisfied checks needs at least ceil(u/D) more qubits, so a branch with |s| + ceil(u/D) > W can
   be cut.
4. A set with H_Z s = 0 is a stabilizer exactly when it has even overlap with each of 8 independent
   Z-type logical representatives. Such a set is reported if it is not a stabilizer. If it is one, it
   is not extended, which is safe by step 1.
5. Translating both blocks by any group element permutes the rows of H_X and of H_Z, so it preserves
   weight, logicals and stabilizers. A logical that touches the left block can be translated to
   contain qubit 0. Otherwise it lies in the right block and can be translated to contain qubit 81.
   Two starts are therefore enough: qubit 0, and qubit 81 with qubits 0 to 80 excluded. Without
   symmetry, every qubit q is a start with qubits 0 to q-1 excluded.

So if the search finds nothing at W = 16 in both sectors, then d_X >= 17 and d_Z >= 17.

### Runs

| Search | Symmetry | X sector | Z sector | Date | Log in `results/exact/` |
|---|---|---|---|---|---|
| In-house search C (`src/engine_c.py`) | starts 0, 81 | none at <= 16 (22.9 s) | none at <= 16 (35.0 s) | 2026-11-25 | `original_record1.json` |
| dist-m4ri 0.16.1, `method=2` | starts 0, 81 | `17 0 0` (9.5 s) | `17 0 0` (12.0 s) | 2026-11-25 | `original_record1.json` |
| Fresh search (`src/cluster.py`) | starts 0, 81 | none at <= 16 (31.9 s) | none at <= 16 (44.2 s) | 2026-11-25 | `fresh_search_W15_17.out` |
| Fresh search | none, 162 starts | none at <= 16 (292 s) | none at <= 16 (381 s) | 2026-11-25 | `fresh_search_allseeds_W16_*.out` |
| Search C, published matrices | starts 0, 81 | none at <= 16 (28.0 s) | none at <= 16 (32.0 s) | 2026-11-27 | `rerun_engine_c_orbit_W16.log` |
| Fresh search, published matrices | starts 0, 81 | none at <= 16 (26.9 s) | none at <= 16 (33.5 s) | 2026-11-27 | `rerun_cluster_orbit_W16.log` |
| dist-m4ri, published matrices | none, all columns | `17 0 0` (49.3 s) | `17 0 0` (54.9 s) | 2026-11-27 | `rerun_distm4ri_allstarts_W16_*.log` |

Times are single-threaded on an Apple M2 Max. Commands are in `results/RERUN.md`. The dist-m4ri line
`17 0 0` means lower bound 17 and no codeword found.

### How independent these are

All of them use the connected-cluster method. Search C reimplements the depth-first enumeration of
Dumer, Kovalev and Pryadko used in dist-m4ri, with the branch exclusion of step 2 and a different
choice of check. The fresh search was written without sight of search C but turned out to be the same
algorithm: on the original labelling both visit 377,500,588 nodes in X and 542,663,168 in Z. That
agreement is evidence against a coding slip and no evidence against a shared flaw in the method.
dist-m4ri is separate code by other authors, with no branch exclusion and one round per weight.

Attempts to get a second kind of evidence failed. A SAT encoding, tried on a Bicycle Race
[[162,8,14]] code, could not prove within 300 s that it has no logical of weight at most 13, so it was
not run on this code. A randomized information-set attack on this code was too weak to find even the
known weight-17 words, so it says nothing. There is no compact certificate for d >= 17.

## Positive controls

| Control | Searches | Outcome | Logs in `results/controls/` |
|---|---|---|---|
| Search C against brute force: 36 small codes per seed, 288 searches per seed, seeds 0, 1, 2, 3, 11 | C | all pass | `test_engine_c_seed*.log` |
| 28 sector distances on small codes | in-house search A and C | all agree | `cross_engineA_engineC.log` |
| Gross code [[144,12,12]] (arXiv:2308.07915) | A, SAT search B, C, dist-m4ri | d = 12 reproduced, nothing at <= 11 | `pc1_engine*.log`, `engineC_gross_*.log`, `engineD_gross*.log` |
| [[72,12,6]], [[90,8,10]], [[108,8,10]] (same paper) | B | published distances reproduced | `pc2_engineB.log` |
| Bicycle Race 7c4fc81e18146a13, [[180,16,14]], weight 7 | A, C, dist-m4ri | database distance reproduced | `pc3_A_7c4*.log`, `engineC_br_*.log`, `engineD_7c4*.log` |
| Bicycle Race c87b9ec626753a5b, [[170,18,16]], weight 8 | A, dist-m4ri | database distance reproduced | `pc3_A_c87*.log`, `engineD_c87*.log` |
| Bicycle Race acb02b92594b75a4, [[186,20,18]], weight 9 | C, dist-m4ri | nothing at <= 17; dist-m4ri finds 18 | `engineC_acb02_*.log`, `engineD_acb02*.log` |
| Recall: the sampler, on a region already searched exhaustively by others (weight 7, orders 42, 45, 49) | C, dist-m4ri | 211 survivors, all [[90,12,9]], the target value 10.80 | `pc4_recall_certification.log` |
| Fresh search against brute force on 22 small cyclic codes | fresh | 22 of 22 | `fresh_bruteforce.out` |
| Fresh search on Bicycle Race codes [[162,4,13]] and [[162,8,14]] | fresh | database distances reproduced | `fresh_database_codes.out` |

The sources of searches A and B and of the control drivers are not included. `verify.py` also has its
own controls: it confirms that a stabilizer is recognised as one and that flipping any single qubit of
a witness breaks commutation.

## Fresh re-derivation

On 2026-11-25 a separate AI agent rebuilt the code with its own group builder, GF(2) library and
distance search before opening any of the original source. It confirmed n = 162, k = 8, check weight
7, the CSS condition and d_X = d_Z = 17, including the run with all 162 start qubits and no symmetry.
It showed by explicit qubit permutations that all 73 search survivors are one code, using group
automorphisms and translations, and it checked all 146 of their recorded weight-17 witnesses. It then
read the original source and found no soundness error. It also ran dist-m4ri on its own matrices and
got distance 17, but the input form it used covers only the Z sector and the log was not saved. The
dist-m4ri runs of 2026-11-27 above cover both sectors.

## Comparison with published codes

The comparison table was frozen on 2026-11-24, before the search began. For each check weight and
length n it holds the largest k d^2 / n' over published CSS codes with at most that check weight and
length n' <= n. Its sources are the Bicycle Race database (github.com/gideonlsx/bicycle-race, commit
cee978f8, by G. Lee, arXiv:2610.13880, data under CC BY 4.0), that project's literature set v8
(2,611 published codes, cut-off 2026-09-29) and five further published codes added by hand. Published distances,
including upper bounds and estimates, are taken at face value. The table file itself is not included
(sha256 963ed97258cf24775abbddd0c54461fdd1b3caec0d5824323670b1314fdcbfdc). The value 96/7 at check
weight 7 and length 162 is set by a Bicycle Race database code, so it can be checked against that
public database. The table is a record of what was published and is not a bound.

| Code | Check weight | k d^2 / n | Note |
|---|---|---|---|
| [[162,8,17]], this entry | 7 | 14.27 | |
| [[126,12,12]] over C63, Bicycle Race 906a026d05554be7 | 7 | 13.71 | sets the table value for 126 <= n < 168 |
| [[126,10,13]], Aydin, arXiv:2606.17268 | 7 | 13.41 | |
| [[162,8,15]], Lin and Pryadko data archive, arXiv:2306.16400 | 7 | 11.11 | best published weight-7 code at n = 162 found in these sources |
| [[144,12,12]] gross code, arXiv:2308.07915 | 6 | 12.00 | |
| [[168,12,15]], Bicycle Race | 7 | 16.07 | higher, at n = 168 |
| [[252,16,20]], Bicycle Race | 7 | 25.40 | higher, at n = 252 |
| [[93,5,<=21]], arXiv:2603.05496 | 7 | at most 23.71 | higher but not CSS, and the distance is an upper bound |
| [[146,18,14]], Bicycle Race | 8 | 24.16 | higher, with weight-8 checks |
| [[160,24,14]], Bicycle Race | 9 | 29.40 | higher, with weight-9 checks |

The claim is therefore narrow. It concerns CSS codes, check weight at most 7 and length at most 162,
against that list. One error is known in the frozen table (the code in the first row of the last section
below is listed with check weight 6 and has weight 8). It affects only lengths of 168 and above.

## Search for prior work

One pass, on 2026-11-25 from 12:28 to 12:40 PST, 15 queries.

| Source | What was looked for | Result |
|---|---|---|
| Literature set v8 | CSS, check weight <= 7, 120 <= n <= 170, k d^2 / n > 11 | nothing at or above 14.27 |
| Bicycle Race database and its latest commits | check weight <= 7, 120 <= n <= 170 | no [[162,8,17]]; no newer database |
| Web search, several phrasings | "[[162,8,17]]", weight-7 bivariate bicycle codes, two-block group-algebra codes of order 81 | no such code |
| github.com/unitaryfoundation/qldpc-challenge at commit b20756d7, and its pull requests | 208 code records with n <= 162 and k d^2 / n > 14.27 by name | none has check weight <= 7; no [[162,8,17]] record |
| arXiv:2610.12782, arXiv:2601.15446 | code parameters, and bounds in the second | nothing at or above; the bounds in 2601.15446 are plotted for small d and were not compared numerically |
| arXiv listings since 2026-09-29 (bivariate bicycle, two-block, group algebra, generalized bicycle, qLDPC distance search) | titles and abstracts, about 55 papers | no weight-7 code at n = 162 |
| codetables.de, [[162,8]] | general bounds without a weight limit | lower bound 30, so no table entry changes |

Not searched: Google Scholar, MathOverflow, X, Zenodo, blogs, and anything posted after the search.
This shows only that the sources above did not contain the code.

## Status words

Status is "Settled, unreviewed". The entry has the completeness argument above and exact checks that
passed, and no human expert has reviewed it. It is not "Certified": d >= 17 has no certificate that can
be checked separately from the search, `verify.py` does not recheck it, and the searches that agree on
it share one method.

Novelty is "Novelty pending". The README asks for two independent searches, including Google Scholar
and MathOverflow, before "no prior found". One search has been made and it covered neither.

## Limits

- Only k d^2 / n and the exact distance are claimed. There is no result about circuit-level distance,
  syndrome-extraction schedules, hook errors, decoders, thresholds, logical gates or hardware layout.
- A high k d^2 / n does not imply a lower logical error rate. Weight-7 checks need more two-qubit gates
  than weight-6 checks.
- The code does not replace the gross code in general.
- The comparison depends on the frozen list and on published distances taken at face value. A code
  missing from the list could equal or beat this one.
- Optimality is not claimed.

## Side results: exact distances of three published codes

These are not covered by the status words above or by `verify.py`. Their matrices and witnesses are not
included, only logs. No search was made for earlier exact values. All three have check weight 8, so none
enters the weight-7 comparison.

| Code | What the paper states | Value found | k d^2 / n |
|---|---|---|---|
| Pandey, arXiv:2610.05307 v1, over S3 x Z14 with a = {(e,e), (e,y), (r,y^3), (r^2,y^3)}, b = {(e,e), (e,y^3), (s1,y^2), (s2,y^10)} | [[168,16,14]], distance from an information-set estimate | d_X = d_Z = 14, check weight 8, under both product orders on S3 | 18.67 |
| Lu, Yang and Guo, arXiv:2609.06572 v1, Table 1 row 9, (l,m) = (8,9), A = 1 + x^4 y^2 + y^4 + y^7, B = 1 + x^2 y^6 + x^5 y^7 + x^7 y^8 | [[144,6,>=15]] | [[144,6,15]] | 9.38 |
| Same table, row 6, (l,m) = (12,6), A = 1 + x^8 y + x y^3 + x^2 y^5, B = 1 + x^11 + x y + y^4 | [[144,10,>=11]] | [[144,10,14]] | 13.61 (8.40 at d = 11) |

For the last two, H_X = (A | B) and H_Z = (B^T | A^T) with x and y generating C_l x C_m.

| Code | Search A, nothing at <= d-1, X / Z | dist-m4ri all columns, nothing at <= d-1, X / Z | Logs in `results/side/` |
|---|---|---|---|
| Pandey (two orders) | 6.5 / 5.0 s and 3.5 / 3.9 s | `14 0 0`, 3.6 / 2.1 s and 3.8 / 2.9 s | `pandey168*`, `engineD_pandey168*` |
| Row 9 | 28.8 / 35.9 s | `15 0 0`, 78.8 / 45.8 s | `lu144_6_A.log`, `engineD_lu144_6_*` |
| Row 6 | 22.2 / 30.9 s | `14 0 0`, 2.3 / 2.6 s | `lu144_10_A.log`, `engineD_lu144_10_*` |

Both programs also find logicals of weight d. The dist-m4ri runs that find weight 14 for the Pandey code
used one start column per symmetry orbit, so they count only as witnesses. On 2026-11-24 a separate AI
agent rebuilt the three codes from the papers, reran the bounds with its own search and with dist-m4ri,
and did not refute any of them.
