# Which product of simplices has the largest projection-body volume?

Local source: INDEX.tsv, physical line 354, entry 088. In
`src/openai_math/chunks/c2.md`, lines 895–900, the abstract compares
two 10-simplices with a 20-simplex. The follow-up here optimizes over
all partitions of the dimension into simplex factors. Novelty: UNVERIFIED.

## Exact result

Write Δ_d for a full-dimensional d-simplex. For a full-dimensional
polytope K in dimension n, put P(K) = vol(ΠK)/vol(K)^(n−1), where
the support function of ΠK at a unit vector is the perpendicular projection
volume. In dimension one the projection onto a point has volume one.
Let M(n) be the largest P among Cartesian products of positive-dimensional
simplices of total dimension n, including a single simplex. Put

    S(d) = (d+1)d^d/d!
    B(n,k) = S(a)^(k−b) S(a+1)^b,   where n = ak+b, 0 ≤ b < k.

For every integer n ≥ 1, **M(n) is the larger of B(n,k) at the two
integers bracketing n/13**, with each k below 1 replaced by 1. At the
winning k, a product of k simplices whose dimensions differ by at most
one attains M(n). In every dimension the maximizing multiset of factor
dimensions is unique.

* The first dimension in which a product beats a simplex is **20**.
  Such a product exists in every dimension n ≥ 20.
* For n = 13q+j ≥ 100 and 0 ≤ j ≤ 12 the maximizer has a residue rule.
  If j ≤ 8, take j factors of dimension 14 and q−j of dimension 13.
  If j ≥ 9, take 13−j factors of dimension 12 and q+j−12 of dimension 13.
  Thus the rule also gives the exact recurrence M(n+13) = S(13) M(n)
  for every n ≥ 100. This onset is sharp: the recurrence fails at n = 99.

## Proof

**Geometric reduction.** For a facet F use its area vector v_F, its
(n−1)-volume times its outward unit normal. For a generic unit vector u,
the facets facing u project to a tiling of the shadow up to boundaries.
Each projected area is the positive part of ⟨v_F,u⟩. The opposite
direction gives the same area, hence the support function is
½ Σ_F |⟨v_F,u⟩|, also for other u by continuity. Thus ΠK is the
Minkowski sum of the centered segments with edge vectors v_F.
An invertible linear map T sends area vectors to |det T| T^(−transpose) v_F
(the normal direction and the base-times-height volume formula give this
transformation). The resulting projection-body volume scales by
|det T|^(n−1), so P is affine invariant.

The coordinate simplex conv(0,e_1,…,e_d) has volume 1/d! and area
vectors −e_i/(d−1)! and (1,…,1)/(d−1)!. The latter follows by projecting
the slanted facet onto each coordinate hyperplane. After scaling by
(d−1)! and translation, its projection body is the unit cube plus
the segment [0,(1,…,1)]. Its volume is d+1: in addition to the cube,
each of the d upper coordinate faces sweeps out a prism of volume one.
The swept interiors are disjoint since the first face reached by tracing
the negative diagonal from outside the cube is unique off a null set.
Dividing by (d−1)!^d and by (1/d!)^(d−1) gives P(Δ_d) = S(d).

For A and C of dimensions a and c and volumes V and W, the facets
of A×C come from either factor. Their vectors are (W v_F,0) and
(0,V v_G), respectively. The segment formula therefore gives
Π(A×C) = (W ΠA) × (V ΠC). Division by (VW)^(a+c−1) gives
P(A×C) = P(A) P(C). It remains to maximize a product of S-values.

**Balancing the factors.** Let r_d = S(d+1)/S(d) =
((d+2)/(d+1))(1+1/d)^d. Directly r_1 = r_2 = 3. Extend the
formula for r to real x ≥ 2. Its logarithmic derivative is

    log(1+1/x) − (x+3)/((x+1)(x+2)).

By strict convexity of 1/t, its integral over [x,x+1] is less than
(2x+1)/(2x(x+1)). This last bound is at most (x+3)/((x+1)(x+2))
precisely when x ≥ 2. Hence r_d strictly decreases from d=2 onward.
Replacing dimensions u,v with u+1,v−1 when v ≥ u+2 multiplies
the value by r_u/r_(v−1) ≥ 1. Each step decreases the sum of squares.
The balanced partition therefore attains B(n,k) at fixed k.

**Choosing the factor count.** Exact integer comparisons give

    S(d+1)^d > S(d)^(d+1) for 1 ≤ d ≤ 12,
    S(14)^13 < S(13)^14.

These are the first thirteen comparisons in verify.py. Let g interpolate
log S(d) linearly between integers d ≥ 1. On each interval g(x)/x
is a constant plus a constant divided by x, so its direction of change
is fixed by its endpoint values. It strictly increases through x=13.
At d=13 we have r_d < S(d)^(1/d). Whenever this holds, the geometric
mean S(d+1)^(1/(d+1)) of d copies of S(d)^(1/d) and one r_d lies
strictly above r_d, hence above r_(d+1). By induction g(x)/x strictly
decreases for x ≥ 13. Now log B(n,k) = k g(n/k) = n g(n/k)/(n/k).
The maximum for integer 1 ≤ k ≤ n is attained at a floor or ceiling
of n/13 clipped to this interval, as claimed.

**First dimension.** For 2 ≤ n ≤ 19 the exact checks in verify.py give
B(n,2) < S(n). In any proper partition in these dimensions, merging
two factors increases the product, since for their total m the best
two-factor value B(m,2) is smaller than S(m). In dimension 20 the ratio
B(20,2)/S(20) = 5588869/5505024 > 1. For n ≥ 20 this ratio of a
balanced pair to the simplex increases at each step: the multiplier
from n to n+1 is r_floor(n/2)/r_n > 1.

**Residue rule.** First suppose q ≥ 12. If j=0 the unique winning count is q. Otherwise the
candidate counts are q and q+1. With q ≥ 12 the two balanced products
have the dimensions listed in the result; their ratio (count q divided
by count q+1) is

    H(j) = r_13^j r_12^(13−j) / S(13).

It strictly decreases with j. The script checks H(8)>1>H(9) exactly.
At the winning count every unbalanced partition has a strictly
improving exchange: its average is at least 12, so its largest part is
at least 12, and transferring a unit from the largest to the smallest
uses the strict ratio inequality whenever their difference is at least
two. This proves uniqueness up to permutation. Increasing q by one
adds a 13-simplex in either case, proving the recurrence.

**Finite boundary and sharpness.** For n below 156 the script computes
the maximum and its multiplicity by integer partition. After processing
part size d, an optimal partition either omits d or uses at least one d.
In the latter class removing one d gives the subproblem for n−d with d
still allowed. The two classes are disjoint, so the update can count ties.
The initial empty partition has weight and multiplicity one. Exact
comparison gives multiplicity one throughout 1 ≤ n < 156 and the stated
residue rule throughout 100 ≤ n < 156. The unique optimizer at 99 uses
five 12s and three 13s; at 112 it uses eight 14s. Adding a 13 to the
first partition therefore falls strictly short of the second maximum.

## Review and reproduction

1. Run `python3 verify.py` in this folder. The finite certificates use
   rational arithmetic. The partition dynamic program checks the formula
   through dimension 240 and certifies the finite boundary above.
   Local run on 2026-11-25 with Python 3.15.2 passed all assertions.
2. Check the shadow normalization, the simplex prism decomposition and
   the facet vectors of the Cartesian product. These are written proofs.
3. Check the ratio derivative, interpolation and tail induction for the
   all-dimensional conclusion. The finite dynamic program only tests it.
4. Independent review, Lean formalization and literature priority are
   UNVERIFIED. The local abstract already gives the dimension-20 example.
