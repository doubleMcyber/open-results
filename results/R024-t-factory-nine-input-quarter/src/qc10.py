"""Exact simulator for adaptive stabilizer protocols on noisy T states (lane QC10).

Written independently of seed/factory_probe.py (not read while writing this file).

Conventions
- n qubits; Pauli strings are written left to right for qubits 1..n. Qubit j (0-based
  string position) is bit (n-1-j) of a basis index.
- omega = exp(i*pi/4). A vector of amplitudes in Z[omega] is an int64 array of shape
  (4, 2**n): row k holds the coefficient of omega**k (omega**4 = -1).
- |T> = (|0> + omega|1>)/sqrt2. Fault pattern e: phi_e = Z^e |T>^{(x)n}. The common factor
  2**(-n/2) is dropped and every projection (I +- P)/2 drops its 1/2; callers track the
  power of two (norm^2 scale 2**(-n) * 4**(-#projections)).
- Real numbers of Q(sqrt2) are pairs (a, b) of Fractions meaning a + b*sqrt2.
- W = (X+Y)/sqrt2 = [[0, conj(omega)], [omega, 0]]. W|T> = |T>, W Z|T> = -Z|T>.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product

import numpy as np


# ---------------------------------------------------------------- Z[omega] arithmetic
def mulw(v: np.ndarray, k: np.ndarray) -> np.ndarray:
    """Multiply entry b of vector v (shape (4, D)) by omega**k[b]."""
    k = np.asarray(k) % 8
    out = np.zeros_like(v)
    for k0 in range(8):
        m = k == k0
        if not m.any():
            continue
        sub = v[:, m]
        res = np.zeros_like(sub)
        for j in range(4):
            e = j + k0
            sgn = 1
            while e >= 4:
                e -= 4
                sgn = -sgn
            res[e] += sgn * sub[j]
        out[:, m] = res
    return out


def conj_coeffs(v: np.ndarray) -> np.ndarray:
    """Complex conjugate: omega^-1 = -omega^3, omega^-2 = -omega^2, omega^-3 = -omega."""
    return np.stack([v[0], -v[3], -v[2], -v[1]])


def zw_mul_scalar(a, b):
    """Product of two Z[omega] scalars given as length-4 integer sequences."""
    r = [0, 0, 0, 0]
    for j in range(4):
        for k in range(4):
            e, s = j + k, 1
            if e >= 4:
                e, s = e - 4, -1
            r[e] += s * int(a[j]) * int(b[k])
    return r


def inner(u: np.ndarray, v: np.ndarray):
    """<u|v> as a Z[omega] scalar (list of 4 Python ints)."""
    cu = conj_coeffs(u).astype(object)
    vv = v.astype(object)
    m = [[sum(cu[j] * vv[k]) for k in range(4)] for j in range(4)]
    r = [0, 0, 0, 0]
    for j in range(4):
        for k in range(4):
            e, s = j + k, 1
            if e >= 4:
                e, s = e - 4, -1
            r[e] += s * m[j][k]
    return r


def zw_to_real(z):
    """A real element c0 + c1 w + c2 w^2 + c3 w^3 has c2 = 0, c3 = -c1; value c0 + c1 sqrt2."""
    c0, c1, c2, c3 = (int(t) for t in z)
    if c2 != 0 or c3 != -c1:
        raise ValueError(f"not real: {z}")
    return (Fraction(c0), Fraction(c1))


def zw_abs2(z):
    return zw_to_real(zw_mul_scalar([z[0], -z[3], -z[2], -z[1]], z))


def r_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def r_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def r_mul(a, b):
    return (a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def r_scale(a, s):
    s = Fraction(s)
    return (a[0] * s, a[1] * s)


def r_inv(a):
    d = a[0] * a[0] - 2 * a[1] * a[1]
    return (a[0] / d, -a[1] / d)


def r_float(a):
    return float(a[0]) + float(a[1]) * 2 ** 0.5


ZERO = (Fraction(0), Fraction(0))


# ---------------------------------------------------------------- Pauli operators
class Pauli:
    """i**ph * prod_j X_j^{x_j} Z_j^{z_j}; x, z are n-bit masks (qubit 1 = most significant)."""

    __slots__ = ("n", "x", "z", "ph")

    def __init__(self, n, x, z, ph=0):
        self.n, self.x, self.z, self.ph = n, x, z, ph % 4

    @classmethod
    def parse(cls, s: str) -> "Pauli":
        ph = 0
        if s[0] in "+-":
            ph = 0 if s[0] == "+" else 2
            s = s[1:]
        n = len(s)
        x = z = 0
        for j, c in enumerate(s):
            bit = 1 << (n - 1 - j)
            if c == "X":
                x |= bit
            elif c == "Z":
                z |= bit
            elif c == "Y":  # Y = i X Z
                x |= bit
                z |= bit
                ph += 1
            elif c != "I":
                raise ValueError(c)
        return cls(n, x, z, ph)

    def __mul__(self, o: "Pauli") -> "Pauli":
        # (X^x1 Z^z1)(X^x2 Z^z2) = (-1)^{z1.x2} X^{x1+x2} Z^{z1+z2}
        sgn = 2 * (bin(self.z & o.x).count("1") % 2)
        return Pauli(self.n, self.x ^ o.x, self.z ^ o.z, self.ph + o.ph + sgn)

    def neg(self) -> "Pauli":
        return Pauli(self.n, self.x, self.z, self.ph + 2)

    def commutes(self, o: "Pauli") -> bool:
        return (bin(self.x & o.z).count("1") + bin(self.z & o.x).count("1")) % 2 == 0

    def key(self):
        return (self.x, self.z)

    def __eq__(self, o):
        return (self.x, self.z, self.ph) == (o.x, o.z, o.ph)

    def __hash__(self):
        return hash((self.x, self.z, self.ph))

    def __repr__(self):
        out, ph = [], self.ph
        for j in range(self.n):
            bit = 1 << (self.n - 1 - j)
            xb, zb = bool(self.x & bit), bool(self.z & bit)
            if xb and zb:
                out.append("Y")
                ph -= 1  # X Z = -i Y
            elif xb:
                out.append("X")
            elif zb:
                out.append("Z")
            else:
                out.append("I")
        ph %= 4
        pre = {0: "+", 1: "+i", 2: "-", 3: "-i"}[ph]
        return pre + "".join(out)

    def conj_W(self, a: int) -> "Pauli":
        """W^a P W^a (W Hermitian). Per site: X -> Y = iXZ, Z -> -Z, XZ -> -iX."""
        x, z, ph = self.x, self.z, self.ph
        for j in range(self.n):
            bit = 1 << j
            if not a & bit:
                continue
            xb, zb = bool(x & bit), bool(z & bit)
            if xb and not zb:
                z |= bit
                ph += 1
            elif zb and not xb:
                ph += 2
            elif xb and zb:  # X Z -> (iXZ)(-Z) = -i X
                z &= ~bit
                ph += 3
        return Pauli(self.n, x, z, ph)

    def apply(self, v: np.ndarray) -> np.ndarray:
        """(P v)[y] = c(y^x) v[y^x] with c(b) = i^ph * (-1)^{popcount(b & z)} (X^x Z^z ordering)."""
        D = v.shape[1]
        idx = np.arange(D)
        src = idx ^ self.x
        par = np.array([bin(b & self.z).count("1") & 1 for b in range(D)])
        k = (2 * self.ph + 4 * par[src]) % 8
        return mulw(v[:, src], k)


def signed_group(gens):
    """All elements of the group generated by commuting Paulis, as {(x, z): ph}; None if -I appears."""
    elems = {}
    n = gens[0].n
    for bits in product((0, 1), repeat=len(gens)):
        p = Pauli(n, 0, 0, 0)
        for b, g in zip(bits, gens):
            if b:
                p = p * g
        if p.key() in elems:
            if elems[p.key()] != p.ph:
                return None
            continue
        elems[p.key()] = p.ph
    return elems


# ---------------------------------------------------------------- states
def basis_bits(n):
    idx = np.arange(2 ** n)
    return (idx[:, None] >> (n - 1 - np.arange(n))) & 1


def phi(n: int, e: int) -> np.ndarray:
    """Z^e |T>^n with the factor 2^(-n/2) dropped: amplitude (-1)^{e.x} omega^{|x|}."""
    D = 2 ** n
    idx = np.arange(D)
    wt = np.array([bin(b).count("1") for b in idx])
    par = np.array([bin(b & e).count("1") & 1 for b in idx])
    v = np.zeros((4, D), dtype=np.int64)
    v[0] = 1
    return mulw(v, wt + 4 * par)


def apply_W(v: np.ndarray, a: int, n: int) -> np.ndarray:
    """W on every qubit in mask a: W|0> = omega|1>, W|1> = omega^-1|0>."""
    D = v.shape[1]
    idx = np.arange(D)
    src = idx ^ a
    k = np.zeros(D, dtype=np.int64)
    for j in range(n):
        bit = 1 << j
        if a & bit:
            k += np.where(src & bit, 7, 1)
    return mulw(v[:, src], k)


def project(v: np.ndarray, P: Pauli, s: int) -> np.ndarray:
    """2 * (I + s P)/2 v = v + s P v (unnormalized)."""
    return v + s * P.apply(v)
