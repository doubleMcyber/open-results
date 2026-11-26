SETTLED the sparse-bias follow-up to row 503. When minus signs have probability \((\log n+t)/n\), the probability of two equal rows tends to \(1-(1+\lambda)e^{-\lambda}\), where \(\lambda=e^{-t}\). I also proved the leading correction from equal rows that contain a minus sign.

[RESULT.md](RESULT.md) contains the statement, proof, and reviewer checklist in 53 lines. [check.py](check.py) contains the exact computation in 88 lines. All coefficient checks passed across 33,866 matrices of orders 1 through 5.

The lead should rerun the script and review the conditional counting argument for the correction term. Novelty is UNVERIFIED.