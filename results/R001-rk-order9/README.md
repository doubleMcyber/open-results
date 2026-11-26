# R001: a 13-stage explicit Runge–Kutta method of order 9

**Statement.** An explicit 13-stage Runge–Kutta method of order 9 exists. Hence a(9) ≤ 13 in OEIS A187102, where the entry says "it seems that a(9) <= 13". With Butcher's lower bound (BIT 25, 1985), 12 ≤ a(9) ≤ 13.

**Certificate.** The method's 77 free coefficients are algebraic numbers in a totally real number field of degree 16. Every coefficient is written as g_j(θ)/f′(θ), where f is the monic minimal polynomial of θ and the g_j are rational polynomials. All 486 order conditions for rooted trees with at most 9 vertices reduce to zero modulo f in exact rational arithmetic. All 16 roots of f are real, with certified rational isolating intervals, so each root gives a real method. Two independently written exact checks reproduced the result. One of them uses only standard-library Python and runs in about 12 minutes.

**Where it lives.**

- Repository with the certificate, the data and the checkers: https://github.com/doubleMcyber/rk13-order9
- Archived record: https://doi.org/10.5281/zenodo.23874041

**Status.** Certified. An exact certificate exists and an independent check reproduced it. No referee has reviewed it yet.
