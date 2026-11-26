"""Positive control for QC10 (route step 2), independent of seed/factory_probe.py.

1. Published schedule (arXiv:2610.31115v1, Prop. 7): measure the eight stabilizers, accept
   only all +1. Expect ideal acceptance 1/128, A(p) = D(p)/256, eps = N(p)/D(p), harmful
   counts 36,45,90,75,76,15,6,1 at weights 2..9, logical moduli {1/sqrt2, 1/sqrt2, 0}.
2. Reordered adaptive schedule (generators 7, 8, 1, 2 first, paper numbering from 1) with
   W^a corrections found here by search. Expect ideal acceptance 1/8, same eps(p).
Usage: python src/positive_control.py  (writes logs/positive_control.txt via tee)
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).parent))
from qc10 import Pauli, r_float, signed_group  # noqa: E402
from protocol import logical_expectations, run_schedule, weight_polys  # noqa: E402

GENS = ["-XZIIZIIIX", "+XIZIZIIXI", "+ZXZZIIXZI", "+ZZXIZXIIZ",
        "-YXYIXIIZZ", "-YYXXIIIII", "+IZIZZIZII", "+IIZZZZIII"]
N = 9


def correction_masks(earlier, g, n=N):
    """All a with W^a <earlier, -g> W^a == <earlier, +g> as signed groups."""
    want = signed_group(earlier + [g])
    out = []
    for a in range(2 ** n):
        conj = [h.conj_W(a) for h in earlier] + [g.neg().conj_W(a)]
        if signed_group(conj) == want:
            out.append(a)
    return out


def mask_str(a, n=N):
    return "{" + ",".join(str(j + 1) for j in range(n) if a >> (n - 1 - j) & 1) + "}"


def report(name, res, gens):
    A, H, harmful, p = weight_polys(res["acc"], res["dmg"])
    a0 = A.subs(p, 0)
    print(f"[{name}] ideal acceptance A(0) = {a0}")
    print(f"[{name}] branches surviving at p=0: {res['nbranches_ideal']}; "
          f"branches outside code space: {res['bad_branches']}")
    D = 2 - 15*p + 87*p**2 - 256*p**3 + 408*p**4 - 336*p**5 + 112*p**6
    Nn = 27*p**2 - 141*p**3 + 324*p**4 - 384*p**5 + 224*p**6 - 48*p**7
    ratioA = sp.simplify(A / (D / 256))
    ratioH = sp.simplify(H / (Nn / 256))
    print(f"[{name}] A(p) / (D(p)/256) = {ratioA};  H(p) / (N(p)/256) = {ratioH}")
    eps = sp.cancel(H / A)
    print(f"[{name}] eps(p) = {eps}")
    lead = sp.limit(eps / p**2, p, 0)
    print(f"[{name}] eps/p^2 at p->0 = {lead}")
    print(f"[{name}] harmful patterns by weight 0..9: {harmful}")
    # eps <= 20 p^2 on [0, 0.01]  <=>  20 A p^2 - H >= 0; divide by p^2 (H has p^2 factor)
    gap = sp.expand(sp.cancel((20 * p**2 * A - H) / p**2))
    roots = sp.Poly(gap, p).count_roots(0, sp.Rational(1, 100))
    g0 = gap.subs(p, 0)
    print(f"[{name}] 20 A - H/p^2: value at 0 = {g0}, real roots in [0, 1/100] = {roots}, "
          f"value at 1/100 = {sp.N(gap.subs(p, sp.Rational(1, 100)))}")
    print(f"[{name}] eps(0.01) = {sp.N(eps.subs(p, sp.Rational(1, 100)), 12)}, "
          f"eps(0.01)/1e-4 = {sp.N(eps.subs(p, sp.Rational(1, 100)) * 10**4, 12)}")
    L, vals = logical_expectations(res["target"], gens)
    print(f"[{name}] logical ops {L}; expectations {[r_float(v) for v in vals]} "
          f"exact {vals}")
    return A, H, eps


def main():
    t0 = time.time()
    gens = [Pauli.parse(s) for s in GENS]
    assert all(g.commutes(h) for g in gens for h in gens)
    grp = signed_group(gens)
    assert grp is not None and len(grp) == 256, "generators not independent / contain -I"
    print("stabilizers commute, independent, -I not in group: OK")

    pub = [(g, None) for g in gens]
    res_pub = run_schedule(pub)
    A1, H1, e1 = report("published", res_pub, gens)

    order = [7, 8, 1, 2, 3, 4, 5, 6]
    steps, earlier = [], []
    for k in order:
        g = gens[k - 1]
        masks = correction_masks(earlier, g)
        print(f"step g{k}: {len(masks)} valid W corrections; smallest: "
              f"{[mask_str(a) for a in sorted(masks, key=lambda a: (bin(a).count('1'), -a))[:4]]}")
        a = min(masks, key=lambda a: (bin(a).count("1"), -a)) if masks else None
        steps.append((g, a))
        earlier.append(g)
    res_ad = run_schedule(steps, check_gens=gens)
    A2, H2, e2 = report("adaptive-7812", res_ad, gens)
    print("eps identical to published:", sp.simplify(e1 - e2) == 0,
          "; A_adaptive / A_published =", sp.simplify(A2 / A1))
    print(f"elapsed {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
