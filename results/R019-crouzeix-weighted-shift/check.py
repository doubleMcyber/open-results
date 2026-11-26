"""Exact arithmetic for the weighted-shift theorem. Run with python3 check.py."""

from fractions import Fraction as Q
from itertools import product
from math import prod

ZERO, HALF, ONE = Q(0), Q(1, 2), Q(1)


def squares(p):
    """Squared normalized weights corresponding to vertex parameters p."""
    return [4 * a * (1 - b) for a, b in zip(p, p[1:])]


def has_unit_radius(w):
    """Assert I-(T+T*)/2 is PSD by component minors and return its singularity."""
    previous, current = ONE, ONE
    singular = False
    for weight_squared in w:
        if weight_squared == 0:
            singular |= current == 0
            previous, current = ONE, ONE
        else:
            assert weight_squared > 0 and current > 0
            previous, current = current, current - weight_squared * previous / 4
            assert current >= 0
    return singular or current == 0


def distance_at_most(x, y, bound):
    """Test (sqrt(x)-sqrt(y))^2 <= bound without square roots."""
    assert min(x, y, bound) >= 0
    remainder = x + y - bound
    return remainder <= 0 or remainder * remainder <= 4 * x * y


def intervals(w):
    return {(s, t): prod(w[s:t]) for s in range(len(w))
            for t in range(s + 1, len(w) + 1)}


def equality_block_squares(edge_count):
    if edge_count == 1:
        return [Q(4)]
    return [Q(2)] + [ONE] * (edge_count - 2) + [Q(2)]


def check_profile(p):
    w = squares(p)
    assert has_unit_radius(w)  # singularity witnesses radius exactly one
    products = intervals(w)
    k2 = max(ONE, max(products.values()))
    assert ONE < k2 <= 4
    assert (k2 == 4) == all(x == HALF for x in p[1:-1])

    # Independently certify the diagonal conjugation and its condition number.
    d2 = [ONE]
    for weight_squared in w:
        d2.append(max(ONE, d2[-1] * weight_squared))
    assert max(d2) == k2 and min(d2) == ONE
    assert all(w[i] * d2[i] <= d2[i + 1] for i in range(len(w)))

    winners = []
    for (s, t), product_squared in products.items():
        middle = prod(1 - (2 * x - 1) ** 2 for x in p[s + 1:t])
        assert product_squared == 4 * p[s] * (1 - p[t]) * middle
        if product_squared != k2:
            continue
        winners.append((s, t))
        b = w.copy()
        b[s:t] = equality_block_squares(t - s)
        if s:
            b[s - 1] = ZERO
        if t < len(w):
            b[t] = ZERO
        assert has_unit_radius(b)
        assert max(intervals(b).values()) == 4
        assert all(distance_at_most(x, y, 4 - k2) for x, y in zip(w, b))
    return k2, winners


def main():
    grid = (Q(1, 16), Q(1, 4), HALF, Q(3, 4), Q(15, 16))
    profile_count = winner_count = 0
    for n in range(2, 7):
        for interior in product(grid, repeat=n - 2):
            _, winners = check_profile((ONE, *interior, ZERO))
            profile_count += 1
            winner_count += len(winners)
    print(f"{profile_count} normalized profiles; {winner_count} maximizing intervals")

    # An interior maximizing block with both attachments cut.
    k2, winners = check_profile((ONE, Q(15, 16), HALF, Q(1, 16), ZERO))
    assert (k2, winners) == (Q(225, 64), [(1, 3)])
    print(f"Five vertices: unique block on vertices 2 through 4, K^2 = {k2}")

    for n in range(2, 33):
        eta = ONE / (n * n * 4)
        w = squares((ONE, 1 - eta, ZERO))
        k2, winners = check_profile((ONE, 1 - eta, ZERO))
        bound = 4 - k2
        assert winners == [(1, 2)] and bound == 4 * eta == w[0]
        assert distance_at_most(w[1], Q(4), bound)
        for other_first_weight_squared in (Q(2), Q(4)):
            assert not distance_at_most(w[0], other_first_weight_squared, bound)
    print("31 rational sharpness certificates; distance squared = 4 - K^2")


if __name__ == "__main__":
    main()
