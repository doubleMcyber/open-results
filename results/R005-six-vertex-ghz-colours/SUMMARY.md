SETTLED row 131’s six-vertex statement by reduction to the cited three-color theorem. Any complex solution with \(D\ge3\) restricts to three colors and preserves every matching product. Two colors are attainable.

[RESULT.md](RESULT.md) contains the proof and reviewer checks (32 lines). [check.py](check.py) verified 10,935 symbolic matching products across all 729 three-colorings and the two-color witness on all 64 colorings (70 lines). [Restriction.lean](Restriction.lean) supplies the reduction (33 lines).

The lead must verify the external three-color certificate and compile the Lean reduction. Novelty is UNVERIFIED.