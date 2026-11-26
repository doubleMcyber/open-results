# Verification record

Revision: the Lean file in this folder, sha256 1fe3240e07c9e9ec8bc60ff4d6482bb7db537ab4214b1888acad8758196b4ff6 (31,930 lines). Run on 2026-11-26 in a bubblewrap sandbox (bubblewrap 0.9.0, Ubuntu 24.04, Lean 4.35.0 eb6cafb7), spec and stock config from the `discoveries` branch (spec sha256 7bb6d8e9bcf84286d0b3ff6994c731e758f3f40dcbee43bbb305a58fa30f7326, config sha256 8457ef0aa16816f165cd60252d13b6601e32b7628eed9a40c2e1f1f9beff8c28).

## File hash (rerun here, 2026-11-26, no Lean build)

```
shasum -a 256 lean/THCFactorization.lean
1fe3240e07c9e9ec8bc60ff4d6482bb7db537ab4214b1888acad8758196b4ff6  lean/THCFactorization.lean
```

This matches the hash printed in the sandbox job log. The Lean build was not run when this entry was assembled.

## Comparator, stock config plus `--challenge-from-export`

The file is placed at `QuantumComputationSpecs/Primitives/THCFactorization.lean`. The challenge export (254,882,246 bytes, sha256 b38576fe108aec87e6d436400dbba1eecf3704ea1296c72b6f286c492cce2c19) was made from the untouched spec in a separate tree.

```
lake comparator --config QuantumComputationSpecs/ChallengeJsons/Primitives/THCFactorization.json --challenge-from-export <challenge export>
Running Lean default kernel on solution
Lean default kernel accepts the solution
Your solution is okay!
comparator exit 0
VERDICT Apos ACCEPTED
```

The literal stock command (no `--challenge-from-export`) also passed (`VERDICT Alit ACCEPTED`), but it compares the file with itself and is not evidence.

## Axioms

Local run on the Mac, `#print axioms` on the solution's two theorems (`THC.AssemblyG` build, file of 23,471 lines, sha256 79bffb06f39cb755…, which is the same proof before the Google-layout wrapping):

```
'QC14.AssemblyG.thc_correctness_G' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.AssemblyG.thc_t_cost_G' depends on axioms: [propext, Classical.choice, Quot.sound]
[57708, 95308]
```

The last line is `#eval stepTG 54 350 10 16` and `#eval stepTG 76 450 10 20`. The comparator enforces the stock config's permitted axioms (propext, Quot.sound, Classical.choice) and accepted. It does not print the axiom list.

Local comparator run on the 23,471-line file (`--root THC.AssemblyG --holes lean/holesG.json`): `Your solution is okay!`, exit 0.

## Negative tests

Sandbox run, same command and export as above, on the same file with one change each:

```
AnegH (a hole's type changed):
error: Challenge and solution theorem statement do not match: 'QuantumComputation.Specs.thc_correctness'
comparator exit 1
VERDICT AnegH REJECTED

AnegT (extra hypothesis added to thc_t_cost):
error: Challenge and solution theorem statement do not match: 'QuantumComputation.Specs.thc_t_cost'
comparator exit 1
VERDICT AnegT REJECTED

SUMMARY Alit=ACCEPTED Apos=ACCEPTED AnegH=REJECTED AnegT=REJECTED
```

Local run, a copy of the 23,471-line solution with a `sorry` in a proof (sha256 02f93525fe0f2000…):

```
error: Illegal axiom detected: 'sorryAx'
comparator exit 1
```

## Numbers

- Qubits: `#eval 2 * 54 + blockAncC 54 350 10 + scratchG 54 350 10 16 + 16` = 6107 and `#eval 2 * 76 + blockAncC 76 450 10 + scratchG 76 450 10 20 + 20` = 11473 (the shape of the spec's `thcTotalLogicalQubits` with the solution's holes; the spec's own abbrev was not evaluated). This was run on the 23,471-line build, not the Google-layout file.
- Walk steps ⌈π·κλ/(2·0.001)⌉ = 512,886 and 2,435,956 (exact fractions, π to 31 digits, with λ = 306.3 and 1201.5, κ = 2^g/(4·d·2^ℵ) = 65536/61479 and 131072/101551). Total T = steps × `stepTG` = 29,597,625,288 and 232,166,094,448. Not a Lean evaluation, because `thcTCost` is noncomputable.
- Lee et al. (arXiv:2011.03494v3): Table III Toffolis 5.3e9 and 3.2e10, qubits 2,142 and 2,196, walk steps ⌈πλ/(2·0.001)⌉ = 481,135 and 1,887,312, per-step T = 4 × Toffolis / steps = 44,062.5 and 67,821.3.
- Ratios: per step 57,708/44,062.5 = 1.3097 and 95,308/67,821.3 = 1.4053; totals 2.96e10/2.12e10 = 1.396 and 2.32e11/1.28e11 = 1.814.

## Not run

The hole check for computability of `thcCandidateProgram` and `thcTCost` was not run on this revision. The Lean build of the file in this folder was not rerun on the Mac.
