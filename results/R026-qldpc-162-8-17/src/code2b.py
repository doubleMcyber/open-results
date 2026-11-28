"""Two-block group-algebra CSS codes C(a, b), built independently of the Bicycle Race scripts.

Convention (same as arXiv:2610.13880 and Lin-Pryadko): for a finite group G and subsets a, b of G,
    L(a)[s*g, g] = 1 for s in a,   R(b)[g*s, g] = 1 for s in b,
    H_X = (L(a) | R(b)),   H_Z = (R(b)^T | L(a)^T).
L(a) and R(b) commute, so H_X H_Z^T = L R + R L = 0 over GF(2).
"""
import json
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUPS = ROOT / 'data' / 'bicycle-race' / 'data' / 'groups.jsonl'


# ---------------------------------------------------------------- groups
class Group:
    def __init__(self, table, name=''):
        self.mul = np.asarray(table, dtype=np.int32)  # mul[i, j] = index of e_i * e_j
        self.order = self.mul.shape[0]
        self.name = name
        assert (self.mul[0] == np.arange(self.order)).all() and (self.mul[:, 0] == np.arange(self.order)).all(), 'element 0 must be identity'
        self.inv = np.array([int(np.where(self.mul[i] == 0)[0][0]) for i in range(self.order)], dtype=np.int32)

    def check(self, trials=2000, rng=np.random.default_rng(0)):
        o = self.order
        for r in range(o):  # Latin square
            assert len(set(self.mul[r])) == o
        x, y, z = rng.integers(0, o, (3, trials))
        assert (self.mul[self.mul[x, y], z] == self.mul[x, self.mul[y, z]]).all(), 'not associative'
        return True

    def is_abelian(self):
        return bool((self.mul == self.mul.T).all())


def abelian_group(orders):
    """Direct product of cyclic groups C_{n1} x ... ; element index = mixed radix of exponents."""
    orders = list(orders)
    o = int(np.prod(orders))
    exps = np.array(np.unravel_index(np.arange(o), orders)).T  # (o, r)
    summ = (exps[:, None, :] + exps[None, :, :]) % np.array(orders)
    tab = np.ravel_multi_index(tuple(summ.reshape(-1, len(orders)).T), orders).reshape(o, o)
    return Group(tab, 'x'.join('C%d' % m for m in orders)), exps


def group_from_br(gap_id):
    """Rebuild SmallGroup(order, id) from the Bicycle Race groups.jsonl generator permutations.
    Generator s is given as the permutation j -> index(e_j * s). Our own closure, not their script."""
    gap_id = list(gap_id)
    for line in open(GROUPS):
        g = json.loads(line)
        if g['gap_id'] == gap_id:
            break
    else:
        raise KeyError(gap_id)
    gens = [np.array(p, dtype=np.int32) for p in g['generators']]
    o = gap_id[0]
    # BFS: word for each element as a sequence of right multiplications from the identity
    word = {0: []}
    frontier = [0]
    while frontier:
        nxt = []
        for j in frontier:
            for gi, p in enumerate(gens):
                t = int(p[j])
                if t not in word:
                    word[t] = word[j] + [gi]
                    nxt.append(t)
        frontier = nxt
    assert len(word) == o, 'generators do not generate'
    tab = np.zeros((o, o), dtype=np.int32)
    for j in range(o):
        col = np.arange(o, dtype=np.int32)
        for gi in word[j]:
            col = gens[gi][col]
        tab[:, j] = col  # e_i * e_j
    G = Group(tab, g['structure'])
    G.check()
    assert G.is_abelian() == g['abelian']
    return G


# ---------------------------------------------------------------- codes
def two_block(G, a, b):
    o = G.order
    L = np.zeros((o, o), dtype=np.uint8)
    R = np.zeros((o, o), dtype=np.uint8)
    for gcol in range(o):
        for s in a:
            L[G.mul[s, gcol], gcol] ^= 1
        for s in b:
            R[G.mul[gcol, s], gcol] ^= 1
    HX = np.hstack([L, R])
    HZ = np.hstack([R.T, L.T])
    assert not ((HX.astype(np.int64) @ HZ.T.astype(np.int64)) % 2).any(), 'H_X H_Z^T != 0'
    return HX, HZ


def bb_code(l, m, A, B):
    """Bravyi et al. bivariate bicycle code; A, B lists of (i, j) exponents of x^i y^j in C_l x C_m."""
    G, exps = abelian_group([l, m])
    idx = {tuple(e): i for i, e in enumerate(exps)}
    a = [idx[(i % l, j % m)] for i, j in A]
    b = [idx[(i % l, j % m)] for i, j in B]
    return two_block(G, a, b)


# ---------------------------------------------------------------- GF(2)
def rref(M):
    """Row-reduce a GF(2) matrix. Returns (R, pivots) with R the nonzero rows."""
    M = (np.asarray(M, dtype=np.uint8) & 1).copy()
    rows, cols = M.shape
    piv = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        p = r + nz[0]
        if p != r:
            M[[r, p]] = M[[p, r]]
        hit = np.nonzero(M[:, c])[0]
        hit = hit[hit != r]
        M[hit] ^= M[r]
        piv.append(c)
        r += 1
    return M[:r], piv


def rank(M):
    return len(rref(M)[1])


def nullspace(M):
    """Basis (rows) of the GF(2) kernel {x : M x = 0}."""
    R, piv = rref(M)
    n = M.shape[1]
    free = [c for c in range(n) if c not in set(piv)]
    basis = np.zeros((len(free), n), dtype=np.uint8)
    for i, f in enumerate(free):
        basis[i, f] = 1
        for r, p in enumerate(piv):
            if R[r, f]:
                basis[i, p] = 1
    return basis


def logical_basis(HX, HZ):
    """Return (LZ, LX): k independent Z-type logicals (in ker H_X, outside rowspace H_Z) and
    X-type logicals (in ker H_Z, outside rowspace H_X), paired so that LX LZ^T = I."""
    def complement(K, S):
        # rows of K independent modulo rowspace(S)
        base = rref(S)[0]
        r0 = len(base)
        out = []
        cur = base
        for v in K:
            t = np.vstack([cur, v[None]])
            if rank(t) > len(cur):
                cur = rref(t)[0]
                out.append(v)
        return np.array(out, dtype=np.uint8).reshape(-1, K.shape[1])
    LZ = complement(nullspace(HX), HZ)
    LX = complement(nullspace(HZ), HX)
    assert len(LZ) == len(LX)
    # symplectic pairing: make LX LZ^T = identity
    Mtx = (LX.astype(np.int64) @ LZ.T.astype(np.int64)) % 2
    k = len(LZ)
    # solve: LX' = Minv LX
    aug = np.hstack([Mtx.astype(np.uint8), np.eye(k, dtype=np.uint8)])
    R, piv = rref(aug)
    assert piv[:k] == list(range(k)), 'logical pairing singular'
    Minv = R[:, k:]
    LX = (Minv.astype(np.int64) @ LX.astype(np.int64)) % 2
    assert ((LX @ LZ.T.astype(np.int64)) % 2 == np.eye(k)).all()
    return LZ.astype(np.uint8), LX.astype(np.uint8)


def params(HX, HZ):
    n = HX.shape[1]
    k = n - rank(HX) - rank(HZ)
    w = int(max(HX.sum(1).max(), HZ.sum(1).max()))
    return n, k, w
