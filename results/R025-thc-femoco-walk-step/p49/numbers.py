"""Python evaluation of the P4.9 Lean definitions in lean/THCFactorization.lean.

This is a hand port of the Lean definitions to exact integer and Fraction arithmetic.
It is not a Lean evaluation. Line numbers refer to lean/THCFactorization.lean
(43,247 lines, sha256 72fa0bd31c1dcd2ec4859ed900c02c8dc2b0374e52587ff8ae93199d05ea5ff7).
Lean's natural-number subtraction truncates at 0; `sub` below does the same.
"""
from fractions import Fraction as Fr

# pi to 31 decimal places, as in R025's walk-step count.
PI = Fr(31415926535897932384626433832795, 10**31)


def sub(a, b):
    return a - b if a >= b else 0


def clog2(n):  # Nat.clog 2 n: least k with n <= 2^k
    k = 0
    while (1 << k) < n:
        k += 1
    return k


def log2(n):  # Nat.log 2 n: floor log, 0 for n <= 1
    return n.bit_length() - 1 if n >= 1 else 0


def ceil(x):  # Nat.ceil on a nonnegative Fraction
    return -((-x.numerator) // x.denominator)


# --- sizes (lines 14328-14427, 15845-15848, 17121, 17816, 25697, 27124, 27595-27599, 34497-34498)
def dC(N, M): return N + M * (M + 1) // 2
def bIC(N, M): return clog2(2 * (N + M) + 1)
def idxC(N, M): return 2 * bIC(N, M) + 1
def gC(N, M, a): return max(idxC(N, M) + 1, clog2(4 * dC(N, M) * 2**a))
def muC(N, M, a): return sub(gC(N, M, a), idxC(N, M) + 1)
def nSupp(N, M): return 2 * N + M * (2 * M - 1) + 1
def sA(N, M): return clog2(nSupp(N, M))
def bP(N, M): return idxC(N, M) + 1
def gP(N, M, a): return bP(N, M) + muC(N, M, a)
def blockAncC(N, M, a): return bP(N, M) + gP(N, M, a)
def halfWidth(N, M, a): return sub(gC(N, M, a), 2)
def slotBitsS(N, M): return clog2(dC(N, M))
def highBitsS(N, M): return sub(bIC(N, M), 1)
def extraS(N, M, a): return sub(sub(halfWidth(N, M, a), slotBitsS(N, M)), a)
def dcSlotWidth(N, M): return clog2(dC(N, M) + 1)
def wordBitsC(N, M, a): return dcSlotWidth(N, M) + 2 + a


# --- the generated decoder network (lines 35311-35507), ported op for op
class Net:
    def __init__(self):
        self.ops = []  # ('add'|'mul', x, y)

    def node(self, kind, x, y):
        self.ops.append((kind, x, y))
        return ('node', len(self.ops) - 1)

    def xor(self, x, y): return self.node('add', x, y)
    def and_(self, x, y): return self.node('mul', x, y)
    def not_(self, x): return self.xor(x, ('one',))


def dcBit(c, i): return ('one',) if (c >> i) & 1 else ('zero',)
def dcVec(k, f): return [f(i) for i in range(k)]
def dcGet(v, k): return v[k] if k < len(v) else ('zero',)
def dcTri(j): return j * (j + 1) // 2


def dcMux(n, c, u, v): return n.xor(v, n.and_(c, n.xor(u, v)))


def dcBorrow(n, x, y, c):
    a = n.xor(n.not_(x), c)
    b = n.xor(y, c)
    return n.xor(c, n.and_(a, b))


def dcSub(n, u, v):
    r, c = [], ('zero',)
    for b in range(len(u)):
        x, y = dcGet(u, b), dcGet(v, b)
        r.append(n.xor(x, n.xor(y, c)))
        c = dcBorrow(n, x, y, c)
    return r, c


def dcAddConst(n, u, constant, h):
    r, c = [], ('zero',)
    for b in range(h):
        x, y = dcGet(u, b), dcBit(constant, b)
        r.append(n.xor(x, n.xor(y, c)))
        if b + 1 < h:
            c = n.xor(c, n.and_(n.xor(x, c), n.xor(y, c)))
    return r


def dcPick(n, N, M, a):
    m, t = slotBitsS(N, M), dcSlotWidth(N, M)
    _, c = dcSub(n, dcVec(a, lambda b: ('seed', 2 + m + b)), dcVec(a, lambda b: ('raw', t + 2 + b)))
    y = []
    for k in range(t):
        x = ('seed', 2 + k) if k < m else ('zero',)
        v = n.xor(('raw', k), dcBit(dC(N, M), k))
        y.append(dcMux(n, c, x, v))
    z = n.xor(('raw', t), n.and_(c, ('raw', t + 1)))
    return y, z


def dcUnrank(n, ell, diff):
    j = dcVec(ell, lambda _: ('zero',))
    r = diff
    for k in reversed(range(ell)):
        q = ell + k + 1
        lo = sub(k, 1)
        borrow = n.not_(dcGet(r, lo))
        flips = []
        for b in range(lo + 1, q):
            x = dcGet(r, b)
            v = n.xor(dcGet(j, sub(b, k)), dcBit(dcTri(2**k), b))
            flips.append(n.xor(v, borrow))
            borrow = dcBorrow(n, x, v, borrow)
        take = n.not_(borrow)
        nxt = dcVec(lo, lambda i: dcGet(r, i))
        nxt.append(n.xor(dcGet(r, lo), take))
        for b in range(lo + 1, q):
            nxt.append(n.xor(dcGet(r, b), n.and_(take, dcGet(flips, b - (lo + 1)))))
        r = nxt
        jj = j
        j = dcVec(ell, lambda b, take=take, jj=jj: take if b == k else dcGet(jj, b))
    return dcVec(ell, lambda i: dcGet(r, i)), j


def dcNetwork(N, M, a):
    n = Net()
    m, t, h, ell = slotBitsS(N, M), dcSlotWidth(N, M), highBitsS(N, M), clog2(M)
    y, z = dcPick(n, N, M, a)
    r, one = dcSub(n, y, dcVec(t, lambda i: dcBit(N, i)))
    _, valid = dcSub(n, y, dcVec(t, lambda i: dcBit(dC(N, M), i)))
    i, j = dcUnrank(n, ell, r)
    aa = dcAddConst(n, i, N, h)
    bb = dcAddConst(n, j, N, h)
    eqBits = [n.not_(n.xor(dcGet(i, b), dcGet(j, b))) for b in range(ell)]
    eq = eqBits[0] if eqBits else ('one',)
    for b in range(1, ell):
        eq = n.and_(eq, dcGet(eqBits, b))
    spin, tau = ('seed', 1), ('seed', 0)
    diag = n.and_(n.not_(one), eq)
    kill = n.and_(diag, n.not_(n.xor(spin, tau)))
    en = n.and_(valid, n.not_(kill))
    for b in range(extraS(N, M, a)):
        en = n.and_(en, n.not_(('seed', 2 + m + a + b)))
    first = n.and_(en, one)
    pair = n.xor(en, first)
    diagonal = n.and_(pair, eq)
    off = n.xor(pair, diagonal)
    spinA = n.and_(spin, n.xor(first, off))
    spinB = n.xor(n.and_(tau, off), diagonal)
    A, B = [spinA], [spinB]
    for b in range(h):
        c = dcBit(N + M, b)
        u = n.and_(first, n.xor(dcGet(y, b), c))
        v = n.and_(pair, n.xor(dcGet(aa, b), c))
        A.append(n.xor(c, n.xor(u, v)))
        B.append(n.xor(c, n.and_(pair, n.xor(dcGet(bb, b), c))))
    sign = n.and_(en, z)
    return A + B + [sign, ('zero',)], n.ops


def dcBudget(N, M, a):  # line 37517: number of mul ops
    return sum(1 for op in dcNetwork(N, M, a)[1] if op[0] == 'mul')


def decWorkC(N, M, a):  # line 35510
    return 3 + len(dcNetwork(N, M, a)[1])


def decodeTC(N, M, a): return 4 * dcBudget(N, M, a)  # line 37521


# --- T per walk step (lines 32527, 38470-38474, 39482, 41243-41653, 42676-42681, 43017)
def prunedAnds(m, L): return sub(sum((L + 2**(j + 1) - 1) // 2**(j + 1) for j in range(m)), 1)
def pfBlocks(s, live): return (live + 2**s - 1) // 2**s
def pfT(m, s, live): return 4 * (sub(2**s, 2) + prunedAnds(sub(m, s), pfBlocks(s, live)))
def lkSplit(m, w): return sub(m, log2(w)) // 2
def splitY(m, w): return lkSplit(m, 2 * w)


def stageTY(m, w, d):
    s = splitY(m, w)
    return 4 * (prunedAnds(sub(m, s), pfBlocks(s, d)) + (2**s - 1) * w)


def bankLiveY(m, w, d): return 2**splitY(m, w) * pfBlocks(splitY(m, w), d)
def closeTY(m, w, d): return pfT(m, m // 2, bankLiveY(m, w, d))


def unloadTU(L, bI):
    h = sub(bI, 1)
    return pfT(h, h // 2, min(L, 2**h))


def rktRowT(N, L, bI, beth):
    return (16 * sub(N, 1) * sub(beth, 2) + 8 * N
            + (4 * prunedAnds(sub(bI, 1), min(L, 2**sub(bI, 1))) + unloadTU(L, bI)))


def selTT(N, M, beth): return 2 * rktRowT(N, N + M, bIC(N, M), beth)


def aliasTCF(N, M, a):
    m, w = slotBitsS(N, M), wordBitsC(N, M, a)
    return stageTY(m, w, dC(N, M)) + closeTY(m, w, dC(N, M)) + 2 * decodeTC(N, M, a)


def pairTCF(N, M, a, beth): return aliasTCF(N, M, a) + 16 * bIC(N, M) + selTT(N, M, beth)


def stepTCF(N, M, a, beth):
    assert N != 0 and 2 <= beth  # the stepTP branch is not used at these parameters
    return pairTCF(N, M, a, beth)


# --- scratch (lines 20724, 22996, 26552-26569, 28926, 29213-29217, 33329, 38057-38067, 43006)
def aliasAnc(b, g, s): return b + 2 * g + 4
def amWord(b, g, s): return b + (b + sub(g, s))


def amWork(s, w):
    k = lkSplit(s, w)
    return 2**k * w + sub(s, k) + 1 + (2**(s // 2) * 1 + sub(s, s // 2) + 1)


def aliasAncM(b, g, s): return aliasAnc(b, g, s) + amWork(s, amWord(b, g, s))


def ancPM(N, M, a):
    return max(bP(N, M) + gP(N, M, a) + 1, aliasAncM(bP(N, M), gP(N, M, a), sA(N, M)))


def selQScr(N, bI, beth): return (N * beth + 2) + 2 * beth + bI


def selLkScr(N, bI, beth):
    return (N * beth + 2) + sub(bI, 1) + 1 + (2**(sub(bI, 1) // 2) + sub(sub(bI, 1), sub(bI, 1) // 2) + 1)


def selRScr(N, bI, beth): return selQScr(N, bI, beth) + selLkScr(N, bI, beth)
def bankWidth(m, w): return 2**lkSplit(m, w) * w


def coreWorkCF(N, M, a):
    m = slotBitsS(N, M)
    return max(ancPM(N, M, a), max(amWork(m, wordBitsC(N, M, a)) + (m + 1), decWorkC(N, M, a)))


def baseWidthCF(N, M, a, beth):
    return coreWorkCF(N, M, a) + wordBitsC(N, M, a) + selRScr(N, bIC(N, M), beth)


def workWidthCF(N, M, a, beth):
    return baseWidthCF(N, M, a, beth) + bankWidth(slotBitsS(N, M), wordBitsC(N, M, a))


def scratchCF(N, M, a, beth):
    assert N != 0 and 2 <= beth  # the scratchG branch is not used at these parameters
    return workWidthCF(N, M, a, beth)


# --- totals (lines 244-245, 25752-25753, 43020-43021) and qubits (spec abbrev, line 43166)
def kappaC(N, M, a): return Fr(2**gC(N, M, a), 4 * dC(N, M) * 2**a)


def qpeWalkSteps(alpha, eps): return ceil(PI * alpha / (2 * eps))


def tCostCF(N, M, a, beth, lam, eps):
    return qpeWalkSteps(max(Fr(1), kappaC(N, M, a) * lam), eps) * stepTCF(N, M, a, beth)


def totalQubits(N, M, a, beth):  # 2N + thcBlockAncillas + thcScratchAncillas + thcCatalystQubits
    return 2 * N + blockAncC(N, M, a) + scratchCF(N, M, a, beth) + beth


# Lee et al., arXiv:2011.03494v3, Table III and Eq. 25 (see VERIFY.md)
CASES = [
    # name, N, M, aleph, beth, lamMax, Lee Toffolis, Lee qubits
    ("Reiher", 54, 350, 10, 16, Fr("306.3"), Fr("5.3e9"), 2142),
    ("Li", 76, 450, 10, 20, Fr("1201.5"), Fr("3.2e10"), 2196),
]
EPS = Fr("0.001")
# R025 (P4.4) values for the comparison: stepTG, total T, qubits
P44 = {"Reiher": (57708, 29597625288, 6107), "Li": (95308, 232166094448, 11473)}
# Lean #eval outputs, quoted in VERIFY.md
PINS = {"Reiher": (43868, 7699), "Li": (67944, 13075)}

for name, N, M, a, beth, lam, leeToff, leeQ in CASES:
    step, scr = stepTCF(N, M, a, beth), scratchCF(N, M, a, beth)
    assert (step, scr) == PINS[name], (name, step, scr)
    kap = kappaC(N, M, a)
    steps = qpeWalkSteps(max(Fr(1), kap * lam), EPS)
    leeSteps = qpeWalkSteps(lam, EPS)
    leeStep = 4 * leeToff / leeSteps
    total = tCostCF(N, M, a, beth, lam, EPS)
    q = totalQubits(N, M, a, beth)
    s44, t44, q44 = P44[name]
    print(f"{name}: N={N} M={M} aleph={a} beth={beth} lamMax={lam}")
    print(f"  gC={gC(N, M, a)} dC={dC(N, M)} kappaC={kap} = {float(kap):.6f}")
    print(f"  slotBitsS={slotBitsS(N, M)} wordBitsC={wordBitsC(N, M, a)} decoder ANDs={dcBudget(N, M, a)}"
          f" decodeTC={decodeTC(N, M, a)} decWorkC={decWorkC(N, M, a)}")
    print(f"  aliasTCF={aliasTCF(N, M, a)} 16*bIC={16 * bIC(N, M)} selTT={selTT(N, M, beth)}")
    print(f"  stepTCF={step} (Lean #eval pin {PINS[name][0]})")
    print(f"  walk steps ceil(pi*kappa*lam/(2*0.001))={steps}")
    print(f"  tCostCF={total} = {float(total):.4e}")
    print(f"  blockAncC={blockAncC(N, M, a)} scratchCF={scr} (Lean #eval pin {PINS[name][1]}) catalyst={beth}")
    print(f"  thcTotalLogicalQubits={q}")
    print(f"  Lee: steps={leeSteps} T per step={float(leeStep):.1f} total T={float(4 * leeToff):.3e} qubits={leeQ}")
    print(f"  ratios to Lee: per step {float(step / leeStep):.4f}, total {float(total / (4 * leeToff)):.4f},"
          f" qubits {float(Fr(q, leeQ)):.3f}")
    print(f"  ratios to P4.4: per step {float(Fr(step, s44)):.4f}, total {float(Fr(total, t44)):.4f},"
          f" qubits {float(Fr(q, q44)):.4f}")


# --- P4.4 per-step cost by part, for the comparison (stepTG, line 31639; pairTS, line 30806)
def ssT(m, w, s): return 8 * (2**sub(m, s) - 1) + 8 * (2**s - 1) * w            # line 6528
def mbl2T(m, w, s, s2): return 4 * (2**sub(m, s) - 1) + 4 * (2**s - 1) * w + ssT(m, 1, s2)  # line 8395
def descBitsS(N, M): return 2 * highBitsS(N, M) + 4
def wordBitsS(N, M, a): return 2 * descBitsS(N, M) + a
def computeTS(N, M, a): return 16 * a + 8 * (descBitsS(N, M) + 3 + extraS(N, M, a))
def decodeTS(N, M, a): return 2 * computeTS(N, M, a) + 8 * (2 * highBitsS(N, M) + 3)


def aliasTS(N, M, a):  # line 27611
    m, w = slotBitsS(N, M), wordBitsS(N, M, a)
    return mbl2T(m, w, lkSplit(m, w), m // 2) + ssT(m, 1, m // 2) + 2 * decodeTS(N, M, a)


def selLkT(bI, w): return mbl2T(sub(bI, 1), w, 0, sub(bI, 1) // 2) + ssT(sub(bI, 1), 1, sub(bI, 1) // 2)


def selTR(N, M, beth):  # line 29686
    return 2 * (16 * sub(N, 1) * sub(beth, 1) + 16 * N + selLkT(bIC(N, M), N * beth + 2))


def stepTG(N, M, a, beth):
    assert 2 <= beth
    return aliasTS(N, M, a) + 2 * (8 * bIC(N, M)) + selTR(N, M, beth)


print()
print("Per-step T by part, P4.4 (stepTG) -> P4.9 (stepTCF):")
for name, N, M, a, beth, *_ in CASES:
    assert stepTG(N, M, a, beth) == P44[name][0]
    m = slotBitsS(N, M)
    old_dec, new_dec = 2 * decodeTS(N, M, a), 2 * decodeTC(N, M, a)
    old_lk, new_lk = aliasTS(N, M, a) - old_dec, aliasTCF(N, M, a) - new_dec
    print(f"  {name}: alias word {wordBitsS(N, M, a)} -> {wordBitsC(N, M, a)} bits;"
          f" PREPARE lookup {old_lk} -> {new_lk}; alias decoder (2 calls) {old_dec} -> {new_dec};"
          f" swaps {16 * bIC(N, M)} -> {16 * bIC(N, M)}; SELECT {selTR(N, M, beth)} -> {selTT(N, M, beth)};"
          f" step {stepTG(N, M, a, beth)} -> {stepTCF(N, M, a, beth)}")

print()
print("SELECT by part (two row SELECTs per step), P4.4 -> P4.9:")
for name, N, M, a, beth, *_ in CASES:
    bI, L = bIC(N, M), N + M
    kick = (2 * 16 * sub(N, 1) * sub(beth, 1), 2 * 16 * sub(N, 1) * sub(beth, 2))
    spin = (2 * 16 * N, 2 * 8 * N)
    angle = (2 * selLkT(bI, N * beth + 2),
             2 * (4 * prunedAnds(sub(bI, 1), min(L, 2**sub(bI, 1))) + unloadTU(L, bI)))
    assert sum(x[0] for x in (kick, spin, angle)) == selTR(N, M, beth)
    assert sum(x[1] for x in (kick, spin, angle)) == selTT(N, M, beth)
    print(f"  {name}: rotation kicks {kick[0]} -> {kick[1]}; spin swaps {spin[0]} -> {spin[1]};"
          f" angle lookup {angle[0]} -> {angle[1]}")
