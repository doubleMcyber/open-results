# The normal Hessian at a product zero of the Werner endpoint inequality

Index row 89, arXiv 2606.03561, studies equality and criticality in the two-copy problem. The local follow-up in `out/short_npt.md`, item (2), asks for the Hessian and its null directions at higher-copy zeros. We settle this question at the aligned product zero below for every copy count, including four copies. The general four-copy inequality and the classification of its other zeros remain open here. Novelty is UNVERIFIED. The local source for the paper is its abstract in `src/arxiv/ext_werner.atom`.

## Statement

Let $d\ge 3$, $n\ge1$, $m=n-1$, $D=d^m$, and $h=2^{-m}$. On operators on $(\mathbb C^d)^{\otimes n}$ set
$$
 f(X)=\sum_{S\subseteq[n]}(-1/2)^{|S|}\|\operatorname{Tr}_S X\|_F^2 .
$$
Use unnormalized partial traces and the real Frobenius metric. On the first site let $P$ project onto the first two coordinate vectors. On the remaining sites let $o$ be the all-zero basis word. Put $X_0=P\otimes |o\rangle\langle o|$. In the smooth manifold of complex rank-two matrices consider
$$
 \mathcal Z=\{P_V\otimes R:\ V\subset\mathbb C^d\text{ a complex two-plane},
 P_V\text{ its orthogonal projector},\ R\in\mathbb C^{D\times D},\ \operatorname{rank}R=1\}.
$$

At $X_0$ the real Hessian of $f$ is positive semidefinite, its kernel is exactly $T_{X_0}\mathcal Z$ of real dimension $4d+4D-10$, and its smallest positive eigenvalue is $2h$. In a neighborhood of $X_0$ within the rank-at-most-two locus, $f\ge0$ and equality holds exactly on $\mathcal Z$. These assertions allow arbitrary complex perturbations and impose no trace or norm constraint.

The same spectrum holds with any chosen active site, any two-plane there, and any unit product vector in place of $o$. Site permutations and conjugation by a product of site unitaries preserve every term of $f$ up to permutation of the subsets, and act isometrically. The nearby equality family allows $R$ to use entangled spectator vectors. For example, when $m\ge2$, take $R=(|o\rangle+t|110\ldots0\rangle)\langle o|$. Its left factor has Schmidt rank two across the first spectator cut for every $t\ne0$.

For $(d,n)=(3,4)$ the Hessian has nullity 110 on a real tangent space of dimension 640 and smallest positive eigenvalue $1/4$. Its eigenvalues in units of $1/4$ and real multiplicities are

| Eigenvalue in units of $1/4$ | 0 | 1 | 2 | 3 | 4 | 5 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Multiplicity | 110 | 30 | 76 | 72 | 144 | 48 | 32 | 96 | 32 |

## Proof

Write $L(Y)=Y-\tfrac12\operatorname{Tr}(Y)I$. Expanding the tensor product gives $f(X)=\langle X,L^{\otimes n}X\rangle_F$, since the adjoint of a partial trace inserts an identity. At every $P_V\otimes R\in\mathcal Z$, the image under $L^{\otimes n}$ is $(P_V-I)\otimes L^{\otimes m}R$. It is orthogonal to the rank-two tangent space. Indeed tangent vectors are sums of matrices with column space in the column space of $X$ or row space in its row space, and both of those supports have first-site factor $V$. Thus every such point is critical. Multiplicativity and $\langle P_V,L(P_V)\rangle=0$ give $f=0$ there.

Let $J=\{(0,o),(1,o)\}$. Ordering $J$ first, a tangent vector has blocks $Y=\left(\begin{smallmatrix}A&B\\ C&0\end{smallmatrix}\right)$. The rank-two chart with top-left block $I+tA$, top-right $tB$, and bottom-left $tC$ has bottom-right block $t^2 C(I+tA)^{-1}B$. Consequently the quadratic Taylor coefficient $Q(Y)$ (half the real Hessian on $Y$) is
$$
 Q(Y)=f(Y)+2\operatorname{Re}\langle L^{\otimes n}X_0,\operatorname{diag}(0,CB)\rangle_F .
$$
The second term is essential. In the ambient matrix space, $L^{\otimes n}X_0$ is diagonal with entry zero when the first letter $k$ is 0 or 1, and entry $-h(-1)^{w(s)}$ at $(k,s)$ with $k\ge2$, where $w(s)$ counts the nonzero spectator letters.

For each spectator word $s$, group the entries of $B$ with exterior column $(k,s)$ into $B_s$ and those of $C$ with exterior row $(k,s)$ into $C_s$. At $s=o$ only $k\ge2$ occurs. At $s\ne o$ all $k$ occur. Superscripts $i,e$ below restrict $k$ to $\{0,1\}$ and its complement, respectively. Thus $B_s^i,C_s^i$ are two-by-two and $(B_s^e)^*$ has the shape of $C_s^e$. Write $M_0=M-\operatorname{Tr}(M)I_2/2$ for the traceless part of a two-by-two matrix. In the formulas $A_0$ denotes this part of $A$.

Different spectator words give orthogonal blocks in $Q$. To see this directly for $f(Y)$, note that $L$ fixes off-diagonal matrix units, and pairs a diagonal unit only with diagonal units. Pairing $|o\rangle\langle s|$ against $L^{\otimes m}(|o\rangle\langle t|)$ requires $s=t$ and then gives $h2^{w(s)}$. The same holds with both units transposed. Pairing opposite orientations gives zero unless both words are $o$. The normal correction involves only matching words since $L^{\otimes n}X_0$ is diagonal. On the first site the quadratic form of $L$ is $\|M\|^2-|\operatorname{Tr}M|^2/2$ with zero padding if needed. Substitution gives the following blocks (all norms are Frobenius).
$$
 Q_o/h=\|A_0\|^2+\|C_o-(B_o)^*\|^2.
$$
For $s\ne o$ and $b=2^{w(s)}$,
$$
 Q_s/h=b\big(\|(B_s^i)_0\|^2+\|(C_s^i)_0\|^2+
 \|B_s^e\|^2+\|C_s^e\|^2\big)
 -2(-1)^{w(s)}\operatorname{Re}\operatorname{Tr}(C_s^e B_s^e).
$$
Here $Q=\sum_s Q_s$. In the exterior pair make the real orthogonal change to $(C_s^e\pm (B_s^e)^*)/\sqrt2$. It diagonalizes the last two norms and the cross term, giving coefficients $b-1,b+1$ in some order. Counting complex entries as two real coordinates gives the spectrum of $Q/h$ (equivalently, the Hessian divided by $2h$).

| Word | Eigenvalue (real multiplicity) |
|---|---|
| $o$ | $0$ ($2+4(d-2)$), $1$ (6), $2$ ($4(d-2)$) |
| each $s\ne o$ | $0$ (4), $b$ (12), $b-1$ ($4(d-2)$), $b+1$ ($4(d-2)$) |

There are $\binom{m}{w}(d-1)^w$ words of weight $w$. Since $b\ge2$ for nonzero words, the least positive coefficient is 1. Adding nullities gives $4d+4D-10$. The manifold $\mathcal Z$ is locally embedded. The Grassmannian of two-planes has real dimension $4(d-2)$, and the manifold of nonzero rank-one complex $D$-square matrices has dimension $4D-2$. The map $(P_V,R)\mapsto P_V\otimes R$ has a smooth local inverse. Tracing out the first factor returns $2R$, and taking the spectator $(o,o)$ block and dividing by $R_{oo}$ recovers $P_V$ near $X_0$. Differentiating criticality along $\mathcal Z$ places its tangent space in the Hessian kernel. The dimensions agree.

Finally, take local coordinates $(u,v)$ on the rank-two manifold in which $\mathcal Z$ is $v=0$. There $f(u,0)=0$ and its first derivatives vanish. The $vv$ Hessian is positive definite at $X_0$ and stays uniformly positive in a sufficiently small coordinate box by continuity. Taylor's integral formula in $v$ gives $f(u,v)\ge c\|v\|^2$ there for some $c>0$. The leading two-by-two minor stays invertible in this box's ambient neighborhood, so the rank-at-most-two locus there consists entirely of rank-two points.

## Reproduction and reviewer checks

Run `python3 check.py` in this folder. The checker builds the real Hessian from the subset partial traces on matrix units, including the second-order rank constraint. It extracts the quadratic coefficient on explicit real and imaginary rank-two paths by evaluating each quartic at five integers. These checks distinguish the signs of the normal correction, which the eigenvalues alone cannot distinguish. All arithmetic is integral. The symbolic proof supplies the arbitrary-$n$ conclusion.

Worker run on 2026-11-25 with macOS system Python 3.9.6, command `/usr/bin/python3 check.py`. All spectrum and path checks passed for $(d,n)=(3,1),(3,2),(3,3),(3,4),(4,4)$. At $(4,4)$ the nullity was 262 out of 2040 real dimensions.

1. Check the unnormalized trace convention against the Werner endpoint functional and the factor of two between the Taylor coefficient and Hessian.
2. Independently derive the $CB$ term in the rank-two chart, including its sign for imaginary tangent directions. Check all spectator orientations and the orthogonal block diagonalization.
3. Rerun the checker. Inspect the full four-copy spectrum, the normal gap and the kernel dimension. Check the local critical-manifold argument separately.
4. Check publication priority, in particular results on normal Hessians at rank-two product zeros. The offline abstract does not establish priority. Independent review and formal verification are UNVERIFIED.
