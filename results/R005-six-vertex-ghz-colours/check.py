"""Check six-vertex color restriction term by term and the sharpness witness."""
from collections import Counter
from itertools import combinations, product

VERTICES = tuple(range(6))
IMAGE = ("alpha", "beta", "gamma")


def matchings(vertices):
    """Pair the first remaining vertex, as in pmSumListAux."""
    if not vertices:
        yield ()
        return
    head, *tail = vertices
    for index, other in enumerate(tail):
        for rest in matchings(tail[:index] + tail[index + 1:]):
            yield ((head, other),) + rest


def edge_partitions():
    """Enumerate triples of different edges and check vertex coverage."""
    edges = combinations(VERTICES, 2)
    return [triple for triple in combinations(edges, 3)
            if len({v for edge in triple for v in edge}) == 6]


def polynomial(terms, labels):
    return Counter(tuple(sorted((u, v, labels[u], labels[v]) for u, v in m))
                   for m in terms)


def restrict_monomials(poly):
    result = Counter()
    for term, coefficient in poly.items():
        mapped = tuple(sorted((u, v, IMAGE[i], IMAGE[j]) for u, v, i, j in term))
        result[mapped] += coefficient
    return result


def verify():
    recursive = list(matchings(VERTICES))
    independent = edge_partitions()
    assert len(recursive) == len(independent) == 15
    profiles = terms = constant = 0
    for x in product(range(3), repeat=6):
        lifted = tuple(IMAGE[i] for i in x)
        small = restrict_monomials(polynomial(recursive, x))
        large = polynomial(independent, lifted)
        assert small == large
        assert (len(set(x)) == 1) == all(a == b for a, b in zip(lifted, lifted[1:]))
        profiles += 1
        terms += sum(small.values())
        constant += len(set(x)) == 1
    print(f"{profiles} profiles, {terms} matching terms, {constant} constant profiles")

    support = {(0, 1, 0, 0), (2, 3, 0, 0), (4, 5, 0, 0),
               (0, 5, 1, 1), (1, 2, 1, 1), (3, 4, 1, 1)}
    totals = Counter()
    for x in product(range(2), repeat=6):
        value = sum(all((u, v, x[u], x[v]) in support for u, v in m)
                    for m in independent)
        assert value == int(len(set(x)) == 1)
        totals[value] += 1
    print(f"two-color witness: {totals[1]} ones, {totals[0]} zeros")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so equality checks are enabled.")
    verify()
