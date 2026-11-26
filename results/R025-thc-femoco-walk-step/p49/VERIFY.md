# Verification record, P4.9 update

Revision: the Lean file in [lean/](lean/), sha256 72fa0bd31c1dcd2ec4859ed900c02c8dc2b0374e52587ff8ae93199d05ea5ff7 (43,247 lines). Run on 2026-11-26 from 10:12 to 10:45 PST, sandbox job 2027077, in a bubblewrap sandbox (bubblewrap 0.9.0, Ubuntu 24.04.5, Lean 4.35.0 eb6cafb7, Lake 5.0.0), spec and stock config from the `discoveries` branch at a88de8f (spec sha256 7bb6d8e9bcf84286d0b3ff6994c731e758f3f40dcbee43bbb305a58fa30f7326, config sha256 8457ef0aa16816f165cd60252d13b6601e32b7628eed9a40c2e1f1f9beff8c28). The file is the Google-layout form of the solution with root `THC.AssemblyCF` and holes file [lean/holesG.json](lean/holesG.json), assembled from a 34,788-line file (sha256 9d28da75578eb594513a8aeabad172e366c7982de7e5fab764b2247c8f0db448).

## File hash (rerun here, 2026-11-26, no Lean build)

```
shasum -a 256 lean/THCFactorization.lean
72fa0bd31c1dcd2ec4859ed900c02c8dc2b0374e52587ff8ae93199d05ea5ff7  lean/THCFactorization.lean
```

The sandbox job log prints the same hash for the file it checked (fourth line of the log):

```
72fa0bd31c1dcd2ec4859ed900c02c8dc2b0374e52587ff8ae93199d05ea5ff7  files/THCFactorization.lean
7bb6d8e9bcf84286d0b3ff6994c731e758f3f40dcbee43bbb305a58fa30f7326  disc/QuantumComputationSpecs/Primitives/THCFactorization.lean
8457ef0aa16816f165cd60252d13b6601e32b7628eed9a40c2e1f1f9beff8c28  disc/QuantumComputationSpecs/ChallengeJsons/Primitives/THCFactorization.json
```

The Lean build was not rerun when this update was assembled.

## Comparator, stock config plus `--challenge-from-export`

The file is placed at `QuantumComputationSpecs/Primitives/THCFactorization.lean`. The challenge export (254,882,246 bytes, sha256 b38576fe108aec87e6d436400dbba1eecf3704ea1296c72b6f286c492cce2c19) was made from the untouched spec in a separate tree. Excerpt from the job log:

```
lake comparator --config QuantumComputationSpecs/ChallengeJsons/Primitives/THCFactorization.json --challenge-from-export <challenge export>
Running Lean default kernel on solution
Lean default kernel accepts the solution
Your solution is okay!
comparator exit 0 wall 142 s end 2026-11-26T10:34:53-08:00
VERDICT Apos ACCEPTED
```

The literal stock command (no `--challenge-from-export`) also passed, but it compares the file with itself and is not evidence:

```
Your solution is okay!
comparator exit 0 wall 435 s end 2026-11-26T10:32:31-08:00
VERDICT Alit ACCEPTED
```

## Negative tests

Same command and export, on the same file with one change each. AnegH adds a parameter `(dummy : ℕ := 0)` to the hole `thcCatalystQubits` (sha256 1fae0ce8233f5e06…). AnegT adds a hypothesis `(hextra : True)` to `thc_t_cost` (sha256 9550a7cef578ad74…).

```
AnegH:
error: Challenge and solution theorem statement do not match: 'QuantumComputation.Specs.thc_correctness'
comparator exit 1 wall 315 s end 2026-11-26T10:40:08-08:00
VERDICT AnegH REJECTED

AnegT:
error: Challenge and solution theorem statement do not match: 'QuantumComputation.Specs.thc_t_cost'
comparator exit 1 wall 316 s end 2026-11-26T10:45:24-08:00
VERDICT AnegT REJECTED

SUMMARY Alit=ACCEPTED Apos=ACCEPTED AnegH=REJECTED AnegT=REJECTED
```

Local run on the Mac, 2026-11-26 08:43 PST, a copy of the 34,788-line solution with a `sorry` in a proof (sha256 74fc9e7bfade4144…):

```
error: Illegal axiom detected: 'sorryAx'
comparator exit 1 (3 min)
```

Local comparator run on the 34,788-line file (`--root THC.AssemblyCF --holes lean/holesG.json`), 08:38 to 08:43 PST: `Your solution is okay!`, exit 0.

## Axioms and the per-step `#eval`

Local run on the Mac, 2026-11-26 08:38 PST, on the `THC.AssemblyCF` modules (the same proof before assembly into one file and before the Google-layout wrapping). Last lines of the local log `logs/p49ax_1126_0838.log`:

```
'QC14.DecodeC.dcSem' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.DecodeC.runList_decodeSteps' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.DecodeC.runList_decodeSteps_inverse' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.DecodeC.dcKraus' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.DecodeC.dcGenerated_count_T' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.DecodeC.decodeSteps_count_T' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.DecodeC.decodeSteps_count_TOFF' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.CompactWord.dcTable_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.CompactWord.dcZeroOut' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.CompactWord.rowWordC_spec' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.PairProgramCF.cfKraus' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.PairProgramCF.cfFwd' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.PairProgramCF.cfInv' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.PairProgramCF.pair_catKetCF' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.PairProgramCF.pair_countCF' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.AssemblyCF.realizes_CF' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.AssemblyCF.count_CF' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.AssemblyCF.thc_correctness_CF' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.AssemblyCF.thc_t_cost_CF' depends on axioms: [propext, Classical.choice, Quot.sound]
[43868, 67944]
```

The last line is `#eval [QC14.AssemblyCF.stepTCF 54 350 10 16, QC14.AssemblyCF.stepTCF 76 450 10 20]`. The two spec theorems are proved by `exact QC14.AssemblyCF.thc_correctness_CF …` and `exact QC14.AssemblyCF.thc_t_cost_CF …`. The comparator enforces the stock config's permitted axioms (propext, Quot.sound, Classical.choice) and accepted. It does not print the axiom list.

The scratch hole was evaluated in Lean once, on the frozen definitions before the proofs were filled in (local log `logs/p49sk_1126_0809.log`):

```
#eval [scratchCF 54 350 10 16, scratchCF 76 450 10 20, …]
[7699, 13075, 7661, 14960]
```

The first two entries are `scratchCF`; the last two belong to an earlier revision. The Python evaluation below, a port of the definitions in the checked file, reproduces both values.

## Numbers

These are Python evaluations of the Lean definitions in [lean/THCFactorization.lean](lean/THCFactorization.lean), not Lean evaluations. [numbers.py](numbers.py) ports `stepTCF`, `scratchCF`, `blockAncC`, `kappaC`, `qpeWalkSteps`, `tCostCF` and the definitions they use to exact integers and fractions, with π to 31 decimal places. It includes the generated decoder network (`dcNetwork`), whose AND count sets `decodeTC`. It also ports P4.4's `stepTG` for the comparison. It checks that its `stepTCF` and `scratchCF` equal the Lean `#eval` values above. `thcTCost` itself cannot be evaluated in Lean, because `qpeWalkSteps` takes a real ε.

Output of `python3 -I numbers.py`:

```
Reiher: N=54 M=350 aleph=10 beth=16 lamMax=3063/10
  gC=28 dC=61479 kappaC=65536/61479 = 1.065990
  slotBitsS=16 wordBitsC=28 decoder ANDs=296 decodeTC=1184 decWorkC=1414
  aliasTCF=15532 16*bIC=160 selTT=28176
  stepTCF=43868 (Lean #eval pin 43868)
  walk steps ceil(pi*kappa*lam/(2*0.001))=512886
  tCostCF=22499283048 = 2.2499e+10
  blockAncC=50 scratchCF=7699 (Lean #eval pin 7699) catalyst=16
  thcTotalLogicalQubits=7873
  Lee: steps=481135 T per step=44062.5 total T=2.120e+10 qubits=2142
  ratios to Lee: per step 0.9956, total 1.0613, qubits 3.676
  ratios to P4.4: per step 0.7602, total 0.7602, qubits 1.2892
Li: N=76 M=450 aleph=10 beth=20 lamMax=2403/2
  gC=29 dC=101551 kappaC=131072/101551 = 1.290701
  slotBitsS=17 wordBitsC=29 decoder ANDs=304 decodeTC=1216 decWorkC=1453
  aliasTCF=18720 16*bIC=176 selTT=49048
  stepTCF=67944 (Lean #eval pin 67944)
  walk steps ceil(pi*kappa*lam/(2*0.001))=2435956
  tCostCF=165508594464 = 1.6551e+11
  blockAncC=53 scratchCF=13075 (Lean #eval pin 13075) catalyst=20
  thcTotalLogicalQubits=13300
  Lee: steps=1887312 T per step=67821.3 total T=1.280e+11 qubits=2196
  ratios to Lee: per step 1.0018, total 1.2930, qubits 6.056
  ratios to P4.4: per step 0.7129, total 0.7129, qubits 1.1592

Per-step T by part, P4.4 (stepTG) -> P4.9 (stepTCF):
  Reiher: alias word 54 -> 28 bits; PREPARE lookup 23044 -> 13164; alias decoder (2 calls) 1776 -> 2368; swaps 160 -> 160; SELECT 32728 -> 28176; step 57708 -> 43868
  Li: alias word 58 -> 29 bits; PREPARE lookup 35060 -> 16288; alias decoder (2 calls) 1872 -> 2432; swaps 176 -> 176; SELECT 58200 -> 49048; step 95308 -> 67944

SELECT by part (two row SELECTs per step), P4.4 -> P4.9:
  Reiher: rotation kicks 25440 -> 23744; spin swaps 1728 -> 864; angle lookup 5560 -> 3568
  Li: rotation kicks 45600 -> 43200; spin swaps 2432 -> 1216; angle lookup 10168 -> 4632
```

- κ is unchanged from P4.4: `tCostCF` uses the same `kappaC N M aleph = 2^gC / (4·dC·2^ℵ)` as P4.4's `tCostG`, and `gC` is still 28 and 29. The walk-step counts 512,886 and 2,435,956 are the same as in the first version.
- Qubits are `2N + thcBlockAncillas + thcScratchAncillas + thcCatalystQubits` with the solution's holes, the spec's `thcTotalLogicalQubits`. They exclude the phase-estimation register, which Lee et al.'s 2,142 and 2,196 include.
- Lee et al. (arXiv:2011.03494v3): Table III Toffolis 5.3e9 and 3.2e10, qubits 2,142 and 2,196, walk steps ⌈πλ/(2·0.001)⌉ = 481,135 and 1,887,312, per-step T = 4 × Toffolis / steps = 44,062.5 and 67,821.3.

## Not run

The hole check for computability of `thcCandidateProgram` and `thcTCost` was not run on this revision. The Lean build of the file in this folder was not rerun. `thcTotalLogicalQubits` and `blockAncC` were not evaluated in Lean for this revision.
