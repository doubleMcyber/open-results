"""Per-syndrome analysis of a fixed nine-qubit stabilizer code (route step 3, first probe).

Measure all r generators once (order irrelevant), get syndrome s in F_2^r. Branch s projects
onto the signed code Pi_s. For fault pattern e, Pi_s phi_e = Z^e Pi_{s+sigma(e)} phi_0, where
sigma(e) is the syndrome of Z^e, so only the 2^r vectors t_s = Pi_s phi_0 are needed.

Branch s is a valid order-2 T branch iff (i) q_s = ||t_s||^2 > 0, (ii) its logical state has
Bloch-vector moduli {1/sqrt2, 1/sqrt2, 0} (Clifford-equivalent to T: the octahedral rotation
group is transitive on cube edges), (iii) every pattern of weight <= 1 is harmless:
Z^e t_{s+sigma(e)} is zero or parallel to t_s.
A protocol accepting a set S of valid syndromes (each with its own Clifford decoder) has
A(p) = sum_{s in S} sum_e w_e ||t_{s+sigma(e)}||^2 and damage
H(p) = sum_{s in S} sum_e w_e (||t_{s'}||^2 - |<t_s|Z^e|t_{s'}>|^2/||t_s||^2), s' = s+sigma(e).
All arithmetic exact (Z[omega] integers, Q(sqrt2) fractions).
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from qc10 import (ZERO, Pauli, mulw, phi, project, r_add, r_float, r_inv, r_mul, r_scale,  # noqa: E402
                  r_sub, zw_to_real, zw_abs2)


def inner_fast(u, v):
    """<u|v> in Z[omega] using int64 (safe while |entries| * D stays below 2^31 squared)."""
    cu = np.stack([u[0], -u[3], -u[2], -u[1]])
    m = cu @ v.T  # m[j,k] = sum conj-coeff_j * coeff_k
    r = [0, 0, 0, 0]
    for j in range(4):
        for k in range(4):
            e, s = j + k, 1
            if e >= 4:
                e, s = e - 4, -1
            r[e] += s * int(m[j, k])
    return r


def apply_Z(v, e, n):
    D = v.shape[1]
    par = np.array([bin(b & e).count("1") & 1 for b in range(D)])
    return mulw(v, 4 * par)


def syndrome_vectors(gens, n=9):
    """t[s] = prod_k (I + (-1)^{s_k} g_k) phi_0 (unnormalized), s bit k = generator k (k=0 first)."""
    r = len(gens)
    leaves = {0: phi(n, 0)}
    for k, g in enumerate(gens):
        nl = {}
        for s, v in leaves.items():
            nl[s] = project(v, g, +1)
            nl[s | (1 << k)] = project(v, g, -1)
        leaves = nl
    return leaves


def sigma(e, gens):
    s = 0
    for k, g in enumerate(gens):
        if bin(e & g.x).count("1") & 1:  # Z^e anticommutes with g iff |e & x(g)| odd
            s |= 1 << k
    return s


def norm2(v):
    return zw_to_real(inner_fast(v, v))


def is_zero(v):
    return not v.any()


def analyse(gens, logicals, n=9, verbose=True):
    r = len(gens)
    t = syndrome_vectors(gens, n)
    q = {s: norm2(v) for s, v in t.items()}
    scale = Fraction(1, 2 ** n * 4 ** r)
    sig = [sigma(e, gens) for e in range(2 ** n)]
    zt = {}  # cache Z^e t_s' for weight <= 1 checks

    def harmless(s, e):
        sp_ = s ^ sig[e]
        if q[sp_] == ZERO:
            return True
        v = apply_Z(t[sp_], e, n)
        ov = zw_abs2(inner_fast(t[s], v))
        # parallel iff |<t|v>|^2 == ||t||^2 ||v||^2
        return r_mul(q[s], q[sp_]) == ov

    rows = []
    for s in range(2 ** r):
        if q[s] == ZERO:
            continue
        qq = r_scale(q[s], scale)
        bloch = []
        for L in logicals:
            val = zw_to_real(inner_fast(t[s], L.apply(t[s])))
            bloch.append(r_mul(val, r_inv(q[s])))
        mods = sorted(abs(r_float(b)) for b in bloch)
        tlike = abs(mods[0]) < 1e-12 and abs(mods[1] - 2 ** -0.5) < 1e-12 and abs(mods[2] - 2 ** -0.5) < 1e-12
        order1 = all(harmless(s, e) for e in [0] + [1 << j for j in range(n)])
        order2 = order1 and all(harmless(s, (1 << i) | (1 << j)) for i in range(n) for j in range(i))
        rows.append(dict(s=s, q=qq, bloch=bloch, tlike=tlike, order2=order1, order3=order2))
    return t, q, scale, sig, rows


def protocol_polys(S, t, q, scale, sig, n=9):
    """Exact accepted weight a_e and damage h_e for accepting syndrome set S."""
    acc, dmg = {}, {}
    for e in range(2 ** n):
        A, H = ZERO, ZERO
        for s in S:
            sp_ = s ^ sig[e]
            if q[sp_] == ZERO:
                continue
            v = apply_Z(t[sp_], e, n)
            ov = zw_abs2(inner_fast(t[s], v))
            A = r_add(A, q[sp_])
            H = r_add(H, r_sub(q[sp_], r_mul(ov, r_inv(q[s]))))
        acc[e] = r_scale(A, scale)
        dmg[e] = r_scale(H, scale)
    return acc, dmg
