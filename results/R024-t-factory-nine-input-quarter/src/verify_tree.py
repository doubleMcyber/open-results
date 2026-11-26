"""Exact verification of an adaptive commuting-path tree (PREREG definitions).

Input: JSON tree {"measure": "+P", "plus": subtree, "minus": subtree} | {"leaf": [8 signed gens]}.
Checks: (1) structure: every leaf below the plus (minus) branch of a node contains +P (-P) in its
stabilizer, so leaves are reached by disjoint outcome strings and the accepted map is the sum of
the leaf projections; (2) each leaf's ideal output is T-like (logical Bloch moduli 0, 1/sqrt2,
1/sqrt2, exact); (3) exact accepted weight and damage per fault pattern (all 512), summed over
leaves; A(p), H(p), eps = H/A, criterion E: 20 p^2 A - H >= 0 on [0, 0.01] by exact root count.
"""
import json, sys
from pathlib import Path
import sympy as sp
sys.path.insert(0, str(Path(__file__).parent))
from qc10 import Pauli, ZERO, r_add, r_float, signed_group
from syndromes import syndrome_vectors, sigma, norm2, protocol_polys
from protocol import weight_polys, logical_expectations


def leaves(t, path=()):
    if "leaf" in t:
        yield [Pauli.parse(s) for s in t["leaf"]], path
    else:
        P = Pauli.parse(t["measure"])
        yield from leaves(t["plus"], path + (P,))
        yield from leaves(t["minus"], path + (P.neg(),))


def main(path):
    tree = json.load(open(path))
    L = list(leaves(tree))
    n = 9
    acc = {e: ZERO for e in range(2 ** n)}
    dmg = {e: ZERO for e in range(2 ** n)}
    for i, (g, pth) in enumerate(L):
        grp = signed_group(g)
        assert grp is not None and len(grp) == 256, "leaf is not an 8-generator stabilizer group"
        for P in pth:
            assert grp.get((P.x, P.z)) == P.ph, f"leaf {i} does not contain measured {P}"
        t = syndrome_vectors(g, n)
        q = {s: norm2(v) for s, v in t.items()}
        scale = __import__("fractions").Fraction(1, 2 ** n * 4 ** len(g))
        sig = [sigma(e, g) for e in range(2 ** n)]
        Lops, vals = logical_expectations(t[0], g)
        mods = sorted(abs(r_float(v)) for v in vals)
        assert abs(mods[0]) < 1e-12 and all(abs(m - 2 ** -0.5) < 1e-12 for m in mods[1:]), f"leaf {i} not T-like {mods}"
        a, h = protocol_polys([0], t, q, scale, sig, n)
        for e in range(2 ** n):
            acc[e] = r_add(acc[e], a[e]); dmg[e] = r_add(dmg[e], h[e])
        print(f"  leaf {i}: path {[repr(P) for P in pth]} ok, ideal acceptance {r_float(a[0])}", flush=True)
    A, H, harmful, p = weight_polys(acc, dmg)
    D = 2 - 15*p + 87*p**2 - 256*p**3 + 408*p**4 - 336*p**5 + 112*p**6
    Nn = 27*p**2 - 141*p**3 + 324*p**4 - 384*p**5 + 224*p**6 - 48*p**7
    print(f"leaves = {len(L)}; A(0) = {A.subs(p, 0)}")
    print(f"A / (D/256) = {sp.simplify(A / (D / 256))}; H / (N/256) = {sp.simplify(H / (Nn / 256))}")
    eps = sp.cancel(H / A)
    print(f"eps/p^2 at 0 = {sp.limit(eps / p**2, p, 0)}; harmful by weight {harmful}")
    gap = sp.expand(sp.cancel((20 * p**2 * A - H) / p**2))
    print(f"criterion E: gap(0) = {gap.subs(p, 0)}, roots in [0,1/100] = {sp.Poly(gap, p).count_roots(0, sp.Rational(1, 100))}, "
          f"gap(1/100) = {sp.N(gap.subs(p, sp.Rational(1, 100)))}")
    print(f"eps(0.01) = {sp.N(eps.subs(p, sp.Rational(1, 100)), 12)}")


if __name__ == "__main__":
    main(sys.argv[1])
