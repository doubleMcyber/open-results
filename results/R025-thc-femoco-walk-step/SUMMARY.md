A Lean 4 solution to the `THCFactorization` spec in google-deepmind/formal-quantum-computation (`QuantumComputationSpecs/Primitives/THCFactorization.lean`): all seven holes filled, `thc_correctness` and `thc_t_cost` proved as stated. The Lean comparator accepted it in its bubblewrap sandbox (stock config plus `--challenge-from-export`), with only the axioms propext, Quot.sound and Classical.choice.

The block encoding is exact for every N and M and uses no Toffoli gates. The proved T count is a per-step count: 57,708 T per walk step at the Reiher FeMoco parameters (N = 54, M = 350) and 95,308 T at Li's (N = 76, M = 450), which is 1.31x and 1.41x Lee et al.'s per-step cost (derived, not printed in their paper). Over a whole phase estimation the proved total is 2.96e10 and 2.32e11 T, which is 1.40x and 1.81x Lee et al.'s totals, with 6,107 and 11,473 logical qubits against their 2,142 and 2,196. This is not a resource improvement and not a FeMoco runtime estimate.

Status: Settled, unreviewed (the Lean statement; the comparator checked the solution against the spec and nothing more). Google has not reviewed it.

[RESULT.md](RESULT.md) has the construction, numbers and caveats. [VERIFY.md](VERIFY.md) has the commands and log excerpts. The Lean file is in [lean/](lean/). The Lean build was not rerun when this entry was assembled; only the file hash was checked.
