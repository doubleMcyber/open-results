# Two monochromatic sum-product pairs first become unavoidable at 396

**Exact statement.** Color the integers in `[N] = {1,...,N}` red or blue. A witness is
an unordered pair of distinct integers `a < b` for which `a, b, a+b, ab` all lie in
`[N]` and have the same color. The least `N` for which every coloring has at least
two witnesses is **396**. The two pairs may overlap and may have different colors.

At 395 the minimum is one. The only pairs that can occur as the sole witness are
`(1,7)`, `(1,8)`, and `(2,7)`. At 396 the minimum is exactly two. Of the nine pairs
that become eligible at 396, precisely `(4,99)` and `(18,22)` are essential in the
following sense. Keep all pairs eligible at 395 and any subset of the nine new
pairs. The retained family forces two witnesses in every coloring of `[396]`
if and only if it contains both of those pairs.

**Source and scope.** This is a finite multiplicity follow-up to physical row
428 (ID 164) of `mine_20261125/out/INDEX.tsv`. Its local source,
`src/openai_math/CONTENTS.md`, lines 3870–3879, gives the existence question for
finite subset sums and products of a single set. For a two-element set these
values are exactly the four in the definition above. In particular, 1 is
permitted, so its product with the other element repeats that element. The
argument below is independent of the infinite theorem. Novelty is UNVERIFIED.

## Colorings attaining the bounds

Let the base red set in `[395]` consist of all numbers congruent to 2, 4, or 6
modulo 8, with 2, 4, 6, 10, 14 removed and 1, 3, 5, 8, 16, 24, 32, 40, 48
added. For each row, also color the indicated extra numbers red and color all
other numbers blue. Each extension listed has exactly the original witness and
the single additional witness in the corresponding column.

| Extra red numbers | Sole witness at 395 | New witness if 396 is blue | New witness if 396 is red |
|---|---|---|---|
| 7 | (1,7) | (4,99) | (18,22) |
| 9, 56 | (1,8) | (4,99) | (18,22) |
| 56 | (2,7) | (4,99) | (18,22) |

The script checks this table by trying every unordered pair directly. Restricting
the first coloring gives at most one witness for every smaller endpoint. Its two
extensions also prove necessity of each essential pair, even when all eight other
new pairs are retained.

## Exhaustive upper bound

For a pair `p=(a,b)`, put `E(p)={a,b,a+b,ab}`. Avoiding `p` requires both colors
in `E(p)`. The full list at 395 has 1,200 pairs. For each positive `a`, the script
takes every `b` from `a+1` through `min(395-a, floor(395/a))`, inclusive.

1. The full family has no avoiding coloring. To classify a possible sole witness,
   temporarily omit a block of pairs. If the remaining family has no avoiding
   coloring, no pair in that block can be the sole witness. Otherwise bisect the
   block and repeat on each half, restoring all pairs outside the current half.
   At a singleton, an avoiding coloring of the remaining family has precisely
   that singleton as its witness because zero witnesses were ruled out. Starting
   with the entire list leaves exactly the three singletons in the table.
2. For each of these three pairs `p`, take the 1,199 old pairs other than `p` and
   add `(4,99)` and `(18,22)`. The script finds no avoiding coloring in each of
   the three cases. Consequently a coloring with sole old witness `p` has at
   least one of these two new witnesses. A coloring with two old witnesses
   already meets the bound.
3. Both new pairs have product 396. For any coloring with one old witness the
   triples `{4,99,103}` and `{18,22,40}` must therefore each be monochromatic and
   have opposite colors. Otherwise one choice of color for 396 would avoid both
   pairs, contradicting step 2. This explains how a single new integer forces
   a second witness in either color. Together with the table this proves all
   three assertions, including the characterization of retained families.

The avoiding-coloring test uses exact integer bit masks. If an edge has both
colors it is satisfied. A fully assigned edge of one color is a contradiction.
If an edge has one unassigned vertex and lacks a color, that vertex must take
the missing color. Opposite requirements on one vertex give a contradiction.
After applying forced assignments to exhaustion, the solver branches on both
colors of a free vertex in an unsatisfied edge. Each branch assigns a new
vertex, so it terminates. If every edge is satisfied the remaining vertices
can be blue. At the root one vertex may be fixed red by swapping color names.
These rules justify every rejection in the finite search.

## Reviewer checks

- From this folder run `python3 -B check.py` (Python 3.10+; standard library).
  Check the three surviving singletons, all six extensions and the endpoint.
- Check the convention for distinct pairs, the inclusive bound on the second
  element, and restoration of constraints when recursing into an omitted block.
- For an independent verification, encode each required edge as a positive
  clause and an all-negative clause over its vertices. Check unsatisfiability
  at 395 for zero witnesses and for every single omission except the three
  in the table. For each exceptional omission check again with both essential
  pairs added. The table supplies satisfying assignments for the omissions.
- Independent lead reproduction, formal proof checking and literature priority
  are UNVERIFIED. This result concerns two colors and two-element sets.

Local verification on 2026-11-25 used CPython 3.15.2 on macOS. Running the script
with the standard library's `runpy` returned normally in 3.60 CPU seconds, with
peak resident memory of 22,773,760 bytes.

A shorter independent SAT check of the endpoint can use one indicator per pair.
For each edge append its indicator as a positive literal to both color clauses
above, then require at most one indicator to be true. This formula should be
satisfiable at 395 and unsatisfiable at 396. Monochromatic edges force their
indicators true, and assigning true exactly to their indicators proves the
converse. This alternative encoding was not run locally.
