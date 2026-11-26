# Exact probability of an 81-edge terminal leave on 18 vertices

Starting from the labeled complete graph, choose a uniformly random present triangle and delete its three edges. Stop when no triangle remains. Write L_n for the final edge count. A finite follow-up to index row 452 (entry 188) asks for the probability of the largest possible leave. The local source gives an asymptotic mean-square theorem for the typical leave size. The finite question here is separately posed.

## Result

The maximum value of L_18 is 81, and its exact probability is

```text
P(L_18 = 81) = 24310 × (58663401763856177956784059601286130713524671 /
                       36145037108264537910963101921068441557322721632518144000000)^2.
```

This is approximately 6.40356903 × 10^(-26). The same calculation gives P(L_14 = 49) = 1716 × (683685 / 84749892731504)^2 and P(L_6 = 9) = 1/10.

## Why the extremal event is a bipartition

In a triangle-free graph on 2v vertices, the endpoints of an edge have disjoint neighborhoods. Summing the bound d(x)+d(y) ≤ 2v over all m edges gives Σ d(x)^2 ≤ 2vm. Cauchy–Schwarz gives Σ d(x)^2 ≥ (2m)^2/(2v), so m ≤ v². At equality every vertex has degree v. The neighborhood of any vertex is an independent v-set. Every vertex in this set needs all v neighbors in its complement. This gives precisely K_(v,v) and determines the unordered bipartition uniquely for v ≥ 1.

Fix a target bipartition. To leave all its crossing edges, every deletion must be internal to a part. To finish with exactly those crossing edges, the deleted triangles on each part must cover every internal edge exactly once. Such a set of triples is a Steiner triple system. Conversely every ordering of the blocks of a pair of such systems is a legal sequence ending at that target. Thus the displayed positive probabilities also prove attainment.

## Factorization for a prescribed complete bipartite leave

More generally, fix parts A,B of positive sizes a,b. Give every triangle of K_(a+b) an independent uniform priority on (0,1). Process the triangles in increasing priority order, accepting a triangle precisely when its edges are all still present. This generates uniform triangle removal. After an accepted deletion, the relative order of the remaining eligible triangles is uniform, since restriction of a uniform permutation to the surviving subset preserves uniformity.

Partition the triangle priorities into two lists. The A list contains triples wholly in A and triples having two vertices in A and one in B. Define an auxiliary process on A using just this list. Delete the edges of each available internal triangle in priority order. When encountering a mixed triple, declare failure if its unique A-edge is still present. The list succeeds if no failure occurs and it deletes every A-edge. Define the B process symmetrically. Until a first possible mixed deletion, every crossing edge remains present. Consequently the global process succeeds exactly when both lists succeed. The lists use disjoint priorities and are independent.

Let F(a,b) denote the A-list success probability. For any positive a,b the probability of a prescribed K_(a,b) leave equals F(a,b)F(b,a). For equal parts the probability of any such leave is binom(2v,v) F(v,v)^2 / 2. This division by two identifies the two orientations of a bipartition.

## Exact counting on one or two parts

For a fixed Steiner system D on v labeled vertices, let S be the blocks still to delete and t(S) the number of triangles in the union of their edges, including triangles outside D. At this state, 3v|S| mixed triples from this side are eligible because each living internal edge can be extended by any opposite vertex. The success probability for deleting exactly the specified remaining blocks obeys

```text
h(empty) = 1
h(S) = sum over d in S of h(S minus d) / (t(S) + 3v|S|).
```

The numerator sums only over prescribed blocks. Every other eligible triangle causes failure for this event. Summing h(D) over all labeled D gives F(v,v), since the deleted block sets identify disjoint events.

The companion script also runs the two-part recurrence directly. From (S,T) its denominator is t(S)+t(T)+3v(|S|+|T|). There is one successful successor per block in S or T, with that block deleted. The probability at (empty,empty) is 1. The script groups subsets by their size, triangle count and multiset of child types. Induction on size gives equal recurrence values within each type. The two-part computation does not use the factorization in its transitions.

To enumerate labeled designs, fix the pairs matched by blocks through vertex 0. Branch on the first uncovered edge and every triple through it whose edges are all uncovered. Each completion occurs once because exactly one of its blocks covers the chosen edge. There are (v−2)!! possible matchings, equivalent under relabeling. The script verifies that permutations of the pairs and swaps inside pairs take one fixed-link completion onto the entire set of fixed-link completions. Thus one design suffices for the two-side calculation. The one-side calculation evaluates every fixed-link completion separately, using explicit edge masks without grouping the states. The script asserts exact agreement between these two computations.

| Part size v | Completions with fixed link | Labeled designs | One-side subset types | Unordered splits |
|---:|---:|---:|---:|---:|
| 3 | 1 | 1 | 2 | 10 |
| 7 | 2 | 30 | 10 | 1,716 |
| 9 | 8 | 840 | 46 | 24,310 |

## An upper bound for all even orders

The same argument bounds this rare event without enumerating designs. For v ≥ 3 with v(v−1) divisible by 6, put k = v(v−1)/6. A successful side must make k internal deletions. If e > 0 internal edges remain, its triangle count t satisfies 3t ≤ (v−2)e by counting incident edge–triangle pairs. The chance that the next eligible triple on its list is internal is t/(t+ve) ≤ (v−2)/(4v−2). Applying this bound at each of the k deletions and using independence of the sides gives

```text
P(L_(2v) = v²) ≤ binom(2v,v)/2 × ((v−2)/(4v−2))^(v(v−1)/3).
```

If v(v−1) is not divisible by 6, the extremal event is impossible by the internal edge count. For even v ≥ 2 it is also impossible because internal triangle deletion always preserves vertex-degree parity.

## Reproduction and reviewer checks

1. Run `python3 -B check.py` from this folder. Use standard-library Python with assertions enabled. The printed probabilities are reduced fractions.
2. Check the equality case in the edge bound, then the disjointness of the labeled partition and triangle-system events. In particular the split multiplier for 18 is 24,310, and the two sides have independent choices of labeled systems.
3. Check the treatment of mixed triples in both derivations. A single remaining edge has nine mixed extensions for v=9. The denominator includes all available internal triangles.
4. Compare the one-side fraction squared times the split count with the direct two-side computation. For K_6, any first triangle leaves ten eligible triangles, only one of which is vertex-disjoint from it. This gives a hand check of 1/10.

Local source: `~/dev/quantum/ideation/mine_20261125/src/openai_math/CONTENTS.md`, entry 188, lines 4352–4361. The exact finite computation was run locally. Independent lead reproduction and formal verification are UNVERIFIED. Novelty is UNVERIFIED.
