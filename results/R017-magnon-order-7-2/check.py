"""Exact arithmetic checks for the ideal-magnon theorem in RESULT.md."""

from fractions import Fraction as F
from itertools import combinations
from math import factorial, prod


def gaussian_moment(degree):
    """Normalized integral of x^degree exp(-x^2) on the real line."""
    assert degree % 2 == 0
    return F(prod(range(1, degree, 2)), 2 ** (degree // 2))


def moments(weights):
    return tuple(sum(a * j**s for j, a in weights.items()) for s in (2, 4, 6))


def heat_axis(weights):
    """Expand exp(-t E(x/sqrt(t))) after factoring out exp(-x^2)."""
    m2, m4, m6 = moments(weights)
    assert m2 == 1
    quartic = 2 * F(m4, factorial(4))
    sextic = 2 * F(m6, factorial(6))
    first = quartic * gaussian_moment(4)
    second = quartic**2 * gaussian_moment(8) / 2 - sextic * gaussian_moment(6)
    return first, second


def heat_product(axes):
    coefficients = [heat_axis(weights) for weights in axes]
    first = [entry[0] for entry in coefficients]
    second = sum(entry[1] for entry in coefficients)
    return sum(first), second + sum(a * b for a, b in combinations(first, 2))


def vertices(radius):
    """Enumerate the feasible two-support laws of mass 1 and mean j^2 = 2."""
    for j, k in combinations(range(1, radius + 1), 2):
        probability = F(2 - j*j, k*k - j*j)
        if 0 <= probability <= 1:
            yield {j: (1 - probability) / j**2, k: probability / k**2}


def mix(left, right, fraction_right):
    return {
        j: (1 - fraction_right) * left.get(j, 0) + fraction_right * right.get(j, 0)
        for j in left.keys() | right.keys()
    }


def main():
    # Independent normalization control using the nearest-neighbor dispersion.
    nearest = [{1: F(1)}] * 3
    assert heat_product(nearest) == (F(3, 16), F(33, 512))

    for radius in range(2, 33):
        choices = list(vertices(radius))
        assert len(choices) == radius - 1
        sixth = []
        second = []
        for weights in choices:
            m2, m4, m6 = moments(weights)
            assert (m2, m4) == (1, 2)
            first, coefficient = heat_product([weights] * 3)
            assert first == F(3, 8)
            assert coefficient == F(41, 128) - F(3 * m6, 192)
            sixth.append(m6)
            second.append(coefficient)
        assert (min(sixth), max(sixth)) == (6, radius**2 + 2)
        bounds = F(37 - 2 * radius**2, 128), F(29, 128)
        assert (min(second), max(second)) == bounds
        assert (min(second) < 0) == (radius >= 5)
        if radius in (2, 4, 5):
            print(f"R={radius}: B in [{bounds[0]}, {bounds[1]}]")

    short, *_, long = list(vertices(5))
    zero = mix(short, long, F(29, 42))
    assert moments(zero) == (1, 2, F(41, 2))
    assert heat_product([zero] * 3) == (F(3, 8), 0)
    assert heat_product([short, zero, long]) == (F(3, 8), F(1, 24))
    print("Checked nearest-neighbor control, R=2..32, zero and unequal axes.")


if __name__ == "__main__":
    main()
