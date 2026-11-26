# The diagonal sunflower threshold and its extremal families

For every integer $n\ge 3$, the minimum size forcing an $n$-sunflower among families of distinct subsets of an $n$-element set is

$$m(n,n)=2^n-\lfloor n/2\rfloor-1.$$

An $n$-sunflower consists of $n$ distinct sets whose pairwise intersections are all the same core. One member may equal the core. The largest family avoiding such a sunflower has one fewer member than the forcing threshold.

Up to relabeling the ground set, the number of families attaining that maximum is 2 for odd $n$, 6 for $n=4$, and 7 for even $n\ge6$.

## Proof

Call the missing subsets deletions. A family avoids all sunflowers exactly when its deletions meet every sunflower. Removing the core from each member leaves pairwise disjoint petals. At most one petal is empty, so at least $n-1$ points lie outside the core. This gives four possible types.

1. With singleton core $\{i\}$, the members are that singleton and every pair containing $i$. Each of the $n-1$ other points must form a separate petal.
2. With empty core and all petals nonempty, the members are all singletons.
3. With empty core and an empty petal, one possibility consists of the empty set and all singletons except one.
4. The remaining possibility consists of the empty set, a pair, and the $n-2$ singletons outside that pair. Indeed, $n-1$ disjoint nonempty petals on $n$ points can exceed singleton size only once, by one point.

Thus all subsets of size at least three belong to every maximum family. Write $e=1$ if the empty set is deleted, and $e=0$ otherwise. Let $S$ consist of the points whose singletons are deleted, put $s=|S|$, and regard deleted pairs as the edges of a simple graph. Type 1 requires every vertex outside $S$ to be incident with a deleted edge. Type 2 requires $s\ge1$. If $e=1$, the other two types are covered. If $e=0$, type 3 requires $s\ge2$. When $s=2$, the unique pair on $S$ must also be deleted to cover type 4. When $s\ge3$, every type 4 sunflower already contains a deleted singleton. These conditions hit all four types.

Put $r=n-s$. Covering the $r$ outside vertices takes at least $\lceil r/2\rceil$ edges. Match outside vertices in pairs, then join any leftover vertex to a point in $S$. This attains the bound, including $r=0$. The forced pair on $S$, when required, covers no outside vertex. The exact deletion counts follow.

| Empty set deleted | Deleted singletons | Minimum deletions |
|---|---|---|
| Yes | $s\ge1$ | $1+s+\lceil(n-s)/2\rceil$ |
| No | $s=2$ | $3+\lceil(n-2)/2\rceil$ |
| No | $s\ge3$ | $s+\lceil(n-s)/2\rceil$ |

Since $s+\lceil(n-s)/2\rceil=\lceil(n+s)/2\rceil$, the overall minimum is $\lfloor n/2\rfloor+2$. The first row at $s=1$ attains it for both parities. Subtracting this minimum from $2^n$ and adding one gives the claimed threshold.

For odd $n$, equality occurs exactly at $(e,s)=(1,1),(0,3)$. For even $n$, it occurs at $(1,1),(1,2),(0,2),(0,3),(0,4)$. Each equality case uses a minimum edge cover of the outside vertices, plus the forced pair for $(0,2)$.

When $r$ is even, all $r$ endpoints are needed, so the covering edges form a perfect matching outside $S$. This includes the empty matching. When $r$ is odd, there is one endpoint to spare. Either one edge joins an outside vertex to $S$ and the rest form a matching, or one outside vertex has degree two and the others have degree one. In the latter case the edges are a three-vertex path and a matching, possible exactly when $r\ge3$. Permutations preserving $S$ as a set act transitively on each listed configuration. The cases differ in $e$, in $s$, or in the presence of a crossing edge. Thus the list classifies all maximum families.

For odd $n$, both equality cases have even $r$, giving two orbits. For even $n$, exactly two cases have odd $r$, namely $(1,1)$ and $(0,3)$. Each contributes two orbits when $n\ge6$, giving seven in total. At $n=4$, the latter case has $r=1$ and loses its path configuration, leaving six.

## Exact computation

The verifier generates sunflowers by assigning each point to the core, to one private petal, or to no member. For orders 3 through 5 it also tests every choice of $n$ distinct subsets directly for equal pairwise intersections. It then tries deletion sets in increasing size on the union of the generated flowers, retaining all solutions at the first feasible size. It groups these solutions into orbits by applying adjacent swaps of the ground points. The search uses neither the deletion bound nor the equality cases to prune candidates.

| $n$ | Sunflowers | Minimum deletions | Forcing threshold | Labeled maximum families | Orbits |
|---:|---:|---:|---:|---:|---:|
| 3 | 10 | 3 | 6 | 4 | 2 |
| 4 | 15 | 4 | 13 | 49 | 6 |
| 5 | 21 | 4 | 29 | 25 | 2 |
| 6 | 28 | 5 | 60 | 615 | 7 |
| 7 | 36 | 5 | 124 | 210 | 2 |
| 8 | 45 | 6 | 251 | 8,610 | 7 |

Verified locally on 2026-11-25 with CPython 3.11.9 on macOS. An instrumented run of the script used 1.72 CPU seconds and 15.7 MiB peak resident memory.

## Source and reviewer checks

This is a side remark on the diagonal subcase k = n of Erdős problem 857. The problem page asks about fixed k and n tending to infinity, so the diagonal case is outside it, and nothing here settles or advances the problem. The entry is line 238 of ~/dev/quantum/ideation/mine_20261125/out/INDEX.tsv (counting the header). The retained extract in /private/tmp/erdos_rows.txt describes the non-uniform forcing threshold. The mining notes in out/misc_notes.md record that the downloaded Erdős files were deleted after extraction. Exact agreement with the Lean predicate is UNVERIFIED. The statement was not found on the problem page or in formal-conjectures; no wider literature search was made. The general two-parameter estimate remains open in the local index.

1. Compare the definition and its threshold convention with FormalConjectures/ErdosProblems/857.lean at revision 9097e2f, including whether one member may equal the core.
2. Check that the four flower types exhaust the possibilities and that the pair forced at $(e,s)=(0,2)$ cannot cover an outside point.
3. Check the equality cases and the exceptional orbit at $n=4$. Run python3 verify.py in this folder to reproduce the finite enumeration.
4. Search the literature before attributing novelty to the threshold or extremizer classification.

The value formula is also proved in Lean (`lean/`, theorem `R008.erdos857_diagonal`). The classification of extremal families is not formalised.
