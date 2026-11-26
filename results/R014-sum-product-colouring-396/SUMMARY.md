SETTLED. The least \(N\) for which every two-coloring of \([1,N]\) has two distinct monochromatic sum-product pairs is **396**. At 395, exactly three pairs can be the sole witness: \((1,7)\), \((1,8)\), and \((2,7)\). Adding just \((4,99)\) and \((18,22)\) forces the second witness at 396, and both are necessary.

[RESULT.md](RESULT.md) contains the proof and explicit colorings (100 lines). [check.py](check.py) verified the claims in 3.60 CPU seconds (120 lines).

The lead should reproduce the upper bound using the supplied independent SAT encoding and check literature priority. Novelty is UNVERIFIED.