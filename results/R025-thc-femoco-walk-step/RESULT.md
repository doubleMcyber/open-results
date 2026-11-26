# A comparator-accepted solution to the THCFactorization spec (Clifford+T, exact block encoding, 1.31x Lee et al. per walk step)

This is a Lean 4 solution to `QuantumComputationSpecs/Primitives/THCFactorization.lean` in google-deepmind/formal-quantum-computation, with all seven holes filled and `thc_correctness` and `thc_t_cost` proved as stated. The Lean file is [lean/THCFactorization.lean](lean/THCFactorization.lean) and the holes file is [lean/holesG.json](lean/holesG.json).

## What it is

- The circuit follows Lee et al. (PRX Quantum 2, 030305, 2021): alias-sampling PREPARE, measured lookups, and Givens rotations applied by phase kickback into the phase-gradient catalyst. Because `IsRounded` puts the data on the circuit's grids, the block encoding is exact (`Heff = thcHamiltonian thc`), for every N and M. It uses no `TOFF` gates.
- The proved T count per walk step is a closed form, `stepTG N M aleph beth`. At the docstring's FeMoco parameters it is 57,708 T (Reiher, N = 54, M = 350) and 95,308 T (Li, N = 76, M = 450). Lee et al.'s per-step cost, taken as 4 × their Table III Toffoli total divided by ⌈πλ/(2·0.001)⌉, is 44,063 and 67,821 T (derived, not a number printed in the paper). That makes ours 1.31x and 1.41x theirs per step.
- The proved total, `thcTCost`, is worse: 2.96e10 and 2.32e11 T, which is 1.40x and 1.81x Lee et al.'s 2.12e10 and 1.28e11. The alias table is padded to 2^g entries, so α = κλ with κ = 1.066 and 1.291.
- `thcTotalLogicalQubits` is 6,107 and 11,473, mostly lookup scratch. Lee et al. report 2,142 and 2,196, a count that includes the phase-estimation register.

So this is a verified THC block encoding at about 1.4x to 1.8x Lee et al.'s total T cost and several times their qubits. It is a per-step count, not a total, and it is not a resource improvement and not a FeMoco runtime estimate. Lee et al.'s totals are given to two significant figures, so the ratios carry about ±1%. The per-step comparison is very slightly tilted in our favour, because Lee et al.'s per-step cost also includes about 32 Toffolis (about 0.3%) of walk reflection, unary iteration and spin swap that the spec does not charge to a candidate.

## Status

Settled, unreviewed. The claim is only what the comparator checked: the two theorems have the statements in Google's spec, with the seven holes filled, and their proofs use only propext, Quot.sound and Classical.choice. No one at Google has reviewed or accepted this.

## How it was checked

`lake comparator` in the bubblewrap sandbox on Linux (Lean 4.35.0, `discoveries` a88de8f; the spec file is unchanged on `main` 489edc7, sha256 7bb6d8e9…). The solution is `THC.AssemblyG`, with holes file `lean/holesG.json`. The Google-layout file checked in the sandbox is `lean/THCFactorization.lean` (31,930 lines, sha256 1fe3240e07c9e9ec8bc60ff4d6482bb7db537ab4214b1888acad8758196b4ff6; the same hash is printed in the sandbox job log). It sits at the Specs path with the stock config, and the challenge comes from `--challenge-from-export` with an export of the untouched spec built in a separate tree. The result was "Your solution is okay!". Two negative controls, one changing a hole's type and one adding a hypothesis to `thc_t_cost`, were rejected with a statement mismatch. The only axioms are propext, Quot.sound and Classical.choice. The file inlines two modules from the author's earlier repository (PreparePauliLCU and ControlledAddConstant, marked as such) and imports `EqualTableAdd` from the arcsin solution in the `discoveries` branch. See [VERIFY.md](VERIFY.md) for commands and log excerpts.

## Caveats

1. The stock config names the same module as challenge and solution. With the solution placed at that path, the stock command compares the file with itself, and any statement change passes. Adding `--challenge-from-export` makes it a real check, so the claim here is "stock config plus `--challenge-from-export`", not "stock comparator". Placing the solution under `QuantumComputationDiscoveries` instead does not work for this spec: the hygienic name in `spinOrbital`'s `by omega` proof embeds the module name, so the comparator reports "Const does not match" on `spinOrbital._proof_2`.
2. `thcCandidateProgram` is a plain `def`. Since the input is real-valued and the gate set is discrete, no correct solution can fill it computably. This one is noncomputable, by choice over the rounding integers that `IsRounded` gives existentially. Marking it `noncomputable`, as the Photochemistry and StoppingPower specs do, or passing the integer rounding data as input, would resolve this.
3. `thcTCost` cannot reduce to a numeral, because `qpeWalkSteps` takes a real ε. The per-step part `stepTG` is computable ℕ.
4. A unitary Clifford+T circuit cannot prepare an exactly uniform state over d ≠ 2^k entries (1/d would have to be dyadic). With an exact block encoding required, the padding cost shows up in α and hence in the walk-step count.

Also not covered: the THC factorization error, the rounding of real factorization data to the grids (assumed by `IsRounded`), the walk reflection, the phase-estimation register, catalyst preparation, magic-state distillation and surface-code overhead. The hole check for this revision (computability of `thcCandidateProgram` and `thcTCost`) is predicted to fail as in points 2 and 3, and was not run.

The construction and proofs were written with AI coding agents and checked by Lean's kernel and the comparator.
