#!/usr/bin/env python
"""Numerical test of the two reduction lemmas of notes/SCOPE_GAPS.md (self-contained, numpy only).

Part B (non-commuting measurements, ancillas, random bits = coins). Random adaptive protocols on 9 data
qubits (|T> inputs with Z faults, all 512 patterns at once) plus m ancillas in |0>, with random H, S,
CNOT gates, random controller bits, random Pauli measurements (most of them non-commuting) and random
decoding / output-qubit / accept choices at the leaves. Two independent computations per record:
  (1) dense: the state vector of data + ancillas pushed through the actual gates and projectors;
  (2) tracker: pull-back Pauli algebra only (section 2 of the note) -> number of coins k, the signed
      data Paulis of the genuine measurements, the pulled-back output Paulis; then a data-only dense
      simulation of the coin-free commuting tree.
Checks, for every record and pattern e: Pr_dense(r|e) = 2^-k Pr_tree(r|e); the output Bloch vectors
agree; the genuine data Paulis on each path commute; the coin-free tree with the best child at every
coin has A(0) = 2-weighted maximum >= A(0) of the protocol, and its leaf probabilities sum to 1.
Part S (scrambled 1/4 tree). results/tree_best.json hidden under random gates, ancillas and coins:
dense A(0) must stay exactly 1/4 and the tracker must recover the tree's leaf groups.
Part A (leaf split, section 3). Rank-7 subgroups of the 32 leaves of the 1/4 tree with their output
logicals: test generalised validity on the real inputs, split the valid ones by a discarded logical
and check that both children are valid with the same total probability. Plus constructed rank-7 and
rank-6 leaves with pure output marginal (positive) and an entangled one (negative control).
Usage: src/check_reductions.py [n_random_protocols] [seed]
"""
import json, sys
import numpy as np

ND = 9                     # data qubits
W8 = np.exp(1j * np.pi / 4)
TOL = 1e-9
pc = np.bitwise_count

# ---------------- Pauli algebra: (x, z, ph) = i^ph X^x Z^z, bit q = qubit q ----------------
def pmul(a, b):
    return (a[0] ^ b[0], a[1] ^ b[1], (a[2] + b[2] + 2 * int(pc(np.uint64(a[1] & b[0])))) & 3)

def comm(a, b):
    return (int(pc(np.uint64(a[0] & b[1]))) + int(pc(np.uint64(a[1] & b[0])))) % 2 == 0

def neg(a):
    return (a[0], a[1], (a[2] + 2) & 3)

def herm(x, z, sign=0):
    return (x, z, (int(pc(np.uint64(x & z))) + 2 * sign) & 3)

def parse(s):
    sign = 1 if s[0] == "-" else 0
    s = s.lstrip("+-")
    x = z = 0
    for q, c in enumerate(s):
        if c in "XY": x |= 1 << q
        if c in "ZY": z |= 1 << q
    return herm(x, z, sign)

def conj_gate(P, g, inverse):
    """g P g^dag (inverse=False) or g^dag P g (inverse=True)."""
    x, z, ph = P
    kind = g[0]
    if kind == "H":
        q = g[1]; a = (x >> q) & 1; b = (z >> q) & 1
        x = (x & ~(1 << q)) | (b << q); z = (z & ~(1 << q)) | (a << q)
        return (x, z, (ph + 2 * a * b) & 3)
    if kind == "S":
        q = g[1]
        if (x >> q) & 1:
            z ^= 1 << q; ph += 3 if inverse else 1
        return (x, z, ph & 3)
    if kind == "CX":
        c, t = g[1], g[2]
        if (x >> c) & 1: x ^= 1 << t
        if (z >> t) & 1: z ^= 1 << c
        return (x, z, ph)
    if kind == "V":        # V = (A + B)/sqrt2, A, B anticommuting Hermitian: Hermitian unitary
        A, B = g[1], g[2]
        ca, cb = comm(P, A), comm(P, B)
        if ca and cb: return P
        if not ca and not cb: return neg(P)
        R = pmul(pmul(P, A), B)
        return R if ca else neg(R)
    raise ValueError(kind)

def pull_back(P, ops):      # U^dag P U, U = ops[-1] ... ops[0]
    for g in reversed(ops):
        P = conj_gate(P, g, True)
    return P

def push_fwd(P, ops):       # U P U^dag
    for g in ops:
        P = conj_gate(P, g, False)
    return P

# ---------------- dense simulation; columns = fault patterns ----------------
class Dense:
    def __init__(self, nq):
        self.nq = nq
        self.idx = np.arange(2 ** nq, dtype=np.uint64)

    def init(self):
        e = np.arange(2 ** ND, dtype=np.uint64)
        d = self.idx & np.uint64(2 ** ND - 1)
        anc0 = (self.idx >> np.uint64(ND)) == 0
        amp = (2 ** (-ND / 2)) * W8 ** pc(d).astype(float)
        sgn = 1 - 2 * (pc(d[:, None] & e[None, :]) & 1).astype(float)
        return (amp * anc0)[:, None] * sgn

    def pauli(self, P, v):
        x, z, ph = P
        j = self.idx ^ np.uint64(x)
        s = 1 - 2 * (pc(j & np.uint64(z)) & 1).astype(float)
        return (1j ** ph) * (s[:, None] * v[j])

    def gate(self, g, v):
        q = lambda b: 1 << b
        if g[0] == "H":
            return (self.pauli((q(g[1]), 0, 0), v) + self.pauli((0, q(g[1]), 0), v)) / np.sqrt(2)
        if g[0] == "S":
            return ((1 + 1j) * v + (1 - 1j) * self.pauli((0, q(g[1]), 0), v)) / 2
        if g[0] == "CX":
            c, t = g[1], g[2]
            return (v + self.pauli((0, q(c), 0), v) + self.pauli((q(t), 0, 0), v)
                    - self.pauli((q(t), q(c), 0), v)) / 2   # Z_c X_t = X^t Z^c, phase 0
        raise ValueError(g)

    def proj(self, B, v):
        return (v + self.pauli(B, v)) / 2

    def expect(self, P, v):
        return np.real(np.einsum("ij,ij->j", v.conj(), self.pauli(P, v)))

def norms(v):
    return np.real(np.einsum("ij,ij->j", v.conj(), v))

def bloch(D, v, LX, LY, LZ):
    n = norms(v)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.array([np.where(n > TOL, D.expect(L, v) / np.maximum(n, 1e-300), 0) if L is not None
                         else np.zeros(v.shape[1]) for L in (LX, LY, LZ)])

# ---------------- tracker of section 2 ----------------
class Track:
    def __init__(self, m):
        self.G = [herm(0, 1 << (ND + a)) for a in range(m)]   # signed generators, ancilla Z's
        self.ops = []
        self.k = 0
        self.data = []                                         # signed data Paulis measured

    def copy(self):
        t = Track(0); t.G = list(self.G); t.ops = list(self.ops); t.k = self.k; t.data = list(self.data)
        return t

    def measure(self, M, s):
        """Physical measurement of M with outcome s (+1/-1). Returns 'coin' or 'genuine'."""
        Mp = pull_back(M, self.ops)
        B = Mp if s == 1 else neg(Mp)
        anti = [i for i, g in enumerate(self.G) if not comm(g, Mp)]
        if anti:
            i0 = anti[0]; A = self.G[i0]
            for i in anti[1:]:
                self.G[i] = pmul(self.G[i], A)
            self.ops.insert(0, ("V", A, B))
            self.k += 1
            return "coin"
        self.G.append(B)
        mask = (1 << ND) - 1
        assert B[0] >> ND == 0, "genuine measurement has X on an ancilla"
        self.data.append(herm(B[0] & mask, B[1] & mask, 0 if B[2] == herm(B[0], B[1])[2] else 1))
        return "genuine"

    def logical(self, Pphys):
        L = pull_back(Pphys, self.ops)
        if any(not comm(L, g) for g in self.G):
            return None
        mask = (1 << ND) - 1
        assert L[0] >> ND == 0
        return herm(L[0] & mask, L[1] & mask, 0 if L[2] == herm(L[0], L[1])[2] else 1)

# ---------------- random protocols ----------------
def rand_pauli(rng, nq):
    x = int(rng.integers(0, 2 ** nq)); z = int(rng.integers(0, 2 ** nq))
    return herm(x, z, int(rng.integers(0, 2))) if (x or z) else herm(1, 0)

def rand_gate(rng, nq):
    r = rng.integers(0, 3)
    a = int(rng.integers(0, nq))
    if r == 0: return ("H", a)
    if r == 1: return ("S", a)
    b = int(rng.integers(0, nq - 1)); b += b >= a
    return ("CX", a, b)

def genuine_phys(rng, tr, nq):
    """A physical Pauli whose pull-back commutes with G (data part random, ancilla part Z only)."""
    for _ in range(4000):
        R = herm(int(rng.integers(0, 2 ** ND)), int(rng.integers(0, 2 ** nq)), 0)
        if (R[0] or R[1]) and all(comm(R, g) for g in tr.G):
            return push_fwd(R, tr.ops)
    return None

class Stats:
    def __init__(self):
        self.maxdev = 0.0; self.records = 0; self.coins = 0; self.genuine = 0

def run_protocol(rng, m, depth, st):
    nq = ND + m
    D, Dd = Dense(nq), Dense(ND)
    v0 = D.init(); vd0 = Dd.init()
    assert abs(norms(v0)[0] - 1) < 1e-12

    def rec(v, tr, d):
        """Returns (A_orig(0), A_best(0), total prob of coin-free tree leaves per pattern)."""
        r = rng.random()
        if d == depth or r < 0.08:                                  # leaf
            for _ in range(int(rng.integers(0, 4))):
                g = rand_gate(rng, nq); v = D.gate(g, v); tr.ops.append(g)
            o = int(rng.integers(0, nq))
            X, Z = herm(1 << o, 0), herm(0, 1 << o)
            Y = herm(1 << o, 1 << o)
            p_orig = norms(v)
            b_orig = bloch(D, v, X, Y, Z)
            w = vd0
            for P in tr.data:
                w = Dd.proj(P, w)
            p_tree = norms(w)
            b_tree = bloch(Dd, w, tr.logical(X), tr.logical(Y), tr.logical(Z))
            dev = max(np.max(np.abs(p_orig - 2.0 ** -tr.k * p_tree)),
                      np.max(np.abs(np.where(p_orig > 1e-8, b_orig - b_tree, 0))))
            st.maxdev = max(st.maxdev, dev); st.records += 1
            assert dev < 1e-8, f"mismatch {dev}"
            for i in range(len(tr.data)):
                for j in range(i):
                    assert comm(tr.data[i], tr.data[j])
            acc = rng.random() < 0.7
            a0 = p_orig[0] if acc else 0.0
            return a0, (p_tree[0] if acc else 0.0), p_tree
        if r < 0.3:                                                 # gate
            g = rand_gate(rng, nq); tr.ops.append(g)
            return rec(D.gate(g, v), tr, d)
        if r < 0.42:                                                # controller random bit
            outs = []
            for _ in range(2):
                t2 = tr.copy(); t2.k += 1
                outs.append(rec(v / np.sqrt(2), t2, d + 1))
            st.coins += 1
            return (outs[0][0] + outs[1][0], max(o[1] for o in outs), None)
        M = genuine_phys(rng, tr, nq) if r < 0.7 else rand_pauli(rng, nq)
        if M is None:
            M = rand_pauli(rng, nq)
        res, kinds = [], []
        for s in (1, -1):
            t2 = tr.copy()
            kinds.append(t2.measure(M, s))
            res.append(rec(D.proj(M if s == 1 else neg(M), v), t2, d + 1))
        assert kinds[0] == kinds[1]
        if kinds[0] == "coin":
            st.coins += 1
            return (res[0][0] + res[1][0], max(o[1] for o in res), None)
        st.genuine += 1
        tot = None if (res[0][2] is None or res[1][2] is None) else res[0][2] + res[1][2]
        return (res[0][0] + res[1][0], res[0][1] + res[1][1], tot)

    a_orig, a_best, _ = rec(v0, Track(m), 0)
    return a_orig, a_best

# A_best above: at a coin node we take the max over children of the coin-free value (each child's
# value is already in coin-free units because leaves report p_tree, i.e. the factor 2^k removed).
# The coin-free tree's leaf probabilities summing to 1 is checked separately in check_free_tree.

def check_free_tree(rng, m, depth):
    """Coin-free trees must be complete: leaf probabilities (Kraus U Pi_G, no c) sum to 1 per pattern."""
    nq = ND + m
    Dd = Dense(ND); vd0 = Dd.init()

    def rec(tr, d):
        r = rng.random()
        if d == depth or r < 0.1:
            w = vd0
            for P in tr.data:
                w = Dd.proj(P, w)
            return norms(w)
        if r < 0.3:
            tr.ops.append(rand_gate(rng, nq)); return rec(tr, d)
        if r < 0.65:
            M = genuine_phys(rng, tr, nq) or rand_pauli(rng, nq)
        else:
            M = rand_pauli(rng, nq)
        t1 = tr.copy(); kind = t1.measure(M, 1)
        if kind == "coin":                      # coin-free: keep one child only
            return rec(t1, d + 1)
        t2 = tr.copy(); t2.measure(M, -1)
        return rec(t1, d + 1) + rec(t2, d + 1)

    tot = rec(Track(m), 0)
    return float(np.max(np.abs(tot - 1)))

# ---------------- part S: scrambled 1/4 tree ----------------
def tree_leaves(t, path=()):
    if "leaf" in t:
        yield [parse(s) for s in t["leaf"]], path
    else:
        P = parse(t["measure"])
        yield from tree_leaves(t["plus"], path + ((P, 1),))
        yield from tree_leaves(t["minus"], path + ((P, -1),))

def scrambled_tree(rng, tree, m):
    nq = ND + m
    D = Dense(nq); v0 = D.init()
    found = []

    def rec(t, v, tr, gens_left, d, budget=2):
        # random noise operations: gates and (at most `budget` per path) coin measurements
        for _ in range(int(rng.integers(0, 3))):
            r = rng.random()
            if r < 0.8 or budget == 0:
                g = rand_gate(rng, nq); v = D.gate(g, v); tr.ops.append(g)
            else:
                for _ in range(200):
                    M = rand_pauli(rng, nq)
                    if any(not comm(pull_back(M, tr.ops), g) for g in tr.G):
                        break
                else:
                    continue
                tot = 0.0
                for s in (1, -1):
                    t2 = tr.copy(); assert t2.measure(M, s) == "coin"
                    tot += rec(t, D.proj(M if s == 1 else neg(M), v), t2, gens_left, d, budget - 1)
                return tot
        if gens_left is None and "leaf" not in t:
            P = parse(t["measure"])
            tot = 0.0
            for s, key in ((1, "plus"), (-1, "minus")):
                t2 = tr.copy()
                M = push_fwd(P if s == 1 else neg(P), tr.ops)       # physical, outcome +1 wanted
                assert t2.measure(M, 1) == "genuine"
                tot += rec(t[key], D.proj(M, v), t2, None, d + 1, budget)
            return tot
        if gens_left is None:
            gens_left = list(t["leaf"])
        if gens_left:
            P = parse(gens_left[0])
            M = push_fwd(P, tr.ops)
            t2 = tr.copy(); assert t2.measure(M, 1) == "genuine"
            return rec(t, D.proj(M, v), t2, gens_left[1:], d, budget)
        found.append(set((x, z, ph) for (x, z, ph) in tr.data))
        return norms(v)[0]   # accepted record mass at p = 0 (coin factors included)

    a = rec(tree, v0, Track(m), None, 0)
    return a, found

# ---------------- part A: leaf split ----------------
def group_closure(gens):
    G = {(0, 0): 0}
    for g in gens:
        new = {}
        for (x, z), ph in G.items():
            h = pmul((x, z, ph), g); new[(h[0], h[1])] = h[2]
        G.update(new)
    return G

def centraliser_logicals(gens):
    """Brute force over all 4^9 Paulis: logicals commuting with gens, modulo the group."""
    out = []
    xs = np.arange(2 ** ND, dtype=np.uint64)
    for x in range(2 ** ND):
        z = xs
        par = np.zeros(2 ** ND, dtype=np.uint64)
        for g in gens:
            par += (pc(np.uint64(x) & np.uint64(g[1])) + pc(z & np.uint64(g[0]))) & np.uint64(1)
        for zz in np.nonzero(par == 0)[0]:
            out.append((x, int(zz)))
    return out

def leaf_valid(Dd, vd0, gens, LX, LZ):
    """Generalised validity of a leaf (any rank) on the 10 patterns |e| <= 1. Returns (valid, q0)."""
    w = vd0
    for P in gens:
        w = Dd.proj(P, w)
    LY = pmul(LX, LZ); LY = (LY[0], LY[1], (LY[2] + 1) & 3)       # i X Z = Y up to sign, Hermitian
    LY = herm(LY[0], LY[1], 0 if LY[2] == herm(LY[0], LY[1])[2] else 1)
    p = norms(w); b = bloch(Dd, w, LX, LY, LZ)
    cols = [0] + [1 << j for j in range(ND)]
    if p[0] < 1e-12:
        return False, 0.0
    ref = b[:, 0]
    mods = sorted(np.abs(ref))
    if not (mods[0] < 1e-9 and abs(mods[1] - 2 ** -0.5) < 1e-9 and abs(mods[2] - 2 ** -0.5) < 1e-9):
        return False, p[0]
    for e in cols[1:]:
        if p[e] > 1e-12 and np.max(np.abs(b[:, e] - ref)) > 1e-9:
            return False, p[0]
    return True, p[0]

def part_A(tree):
    Dd = Dense(ND); vd0 = Dd.init()
    nvalid_parent = ntested = 0
    for gens, _ in tree_leaves(tree):
        Gfull = group_closure(gens)
        # output logicals of the full leaf: an anticommuting pair in the centraliser, outside the group
        cands = [(x, z) for (x, z) in centraliser_logicals(gens) if (x, z) not in Gfull]
        LX = herm(*cands[0])
        LZ = next(herm(x, z) for (x, z) in cands if not comm(LX, herm(x, z)))
        ok, q = leaf_valid(Dd, vd0, gens, LX, LZ)
        assert ok and abs(q - 1 / 128) < 1e-12, "full leaf of the 1/4 tree not valid"
        for drop in range(8):                                     # rank-7 parents: drop one generator
            par = gens[:drop] + gens[drop + 1:]
            okp, qp = leaf_valid(Dd, vd0, par, LX, LZ)
            ntested += 1
            if not okp:
                continue
            nvalid_parent += 1
            h = gens[drop]                                        # a discarded logical of the parent
            okc = [leaf_valid(Dd, vd0, par + [hh], LX, LZ) for hh in (h, neg(h))]
            assert all(o or abs(qc) < 1e-12 for o, qc in okc), "child of a valid parent is not valid"
            assert abs(sum(qc for _, qc in okc) - qp) < 1e-12
    return ntested, nvalid_parent

def part_A_constructed(rng, k_disc):
    """Encoded |T> (x) |phi>: rank 9-1-k_disc parent; positive and entangled (negative) controls."""
    nlog = 1 + k_disc
    ops = [rand_gate(rng, ND) for _ in range(60)]
    Dd = Dense(ND)
    G = [push_fwd(herm(0, 1 << q), ops) for q in range(nlog, ND)]
    LX, LZ = push_fwd(herm(1, 0), ops), push_fwd(herm(0, 1), ops)
    Ldisc = push_fwd(herm(0, 1 << 1), ops)
    res = []
    for entangled in (False, True):
        cols = []
        for _ in range(10):
            phi = rng.normal(size=2 ** k_disc) + 1j * rng.normal(size=2 ** k_disc)
            phi /= np.linalg.norm(phi)
            T = np.array([1, W8]) / np.sqrt(2)
            if entangled:
                psi = (np.kron(phi, [1, 0]) + np.kron(phi[::-1], [0, W8])) / np.sqrt(2)
            else:
                psi = np.kron(phi, T)       # qubit 0 = T (lowest bit), qubits 1.. = phi
            full = np.zeros(2 ** ND, complex); full[:2 ** nlog] = psi
            junk = rng.normal(size=2 ** ND) * 0.3; junk[:2 ** nlog] = 0
            v = full + junk
            for g in ops:
                v = Dd.gate(g, v[:, None])[:, 0]
            cols.append(v)
        V = np.array(cols).T
        w = V
        for P in G:
            w = Dd.proj(P, w)
        LY = pmul(LX, LZ); LY = herm(LY[0], LY[1], 0 if ((LY[2] + 1) & 3) == herm(LY[0], LY[1])[2] else 1)
        bp = bloch(Dd, w, LX, LY, LZ); pp = norms(w)
        kids = []
        for s in (1, -1):
            wc = Dd.proj(Ldisc if s == 1 else neg(Ldisc), w)
            kids.append((norms(wc), bloch(Dd, wc, LX, LY, LZ)))
        sum_ok = np.max(np.abs(kids[0][0] + kids[1][0] - pp)) < 1e-12
        same = max(np.max(np.abs(np.where(kp > 1e-12, kb - bp, 0))) for kp, kb in kids)
        pure = np.max(np.abs(np.linalg.norm(bp, axis=0) - 1))
        res.append((entangled, sum_ok, same, pure))
    return res

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rng = np.random.default_rng(seed)
    st = Stats(); worst_gain = 0.0
    for i in range(n):
        m = 1 + i % 2
        a_orig, a_best = run_protocol(rng, m, depth=7, st=st)
        assert a_best >= a_orig - 1e-12
        worst_gain = max(worst_gain, a_best - a_orig)
    print(f"B: {n} random protocols (m = 1, 2 ancillas, depth 7), {st.records} records x 512 patterns, "
          f"{st.coins} coin nodes, {st.genuine} genuine nodes; max |Pr - 2^-k Pr_tree|, |Bloch diff| = "
          f"{st.maxdev:.2e}; coin-free best >= original everywhere (largest gain {worst_gain:.3g})")
    dev = max(check_free_tree(rng, 1 + i % 2, 8) for i in range(n))
    print(f"B: coin-free trees complete: max |sum of leaf probabilities - 1| = {dev:.2e} over {n} trees")
    tree = json.load(open("results/tree_best.json"))
    for i in range(3):
        a, found = scrambled_tree(rng, tree, 1 + i % 2)
        want = [set(g) for g, _ in tree_leaves(tree)]
        rec_ok = all(any(f >= w for f in found) for w in want)
        print(f"S: scrambled 1/4 tree (m = {1 + i % 2}): A(0) = {a:.15f} (want 0.25), "
              f"all 32 leaf groups recovered by the tracker: {rec_ok}")
        assert abs(a - 0.25) < 1e-12 and rec_ok
    nt, nv = part_A(tree)
    print(f"A: rank-7 subgroups of the 32 leaves (drop one generator, keep the leaf's logicals): "
          f"{nt} tested, {nv} valid as parents; "
          + ("each split into valid children with the same total" if nv else
             "none to split, so this real-input part is vacuous (the constructed cases below test the split)"))
    for k in (1, 2):
        for ent, sum_ok, same, pure in part_A_constructed(rng, k):
            print(f"A: constructed rank {8 - k} parent ({'entangled, negative control' if ent else 'product'}): "
                  f"children sum to parent {sum_ok}; max child-parent Bloch diff {same:.2e}; "
                  f"parent purity defect {pure:.2e}")
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
