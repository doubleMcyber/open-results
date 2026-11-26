# The square-plus-one star case of Erdős problem 552

The source is line 187 of `mine_20261125/out/INDEX.tsv`, entry `ErdosProblems/552.lean`. It asks for the two-color Ramsey number of a four-cycle against the star with **n leaves**. Copies are ordinary subgraphs and may have chords.

**Result.** Write S(n) for the star with n leaves. For every integer q ≥ 2,
R(C₄, S(q²+1)) ≤ q²+q+2. Equality holds for every prime power q. In particular, R(C₄, S(26)) = 32.

The argument below proves the general bound and uses a small exhaustive computation for one exceptional degree. The full determination for arbitrary leaf counts remains open in the cited index. Novelty is UNVERIFIED. The exact formula may already appear in the literature.

## An obstruction for graphs of minimum degree d

We prove that for every integer d ≥ 3, a simple graph on N = d(d−1)+2 vertices with minimum degree at least d contains a four-cycle. Suppose instead that G avoids four-cycles. Any two distinct vertices have at most one common neighbor. From a vertex x there are at least deg(x)(d−1) two-step walks that do not return to x, and they have distinct endpoints. There are just N−1 = d(d−1)+1 possible endpoints. Thus deg(x) = d for every x, and exactly one vertex p(x) distinct from x has no common neighbor with x. This relation is symmetric, so p partitions the vertices into pairs.

Write A for the adjacency matrix, P for the permutation matrix of p, J for the all-ones matrix and I for the identity. Counting common neighbors gives

    A² = (d−1)I + J − P.

Regularity gives AJ = JA, hence AP = PA. In particular p is an automorphism. Between two distinct pairs the edges form a matching of size two or there are no edges. Indeed, p exchanges the two endpoints in each pair, and a vertex cannot be adjacent to both members of another pair.

In the neighborhood of x, every vertex has exactly one neighbor within that neighborhood, except p(x) if present, which has zero. Counting the endpoints of this matching shows that x and p(x) are adjacent exactly when d is odd. For odd d every pair therefore has an internal edge. Any matching joining two pairs then completes a four-cycle with their internal edges. A joining matching exists since d ≥ 3. This disposes of odd d.

For even d let Q be the simple graph adjacency matrix on the N/2 pairs, with an edge for each joining matching. It is d-regular. On vectors constant on each pair, A acts as Q, P acts as I, and J acts as twice the all-ones matrix on pairs. Consequently

    Q² = (d−2)I + 2J.

On the constant vector Q has eigenvalue d. On its orthogonal complement all eigenvalues of the real symmetric Q are ±√(d−2). Since Q has zero diagonal, the zero trace forces d = m√(d−2) for some positive integer m. Thus √(d−2) is rational and hence is an integer t. It divides d = t²+2, so divides 2. The only even possibility is d = 6.

## The 16-pair computation for d = 6

There are 32 original vertices and 16 pairs. Every two distinct vertices in Q have exactly two common neighbors. Label the two vertices in each pair by bits. Its matching to another pair preserves or flips those bits. Write the corresponding edge bit as 0 or 1. On every four-cycle of Q the sum of its edge bits must be odd. An even sum lifts the four-cycle to a four-cycle in G through either starting vertex.

In particular Q cannot contain a K₄. Its three undirected Hamilton cycles would give three odd equations, yet each of the six edges occurs twice in their sum. In the neighborhood of a root, each of the six vertices has degree two within the neighborhood, since it and the root have two common neighbors. Two disjoint triangles would give a K₄ with the root. Hence the neighborhood is a six-cycle.

Label the root 0 and its cyclically ordered neighbors 1 through 6. Every pair of ring vertices already has the root as a common neighbor. Six of the fifteen pairs have one further common neighbor on the ring. Each of the other nine must have a unique common neighbor outside the root and ring. Each of the nine outside vertices has exactly two neighbors on the ring, by its common-neighbor count with the root. Thus the nine remaining ring pairs label the nine outside vertices bijectively. The checker labels them 7 through 15 by lexicographic order of their ring pairs.

Only edges among the nine outside vertices remain undecided. For each outside vertex the checker tries every choice of four of the other eight vertices. It checks its common-neighbor count with each ring vertex, then assembles rows in increasing order, enforcing symmetry and the common-neighbor count with each earlier outside vertex. Every possible Q with the chosen root and ring labels is represented. Direct checks on each completed graph verify all degrees and common-neighbor counts.

There is exactly one completion. It has 60 distinct four-cycles. Here is an odd parity certificate, with each row giving one cycle in cyclic order.

    0 2 1 6
    0 2 10 3
    0 3 4 5
    0 1 8 4
    0 4 14 5
    0 1 9 6
    1 6 9 8
    4 5 14 8
    1 2 10 9
    3 4 14 10
    8 9 10 14

Each edge occurs an even number of times across the eleven cycles. Adding their equations modulo two gives 0 = 1. This excludes d = 6 and finishes the obstruction.

## From the obstruction to the Ramsey number

Set d = q+1 and N = q²+q+2. In any coloring of the complete graph on N vertices which avoids a blue star with q²+1 leaves, each vertex has blue degree at most q². Every red degree is therefore at least q+1. The obstruction gives a red four-cycle.

For the lower bound, let q be a prime power and take the one-dimensional subspaces of the three-dimensional vector space over the field of order q. These give (q³−1)/(q−1) = q²+q+1 vertices. Join distinct points by a red edge when their representative vectors have zero dot product. Each orthogonal plane contains q+1 projective points, so deleting a possible self-incidence leaves red degree at least q. Two distinct points have independent representatives, and their two orthogonal planes intersect in a one-dimensional space. They have at most one common red neighbor. There is no red four-cycle, and every blue degree is at most q². This gives the lower bound on q²+q+1 vertices. For q = 5 the checker constructs all 31 points explicitly.

## Reproduction and review

Run `/usr/bin/python3 -B check.py` from this folder, with assertions enabled. The script uses the Python standard library. The worker ran it with Python 3.9.6 on macOS. The observed counts were 31 points, six of degree five and 25 of degree six, one labeled quotient completion, 60 squares, and an 11-square contradiction.

1. Check the distinct-endpoint count, the involution, and the parity of the matching in each neighborhood.
2. Check the action on pair-constant vectors and the trace argument, including the even-degree restriction.
3. Rerun the checker. Audit the root normalization and the completeness of the outside-row choices. Check the eleven displayed cycles and their edge parities.
4. Check the field construction in characteristic two as well as odd characteristic, and the translation from degrees to the number of leaves.
5. Literature priority and independent lead review are UNVERIFIED. No Lean formalization or cluster check was performed.
