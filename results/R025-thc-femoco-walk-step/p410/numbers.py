"""Python evaluation of the P4.10 Lean definitions in lean/THCFactorization.lean.

This is a hand port of the Lean definitions to exact integer and Fraction arithmetic.
It is not a Lean evaluation. Line numbers refer to lean/THCFactorization.lean
(44,015 lines, sha256 7df98e958a471bead42b5b2c3ccddcdd1328b679a9cc710d24d426a65ff3d40e).
Lines 1-38,455 of that file are identical to the P4.9 file (../p49/lean/THCFactorization.lean),
and lines 38,458-42,556 of the P4.9 file reappear unchanged 593 lines later, so the shared
definitions below are the ones ported in ../p49/numbers.py. The P4.10 definitions are
aliasTCG, pairTCG, stepTCG, coreWorkCG, baseWidthCG, workWidthCG, scratchCG and tCostCG.
The P4.9 definitions stepTCF and scratchCF are ported from ../p49/lean/THCFactorization.lean
(lines 42676-42681, 43017, 38057-38067, 43006) for the comparison.
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


# --- T per walk step, shared parts (lines 32527, 39063-39067, 40075, 41836-42246)
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


# --- P4.10 T per walk step (lines 43413-43418, 43785): one decoder call per step instead of two.
# The decoder's work register stays live through SELECT, and the PREPARE inverse uncomputes it by
# measurement at 0 T (DecodeCS.decodeCloseSteps), so aliasTCG charges decodeTC once.
def aliasTCG(N, M, a):
    m, w = slotBitsS(N, M), wordBitsC(N, M, a)
    return stageTY(m, w, dC(N, M)) + closeTY(m, w, dC(N, M)) + decodeTC(N, M, a)


def pairTCG(N, M, a, beth): return aliasTCG(N, M, a) + 16 * bIC(N, M) + selTT(N, M, beth)


def stepTCG(N, M, a, beth):
    assert N != 0 and 2 <= beth  # the stepTP branch is not used at these parameters
    return pairTCG(N, M, a, beth)


# --- P4.9 T per walk step, for the comparison (P4.9 file, lines 42676-42681, 43017)
def aliasTCF(N, M, a):
    m, w = slotBitsS(N, M), wordBitsC(N, M, a)
    return stageTY(m, w, dC(N, M)) + closeTY(m, w, dC(N, M)) + 2 * decodeTC(N, M, a)


def pairTCF(N, M, a, beth): return aliasTCF(N, M, a) + 16 * bIC(N, M) + selTT(N, M, beth)


def stepTCF(N, M, a, beth):
    assert N != 0 and 2 <= beth  # the stepTP branch is not used at these parameters
    return pairTCF(N, M, a, beth)


# --- scratch, shared parts (lines 20724, 22996, 26544-26569, 28926, 29213-29217, 33329)
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


# --- P4.10 scratch (lines 38470-38480, 43774): the decoder work register gets its own region
def coreWorkCG(N, M, a):
    m = slotBitsS(N, M)
    return max(ancPM(N, M, a), amWork(m, wordBitsC(N, M, a)) + (m + 1))


def baseWidthCG(N, M, a, beth):
    return coreWorkCG(N, M, a) + wordBitsC(N, M, a) + selRScr(N, bIC(N, M), beth) + decWorkC(N, M, a)


def workWidthCG(N, M, a, beth):
    return baseWidthCG(N, M, a, beth) + bankWidth(slotBitsS(N, M), wordBitsC(N, M, a))


def scratchCG(N, M, a, beth):
    assert N != 0 and 2 <= beth  # the scratchG branch is not used at these parameters
    return workWidthCG(N, M, a, beth)


# --- P4.9 scratch, for the comparison (P4.9 file, lines 38057-38067, 43006)
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


# --- totals (lines 244-245, 25752-25753, 43788-43789) and qubits (spec abbrev, line 43934)
def kappaC(N, M, a): return Fr(2**gC(N, M, a), 4 * dC(N, M) * 2**a)


def qpeWalkSteps(alpha, eps): return ceil(PI * alpha / (2 * eps))


def tCostCG(N, M, a, beth, lam, eps):
    return qpeWalkSteps(max(Fr(1), kappaC(N, M, a) * lam), eps) * stepTCG(N, M, a, beth)


def totalQubits(N, M, a, beth, scratch):  # 2N + thcBlockAncillas + thcScratchAncillas + thcCatalystQubits
    return 2 * N + blockAncC(N, M, a) + scratch(N, M, a, beth) + beth


# Lee et al., arXiv:2011.03494v3, Table III and Eq. 25 (see VERIFY.md)
CASES = [
    # name, N, M, aleph, beth, lamMax, Lee Toffolis, Lee qubits
    ("Reiher", 54, 350, 10, 16, Fr("306.3"), Fr("5.3e9"), 2142),
    ("Li", 76, 450, 10, 20, Fr("1201.5"), Fr("3.2e10"), 2196),
]
EPS = Fr("0.001")
# Lean #eval outputs, quoted in VERIFY.md: (stepTCG, scratchCG, stepTCF, scratchCF)
PINS = {"Reiher": (42684, 9113, 43868, 7699), "Li": (66728, 14528, 67944, 13075)}
# R025 P4.9 values (p49/numbers.py): walk steps, total T, qubits
P49 = {"Reiher": (512886, 22499283048, 7873), "Li": (2435956, 165508594464, 13300)}
# R025 P4.4 values: stepTG, total T, qubits
P44 = {"Reiher": (57708, 29597625288, 6107), "Li": (95308, 232166094448, 11473)}

for name, N, M, a, beth, lam, leeToff, leeQ in CASES:
    step, scr = stepTCG(N, M, a, beth), scratchCG(N, M, a, beth)
    step9, scr9 = stepTCF(N, M, a, beth), scratchCF(N, M, a, beth)
    assert (step, scr, step9, scr9) == PINS[name], (name, step, scr, step9, scr9)
    kap = kappaC(N, M, a)
    steps = qpeWalkSteps(max(Fr(1), kap * lam), EPS)
    leeSteps = qpeWalkSteps(lam, EPS)
    leeStep = 4 * leeToff / leeSteps
    total = tCostCG(N, M, a, beth, lam, EPS)
    q = totalQubits(N, M, a, beth, scratchCG)
    q9 = totalQubits(N, M, a, beth, scratchCF)
    steps9, t9, q9pin = P49[name]
    assert steps == steps9 and q9 == q9pin and steps * step9 == t9  # kappa and walk steps unchanged from P4.9
    s44, t44, q44 = P44[name]
    print(f"{name}: N={N} M={M} aleph={a} beth={beth} lamMax={lam}")
    print(f"  gC={gC(N, M, a)} dC={dC(N, M)} kappaC={kap} = {float(kap):.6f}")
    print(f"  slotBitsS={slotBitsS(N, M)} wordBitsC={wordBitsC(N, M, a)} decoder ANDs={dcBudget(N, M, a)}"
          f" decodeTC={decodeTC(N, M, a)} decWorkC={decWorkC(N, M, a)}")
    print(f"  aliasTCG={aliasTCG(N, M, a)} (P4.9 aliasTCF={aliasTCF(N, M, a)}) 16*bIC={16 * bIC(N, M)}"
          f" selTT={selTT(N, M, beth)}")
    print(f"  stepTCG={step} (Lean #eval pin {PINS[name][0]}); P4.9 stepTCF={step9} (pin {PINS[name][2]});"
          f" difference {step9 - step}")
    print(f"  walk steps ceil(pi*kappa*lam/(2*0.001))={steps} (P4.9 {steps9})")
    print(f"  tCostCG={total} = {float(total):.4e}")
    print(f"  blockAncC={blockAncC(N, M, a)} scratchCG={scr} (Lean #eval pin {PINS[name][1]});"
          f" P4.9 scratchCF={scr9} (pin {PINS[name][3]}); difference +{scr - scr9}; catalyst={beth}")
    print(f"  coreWorkCF={coreWorkCF(N, M, a)} coreWorkCG={coreWorkCG(N, M, a)}")
    print(f"  thcTotalLogicalQubits={q} (P4.9 {q9})")
    print(f"  Lee: steps={leeSteps} T per step={float(leeStep):.1f} total T={float(4 * leeToff):.3e} qubits={leeQ}")
    print(f"  Lee minus stepTCG: {float(leeStep - step):.1f} T per step")
    print(f"  ratios to Lee: per step {float(step / leeStep):.4f}, total {float(total / (4 * leeToff)):.4f},"
          f" qubits {float(Fr(q, leeQ)):.3f}")
    print(f"  ratios to P4.9: per step {float(Fr(step, step9)):.4f}, total {float(Fr(total, t9)):.4f},"
          f" qubits {float(Fr(q, q9)):.4f}")
    print(f"  ratios to P4.4: per step {float(Fr(step, s44)):.4f}, total {float(Fr(total, t44)):.4f},"
          f" qubits {float(Fr(q, q44)):.4f}")
