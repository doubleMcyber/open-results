"""Check the sharp GF(4) bound for the 35 balanced cuts of eight parties."""
from functools import lru_cache
from itertools import combinations, permutations, product

V = tuple(range(8))
BASE = frozenset(range(4))
CUTS = tuple(s for s in combinations(V, 4) if 0 in s)
CUT_ID = {frozenset(s): i for i, s in enumerate(CUTS)}
# 0, 1, t, t+1 for t^2=t+1. Addition is XOR.
MUL = ((0, 0, 0, 0), (0, 1, 2, 3), (0, 2, 3, 1), (0, 3, 1, 2))
INV = {1: 1, 2: 3, 3: 2}
I2 = (1, 0, 0, 1)
MATRICES = tuple(product(range(4), repeat=4))


def cut_id(s):
    return CUT_ID[frozenset(s if 0 in s else set(V) - set(s))]


def matchings(vertices):
    if not vertices:
        yield ()
        return
    a, *rest = vertices
    for i, b in enumerate(rest):
        for tail in matchings(rest[:i] + rest[i + 1:]):
            yield ((a, b),) + tail


def determinant_patterns():
    basis = {}
    perfect = tuple(matchings(V))
    assert len(perfect) == 105 and len(CUTS) == 35
    for matching in perfect:
        word = sum(1 << i for i, s in enumerate(CUTS)
                   if all((a in s) != (b in s) for a, b in matching))
        while word and word.bit_length() in basis:
            word ^= basis[word.bit_length()]
        if word:
            basis[word.bit_length()] = word
    assert len(basis) == 14
    words = [0]
    for row in basis.values():
        words.extend([v ^ row for v in words])

    # Bit k of columns[i] tells whether words[k] has coordinate i set.
    columns = [int("".join("1" if word >> i & 1 else "0" for word in reversed(words)), 2)
               for i in range(len(CUTS))]
    patterns = set()
    any_high = (1 << len(words)) - 1
    for low in words:
        allowed = any_high
        for i, column in enumerate(columns):
            if not (low >> i & 1):
                allowed &= column
        while allowed:
            bit = allowed & -allowed
            patterns.add((low, words[bit.bit_length() - 1]))
            allowed ^= bit
    assert len(patterns) == 10800
    return patterns


def pattern_orbits():
    patterns = determinant_patterns()
    moves = []
    for i in range(7):
        image = list(V)
        image[i], image[i + 1] = image[i + 1], image[i]
        moves.append(tuple(cut_id({image[v] for v in s}) for s in CUTS))

    @lru_cache(None)
    def permute(move, word):
        return sum(((word >> i) & 1) << j for i, j in enumerate(moves[move]))

    while patterns:
        rep = min(patterns)
        queue = [rep]
        patterns.remove(rep)
        for a, b in queue:
            images = [(b, a), (a ^ b, b)]  # generate all permutations of 1,t,t+1
            images.extend((permute(i, a), permute(i, b)) for i in range(7))
            for item in images:
                if item in patterns:
                    patterns.remove(item)
                    queue.append(item)
        yield rep, len(queue)


def det4(mat):
    value = 0
    for j, k, l, m in permutations(range(4)):
        left = MUL[mat[0][j]][mat[1][k]]
        right = MUL[mat[2][l]][mat[3][m]]
        value ^= MUL[left][right]
    return value


def det2(mat):
    a, b, c, d = mat
    return MUL[a][d] ^ MUL[b][c]


def plus(x, y):
    return tuple(a ^ b for a, b in zip(x, y))


def complete(weights, x, y):
    """Solve w0 I + w1 X + w2 Y + w3 Z = 0 for Z over GF(4)."""
    u, v, w, z = weights
    return tuple(MUL[INV[z]][MUL[u][a] ^ MUL[v][b] ^ MUL[w][c]]
                 for a, b, c in zip(I2, x, y))


def obstruction(pattern):
    low, high = pattern
    p = [((low >> k) & 1) | (((high >> k) & 1) << 1) for k in range(len(CUTS))]

    def raw(rows, cols):
        s = BASE.difference(rows).union(j + 4 for j in cols)
        return MUL[p[cut_id(s)]][INV[p[cut_id(BASE)]]]

    ds = [[raw((i,), (j,)) for j in range(4)] for i in range(4)]
    alpha = [MUL[x][INV[ds[0][0]]] for x in ds[0]]
    beta = [r[0] for r in ds]

    def target(rows, cols):
        h = raw(rows, cols)
        for i in rows:
            h = MUL[h][INV[beta[i]]]
        for j in cols:
            h = MUL[h][INV[alpha[j]]]
        return h

    pairs = ((1, 2), (1, 3), (2, 3))
    options = {}
    for i in (1, 2, 3):
        cells = {}
        for j in (1, 2, 3):
            d = target((i,), (j,))
            e = target((0, i), (0, j))
            cells[j] = {x for x in MATRICES if det2(x) == d and det2(plus(x, I2)) == e}
        required = [target((0, i), pair) for pair in pairs]
        rows = set()
        for x, y in product(cells[1], cells[2]):
            z = complete(alpha, x, y)
            row = (I2, x, y, z)
            if z in cells[3] and [det2(plus(row[j], row[k])) for j, k in pairs] == required:
                rows.add(row)
        options[i] = rows

    joint = passed = 0
    required_minor = target((1, 2), (1, 2))
    for r, s in product(options[1], options[2]):
        last = (I2,) + tuple(complete(beta, r[j], s[j]) for j in (1, 2, 3))
        if last not in options[3]:
            continue
        joint += 1
        minor = [row[1][k:k+2] + row[2][k:k+2] for row in (r, s) for k in (0, 2)]
        if det4(minor) == required_minor:
            passed += 1
    return tuple(len(options[i]) for i in (1, 2, 3)), joint, passed


def check_example():
    weights = (0, 1, 0, 1, 1, 1, 1, 2)
    representatives = ((0, 1), (0, 2), (0, 4), (0, 5), (0, 6), (0, 7), (4, 5), (4, 6))
    rotation = (1, 2, 3, 0, 5, 6, 7, 4)
    edge = {}
    for (i, j), weight in zip(representatives, weights):
        for _ in range(4):
            edge[i, j] = edge[j, i] = weight
            i, j = rotation[i], rotation[j]
    assert len(edge) == 56
    p = [det4([[edge[i, j] for j in sorted(set(V) - set(s))] for i in s]) for s in CUTS]
    singular = [s for s, d in zip(CUTS, p) if d == 0]
    assert singular == [(0, 2, 4, 6)]
    pattern = (sum((d & 1) << k for k, d in enumerate(p)),
               sum((d >> 1) << k for k, d in enumerate(p)))
    counts = obstruction(pattern)
    assert counts[-1] > 0
    print("Example: 34 nonsingular cuts. Singular side:", singular[0])
    print("Positive control: row options, joint rows, passing final minor:", counts)


def main():
    check_example()
    expected = {10080: ((12, 60, 12), 0, 0), 720: ((60, 60, 60), 120, 0)}
    for pattern, size in pattern_orbits():
        counts = obstruction(pattern)
        print("Pattern:", pattern, "orbit:", size, "counts:", counts)
        assert counts == expected.pop(size)
    assert not expected


if __name__ == "__main__":
    main()
