# Degree 175 is minimal for ten very general 55-fold points

## Statement

Let ζ be a primitive complex fifth root of unity. In the affine chart Z=1 of
the complex projective plane, take the ten points

$$
  (ζ^k,ζ^{2k}),\qquad (2ζ^k,7ζ^{2k}),\qquad 0\le k<5.
$$

For d ≥ 0 let V(d,m) be the vector space of homogeneous degree-d forms
vanishing to order at least m at all ten points. Then for m = 55,

$$
  \dim V(d,55)=\max\{0,\tbinom{d+2}{2}-15400\}.
$$

In particular V(174,55) is zero and V(175,55) has dimension 176.
The same formula holds for ten very general complex projective points.
In both configurations a general degree-175 member is irreducible, has an
ordinary 55-fold point at each specified point, and is smooth elsewhere.
The calculation also gives the corresponding dimension formula with
10 binom(m+1,2) conditions for m equal to 1, 6 and 12.

## Relation to the source

The local source is entry 039, “Nagata’s conjecture and maximal Seshadri
constants”, in [the local source catalogue](../../../ideation/mine_20261125/src/openai_math/CONTENTS.md),
lines 1101–1110 ([index](../../../ideation/mine_20261125/out/INDEX.tsv), line 308). Its abstract states that
10m < d√10 for a nonzero curve at ten very general points of equal
multiplicity m. At m = 55 this permits d = 174, since 174² = 30276
and 10·55² = 30250. The finite follow-up asks whether equality between
the counts of conditions and coefficients at d = 174 forces emptiness.
The answer is yes. The proof below is independent of the source's theorem.
Novelty is UNVERIFIED.

## Proof and exact computation

1. Dehomogenizing identifies degree-d forms with polynomials in x,y of
   total degree at most d. Order at least m at (u,v) means that every
   coefficient of SᵃTᵇ in f(u+S,v+T) vanishes for a+b<m.
   These are binom(m+1,2) linear conditions per point.

2. Substitution (x,y) ↦ (ζx,ζ²y) preserves the set of points, hence the
   kernel of the jet map. Write T for this substitution. The projection
   onto weight r sends f to the sum of ζ⁻ʳᵏ Tᵏf/5 over k=0,…,4.
   Thus if f is in the kernel then each weight component is too.
   The r-component is spanned by xⁱyʲ with i+2j ≡ r modulo 5.
   For a weight-r polynomial, vanishing to order m at one orbit
   representative implies the same at every point in that orbit, by
   invertibility of the coordinate substitution and its scalar action.
   The two orbits have five points each and are disjoint since their
   first coordinates have different absolute values.

3. In weight r, use the representatives (u,v)=(1,1),(2,7). Multiply
   each jet equation by uᵃvᵇ. The matrix entry for column (i,j) and
   row (u,v,a,b) is the integer

   $$
      \binom{i}{a}\binom{j}{b}u^iv^j.
   $$

   An out-of-range binomial coefficient is zero. At the degrees below,
   each of the five blocks is square of order m(m+1), as direct counting
   in check.py verifies. The table gives their determinants modulo 1009.
   Columns are ordered by (i,j) lexicographically. Within each point the
   rows are ordered by (a+b,a) lexicographically.

| m | d | Block order | r=0 | r=1 | r=2 | r=3 | r=4 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 2 | 97 | 668 | 1006 | 1003 | 988 |
| 6 | 19 | 42 | 622 | 450 | 539 | 806 | 222 |
| 12 | 38 | 156 | 940 | 545 | 663 | 328 | 710 |
| 55 | 174 | 3080 | 466 | 343 | 54 | 188 | 719 |

The residues certify that each integer determinant is nonzero. The
fifth root occurs only in the complex decomposition, so the modular
computation needs no choice of a fifth root in the prime field.

4. In each displayed degree the full jet map is injective, and its
   domain and target both have dimension 10 binom(m+1,2). It is therefore
   bijective. For smaller degrees the affine polynomial spaces are
   subspaces of this domain and retain injectivity. Larger polynomial
   spaces contain this domain and retain surjectivity. Rank-nullity
   gives the claimed formula in every degree.

5. For varying ordered affine points, the full jet matrix has polynomial
   entries in the twenty coordinates. Its determinant in the displayed
   degree is nonzero at the configuration above. It stays nonzero on a
   nonempty Zariski open set of ten-point configurations. The same
   degree argument applies throughout that set, hence at very general
   projective points. The intersection for all four m contains our
   exhibited configuration.

## Geometry in the first nonempty degree

Blow up the ten points and write H for the pullback of a line and Eᵢ
for the exceptional curves. The degree-175 system on the blowup has
divisor class D = 175H − 55ΣEᵢ. We show that this system has no base point.

For any Q away from the ten centers, choose a line L through Q avoiding
the centers and a degree-175 form M nonzero at Q. At the centers, M/L
defines jets of a degree-174 section. By jet surjectivity choose a
degree-174 form G with those jets through order 54. Then M − LG is in
the required system and is nonzero at Q. This construction also applies
to a point Q at infinity, since all prescribed jets are at the centers.

At a center P, prescribe any homogeneous degree-54 local polynomial
as the jet of G at P, with lower coefficients zero and all jets zero at
the other nine centers. Multiply G by a line through P. The degree-55
leading terms obtained this way span every binary form of degree 55,
since each degree-55 monomial is a local coordinate times a degree-54
monomial. Hence restrictions to Eᵢ span its entire degree-55 system.
This proves freedom from base points there. A general member meets each
Eᵢ in 55 distinct simple points, because binary forms with a repeated
root form a proper closed set, and there are only ten Eᵢ.

Now D² = 175² − 10·55² = 375. A base-point-free system with image of
dimension at most one has self-intersection zero (two general hyperplane
sections have disjoint pullbacks). Its image here is therefore a surface.
Bertini's smoothness and irreducibility theorems over the complex numbers
give a smooth irreducible general member on the blowup. Blowing down the
Eᵢ yields the stated ordinary singularities.

## Local verification

On November 25, 2026, CPython 3.11.9 and NumPy 2.4.2 on macOS reproduced
the table in 43.92 CPU seconds with peak resident memory 310,558,720 bytes.
A separate calculation without the weight decomposition used all ten actual points over GF(101),
with ζ = 36. Using unscaled Taylor coefficients, ordering columns by
(i+j,i), points by orbit then k, and rows at each point by (a+b,a),
ordinary integer modular elimination gave determinants 78, 3 and 47
for m = 1, 6 and 12 respectively. The degree-174 result uses the five
modulo-1009 blocks in the table.

## Reviewer checks

- Run `python3 -B check.py` from this folder with NumPy installed. Compare
  all twenty residues with the table. To check a single block, for example,
  run `python3 -B check.py --case 55 --residue 0`.
- Check the block elimination against ordinary modular PLU. The script
  swaps whole rows, stores the multipliers below the diagonal, and
  multiplies the pivots with the row-permutation sign. The largest
  binary64 dot product uses at most 32 terms of size at most 1008².
  Including the subtraction its absolute value is below 33 million,
  so every intermediate integer is exactly representable.
- For an independent computer-algebra check, construct the matrices in
  step 3 directly over GF(1009) in the specified order and take their
  determinants. Confirm that multiplicity uses all a+b<m and that
  ordinary vector-space dimension counts forms before projectivization.
- For the geometric corollary, check surjectivity onto leading forms at
  each center and the image-dimension hypothesis for Bertini.
- Independent lead reproduction and literature priority are UNVERIFIED.
