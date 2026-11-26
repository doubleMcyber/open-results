"""Adaptive measurement schedules on n noisy T inputs, simulated exactly for every fault pattern.

A schedule is a list of steps (P, a): measure signed Pauli P, keep outcome +1; on outcome -1
apply W^a (W = (X+Y)/sqrt2 on the qubits in bitmask a) and continue, or reject if a is None.
The simulator does not assume anything about the corrections: it projects, applies W^a
literally, and at the end checks that every surviving branch lies in the joint +1 eigenspace
of all measured operators (the code space the decoder expects).
"""
from __future__ import annotations

from fractions import Fraction

import sympy as sp

from qc10 import (ZERO, Pauli, apply_W, inner, phi, project, r_add, r_float, r_inv,
                  r_mul, r_scale, r_sub, zw_abs2, zw_to_real, signed_group)


def gf2_rank(rows):
    rows = [r for r in rows if r]
    rank = 0
    rows = list(rows)
    while rows:
        piv = max(rows)
        hb = piv.bit_length() - 1
        rows = [r ^ piv if (r >> hb) & 1 else r for r in rows if r != piv]
        rows = [r for r in rows if r]
        rank += 1
    return rank


def logical_ops(gens):
    """Two anticommuting Paulis that commute with all gens and are outside their span."""
    n = gens[0].n
    span = signed_group(gens)
    cands = []
    for x in range(2 ** n):
        for z in range(2 ** n):
            P = Pauli(n, x, z, 0)
            if (x, z) in span:
                continue
            if all(P.commutes(g) for g in gens):
                cands.append(P)
                if len(cands) > 40:
                    break
        if len(cands) > 40:
            break
    for i, A in enumerate(cands):
        for B in cands[i + 1:]:
            if not A.commutes(B):
                return A, B
    raise RuntimeError("no logical pair found")


def run_schedule(steps, n=9, check_gens=None):
    """Simulate every fault pattern. Returns dict with per-pattern acceptance a_e, damage h_e
    (Q(sqrt2) pairs, true values = int values * scale), the target vector, and diagnostics."""
    if check_gens is None:
        check_gens = [P for P, _ in steps]
    nproj = len(steps)
    scale = Fraction(1, 2 ** n * 4 ** nproj)
    finals = {}
    for e in range(2 ** n):
        branches = [(phi(n, e), ())]
        for (P, a) in steps:
            nb = []
            for v, hist in branches:
                vp = project(v, P, +1)
                if vp.any():
                    nb.append((vp, hist + (0,)))
                if a is not None:
                    vm = project(v, P, -1)
                    if vm.any():
                        nb.append((apply_W(vm, a, n), hist + (1,)))
            branches = nb
        finals[e] = branches
    # every surviving branch must be stabilized by all check generators
    bad = 0
    for e, brs in finals.items():
        for v, _ in brs:
            for g in check_gens:
                if not (g.apply(v) == v).all():
                    bad += 1
                    break
    target = [v for v, h in finals[0] if all(b == 0 for b in h)]
    assert len(target) == 1, "fault-free all-plus branch missing"
    t = target[0]
    tt = zw_to_real(inner(t, t))
    acc, dmg = {}, {}
    for e, brs in finals.items():
        A, H = ZERO, ZERO
        for v, _ in brs:
            vv = zw_to_real(inner(v, v))
            ov = zw_abs2(inner(t, v))
            A = r_add(A, vv)
            H = r_add(H, r_sub(vv, r_mul(ov, r_inv(tt))))
        acc[e] = r_scale(A, scale)
        dmg[e] = r_scale(H, scale)
    return dict(acc=acc, dmg=dmg, target=t, scale=scale, bad_branches=bad,
                nbranches_ideal=len(finals[0]))


def weight_polys(acc, dmg, n=9):
    p = sp.symbols("p")
    s2 = sp.sqrt(2)
    A = sp.Integer(0)
    H = sp.Integer(0)
    harmful = [0] * (n + 1)
    for e in range(2 ** n):
        w = bin(e).count("1")
        we = p ** w * (1 - p) ** (n - w)
        a, h = acc[e], dmg[e]
        A += (sp.Rational(a[0]) + sp.Rational(a[1]) * s2) * we
        H += (sp.Rational(h[0]) + sp.Rational(h[1]) * s2) * we
        if h != ZERO:
            harmful[w] += 1
    return sp.expand(A), sp.expand(H), harmful, p


def logical_expectations(t, gens):
    A, B = logical_ops(gens)
    C = A * B
    C = Pauli(C.n, C.x, C.z, C.ph + 1)  # i*A*B is Hermitian when A, B anticommute
    tt = zw_to_real(inner(t, t))
    out = []
    for L in (A, B, C):
        val = zw_to_real(inner(t, L.apply(t)))
        out.append(r_mul(val, r_inv(tt)))
    return (A, B, C), out
