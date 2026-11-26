SETTLED the three-string follow-up to row 393. For three substring-free words of length at most \(L\) over an alphabet of at least three symbols, if the first Greedy overlap beats every alternative by at least \(k\ge0\), the sharp worst-case ratio is \(1+\max(0,L-1-2k)/(L+k+2)\), for \(k<L\).

[Proof and sharp examples](RESULT.md) (83 lines). The [exact checker](check.py) (121 lines) passed on 236,753 triples and 300 constructed witnesses.

The lead should rerun the checker, review the overlap argument, and check prior work. Novelty is UNVERIFIED. The arbitrary-cardinality question remains unresolved here.