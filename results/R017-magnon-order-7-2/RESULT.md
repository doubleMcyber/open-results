# Sharp range of the second lattice correction for matched ideal magnons

Source: physical line 535 of `out/INDEX.tsv`, ID 271. In the local
`src/openai_math/CONTENTS.md`, lines 6831–6849, the companion abstract
relates the nearest-neighbor magnetization deficit to the ideal-magnon
density through order five halves. A follow-up is to determine how much
the next ideal-gas coefficient can vary among dispersions that agree
through degree four. The following gives its exact range for one fixed
quartic Taylor polynomial. The energy and inverse temperature use units
in which the quadratic coefficient is one.

## Statement

Let R be an integer at least 2. Select one representative of every pair
of nonzero lattice vectors ±v in Z³ with max-coordinate norm at most R.
Let a_v be arbitrary nonnegative real weights, including zeros, and set

    E(k) = 2 ∑_v a_v (1 − cos(v·k)).

Assume the Taylor expansion at zero is

    E(k) = |k|² − (k₁⁴ + k₂⁴ + k₃⁴)/6 + O(|k|⁶).

On the torus with normalized Lebesgue measure define the infinite-volume
ideal-magnon density D(b) by integrating 1/(exp(b E(k)) − 1), for b > 0.
As b tends to infinity,

    D(b) = (4πb)^(−3/2) [ ζ(3/2) + (3/8) ζ(5/2)/b
                            + B ζ(7/2)/b² + O(b^(−3)) ].

The set of attainable B is the entire closed interval

    [(37 − 2R²)/128, 29/128].

Thus R = 5 is the smallest range that allows a negative B under the
stated matching. At R = 5 the endpoints are −13/128 and 29/128. If the
range is allowed to vary over finite integers, B has no lower bound.

Explicit R = 5 witnesses use identical weights on each axis. Taking
a₁ = 2/3 and a₂ = 1/12 gives B = 29/128. Taking a₁ = 23/24 and
a₅ = 1/600 gives B = −13/128. All unlisted weights are zero. Mixing
these weight vectors with respective fractions 13/42 and 29/42 gives
B = 0.

## Proof

The coefficient of k_i² k_j² for i ≠ j is −(1/2) ∑_v a_v v_i² v_j².
It vanishes by hypothesis. Each summand in that sum is nonnegative, so
every positive-weight vector lies on a coordinate axis. Write a_ij for
the weight of the pair ±j e_i, with 1 ≤ j ≤ R. Put
m_s(i) = ∑_j a_ij j^s. Matching pure powers gives m_2(i) = 1 and
m_4(i) = 2 on each axis. The numbers p_ij = a_ij j² therefore form a
probability distribution with mean 2 for the random variable X = j².
Each axis has positive weight at j = 1, since all other X are at least
4. In particular each axis dispersion has its only torus zero at 0.

The sixth moment m_6(i) equals the expectation of X². On the permitted
squares, (X − 1)(X − 4) ≥ 0, while (X − 1)(X − R²) ≤ 0. Taking
expectations gives

    6 ≤ m_6(i) ≤ R² + 2.

For J = 2 or J = R put p_iJ = 1/(J² − 1), p_i1 = 1 − p_iJ, and set
the remaining probabilities to zero. These choices have mean 2 and
give sixth moments 6 and R² + 2 respectively. Convex mixtures give
every intermediate moment, independently on each axis.

For the asymptotics let h_i(t) be the normalized circle integral of
exp(−t E_i(k)), where E_i is the contribution from axis i. Near zero,

    E_i(k) = k² − A k⁴ + C_i k⁶ + O(k⁸),
    A = 1/6,    C_i = m_6(i)/360.

Locally u = sign(k) sqrt(E_i(k)) is an odd analytic change of variable
with derivative one at zero, since E_i(k)/k² is even analytic and
positive there. Substitution into E_i(k(u)) = u² gives

    k(u) = u + (A/2)u³ + (7A²/8 − C_i/2)u⁵ + O(u⁷).

Integrate exp(−t u²) times the derivative of this series near zero.
The Gaussian even moments of orders two and four, divided by the
zeroth moment, are 1/(2t) and 3/(4t²), respectively. The derivative
remainder is O(u⁶) by analyticity, giving relative error O(t^(−3)).
Outside a fixed small interval E_i has a positive minimum by compactness.
Extending the local Gaussian polynomial integrals to the real line also
has exponentially small error. Including the normalization gives

    h_i(t) = (4πt)^(−1/2) [1 + 1/(8t)
                             + (35/384 − m_6(i)/192)/t² + O(t^(−3))].

The three circle integrals multiply because E is a sum over axes. The
three pairwise products of first-order terms contribute 3/64, so

    B = 41/128 − (m_6(1) + m_6(2) + m_6(3))/192.

For fixed weights, the full heat-integral error is O(t^(−9/2)) for all
sufficiently large t. Expand the Bose factor as ∑_{n≥1} exp(−nbE).
Monotone convergence permits termwise integration. Summing the heat
expansion at t = nb gives the displayed zeta factors and an absolute
error O(b^(−9/2) ζ(9/2)). The isolated singularity at k = 0 has
measure zero. Substituting the sharp moment endpoints proves the range.
Choosing the same mixture on each axis fills it, including both ends.

## Verification and scope

- Run `python3 check.py` in this folder. It evaluates the Gaussian
  expansion by expanding the exponential directly, an arithmetic route
  independent of the inverse series in the proof. It enumerates moment
  vertices for small R and checks both endpoints, mixtures and signs.
- Executed locally with Python 3.15.2. All assertions passed for
  R = 2 through 32. The nearest-neighbor normalization control, which
  uses quartic coefficient −1/12 on each axis, yields first correction
  3 ζ(5/2)/(128 π^(3/2)) in D(b), matching the local abstract at S = 1.
- Review the mixed-monomial coefficient, the two support inequalities,
  the Gaussian normalization and the sum of the heat remainders.
- The proof establishes the ideal density for each fixed interaction.
  The interacting magnetization at order seven halves is UNVERIFIED.
  The constants in the remainder may depend on the interaction and R.
- Novelty is UNVERIFIED. The local source is an abstract. Independent
  lead review and comparison with the literature are pending.
