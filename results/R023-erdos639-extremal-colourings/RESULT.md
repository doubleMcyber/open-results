For 2-colourings of the edges of K_n, the maximum number of edges lying in no monochromatic triangle is 10, 12, 16 for n = 6, 7, 8, and the extremal colourings number exactly 360, 5950, 14630, falling into 1, 5, 5 isomorphism classes (vertex permutations and colour swap); for n = 8 the uncovered edges of every extremal colouring form K_{4,4}.

Source: line 215 of sources/INDEX.tsv (ErdosProblems/639.lean, "at most n^2/4 edges not in a monochromatic triangle").
Known (not claimed): the maximum is floor(n^2/4) for n >= 7, 10 for n = 6, binom(n,2) for n <= 5 (Keevash-Sudakov, per erdosproblems.com/639). The web search found no classification of the extremal colourings, so the counts below are the new content.

## Statement and counts (colourings counted with colour swap, i.e. 2 x the "edge 0 fixed" count)
| n | max uncovered | extremal colourings | classes up to S_n and colour swap |
| 5 | 10 | 12 | 1 (the pentagon colouring) |
| 6 | 10 | 360 | 1 |
| 7 | 12 | 5950 | 5 |
| 8 | 16 | 14630 | 5 |
(n = 4: max 6, 18 colourings, 2 classes.)

Class sizes (edge-0-fixed colourings per class, double for all colourings):
n=7: 420 (uncovered graph non-bipartite, degrees 2,2,2,3,3,6,6, 7 mono triangles), and four classes of sizes 840, 1260, 420, 35 whose uncovered graph is bipartite with degrees 3,3,3,3,4,4,4 (K_{3,4}, 5 mono triangles).
n=8: sizes 840, 3360, 2520, 560, 35; all have exactly 8 monochromatic triangles and uncovered graph 4-regular bipartite on 8 vertices, hence K_{4,4}.
n=6: one class, 2 monochromatic triangles, 10 uncovered edges (uncovered degrees 2,2,3,3,5,5).

## Proof
Finite statement. The colouring space has 2^(C(n,2)-1) elements after fixing edge 0 (colour swap is a bijection), at most 2^27 for n=8. For each colouring the covered set is the union of the edge sets of monochromatic triangles; the uncovered count is C(n,2) minus its size. Exhaustive maximisation and counting give the table. Classes are computed by taking, for each extremal colouring, the minimum over all n! vertex permutations and both colour assignments of the adjacency bit-code (exact, no heuristics). The K_{4,4} claim for n=8 follows because a bipartite graph on 8 vertices that is 4-regular must have sides 4 and 4 and so is K_{4,4}; bipartiteness and regularity are read off the five canonical representatives (describe.py).
No paper argument beyond the exhaustive check is given for the class counts; the maxima agree with the published theorem.

## Computation
- enum.c (C, exhaustive, uint32 masks) for n=4..8; prints max and count, writes extremal colourings.
- verify_py.py: independent numpy enumeration, n=4..7, same maxima and counts (9, 6, 180, 2975).
- verify_py8.py: independent numpy enumeration n=8, same max 16 and count 7315.
- classify2.py: exact canonical form over all n! permutations and colour swap; describe.py: structure of the classes. Outputs classes*.json.

## Limits
n=9 (2^35 colourings, 36-bit masks, enum64.c) did not finish within the 10-minute script limit and was stopped; no claim for n >= 9. No general-n proof of the structure (it is observed for n=8 only; at n=7 the extremal set is not a single family, one class has a non-bipartite uncovered graph).

## Independent check
independent_count.c (separate C enumeration over all colourings, n = 4..8) gives the same maxima and counts, and confirms that for n = 8 the uncovered edges of all 14,630 extremal colourings form a triangle-free graph with 16 edges, hence K_{4,4} by Mantel's theorem. independent_classes.py counts orbits under vertex transpositions and colour swap by graph search (no canonical forms): 1 class for n = 6, 5 for n = 7, and, with independent_dump8.c piped into independent_classes8.py, 5 classes among 14,630 colourings for n = 8.
