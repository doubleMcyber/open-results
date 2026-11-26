# A sharp symmetry obstruction for AME(11,3)

For a pure eleven-qutrit stabilizer state, call a five-site set *deficient* if its reduced density operator differs from the identity divided by 243.

**Theorem.** Suppose the automorphisms of the stabilizer's Pauli label space, allowing site permutations and independent single-qutrit Clifford transformations, act transitively on the eleven sites. At least 33 of the 462 five-site sets are deficient. The minimum is exactly 33. An attaining state has every four-site reduction maximally mixed. In particular, an AME(11,3) stabilizer state would have intransitive site action even with these local changes of basis.

The source is physical line 139 of `out/INDEX.tsv`, entry `OpenQuantumProblems/35.lean`. Its local snapshot is `src/misc/fc/FormalConjectures__OpenQuantumProblems__35.lean` under `~/dev/quantum/ideation/mine_20261125/`. Lines 850–854 pose unrestricted existence. The following entry gives a circulant construction for eleven parties of local dimension four. This result settles the transitive stabilizer case in local dimension three. The unrestricted benchmark remains unresolved here. Novelty is UNVERIFIED.

## From transitivity to a cyclic shift

A pure qutrit stabilizer has an eleven-dimensional Lagrangian label space $L\subseteq(\mathbb F_3^2)^{11}$ for the sum of the sitewise alternating forms. Its automorphism group here is the stabilizer of $L$ in $\mathrm{SL}_2(3)^{11}\rtimes S_{11}$. Single-qutrit Cliffords induce these local symplectic changes on labels. Stabilizer eigenvalues affect only the phases in the partial-trace test below.

Transitivity implies that 11 divides the group order. Cauchy's theorem gives an element of order 11. The kernel of the permutation action lies in a group of order $24^{11}$, so the element permutes the sites in an 11-cycle. Transport a symplectic basis around that cycle using the element. The basis returns to itself because the eleventh power is the identity. In these local bases, after numbering the sites in cycle order, the element acts by the ordinary cyclic shift. These changes preserve supports up to relabeling. Conversely, invariance under the ordinary cyclic shift implies transitivity.

## Classification for a fixed shift

Write $R=\mathbb F_3[x]/(x^{11}-1)$. Encode each of the two Pauli coordinates as a polynomial whose coefficients are the site values. A shift-invariant linear space is an $R$-submodule of $R^2$, since the shift multiplies by $x$. Write $\bar f(x)=f(x^{-1})$ in $R$. The constant term of $u\bar z-v\bar w$ is the symplectic pairing of $(u,v)$ and $(w,z)$. Pairing against all shifts tests every coefficient. Thus orthogonality to the submodule is equivalent to vanishing of this polynomial for all its vectors.

Over $\mathbb F_3$ one has $x^{11}-1=(x-1)gh$, where

$$
g=x^5+x^4+2x^3+x^2+2,\qquad
h=x^5+2x^3+x^2+2x+2.
$$

Every nontrivial eleventh root has Frobenius orbit of size five, since the powers of 3 modulo 11 run through $1,3,9,5,4$. The quintics are therefore irreducible. Negation interchanges the two exponent orbits, so the involution fixes the scalar component and interchanges the quintic components in the Chinese remainder decomposition $R=\mathbb F_3\times K\times K'$. Both larger fields have 243 elements.

The component idempotents split every submodule into vector spaces on the three factors. A self-dual submodule chooses one of four lines on the scalar factor. On $K^2$ choose any subspace $U$. On $(K')^2$ the choice is forced to be its annihilator under the reciprocal pairing. In particular, for $U=K(1,t)$, a vector $(w,z)$ in the reciprocal component must satisfy $\bar z=t\bar w$, giving slope $\bar t$. The vertical line pairs with the vertical line. The zero and whole-plane choices pair with one another. Each choice yields a self-dual space, so there are $4(244+2)=984$ distinct labeled spaces for this shift.

The checker realizes the two minimal ideals using $a=(x-1)g$ and $b=(x-1)h$. Each vanishes in the other two factors and is invertible in its own field component. Its first five shifts form an $\mathbb F_3$-basis, since a nonzero polynomial of degree below five cannot vanish in that component. The all-ones vector spans the scalar ideal. The 243 representatives for $t$ of degree below five, the vertical line, and the two plane/zero choices give the generators in the computation.

## Exact cut test and witness

The density operator of a pure stabilizer state is the normalized sum of its stabilizer Paulis with their eigenvalue phases. The partial trace onto a set $S$ retains precisely the terms supported in $S$. Distinct retained labels give linearly independent Paulis on $S$. Thus $S$ is deficient exactly when a nonzero label in $L$ vanishes outside $S$. Equivalently the eleven generator rows, restricted to both coordinates on $S^c$, have rank below eleven over $\mathbb F_3$. Every nonempty proper subset has a shift orbit of size eleven, so 42 representatives cover the 462 five-site sets.

| Deficient five-site sets | Spaces with a quintic line | Spaces with a quintic plane/zero pair |
|---:|---:|---:|
| 33 | 360 | 0 |
| 66 | 0 | 8 |
| 132 | 120 | 0 |
| 154 | 120 | 0 |
| 165 | 120 | 0 |
| 176 | 120 | 0 |
| 286 | 120 | 0 |
| 462 | 16 | 0 |

For the witness take $[I_{11}\mid A]$, where $A$ is the symmetric circulant with first row $(0,0,0,0,1,2,2,1,0,0,0)$. Each successive row shifts right once. All 330 four-site reductions are maximally mixed. The 33 deficient five-site sets are precisely the cyclic translates of the following three sets, with sites numbered from zero.

$$
\{0,1,2,3,7\},\qquad \{0,1,3,5,6\},\qquad \{0,1,4,6,8\}.
$$

A second witness check enumerates labels $(v,vA)$ directly. A label of weight at most five must have $v$ supported on at most five sites. Normalize its first nonzero entry to one. Exactly one normalized label occurs on each of the 33 supports above, and none occurs on fewer sites. This test uses neither elimination nor orbit representatives to find the supports.

## Reproduction and review

Run `python3 -B check.py` in this folder. The script uses the Python standard library and exact arithmetic modulo three. I ran it locally with Python 3.11.9 and obtained the table, both witness counts and the three support orbits. The measured run used 2.42 CPU seconds or less and 18.2 MB peak resident memory or less. The checker verifies that all 984 spaces are distinct, isotropic, eleven-dimensional and invariant under the chosen shift.

- Check the reduction from transitivity to ordinary cyclic invariance and the reciprocal pairing of the field factors.
- Rerun the script, verify that the two column blocks correspond to the same site order, and reproduce the histogram and witness counts.
- Independently assess priority before making any novelty claim. Lead review and Lean verification are UNVERIFIED.
