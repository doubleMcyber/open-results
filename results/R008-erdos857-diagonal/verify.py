"""Enumerate sunflowers, minimum deletion sets, and relabeling orbits."""

from functools import reduce
from itertools import combinations
from operator import or_


def sunflowers(n):
    """Assign each point to the core, to no member, or to one private petal."""
    flowers = set()

    def assign(i, core, petals):
        # At most one of the n private petals can be empty.
        if len(petals) + n - i < n - 1:
            return
        if i == n:
            if len(petals) == n - 1:
                petals = petals + (0,)
            flowers.add(tuple(sorted(core | p for p in petals)))
            return
        point = 1 << i
        assign(i + 1, core | point, petals)
        assign(i + 1, core, petals)
        # New nonempty petals are numbered by their smallest point.
        assign(i + 1, core, petals + (point,))
        for j, petal in enumerate(petals):
            new_petals = petals[:j] + (petal | point,) + petals[j + 1:]
            assign(i + 1, core, new_petals)

    assign(0, 0, ())
    return flowers


def direct_sunflowers(n):
    """Independent literal test over every n-subfamily for n <= 5."""
    result = set()
    for family in combinations(range(1 << n), n):
        core = family[0] & family[1]
        if all(a & b == core for a, b in combinations(family, 2)):
            result.add(family)
    return result


def minimizers(flowers):
    # Sets absent from every sunflower cannot belong to a minimum transversal.
    support = sorted({member for flower in flowers for member in flower})
    hit = {member: 0 for member in support}
    for j, flower in enumerate(sorted(flowers)):
        for member in flower:
            hit[member] |= 1 << j
    all_hit = (1 << len(flowers)) - 1
    for size in range(len(support) + 1):
        winners = {
            deletion for deletion in combinations(support, size)
            if reduce(or_, map(hit.__getitem__, deletion), 0) == all_hit
        }
        if winners:
            return size, winners
    raise AssertionError("The entire support should hit every flower.")


def orbit_count(n, winners):
    """Enumerate components under adjacent transpositions, which generate S_n."""
    swaps = []
    for i in range(n - 1):
        a, b = 1 << i, 1 << (i + 1)
        swaps.append([s ^ (a | b) if bool(s & a) != bool(s & b) else s
                      for s in range(1 << n)])
    unseen = set(winners)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            deletion = stack.pop()
            for swap in swaps:
                other = tuple(sorted(swap[s] for s in deletion))
                assert other in winners
                if other in unseen:
                    unseen.remove(other)
                    stack.append(other)
    return count


def main():
    print("n  flowers  min_deleted  m(n,n)  labeled_extremizers  orbits")
    for n in range(3, 9):
        flowers = sunflowers(n)
        if n <= 5:
            assert flowers == direct_sunflowers(n)
        size, winners = minimizers(flowers)
        orbits = orbit_count(n, winners)
        threshold = (1 << n) - size + 1
        print(n, len(flowers), size, threshold, len(winners), orbits)
        assert size == n // 2 + 2
        assert orbits == (2 if n % 2 else 6 if n == 4 else 7)


if __name__ == "__main__":
    main()
