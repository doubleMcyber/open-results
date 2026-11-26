A side remark on Erdős problem 857, diagonal case k = n only. The problem concerns fixed k and n tending to infinity, so this statement is outside it and does not settle or advance it. For every \(n\ge3\), the minimum family size forcing an \(n\)-sunflower on \(n\) points is \(2^n-\lfloor n/2\rfloor-1\). Up to relabeling, there are two extremal families for odd \(n\), six for \(n=4\), and seven for even \(n\ge6\).

[RESULT.md](RESULT.md) contains the proof and reviewer checks (60 lines). [verify.py](verify.py) independently reproduced the thresholds and orbit counts for \(3\le n\le8\) (100 lines).

The lead should rerun the script and confirm that the source permits one member to equal the core. The statement is not on the problem page or in formal-conjectures; no wider literature search was made. The general two-parameter problem remains open.

[lean/](lean/) holds a Lean 4 proof of the value formula m(n,n) = 2^n − ⌊n/2⌋ − 1 for all n ≥ 3 (standard axioms propext, Classical.choice, Quot.sound; no sorry). The classification of the extremal families is not in Lean.
