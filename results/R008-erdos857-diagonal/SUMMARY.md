SETTLED the diagonal case of Erdős problem 857. For every \(n\ge3\), the minimum family size forcing an \(n\)-sunflower on \(n\) points is \(2^n-\lfloor n/2\rfloor-1\). Up to relabeling, there are two extremal families for odd \(n\), six for \(n=4\), and seven for even \(n\ge6\).

[RESULT.md](RESULT.md) contains the proof and reviewer checks (60 lines). [verify.py](verify.py) independently reproduced the thresholds and orbit counts for \(3\le n\le8\) (100 lines).

The lead should rerun the script and confirm that the source permits one member to equal the core. Novelty is UNVERIFIED. The general two-parameter problem remains open.