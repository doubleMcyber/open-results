# At most 34 perfect balanced cuts for an eight-party GF(4) graph state

Among all symmetric, zero-diagonal 8 × 8 matrices A over
F = GF(4), the maximum number of unordered balanced cuts S | T with
det A[S,T] ≠ 0 is **34 out of 35**. The edge weights may vary independently.
Equivalently, an eight-ququart GF(4) graph state can have 34 maximally
mixed balanced cuts, but every such state has at least one deficient cut.

The target is the graph-state subcase of `ame_8_4_open` in INDEX.tsv line
267, APNOutputs/AICollaborator/QuantumOptics/35.lean (lines 759–763).
[Local benchmark source]((local file))
The unrestricted existence of AME(8,4) remains unresolved by this work.
Novelty UNVERIFIED. The proof below uses exact finite enumeration.
There is no Lean build or formal proof certificate.

## Graph states and a sharp example

Write F = {0,1,t,t+1}, where t² = t+1, and Tr(z) = z+z². For x ∈ F⁸
the normalized state amplitude is 4⁻⁴ (−1)^Tr(Σ_{i<j} Aᵢⱼ xᵢxⱼ).
Up to a sign, entry (u,v) of the reduced state on a balanced side S is
4⁻⁸ times the sum over y ∈ Fᵀ of (−1)^Tr((u−v)ᵗ A[S,T] y).
The character sum is 4⁴ if (u−v)ᵗ A[S,T] = 0 and is zero otherwise.
For a nonzero coefficient c, translating its y-coordinate by t/c changes
the sign of every summand. Hence the marginal is I/4⁴ exactly when the cut
matrix is invertible. The complement has the transposed cut matrix.

For a witness, impose (0123)(4567) symmetry and assign the following
weights to edge-orbit representatives, extending by the permutation.

| Edge | 01 | 02 | 04 | 05 | 06 | 07 | 45 | 46 |
| ---- | -- | -- | -- | -- | -- | -- | -- | -- |
| Weight | 0 | 1 | 0 | 1 | 1 | 1 | 1 | t |

Checking all 35 determinants leaves precisely {0,2,4,6} | {1,3,5,7}
singular. The rest of the proof rules out 35 for an arbitrary A.

## Only two cut-determinant patterns need testing

Index cuts by the lexicographically ordered four-subsets containing 0.
Write p(S) = det A[S,Sᶜ], and use p(Sᶜ) = p(S) for either side of a cut.
For a perfect matching M of the eight vertices, let v(M) be its binary
35-vector indicating the cuts it crosses on every edge. In characteristic
two the determinant expansion gives the vector identity

    p = Σ_M (Π_{ij∈M} Aᵢⱼ) v(M).

Let H be the binary span of the 105 vectors v(M). Both binary coefficient
planes a,b of p = a + t b must belong to H. Binary elimination gives
dim H = 14. Enumerate the ordered pairs in H × H whose bitwise union
covers all 35 cuts. Exactly 10,800 survive. Permuting the eight vertices
and permuting the three nonzero field values splits these into two orbits.
A field-value permutation is a global nonzero scalar times the identity
or Frobenius. Scaling all edges at one vertex multiplies every p(S) by
the scalar, and field conjugation acts entrywise on A. These operations
therefore preserve realizability.

| Binary planes (bit 0 is the first cut) | Orbit size |
| --- | ---: |
| (2609868375, 32069500861) | 10,080 |
| (2908840579, 32061185917) | 720 |

The following necessary conditions exclude both representatives.

## Recovering necessary two-by-two blocks

Use the 8 × 16 generator matrix [I₈ | A], with columns grouped in pairs
(Xᵢ,Zᵢ) for each vertex i. Selecting four entire pairs with vertex set R
has determinant p(R) by expansion along the four unit columns. On a pair
use the alternating form J = [[0,1],[1,0]]. The rows are mutually
orthogonal for the direct sum of these forms because A is symmetric.

Let U = {0,1,2,3}. If every p(R) is nonzero, the eight columns for U are
invertible. Multiply all rows on the left by their inverse, obtaining
[I₈ | B] in paired column order, where B is a 4 × 4 array of 2 × 2 blocks.
Output pair j denotes vertex 4+j. For equally sized index sets I,K in
{0,1,2,3}, expansion along retained input columns gives

    det B[I,K] = p((U ∖ I) ∪ {4+j : j∈K}) / p(U).

Set dᵢⱼ = det Bᵢⱼ. Each is nonzero. Write J₄ for four diagonal copies of J.
Row orthogonality gives B J₄ Bᵗ = J₄. In particular B is invertible,
and inversion gives Bᵗ J₄ B = J₄.

Normalize Cᵢⱼ = Bᵢ₀⁻¹ Bᵢⱼ B₀ⱼ⁻¹ B₀₀. Every block of its first row and
first column is the identity E. Set βᵢ = dᵢ₀ and αⱼ = d₀ⱼ/d₀₀. The target
determinant of a square block subarray C[I,K] is now explicitly known:

    h(I,K) = det B[I,K] / ((Π_{i∈I} βᵢ)(Π_{j∈K} αⱼ)).

For i > 0, row orthogonality against block row 0 gives Σⱼ αⱼ Cᵢⱼ = 0.
For j > 0, column orthogonality against block column 0 gives
Σᵢ βᵢ Cᵢⱼ = 0. To see both identities, substitute
Bᵢⱼ = Bᵢ₀ Cᵢⱼ (B₀₀⁻¹ B₀ⱼ) and use X J Xᵗ = Xᵗ J X = (det X)J
for every 2 × 2 matrix X. The remaining outer factors are invertible.

For each i = 1,2,3 enumerate possible block rows (E,X,Y,Z).
Each nonfirst block W at column j must satisfy det W = h({i},{j}) and
det(E+W) = h({0,i},{0,j}), by subtracting the top block row of the latter
minor from the bottom one in the normalized two-by-two block array.
Choose X,Y among the 256 two-by-two matrices subject to these tests.
The row relation determines Z = (α₀E + α₁X + α₂Y)/α₃.
Test Z and the other three two-column minors on block rows 0,i.
For columns j,k their determinants are det(Cᵢⱼ + Cᵢₖ), by block elimination.

Choose candidate rows 1 and 2. The column relations determine row 3 on
columns 1,2,3, and C₃₀ = E. Require the resulting row to be in the row-3
list. Finally test the single 4 × 4 minor on block rows and columns {1,2}
against h({1,2},{1,2}).

| Orbit size | Row options for 1,2,3 | Row pairs passing row 3 | Passing final minor |
| ---: | --- | ---: | ---: |
| 10,080 | 12,60,12 | 0 | 0 |
| 720 | 60,60,60 | 120 | 0 |

A witness would have passed every test. The upper bound follows.

## Equivalent linear-code statement

An eight-dimensional F-linear totally isotropic subspace of (F²)⁸ has
at most 34 unordered balanced cuts on which projection to four coordinate
pairs is bijective. The same example attains 34. To pass to graph form,
take an eight-row generator matrix. From each coordinate pair select one
column, maximizing the rank r of the selection. Swap within pairs to call
the selected columns X and the others Z. Such swaps preserve J in
characteristic two. Relabel so the first r columns of X are independent.
If r < 8, choose row coordinates making the last 8−r rows of X zero.
For a site outside the first r, its Z column must also have zero bottom
part, since swapping it into the selection would otherwise increase r.
Each bottom generator row is therefore supported only on the Z columns
of the first r sites. Orthogonality against every generator row makes
its entries there the coefficients of a zero combination of the
independent first r columns of X. A zero generator row contradicts full rank, so X is invertible.
Row reduction gives [I | A] with A symmetric by isotropy. Subtract AᵢᵢXᵢ
from Zᵢ to clear its diagonal. The changes within coordinate pairs and the
common row operations preserve bijectivity of every four-pair projection.

## Reproduction

Run `python3 -B verify.py` from this folder, with no dependencies beyond
the standard library. In addition to both exclusion counts above, the
34-cut example passed the same block test with row-list sizes 60,76,60
and 60 row pairs passing the final minor. A separate local calculation
normalizing the first block row and column to diag(1,dᵢⱼ), with direct
4 × 4 determinants, reproduced both exclusion rows of the table.
The verifier ran locally under CPython 3.11.9 on Darwin arm64.

## Reviewer checks

1. Run the verifier with Python 3.11 or later. Check the
   sharp example independently and reproduce both orbit sizes and both
   obstruction counts. Check that the same obstruction test accepts the
   sharp example's determinant pattern as a positive control.
2. Audit the matching expansion, field-value action and normalization
   of the paired minors. The exclusion uses row and column orthogonality.
3. Search for prior GF(4)-linear stabilizer or quantum MDS code results,
   including a GF(4)-linear pure [[8,0,5]]₄ code. Novelty and independent lead review
   are UNVERIFIED. This argument does not test arbitrary quantum states.
