# Equal rows in the sparse-bias window

Source: INDEX.tsv line 503, openai_math item 239, and the abstract “The sharp singularity rate for biased symmetric sign matrices” in src/openai_math/CONTENTS.md. The abstract treats a fixed bias. This follow-up concerns the same agreeing-row event as the probability of a minus sign tends to zero.

## Statement

Let the upper triangular entries, including the diagonal, of a symmetric sign matrix of order n be independent. Write q for the probability of a minus sign and a = 1-q. Let D be the event that two distinct rows agree and I the number of all-plus rows. Fix any real t and take q = (log n + t)/n for n sufficiently large. Write λ = exp(-t). Then

    P(D) → 1 - (1+λ) exp(-λ),
    P(D) - P(I ≥ 2) ~ (1+λ) exp(-λ) λ² (log n)² / (2n).

The second line measures the excess over the *finite-n* all-plus-row probability. Both statements concern equality of rows. Other mechanisms of singularity are outside their scope.

## Proof

View minus entries as edges of a graph with one possible loop per vertex. I counts vertices incident to no edge. For any fixed k, k specified vertices are isolated with probability a raised to kn-k(k-1)/2, the number of independent entries incident to them. The kth falling factorial moment of I is therefore (n)_k times this probability, tending to λ^k since n q² tends to zero. By the factorial moment criterion for Poisson convergence, I converges in law to Poisson(λ). In particular P(I ≤ 1) tends to h = (1+λ) exp(-λ).

Call an unordered pair of vertices a cherry if each has precisely one incident edge, both to the same third vertex. For a fixed pair, the three internal entries must be plus, and the entries to each outside vertex must both be plus except at one common neighbor. Its probability is exactly

    C = (n-2) q² a^(2n-3).

Writing X for the number of cherries, we obtain E[X] = binom(n,2) C, asymptotic to L = λ² (log n)²/(2n).

For a specified pair to agree, its three internal entries must be constant and its two entries to each outside vertex must agree. Put s = a²+q². For an agreeing pair that is neither isolated nor a cherry, either all three internal entries are minus, or at least two outside vertices are common minus neighbors. Its probability is bounded above by

    q³ s^(n-2) + binom(n-2,2) q⁴ s^(n-4).

The first term fixes the internal entries. The second chooses two common neighbors and drops the internal constraint. Since s^n/a^(2n) = (1+q²/a²)^n tends to one, these terms divided by C are respectively O(q/n) and O(n q²). Hence the expected count of such pairs is o(L).

Fix a cherry, including its center, and condition on its defining entries. The two leaves and center are nonisolated. Entries amongst the remaining n-3 vertices and from them to the center are still independent. For k specified remaining vertices to be isolated, k(n-2)-k(k-1)/2 further entries must be plus, since their entries to the two leaves were already fixed. The factorial moment argument above, with (n-3)_k choices, again gives P(I ≤ 1 | fixed cherry) → h.

Under the same conditioning the probability of any other cherry tends to zero. A fixed leaf cannot be a center, and the fixed center cannot be a leaf. Another cherry at the fixed center requires at least one further leaf there. The expected number of such leaves is (n-3) q a^(n-3): each needs its center edge and no edge within the remaining n-3 vertices, including its own loop. This expectation tends to zero. A cherry at a different center must use three remaining vertices. Summing over their choices and checking only entries internal to the remaining submatrix bounds its expected count by O(n³ q² a^(2(n-3)-3)), which tends to zero. These bounds do not depend on the labels of the fixed cherry.

Sum the conditional probabilities over choices of leaves and center. By the preceding two paragraphs E[X 1_{I≤1}] = (h+o(1)) E[X], while E[X 1_{X≥2}] = o(E[X]). Thus P(X≥1, I≤1) is asymptotic to hL. Any remaining contribution to P(D, I≤1) requires an agreeing pair that is neither isolated nor a cherry and has probability o(L). Since I≥2 implies D, this proves the second line. Combining it with the Poisson limit gives the first.

## Exact finite-size computation

For an independent check, partition the indices into blocks of sizes b₁,...,bᵣ. Requiring equal rows within each block forces one constant sign on each block rectangle (one triangle on a diagonal block). Their independent entry counts are bᵢbⱼ for i<j and bᵢ(bᵢ+1)/2 on the diagonal. The probability of the constraints is the product of a^m+q^m over these counts m. Multiply by the product over blocks of (-1)^(bᵢ-1)(bᵢ-1)! and sum over all set partitions. This gives P(D complement). Indeed for any realized matrix the surviving partitions refine its equal-row classes. Within each such class, the signed weights sum to the sum of permutation signs, by grouping permutations by their cycle supports. This sum is zero for class size at least two (pair permutations by a transposition) and one for a singleton.

For the isolated-row term use the same incident-entry count as in the proof:
    
    P(I ≤ 1) = Σ_{j=0}^n (-1)^j (1-j) binom(n,j) a^(jn-j(j-1)/2).

For a realized I=i the corresponding binomial sum through i is one at i=0,1 and zero thereafter, by the binomial theorem and its derivative. Subtracting P(D complement) gives the exact excess probability in the second line.

Local check: Python 3.11.9, command `python3 check.py`. All three coefficient comparisons passed for each order from 1 through 5 (33,866 matrices in total). For example, at order 5 exactly 110 matrices with three minus entries on or above the diagonal had agreeing rows and at most one isolated vertex.

## Review

1. Check the independent-entry counts, especially loops and edges to the conditioned cherry center.
2. Check the two conditional first-moment bounds for other cherries and the order of the non-cherry remainder relative to L.
3. Run python3 check.py from this folder. It compares complete coefficient vectors by exhaustive enumeration for n=1 through 5, including the count of cherries. Finite enumeration checks the identities. The limit and error scale use the written proof.
4. Novelty UNVERIFIED. The local abstract states the fixed-bias rate and supplies no priority evidence for this sparse-bias follow-up. Independent proof review and formal verification are pending.
