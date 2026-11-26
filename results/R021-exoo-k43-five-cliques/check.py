"""Verify the three-addition result for Exoo's 43-vertex colouring."""
from collections import Counter
from itertools import chain, combinations
from math import comb

N = 43
RED_LENGTHS = (1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21)
BLUE_LENGTHS = tuple(d for d in range(1, 22) if d not in RED_LENGTHS)


def edge(u, v):
    return (u, v) if u < v else (v, u)


def edges(lengths):
    return [edge(i, (i + d) % N) for d in lengths for i in range(N)]


red = edges(RED_LENGTHS)
blue = edges(BLUE_LENGTHS)
red_id = {p: i for i, p in enumerate(red)}
blue_id = {p: i for i, p in enumerate(blue)}


def almost_cliques(pair, other):
    """For each K5 with unique exceptional edge pair, yield its other nine IDs."""
    u, v = pair
    common = [x for x in range(N) if edge(u, x) in other and edge(v, x) in other]
    for tri in combinations(common, 3):
        if all(p in other for p in combinations(tri, 2)):
            body = tuple(other[edge(a, b)] for a in (u, v) for b in tri)
            yield body + tuple(other[p] for p in combinations(tri, 2))


def witnesses(pair):
    """The set of all private witnesses, and those killed by each blue addition."""
    all_witnesses = 0
    killed = {}
    for i, body in enumerate(almost_cliques(pair, blue_id)):
        all_witnesses |= 1 << i
        for b in body:
            killed[b] = killed.get(b, 0) | (1 << i)
    return all_witnesses, killed


private = [witnesses(p) for p in red]
candidates = [[body for body in almost_cliques(p, red_id)
               if all(private[e][0] for e in body)] for p in blue]


def after_two(f, g):
    return [all_w & ~kills.get(f, 0) & ~kills.get(g, 0) for all_w, kills in private]


def packing(triple, live, target):
    """Choose up to target cliques, reserving one witness per body edge."""
    f, g, h = triple
    capacity = {}
    selected = []
    for body in chain(candidates[f], candidates[g], candidates[h]):
        for e in body:
            if e not in capacity:
                capacity[e] = (live[e] & ~private[e][1].get(h, 0)).bit_count()
            if capacity[e] == 0:
                break
        else:
            for e in body:
                capacity[e] -= 1
            selected.append(body)
            if len(selected) == target:
                break
    return selected


def canonical(triple):
    """Represent a translation/reflection class with a shortest edge at start 0."""
    result = []
    for sign in (1, -1):
        encoded = []
        for i in triple:
            length_index, start = divmod(i, N)
            d = BLUE_LENGTHS[length_index]
            # Reflection maps {s,s+d} to {-s-d,-s}.
            encoded.append((length_index, start if sign == 1 else (-start - d) % N))
        for j, origin in encoded:
            if j == min(triple) // N:
                result.append(tuple(sorted(k*N + (s-origin) % N for k, s in encoded)))
    return min(result)


def scan(target):
    tested = residual = 0
    representatives = set()
    for f in range(0, len(blue), N):
        for g in range(f + 1, len(blue) - 1):
            live = after_two(f, g)
            for h in range(g + 1, len(blue)):
                triple = f, g, h
                tested += 1
                if len(packing(triple, live, target)) < target:
                    residual += 1
                    representatives.add(canonical(triple))
    return tested, residual, sorted(representatives)


def five_cliques(allowed):
    """Enumerate cliques in increasing vertex order via common higher neighbours."""
    later = [0] * N
    for u, v in allowed:
        later[u] |= 1 << v

    def grow(prefix, choices):
        if len(prefix) == 5:
            yield prefix
            return
        while choices.bit_count() >= 5 - len(prefix):
            bit = choices & -choices
            choices ^= bit
            v = bit.bit_length() - 1
            yield from grow(prefix + (v,), choices & later[v])
    yield from grow((), (1 << N) - 1)


def clique_masks(allowed, unknown):
    counts = Counter()
    for clique in five_cliques(allowed):
        mask = sum(1 << red_id[p] for p in combinations(clique, 2) if p in unknown)
        counts[mask] += 1
    return counts


def residual_problem(triple, cap):
    """Relax the defect budget by charging the guaranteed packing first."""
    f, g, h = triple
    live = after_two(f, g)
    selected = packing(triple, live, cap + 1)
    budget = cap - len(selected)
    if budget < 0:
        return None
    spare = [(w & ~private[e][1].get(h, 0)).bit_count() for e, w in enumerate(live)]
    for body in selected:
        for e in body:
            spare[e] -= 1
    assert min(spare) >= 0
    unknown = {p for e, p in enumerate(red) if spare[e] <= budget}
    additions = {blue[i] for i in triple}
    red_terms = clique_masks(set(red) | additions, unknown)
    blue_terms = clique_masks((set(blue) - additions) | unknown, unknown)

    # Remove exactly the chosen candidates and their reserved witnesses.
    for body in selected:
        mask = sum(1 << e for e in body if red[e] in unknown)
        red_terms[mask] -= 1
    for p in unknown:
        e = red_id[p]
        bit = 1 << e
        assert blue_terms[bit] == (live[e] & ~private[e][1].get(h, 0)).bit_count()
        blue_terms[bit] = spare[e]
    assert min(red_terms.values(), default=0) >= 0
    return ([(m, w) for m, w in red_terms.items() if w],
            [(m, w) for m, w in blue_terms.items() if w], budget)


def feasible(red_terms, blue_terms, budget):
    """Can these monochromatic-clique penalties sum to at most budget?"""
    budget -= sum(w for m, w in chain(red_terms, blue_terms) if not m)
    if budget < 0:
        return False
    red_terms = [(m, w) for m, w in red_terms if m]
    blue_terms = [(m, w) for m, w in blue_terms if m]
    if min(sum(w for m, w in red_terms), sum(w for m, w in blue_terms)) <= budget:
        return True  # Giving all undecided edges the same colour works.
    force_red = force_blue = 0
    priority = Counter()
    for terms, is_red in ((red_terms, True), (blue_terms, False)):
        for m, w in terms:
            size = m.bit_count()
            if size == 1 and w > budget:
                if is_red:
                    force_blue |= m
                else:
                    force_red |= m
            elif size <= 3:
                # Affects only the branching order.
                score = w * {1: 16, 2: 4, 3: 1}[size]
                while m:
                    bit = m & -m
                    m ^= bit
                    priority[bit] += score
    if force_red & force_blue:
        return False

    def extend(r, b):
        return feasible([(m & ~r, w) for m, w in red_terms if not m & b],
                        [(m & ~b, w) for m, w in blue_terms if not m & r], budget)

    if force_red or force_blue:
        return extend(force_red, force_blue)
    if priority:
        bit = max(priority, key=priority.get)
    else:
        mask = red_terms[0][0]
        bit = mask & -mask
    return extend(bit, 0) or extend(0, bit)


def upper_bound(additions, deletions):
    """Independent direct test of every labelled five-set of the witness."""
    assert len(additions) == 3 and additions <= set(blue) and deletions <= set(red)
    final_red = (set(red) - deletions) | additions
    red_count = blue_count = 0
    for vertices in combinations(range(N), 5):
        pairs = combinations(vertices, 2)
        first = next(pairs) in final_red
        if all((p in final_red) == first for p in pairs):
            if first:
                red_count += 1
            else:
                blue_count += 1
    return red_count, blue_count


def verify(minimum, additions, deletions):
    rc, bc = upper_bound(additions, deletions)
    print("Witness, red and blue five-sets:", rc, bc, flush=True)
    assert rc + bc == minimum
    tested, residual, reps = scan(minimum)
    assert tested == sum(comb(429 - f, 2) for f in range(0, 430, 43)) == 352395
    print("Normalized triples, packing misses, symmetry classes:", tested, residual, len(reps), flush=True)
    search_count = 0
    for triple in reps:
        problem = residual_problem(triple, minimum - 1)
        if problem is not None:
            if feasible(*problem):
                raise ValueError(f"Lower bound unproved for {triple}")
            search_count += 1
    print("Residual searches excluded:", search_count)
    print("Exact minimum:", minimum)


if __name__ == "__main__":
    added = {(13, 30), (0, 26), (10, 29)}
    deleted = {edge(i, (i + 1) % N) for i in range(N) if (5 * i) % N < 18}
    verify(11, added, deleted)
