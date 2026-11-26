"""Exact arithmetic constraints on the residual ten-cycle type."""

from collections import defaultdict
from itertools import combinations, permutations, product


def permute(rows, perm):
    return tuple(sum(((rows[i] >> j) & 1) << v for v, j in enumerate(perm)) for i in perm)


def graphs5():
    """Adjacency rows as bitsets for every labeled graph on five vertices."""
    for m in range(1024):
        rows = [0] * 5
        for t, (i, j) in enumerate(combinations(range(5), 2)):
            if m >> t & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
        yield tuple(rows)


def gram(rows):
    """Compute row inner products over the field of two elements."""
    return tuple(sum(((a & b).bit_count() % 2) << j for j, b in enumerate(rows)) for a in rows)


def quadratic(rows):
    return tuple(g ^ r ^ 1 << i for i, (r, g) in enumerate(zip(rows, gram(rows))))


def odd_graphs():
    """Enumerate the parity patterns in the block order of the written proof."""
    ts = defaultdict(list)
    for r in graphs5():
        ts[quadratic(r)].append(r)
    seen = set()
    for r in graphs5():
        if r in seen:
            continue
        seen.update(permute(r, p) for p in permutations(range(5)))
        target = quadratic(r)

        def extend(bs, cols):
            i = len(bs)
            if i == 5:
                bt = tuple(sum(((b >> j) & 1) << u for u, b in enumerate(bs)) for j in range(5))
                for t in ts[gram(bt)]:
                    if any(u.bit_count() + v.bit_count() not in (1, 5) for u, v in zip(t, bt)):
                        continue
                    if any(
                        ((r[i] & bt[j]).bit_count() - (bs[i] & t[j]).bit_count()) % 2
                        for i in range(5)
                        for j in range(5)
                    ):
                        continue
                    yield tuple(u | v << 5 for u, v in zip(r, bs)) + tuple(
                        u | v << 5 for u, v in zip(bt, t)
                    )
                return
            for b in range(32):
                if b.bit_count() + r[i].bit_count() not in (1, 5):
                    continue
                if any(
                    ((b & v).bit_count() % 2) != ((target[i] >> j) & 1) for j, v in enumerate(bs)
                ):
                    continue
                cnew = [(x << 1) | ((b >> j) & 1) for j, x in enumerate(cols)]
                if cnew != sorted(cnew):
                    continue
                yield from extend(bs + [b], cnew)

        yield from extend([], [0] * 5)


def top_blocks(perm, heavy):
    """Build signed top blocks R and C with the prescribed Gram matrix."""
    norm = 13 if heavy == 2 else 9
    for signs in product((-1, 1), repeat=6):
        r = [[0] * 5 for _ in range(5)]
        for i in range(1, 5):
            r[0][i] = r[i][0] = 1
        for (i, j), v in zip(combinations(range(1, 5), 2), signs):
            r[i][j] = r[j][i] = v
        target = [
            [norm * (i == j) - r[i][j] - sum(a * b for a, b in zip(r[i], r[j])) for j in range(5)]
            for i in range(5)
        ]
        rows = []
        for i in range(5):
            choices = []
            available = [j for j in range(5) if j not in (i, perm[i])]
            for support in (combinations(available, 2) if heavy == 2 else [(perm[i],)]):
                for values in product((-2, 2), repeat=heavy):
                    row = [0] * 5
                    row[i] = 1
                    for j, v in zip(support, values):
                        row[j] = v
                    choices.append(row)
            rows.append(choices)

        def extend(fixed):
            i = len(fixed)
            if i == 5:
                if all(sum(abs(x[j]) == 2 for x in fixed) == heavy for j in range(5)):
                    yield fixed
                return
            for row in rows[i]:
                if all(
                    sum(a * b for a, b in zip(row, prev)) == target[i][j]
                    for j, prev in enumerate(fixed)
                ):
                    yield from extend(fixed + [row])

        for c in extend([]):
            yield r, c


def signed_blocks(perm, heavy):
    """Complete the bottom block subject to the cross equation RC + CS = 0."""
    for r, c in top_blocks(perm, heavy):
        for vals in product((-1, 1), repeat=10):
            s = [[0] * 5 for _ in range(5)]
            for (i, j), v in zip(combinations(range(5), 2), vals):
                s[i][j] = s[j][i] = v
            if any(
                sum(r[i][k] * c[k][j] + c[i][k] * s[k][j] for k in range(5))
                for i in range(5)
                for j in range(5)
            ):
                continue
            yield [r[i] + c[i] for i in range(5)] + [
                [c[j][i] for j in range(5)] + [s[i][j] - (i == j) for j in range(5)]
                for i in range(5)
            ]


def ramsey_clauses(plus, minus):
    # Literal 1 is permanently true. Every other variable is a free uniform block.
    v = 1
    cells = {}
    for i, j in combinations(range(20), 2):
        a, b = i // 2, j // 2
        p, q = plus[a][b], minus[a][b]
        numerator = p + q if (i - j) % 2 == 0 else p - q
        assert numerator in (-2, 0, 2)
        mode = numerator // 2
        if mode:
            cells[i, j] = (mode, -mode)
        else:
            v += 1
            cells[i, j] = (v, v)
    edges = [[0] * 40 for _ in range(40)]
    for i, j in combinations(range(40), 2):
        a, b = i // 2, j // 2
        if a == b:
            lit = 1 if a // 2 >= 5 else -1
        else:
            lit = cells[a, b][(i - j) % 2]
        edges[i][j] = edges[j][i] = lit
    clauses = set()
    for color in [1, -1]:

        def extend(vertices, candidates, free):
            if len(vertices) == 5:
                clauses.add(frozenset(free))
                return
            for t, x in enumerate(candidates):
                if len(candidates) - t < 5 - len(vertices):
                    break
                add = [-color * edges[x][w] for w in vertices]
                if 1 in add:
                    continue
                extend(vertices + [x], candidates[t + 1 :], free | {a for a in add if a != -1})

        extend([], list(range(40)), set())
    return edges, clauses


def reduce_clauses(cs):
    while True:
        if frozenset() in cs:
            return None
        units = {next(iter(c)) for c in cs if len(c) == 1}
        if not units:
            return cs
        neg = {-u for u in units}
        if units & neg:
            return None
        cs = {c - neg for c in cs if not c & units}


def solve(clauses, limit=200000):
    """Store active clauses by remaining length, one bit per clause."""
    clauses = sorted(tuple(sorted(c)) for c in clauses)
    occ = defaultdict(int)
    layers = [0] * (1 + max(map(len, clauses)))
    for i, c in enumerate(clauses):
        bit = 1 << i
        layers[len(c)] |= bit
        for lit in c:
            occ[lit] |= bit
    nodes = 0

    def setlit(layers, lit):
        sat, neg = occ[lit], occ[-lit]
        fixed = ~(sat | neg)
        return [(m & fixed) | (n & neg) for m, n in zip(layers, layers[1:] + [0])]

    def visit(ls, used):
        nonlocal nodes
        nodes += 1
        if nodes > limit:
            raise RuntimeError("search bound")
        while ls[1] and not ls[0]:
            bit = ls[1] & -ls[1]
            c = clauses[bit.bit_length() - 1]
            (lit,) = [v for v in c if not (used >> abs(v)) & 1]
            ls = setlit(ls, lit)
            used |= 1 << abs(lit)
        if ls[0]:
            return False
        m = next((q for q in ls if q), 0)
        if not m:
            return True
        c = clauses[(m & -m).bit_length() - 1]
        cand = [v for v in c if not (used >> abs(v)) & 1]
        lit = max(cand, key=lambda v: ((occ[v] | occ[-v]) & m).bit_count())
        used |= 1 << abs(lit)
        return visit(setlit(ls, lit), used) or visit(setlit(ls, -lit), used)

    return visit(layers, 0), nodes


def check_template(edges, plus, minus):
    """Reconstruct the prescribed action on all cycle sum/difference vectors."""
    for chosen_bit in (0, 1):
        adjacency = [[0] * 40 for _ in range(40)]
        for i, j in combinations(range(40), 2):
            literal = edges[i][j]
            value = literal == 1 if abs(literal) == 1 else bool(chosen_bit)
            adjacency[i][j] = adjacency[j][i] = int(value)
        for sign, matrix in ((1, plus), (-1, minus)):
            for cycle in range(10):
                # On the four vertices of the cycle the vector is (1,-1,sign,-sign).
                for row in range(40):
                    actual = sum(
                        adjacency[row][4 * cycle + j] * w
                        for j, w in enumerate((1, -1, sign, -sign))
                    )
                    expected = matrix[row // 4][cycle] * (1, -1, sign, -sign)[row % 4]
                    assert actual == expected


def direct_clauses(edges):
    """Independently visit every five-set and both of its forbidden colors."""
    all_clauses = set()
    for five in combinations(range(40), 5):
        literals = {edges[i][j] for i, j in combinations(five, 2)}
        if -1 not in literals:
            all_clauses.add(frozenset(-v for v in literals if v != 1))
        if 1 not in literals:
            all_clauses.add(frozenset(v for v in literals if v != -1))
    return all_clauses


def set_dpll(clauses):
    """Independent DPLL using literal sets and simultaneous unit propagation."""
    residual = reduce_clauses(clauses)
    if residual is None:
        return False
    if not residual:
        return True
    small = min(residual, key=lambda c: (len(c), tuple(sorted(c))))
    lit = min(small, key=abs)
    return any(set_dpll(residual | {frozenset([l])}) for l in (lit, -lit))


if __name__ == "__main__":
    patterns = list(odd_graphs())
    low = tuple(1 << (9 - i) for i in range(10))
    high = tuple(low[i] | ((31 if i < 5 else 31 << 5) ^ (1 << i)) for i in range(10))
    assert len(patterns) == 2 and set(patterns) == {low, high}
    print("Odd-position graphs: matched pairs, or two five-cliques with a matching.")
    for perm in ((1, 2, 3, 4, 0), (1, 0, 3, 4, 2)):
        plus_blocks = list(signed_blocks(perm, 2))
        minus_blocks = list(signed_blocks(perm, 1))
        counts = (len(plus_blocks), len(minus_blocks))
        assert counts == ((2, 1) if perm[0:2] == (1, 2) else (0, 1))
        print("Heavy-minus permutation, surviving plus and minus matrices:", perm, counts)
        for plus in plus_blocks:
            for minus in minus_blocks:
                edges, clauses = ramsey_clauses(plus, minus)
                check_template(edges, plus, minus)
                assert direct_clauses(edges) == clauses
                feasible, nodes = solve(clauses)
                assert not feasible and not set_dpll(clauses)
                print("Distinct clauses, DPLL nodes, verdict:", len(clauses), nodes, "UNSAT")
