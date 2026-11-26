A Lean 4 solution to the `THCFactorization` spec in google-deepmind/formal-quantum-computation (`QuantumComputationSpecs/Primitives/THCFactorization.lean`): all seven holes filled, `thc_correctness` and `thc_t_cost` proved as stated. The Lean comparator accepted it in its bubblewrap sandbox (stock config plus `--challenge-from-export`), with only the axioms propext, Quot.sound and Classical.choice.

The block encoding is exact for every N and M and uses no Toffoli gates. The current version (P4.9, 2026-11-26) proves 43,868 T per walk step at the Reiher FeMoco parameters (N = 54, M = 350) and 67,944 T at Li's (N = 76, M = 450). That is 0.9956x and 1.0018x Lee et al.'s per-step cost (derived from their Table III, which carries about ±1%), so it is parity per step, not an improvement. Over a whole phase estimation the proved total is 2.25e10 and 1.66e11 T, which is 1.06x and 1.29x Lee et al.'s totals, with 7,873 and 13,300 logical qubits against their 2,142 and 2,196. The gap in the totals is alias padding that the spec's exact block encoding forces. This is not a resource improvement and not a FeMoco runtime estimate.

The first version (P4.4) had 57,708 and 95,308 T per step (1.31x and 1.41x) and is kept in the entry.

Status: Settled, unreviewed (the Lean statement; the comparator checked each solution against the spec and nothing more). Google has not reviewed it.

[RESULT.md](RESULT.md) has the update, the construction, the numbers and the caveats. [p49/VERIFY.md](p49/VERIFY.md) and [VERIFY.md](VERIFY.md) have the commands and log excerpts for the two versions. The Lean files are in [p49/lean/](p49/lean/) and [lean/](lean/). The Lean builds were not rerun when this entry was assembled; only the file hashes were checked.
