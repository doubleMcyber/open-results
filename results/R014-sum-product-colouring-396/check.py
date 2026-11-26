"""Verify the two-witness finite sums and products threshold. Python 3.10+."""
from collections import Counter
from itertools import combinations


def configurations(n):
    return [(a, b) for a in range(1, n + 1)
            for b in range(a + 1, min(n - a, n // a) + 1)]


def edge(pair):
    a, b = pair
    return {a, b, a + b, a * b}


def find_coloring(pairs):
    """Find a coloring avoiding every supplied pair, or certify impossibility."""
    edges = [sum(1 << v for v in edge(pair)) for pair in pairs]
    incidence = Counter(v for pair in pairs for v in edge(pair))
    order = [1 << v for v, _ in incidence.most_common()]

    def search(red, blue):
        while True:
            red_units = blue_units = 0
            for mask in edges:
                if mask & red and mask & blue:
                    continue
                free = mask & ~(red | blue)
                if not free:
                    return None
                if free.bit_count() == 1:
                    if not mask & red:
                        red_units |= free
                    if not mask & blue:
                        blue_units |= free
            if red_units & blue_units:
                return None
            if not (red_units | blue_units):
                break
            red |= red_units
            blue |= blue_units

        pending = 0
        for mask in edges:
            if not (mask & red and mask & blue):
                pending |= mask & ~(red | blue)
        if not pending:
            return red  # All edges already have both colors. Color the rest blue.
        bit = next(bit for bit in order if bit & pending)
        found = search(red | bit, blue)
        if found is None:
            return search(red, blue | bit)
        return found

    return search(order[0] if order else 0, 0)  # Interchanging colors is harmless.


def possible_sole_pairs(pairs):
    """Input admits no coloring avoiding all pairs. Split possible exceptions."""
    def visit(block):
        omitted = set(block)
        if find_coloring([p for p in pairs if p not in omitted]) is None:
            return []
        if len(block) == 1:
            return block
        mid = len(block) // 2
        return visit(block[:mid]) + visit(block[mid:])

    return visit(pairs)


def direct_witnesses(n, red):
    """Independent definition-level check of the displayed colorings."""
    result = []
    for a, b in combinations(range(1, n + 1), 2):
        if a + b <= n and a * b <= n:
            if (a in red) == (b in red) == (a + b in red) == (a * b in red):
                result.append((a, b))
    return result


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    n = 395
    pairs = configurations(n)
    exceptions = [(1, 7), (1, 8), (2, 7)]
    bridges = [(4, 99), (18, 22)]
    boundary = sorted(set(configurations(n + 1)) - set(pairs))
    require(set(bridges) <= set(boundary), "Bridge outside the boundary")
    require(find_coloring(pairs) is None, "Zero witnesses at 395")
    sole = possible_sole_pairs(pairs)
    require(sole == exceptions, f"Possible sole witnesses: {sole}")
    print(f"{len(pairs)} pairs at 395. Possible sole witnesses: {sole}")

    base = {i for i in range(1, n + 1) if i % 8 in (2, 4, 6)}
    base -= {2, 4, 6, 10, 14}
    base |= {1, 3, 5, 8, 16, 24, 32, 40, 48}
    for pair, extra_red in zip(exceptions, ({7}, {9, 56}, {56})):
        red = base | extra_red
        require(direct_witnesses(n, red) == [pair], "Bad lower coloring")
        for color, extended, bridge in (("blue", red, bridges[0]),
                                        ("red", red | {n + 1}, bridges[1])):
            actual = direct_witnesses(n + 1, extended)
            require(actual == sorted([pair, bridge]), "Unexpected extension")
            print(f"Sole {pair}, then {color} 396 gives exactly {actual}")

        # A coloring with sole old witness 'pair' must meet a bridge in either color.
        required = [p for p in pairs if p != pair] + bridges
        require(find_coloring(required) is None, f"Both bridges avoidable for {pair}")

    print(f"{len(boundary)} new pairs. The unique minimal forcing subset is {bridges}.")
    print("Least interval endpoint forcing two distinct witness pairs: 396")


if __name__ == "__main__":
    main()
