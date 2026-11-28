"""Engine C: exact lower-bound / witness search for CSS codes by connected-cluster enumeration.

Written independently of the other engines (only code2b is imported, for GF(2) helpers and
the group-algebra builders). Method: the depth-first codeword enumeration of Dumer-Kovalev-Pryadko
(dist-m4ri, dist_cc.c), reimplemented in numba with these differences from dist-m4ri:

* One DFS to depth T (dist-m4ri runs one round per weight w and tests exact weight w at the leaves).
  Any nontrivial codeword of weight <= T met on the way is returned.
* Sibling exclusion. At a node the search branches on the available qubits c_1..c_m of a check row
  with nonzero syndrome. Branch j adds c_j and forbids c_1..c_{j-1} for its whole subtree, so the
  branches partition the targets and every qubit set is visited at most once. dist-m4ri has no such
  exclusion (the same set is reached in several orders).
* Row choice. The branching row is the nonzero-syndrome row with the fewest available qubits (not the
  first nonzero row). A nonzero-syndrome row with no available qubit prunes the node.
* Pruning on syndrome weight: wt(s) <= (T-|S|) * max column weight (as in dist-m4ri).
* Start-set / orbit reduction (see cc_lower).

Correctness argument ("none" is a proof). Let c be a nontrivial logical of weight <= T of the sector
and take c of minimum weight among nontrivial logicals. No nonzero proper subset S of c is a codeword
(S trivial: c+S is nontrivial and lighter; S nontrivial: lighter than c). So every proper subset S of
c that the DFS builds has nonzero syndrome. At a node S (S subset of c, no forbidden qubit in c) any
nonzero-syndrome row r of S has odd overlap with c\\S, so c\\S contains an available qubit of row r;
exactly one branch (the first, in row order, of the qubits of c in row r that are not in S) keeps c
alive. Hence c is reached at a leaf with zero syndrome, and a zero-syndrome set that is trivial is not
descended into (it cannot be a prefix of c). The DFS therefore finds some nontrivial logical of weight
<= T whenever one exists. Nontriviality of a zero-syndrome set is tested by its parity against k
vectors of ker(other check matrix) that are independent modulo rowspace(own check matrix).
"""
import sys
import time
from pathlib import Path

import numpy as np
from numba import njit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import code2b  # noqa: E402  (only local dependency)

U1, U2, U4, U56, U58 = np.uint64(1), np.uint64(2), np.uint64(4), np.uint64(56), np.uint64(58)
M1 = np.uint64(0x5555555555555555)
M2 = np.uint64(0x3333333333333333)
M4 = np.uint64(0x0F0F0F0F0F0F0F0F)
H01 = np.uint64(0x0101010101010101)
DEBRUIJN = np.uint64(0x03F79D71B4CB0A89)
_CTZ = np.zeros(64, dtype=np.int64)
for _i in range(64):
    _CTZ[int(((1 << _i) * 0x03F79D71B4CB0A89) & 0xFFFFFFFFFFFFFFFF) >> 58] = _i


@njit(cache=True, inline='always')
def _popcnt(x):
    x = x - ((x >> U1) & M1)
    x = (x & M2) + ((x >> U2) & M2)
    x = (x + (x >> U4)) & M4
    return (x * H01) >> U56


@njit(cache=True)
def _search(start, T, W, KW, colv, cptr, crow, rptr, rcol, lmask, blocked0, maxcw, max_nodes, ctz, S):
    """DFS from the single qubit `start` (in S[0]) with the qubits blocked0 forbidden.
    Returns (status, length, nodes): status 0 exhausted, 1 found (S[:length]), 2 node cap hit."""
    n = colv.shape[0]
    m = rptr.shape[0] - 1
    blocked = blocked0.copy()
    avail = np.zeros(m, dtype=np.int64)
    for r in range(m):
        c = 0
        for t in range(rptr[r], rptr[r + 1]):
            if blocked[rcol[t]] == 0:
                c += 1
        avail[r] = c
    syn = np.zeros(W, dtype=np.uint64)
    ls = np.zeros(KW, dtype=np.uint64)
    frow = np.zeros(T + 2, dtype=np.int64)
    fptr = np.zeros(T + 2, dtype=np.int64)
    fbase = np.zeros(T + 2, dtype=np.int64)
    blist = np.zeros(n + 2, dtype=np.int64)
    bl = 0
    nodes = 0

    # add the start qubit
    S[0] = start
    blocked[start] = 1
    for t in range(cptr[start], cptr[start + 1]):
        avail[crow[t]] -= 1
    for w in range(W):
        syn[w] ^= colv[start, w]
    for w in range(KW):
        ls[w] ^= lmask[start, w]
    nodes += 1
    zero = True
    for w in range(W):
        if syn[w] != 0:
            zero = False
    if zero:
        nz = False
        for w in range(KW):
            if ls[w] != 0:
                nz = True
        if nz:
            return 1, 1, nodes
        return 0, 0, nodes
    if T < 2:
        return 0, 0, nodes

    d = 1
    need_enter = True
    while d >= 1:
        if need_enter:
            need_enter = False
            # node with |S| = d, syn != 0, d < T: choose the branching row
            swt = 0
            best = -1
            bestav = 1 << 40
            for w in range(W):
                x = syn[w]
                swt += int(_popcnt(x))
                while x != 0:
                    b = x & (~x + U1)
                    r = w * 64 + ctz[(b * DEBRUIJN) >> U58]
                    x ^= b
                    a = avail[r]
                    if a < bestav:
                        bestav = a
                        best = r
            if swt > (T - d) * maxcw or bestav <= 0:
                # prune: behave like an exhausted frame
                frow[d] = -1
            else:
                frow[d] = best
                fptr[d] = rptr[best]
                fbase[d] = bl
        # iterate candidates of frame d
        r = frow[d]
        found_cand = False
        col = -1
        if r >= 0:
            p = fptr[d]
            end = rptr[r + 1]
            while p < end and blocked[rcol[p]] != 0:
                p += 1
            if p < end:
                col = rcol[p]
                fptr[d] = p + 1
                found_cand = True
        if not found_cand:
            # frame exhausted: release its blocks, return to the parent
            if r >= 0:
                while bl > fbase[d]:
                    bl -= 1
                    q = blist[bl]
                    blocked[q] = 0
                    for t in range(cptr[q], cptr[q + 1]):
                        avail[crow[t]] += 1
            d -= 1
            if d >= 1:
                q = S[d]  # undo the parent's column but keep it blocked for later siblings
                for w in range(W):
                    syn[w] ^= colv[q, w]
                for w in range(KW):
                    ls[w] ^= lmask[q, w]
                blist[bl] = q
                bl += 1
            continue
        # add col
        if max_nodes > 0 and nodes >= max_nodes:
            return 2, 0, nodes
        nodes += 1
        S[d] = col
        blocked[col] = 1
        for t in range(cptr[col], cptr[col + 1]):
            avail[crow[t]] -= 1
        zero = True
        for w in range(W):
            syn[w] ^= colv[col, w]
            if syn[w] != 0:
                zero = False
        for w in range(KW):
            ls[w] ^= lmask[col, w]
        if zero:
            nz = False
            for w in range(KW):
                if ls[w] != 0:
                    nz = True
            if nz:
                return 1, d + 1, nodes
            # trivial codeword: not a prefix of a minimum-weight logical; undo, keep blocked
            for w in range(W):
                syn[w] ^= colv[col, w]
            for w in range(KW):
                ls[w] ^= lmask[col, w]
            blist[bl] = col
            bl += 1
        elif d + 1 >= T:
            # |S| = T and syndrome nonzero: dead end
            for w in range(W):
                syn[w] ^= colv[col, w]
            for w in range(KW):
                ls[w] ^= lmask[col, w]
            blist[bl] = col
            bl += 1
        else:
            d += 1
            need_enter = True
    return 0, 0, nodes


# ------------------------------------------------------------------------------ python side
def _logical_tests(H, Other):
    """k vectors of ker(Other) independent modulo rowspace(H). A vector c in ker(H) is a nontrivial
    logical of H's sector iff its parity against one of them is 1 (rowspace(Other) = ker(Other)^perp,
    and rowspace(H) is orthogonal to ker(H))."""
    n = H.shape[1]
    piv = {}

    def reduce(v):
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                return v
        return 0

    def toint(row):
        return int(''.join('1' if x else '0' for x in row[::-1]), 2) if len(row) else 0

    for row in H:
        v = reduce(toint(row))
        if v:
            piv[v.bit_length() - 1] = v
    tests = []
    for row in code2b.nullspace(Other):
        v0 = toint(row)
        v = reduce(v0)
        if v:
            piv[v.bit_length() - 1] = v
            tests.append(row.astype(np.uint8))
    k = n - code2b.rank(H) - code2b.rank(Other)
    assert len(tests) == k, (len(tests), k)
    return np.array(tests, dtype=np.uint8).reshape(len(tests), n)


def _pack_cols(M):
    """bit-pack the columns of an (m, n) 0/1 matrix into an (n, ceil(m/64)) uint64 array."""
    m, n = M.shape
    W = max(1, (m + 63) // 64)
    out = np.zeros((n, W), dtype=np.uint64)
    for r in range(m):
        out[np.nonzero(M[r])[0], r // 64] |= np.uint64(1) << np.uint64(r % 64)
    return out


def cc_lower(HX, HZ, sector, T, starts=None, orbits=None, max_nodes=None):
    """Connected-cluster search for a nontrivial logical of weight <= T.

    sector 'Z': c with HX c = 0, c not in rowspace(HZ).  sector 'X': HZ c = 0, c not in rowspace(HX).
    Returns (status, support, stats):
      'none'   every nontrivial logical of the sector has weight > T (proof, see module docstring),
      'found'  support = sorted qubit list of a nontrivial logical of weight <= T (re-verified here),
      'capped' max_nodes exhausted first (nothing proven).

    Start-set reduction. `starts` = [q_1..q_s], `orbits` = list of qubit lists (default: singletons).
    The search from q_i looks for logicals containing q_i and no qubit of orbit(q_1) ∪ ... ∪ orbit(q_{i-1}).
    This is complete (so 'none' is a proof) iff
      (a) orbits are orbits of a group Gamma of qubit permutations that maps the code to itself
          (preserves rowspace(HX) and rowspace(HZ), hence weight and nontriviality of logicals), and
      (b) the orbits of the starts cover all qubits.
    Proof: for a minimum-weight nontrivial logical c let i be the least index with c meeting
    orbit(q_i). Some g in Gamma maps a qubit of c in that orbit to q_i; g(c) is again a nontrivial
    logical of the same weight, contains q_i and (orbits are Gamma-invariant) misses every earlier
    orbit. (b) is enforced (ValueError). (a) is the caller's duty; orbits_2bga builds and verifies it.
    Default (starts=None, orbits=None): starts 0..n-1, singleton orbits, i.e. "q_i is the smallest
    qubit of c", the usual dist-m4ri order.
    """
    HX = np.asarray(HX, dtype=np.uint8) & 1
    HZ = np.asarray(HZ, dtype=np.uint8) & 1
    if sector == 'Z':
        H, Other = HX, HZ
    elif sector == 'X':
        H, Other = HZ, HX
    else:
        raise ValueError(sector)
    m, n = H.shape
    t0 = time.time()
    T = int(T)
    if starts is None:
        starts = list(range(n))
    starts = [int(s) for s in starts]
    if orbits is None:
        orbits = [[q] for q in range(n)]
    orb_of = -np.ones(n, dtype=np.int64)
    for oi, o in enumerate(orbits):
        for q in o:
            if orb_of[q] != -1:
                raise ValueError('orbits overlap at qubit %d' % q)
            orb_of[q] = oi
    if (orb_of < 0).any():
        raise ValueError('orbits must partition all qubits')
    if set(int(orb_of[s]) for s in starts) != set(range(len(orbits))):
        raise ValueError('orbits of the starts do not cover all qubits: "none" would not be a proof')

    tests = _logical_tests(H, Other)
    k = len(tests)
    stats = dict(sector=sector, T=T, k=k, n=n, nodes=0, per_start=[], seconds=0.0, n_starts=len(starts))
    if k == 0 or T < 1:
        stats['seconds'] = time.time() - t0
        return 'none', None, stats
    KW = max(1, (k + 63) // 64)
    lmask = _pack_cols(tests)
    colv = _pack_cols(H)
    W = colv.shape[1]
    cptr = np.zeros(n + 1, dtype=np.int64)
    cptr[1:] = np.cumsum(H.sum(axis=0))
    crow = np.concatenate([np.nonzero(H[:, q])[0] for q in range(n)]).astype(np.int64) if cptr[-1] else np.zeros(0, np.int64)
    rptr = np.zeros(m + 1, dtype=np.int64)
    rptr[1:] = np.cumsum(H.sum(axis=1))
    rcol = np.concatenate([np.nonzero(H[r])[0] for r in range(m)]).astype(np.int64) if rptr[-1] else np.zeros(0, np.int64)
    maxcw = int(H.sum(axis=0).max())
    S = np.zeros(T + 2, dtype=np.int64)
    blocked0 = np.zeros(n, dtype=np.uint8)
    budget = 0 if max_nodes is None else int(max_nodes)
    status = 'none'
    support = None
    for si, s in enumerate(starts):
        if blocked0[s]:  # start lies in an earlier start's orbit: nothing new to search
            stats['per_start'].append((s, 0))
            continue
        left = 0 if max_nodes is None else max(1, budget - stats['nodes'])
        st, ln, nd = _search(s, T, W, KW, colv, cptr, crow, rptr, rcol, lmask, blocked0, maxcw, left, _CTZ, S)
        stats['nodes'] += int(nd)
        stats['per_start'].append((s, int(nd)))
        if st == 1:
            support = sorted(int(q) for q in S[:ln])
            status = 'found'
            break
        if st == 2:
            status = 'capped'
            break
        for q in orbits[int(orb_of[s])]:
            blocked0[q] = 1
    if support is not None:  # independent re-verification of the witness
        c = np.zeros(n, dtype=np.int64)
        c[support] = 1
        assert not ((H.astype(np.int64) @ c) % 2).any(), 'witness not in kernel'
        assert ((tests.astype(np.int64) @ c) % 2).any(), 'witness trivial'
        assert len(support) <= T
    stats['seconds'] = time.time() - t0
    return status, support, stats


# ------------------------------------------------------------------------------ automorphisms
def _perm_preserves(M, perm):
    """True iff permuting the columns of M by qubit map q -> perm[q] maps the row set of M into itself."""
    inv = np.empty_like(perm)
    inv[perm] = np.arange(len(perm))
    rows = {np.packbits(r).tobytes() for r in M}
    return all(np.packbits(r[inv]).tobytes() in rows for r in M)


def orbits_2bga(G, HX, HZ, return_gens=False):
    """Qubit orbits of a two-block group-algebra code under translation automorphisms.
    Qubits 0..o-1 are the left block (group element g), o..2o-1 the right block. Candidate generators,
    for every h in G: each block is moved by g -> g*h or g -> h*g (4 combinations). A candidate is
    used only if it maps the row set of HX into itself and the row set of HZ into itself (checked
    numerically here, so only genuine automorphisms enter; for abelian groups all candidates pass,
    for non-abelian groups only those compatible with the code, e.g. central h or h fixing a or b)."""
    o = G.order
    HX = np.asarray(HX, dtype=np.uint8)
    HZ = np.asarray(HZ, dtype=np.uint8)
    assert HX.shape == (o, 2 * o) and HZ.shape == (o, 2 * o)
    g = np.arange(o)
    gens = []
    for h in range(o):
        maps = {'R': G.mul[g, h], 'L': G.mul[h, g]}
        for kl in 'RL':
            for kr in 'RL':
                perm = np.concatenate([maps[kl], o + maps[kr]]).astype(np.int64)
                if (perm == np.arange(2 * o)).all():
                    continue
                if _perm_preserves(HX, perm) and _perm_preserves(HZ, perm):
                    gens.append((h, kl, kr, perm))
    parent = list(range(2 * o))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for _, _, _, perm in gens:
        for q in range(2 * o):
            a, b = find(q), find(int(perm[q]))
            if a != b:
                parent[max(a, b)] = min(a, b)
    groups = {}
    for q in range(2 * o):
        groups.setdefault(find(q), []).append(q)
    orbs = sorted(groups.values(), key=lambda x: x[0])
    if return_gens:
        return orbs, [(h, kl, kr) for h, kl, kr, _ in gens]
    return orbs
