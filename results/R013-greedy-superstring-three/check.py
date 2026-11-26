"""Exact finite checks for the three-string Greedy theorem in RESULT.md."""

from collections import deque
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product


@lru_cache(maxsize=8192)
def overlap(left, right):
    for size in range(min(len(left), len(right)), 0, -1):
        if left.endswith(right[:size]):
            return size
    return 0


def greedy_choices(words):
    """Yield pair, first-choice margin, and final length for every first tie."""
    scores = {(i, j): overlap(words[i], words[j]) for i, j in permutations(range(3), 2)}
    ordered = sorted(scores.values(), reverse=True)
    for pair, score in scores.items():
        if score != ordered[0]:
            continue
        i, j = pair
        merged = words[i] + words[j][score:]
        other = words[3 - i - j]
        if other in merged or merged in other:
            length = max(len(merged), len(other))
        else:
            length = len(merged) + len(other) - max(overlap(merged, other), overlap(other, merged))
        yield pair, score - ordered[1], length


def shortest_length(words):
    """Breadth-first search by appended letter, without pairwise overlaps."""
    alphabet = sorted(set("".join(words)))
    prefixes = {word[:length] for word in words for length in range(len(word) + 1)}
    transitions = {}
    for prefix in prefixes:
        steps = []
        for letter in alphabet:
            suffix = prefix + letter
            while suffix not in prefixes:
                suffix = suffix[1:]
            hits = sum(1 << i for i, word in enumerate(words) if suffix.endswith(word))
            steps.append((suffix, hits))
        transitions[prefix] = steps

    queue = deque([("", 0, 0)])
    seen = {("", 0)}
    while queue:
        prefix, mask, length = queue.popleft()
        for suffix, hits in transitions[prefix]:
            state = (suffix, mask | hits)
            if state[1] == 7:
                return length + 1
            if state not in seen:
                seen.add(state)
                queue.append((*state, length + 1))
    raise AssertionError("The concatenation is always a superstring")


def bound(cap, margin):
    return 1 + Fraction(max(0, cap - 1 - 2 * margin), cap + margin + 2)


def require(condition, details):
    if not condition:
        raise AssertionError(details)


def exhaust(alphabet, cap):
    pool = ["".join(chars) for size in range(1, cap + 1) for chars in product(alphabet, repeat=size)]
    maxima = {}
    triples = choices = 0
    for words in combinations(pool, 3):
        if any(left in right for left, right in permutations(words, 2)):
            continue
        triples += 1
        optimum = shortest_length(words)
        actual_cap = max(map(len, words))
        for pair, margin, length in greedy_choices(words):
            choices += 1
            ratio = Fraction(length, optimum)
            require(1 <= ratio <= bound(actual_cap, margin), (words, pair, margin, length, optimum))
            for k in range(margin + 1):
                maxima[k] = max(maxima.get(k, 0), ratio)
    for k, maximum in sorted(maxima.items()):
        require(maximum <= bound(cap, k), (alphabet, cap, k, maximum))
        if len(alphabet) >= 3 or k == 0:
            require(maximum == bound(cap, k), (alphabet, cap, k, maximum))
    print(f"alphabet={alphabet} L={cap}: {triples} triples, {choices} first choices, maxima {maxima}")


def check_witnesses(limit):
    checked = 0
    for cap in range(1, limit + 1):
        a = cap - 1
        for k in range(cap):
            if a <= 2 * k:
                words = ("0" * cap, "0" * a + "1", "2")
            else:
                period = "0" * k + "1"
                text = period * ((a + len(period)) // len(period))
                p, q = text[:a], text[k:a + 1]
                words = ("#" + p, p + "#", q)
            require(all(left not in right for left, right in permutations(words, 2)), words)
            optimum = shortest_length(words)
            pair_data = {pair: (margin, length) for pair, margin, length in greedy_choices(words)}
            margin, length = pair_data[(0, 1)]
            require(margin >= k and Fraction(length, optimum) == bound(cap, k), (cap, k, pair_data))
            if a > 2 * k:
                require((margin, length, optimum) == (k, 2 * a - k + 3, a + k + 3), (cap, k))
            checked += 1
    print(f"Constructed witnesses: {checked} parameter pairs through L={limit}")


if __name__ == "__main__":
    exhaust("01", 5)
    exhaust("012", 4)
    check_witnesses(24)
