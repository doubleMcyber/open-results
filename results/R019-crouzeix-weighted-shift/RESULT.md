# Stability of the sharp Crouzeix bound for finite weighted shifts

**Settled follow-up to INDEX.tsv line 589, family 325.** The catalogue reports
a universal constant 2 for matrix-polynomial evaluation on a numerical range.
For a finite weighted shift, how close does near equality force the weights
to an actual equality case? The bound below is independent of the number of
weights. All distances compare shifts in the same ordered orthonormal basis.

## Statement

Let S on C^n, n ≥ 2, send e_i to a_i e_{i+1} for i < n and e_n to zero,
with a_i > 0. Write W(S) = {x* S x : ‖x‖ = 1}, r = max{|z| : z ∈ W(S)},
and T = S/r, with weights u_i = a_i/r. Define C(S) as the least K such that
for every size d and every d-by-d matrix polynomial P(z) = Σ A_l z^l,
‖Σ T^l ⊗ A_l‖ ≤ K max_{z ∈ W(T)} ‖P(z)‖. This equals the constant for S
by changing the argument of the polynomial. Vector norms are Euclidean. Matrix norms are the induced operator norms.
The same definition of C applies to any nonzero nonnegative weighted shift.

1. C(S) is exactly the largest product of consecutive normalized weights,
   including the empty product 1. A scalar monomial attains it.
2. Write K = C(S) and δ = 1 − K²/4. Then K ≤ 2. There is a nonnegative
   weighted shift B of the same size with numerical radius 1, C(B) = 2, and
   ‖T − B‖ ≤ 2√δ = √(4−K²). One obtains B by replacing a single consecutive block
   and cutting its attachments. The block on two vertices has weight 2.
   On three or more vertices its two end weights are √2 and all others are 1.
   Every other weight outside the cut and block is preserved.
3. For positive weights K = 2 exactly when T is one of those full blocks.
   The distance bound is attained for each 0 < δ ≤ 1/16 by a three-vertex
   example, even with the best choice among all normalized nonnegative
   equality shifts in the same basis. Both the coefficient and exponent are sharp.

## Proof

Conjugation by diagonal phases rotates S by any angle. The unit sphere is
connected, its image W(S) contains zero, and its largest modulus is attained.
Consequently W(S) is the closed disk of radius r. Its rightmost point is
the largest eigenvalue of (S+S*)/2 by the Rayleigh principle. In particular
r is positive. Scaling now gives W(T) equal to the closed unit disk.

Let M be the maximum in part 1. Distinct nonzero columns of T^l have disjoint
supports, so ‖T^l‖ is the largest length-l product for 0 ≤ l < n. Taking
P(z) = z^l proves the lower bound. For the upper bound put d_1 = 1 and
d_{i+1} = max(1,u_i d_i). Induction identifies d_j with the largest suffix
product ending at vertex j, allowing the empty suffix. Thus max d_j = M.
For D = diag(d_j), D^{-1}TD has weights b_i = u_i d_i/d_{i+1} in [0,1],
and ‖D‖ ‖D^{-1}‖ = M.

Here is a direct matrix-polynomial bound for that last shift. The shift J
with all weights 1 acts on the powers 1,z,...,z^{n−1} in L² of the unit circle
by compressed multiplication by z (use normalized arc length). Tensor this
space with C^d for matrix polynomials. Each power is the compressed power, since
multiplication only raises degrees. Therefore ‖P[J]‖ ≤ max_{|z|=1} ‖P(z)‖.
Give edges independent random signs of means b_i. Each signed shift is a
diagonal-unitary conjugate of J (use cumulative products of signs). The
average of its l-th power is the l-th power of the shift with weights b_i,
since a length-l path uses distinct edges. Average the polynomial and apply
the triangle inequality, then conjugate by D ⊗ I_d. This proves part 1.
Also M > 1. Otherwise T would be a contraction attaining |x* T x| = 1
at a unit vector, forcing T x to be a unimodular multiple of x by equality
in Cauchy–Schwarz, impossible for a nilpotent matrix.

Take a positive eigenvector h of (T+T*)/2 for eigenvalue 1. It exists by
Perron–Frobenius for the connected nonnegative path matrix. Put p_n = 0
and p_i = u_i h_{i+1}/(2h_i) for i < n. The eigenvector equation gives
p_1 = 1 and 1−p_{i+1} = u_i h_i/(2h_{i+1}). Thus 0 < p_i < 1 internally.
For each interval of vertices [s,t] with s < t, multiplication gives

    (u_s ⋯ u_{t−1})² / 4
       = p_s (1−p_t) ∏_{s<j<t} [1−(2p_j−1)²].                    (1)

Indeed u_i² = 4p_i(1−p_{i+1}), and 4p_j(1−p_j) = 1−(2p_j−1)².
All factors in (1) are in [0,1]. Equality to 1 requires s = 1, t = n,
and every internal p_j = 1/2. This gives precisely the listed weights.
Conversely the listed blocks have radius 1. For the two-vertex block use
h = (1,1). For longer blocks use h equal to 1 at both ends and √2 inside.
Direct substitution gives (T+T*)h/2 = h and positivity gives the top
eigenvalue. Their full product is 2. This proves the exact equality claim.

Choose a maximizing interval [s,t], with s < t since M > 1. Set q = p outside
[s,t], q_s = 1, q_t = 0, and q_j = 1/2 internally. Give B the weights
2√(q_i(1−q_{i+1})). This replaces the block and cuts both attachments
when present. The remaining components are principal subshifts
of T and have numerical radius at most 1 by compression. The replacement
block has radius 1. Their direct sum B has radius 1 (its quadratic forms
are convex combinations of the component quadratic forms). Components
inherited from T obey the disk polynomial bound with constant K because
every power of a consecutive principal subshift is the corresponding
compression of the power of T. The replacement block has disk constant 2.
The norm of a direct sum is the largest summand norm, so C(B) = 2.

To estimate the change, set v(p) = (√p, √(1−p)) and let
F_j = ⟨v(p_j),v(q_j)⟩. Outside the interval F_j = 1. At the two ends
F_s² = p_s and F_t² = 1−p_t. At an internal vertex put g = 4p_j(1−p_j).
There F_j² = (1+√g)/2 ≥ g because 0 ≤ g ≤ 1. Multiplying and using (1)
shows ∏ F_j² ≥ 1−δ. Each F_j lies in [0,1], hence F_i² F_{i+1}² ≥ 1−δ.

For nonnegative unit vectors x,y of inner product f, any coordinate k obeys
|x_k−y_k| ≤ √(1−f²). Indeed, if x_k ≥ y_k, then
x_k−y_k ≤ x_k−f y_k ≤ ‖x−fy‖ = √(1−f²). Interchange x,y otherwise.
Apply this to the four-coordinate vectors v(p_i) ⊗ v(p_{i+1}) and
v(q_i) ⊗ v(q_{i+1}), whose inner product is F_i F_{i+1}. Their (1,2)
coordinates give half the old and new edge weights, respectively, including
at the cuts. Thus each weight differs by at most 2√δ. The difference of the
shifts has orthogonal columns, so its norm is the largest weight difference.

For sharpness fix 0 < η ≤ 1/16. Take n = 3 with weights
(2√η, 2√(1−η)). The symmetric part has eigenvalues 0 and
±√(u_1²+u_2²)/2, so r = 1. The first weight is ≤ 1/2 and the second is > 1.
Part 1 gives K = 2√(1−η), hence δ = η. There are exactly three normalized
nonnegative equality shifts here. The positive one has weights (√2,√2)
by the equality classification. A reducible one has a single
weight 2 and the other zero, since a lone edge has numerical radius half
its weight. The choice (0,2) has distance exactly 2√η, using
1−√(1−η) ≤ η ≤ √η. Both other choices differ on the first weight by at
least √2−1/2 > 1/2 ≥ 2√η. This establishes the claimed optimality.

## Exact computation and review

For p = (1,15/16,1/2,1/16,0), the squared weights are
(1/4,15/8,15/8,1/4). Their unique maximizing interval is the middle two
edges, so K = 15/8 and the scalar extremizer is z². The construction gives
B with squared weights (0,2,2,0). This example requires both attachments
to be cut.

I ran `python3 check.py` on macOS arm64 with Python 3.11.9. It checked all
781 profiles with two through six vertices and internal parameters in
{1/16,1/4,1/2,3/4,15/16}, including all 1,012 maximizing intervals with
ties counted. It checked 31 rational instances of the sharpness example.
The script uses tridiagonal determinants to certify the numerical radii and
rational comparisons to test the operator distances without rounding.

The local abstract supplies the motivating inequality. The proof above is
independent of the general theorem. Novelty is UNVERIFIED.
[Local catalogue, family 325]((local file))

- Run `python3 check.py` from this directory for exact rational certificates.
- Check the polynomial compression and averaging argument at arbitrary coefficient
  size, including compression onto either surviving exterior component.
- Check identity (1) for single-edge and boundary intervals, and the construction
  for intervals with no exterior component, one exterior component, or two.
- Check the adjacent-coordinate estimate giving the sharp coefficient and the
  three-vertex example against all normalized nonnegative equality cases.
- Check prior work on weighted shifts, spectral sets and stability of Crouzeix
  extremizers. Formal verification and independent lead review are UNVERIFIED.
