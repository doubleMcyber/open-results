# Verification record, P4.10 update

Revision: the Lean file in [lean/](lean/), sha256 7df98e958a471bead42b5b2c3ccddcdd1328b679a9cc710d24d426a65ff3d40e (44,015 lines). Run on 2026-11-26 from 11:18 to 11:52 PST, sandbox job 2027259, in a bubblewrap sandbox (bubblewrap 0.9.0, Ubuntu 24.04.5, Lean 4.35.0 eb6cafb7, Lake 5.0.0), spec and stock config from the `discoveries` branch at a88de8f (spec sha256 7bb6d8e9bcf84286d0b3ff6994c731e758f3f40dcbee43bbb305a58fa30f7326, config sha256 8457ef0aa16816f165cd60252d13b6601e32b7628eed9a40c2e1f1f9beff8c28). The file is the Google-layout form of the solution with root `THC.AssemblyCG` and holes file [lean/holesG.json](lean/holesG.json), assembled from a 35,556-line file (sha256 af0404f95f7fc0521c084973efb5b5d4b70b5ce2e71843f0152a5b0cc53a3df5).

## File hash (rerun here, 2026-11-26, no Lean build)

```
shasum -a 256 lean/THCFactorization.lean
7df98e958a471bead42b5b2c3ccddcdd1328b679a9cc710d24d426a65ff3d40e  lean/THCFactorization.lean
```

The sandbox job log prints the same hash for the file it checked (fourth line of the log):

```
7df98e958a471bead42b5b2c3ccddcdd1328b679a9cc710d24d426a65ff3d40e  files/THCFactorization.lean
7bb6d8e9bcf84286d0b3ff6994c731e758f3f40dcbee43bbb305a58fa30f7326  disc/QuantumComputationSpecs/Primitives/THCFactorization.lean
8457ef0aa16816f165cd60252d13b6601e32b7628eed9a40c2e1f1f9beff8c28  disc/QuantumComputationSpecs/ChallengeJsons/Primitives/THCFactorization.json
```

The Lean build was not rerun when this update was assembled.

## Comparator, stock config plus `--challenge-from-export`

The file is placed at `QuantumComputationSpecs/Primitives/THCFactorization.lean` and checked with `lake comparator --config QuantumComputationSpecs/ChallengeJsons/Primitives/THCFactorization.json --challenge-from-export <challenge export>`. The challenge export (254,882,246 bytes, sha256 b38576fe108aec87e6d436400dbba1eecf3704ea1296c72b6f286c492cce2c19) was made from the untouched spec in a separate tree. Excerpt from the job log:

```
Running Lean default kernel on solution
Lean default kernel accepts the solution
Your solution is okay!
comparator exit 0 wall 154 s end 2026-11-26T11:41:32-08:00
VERDICT Apos ACCEPTED
```

The literal stock command (no `--challenge-from-export`) also passed, but it compares the file with itself and is not evidence:

```
Your solution is okay!
comparator exit 0 wall 449 s end 2026-11-26T11:38:58-08:00
VERDICT Alit ACCEPTED
```

## Negative tests

Same command and export, on the same file with one change each. AnegH adds a parameter `(dummy : ℕ := 0)` to the hole `thcCatalystQubits` (sha256 f42621452109c938…). AnegT adds a hypothesis `(hextra : True)` to `thc_t_cost` (sha256 7bfccb8562b67685…).

```
AnegH:
error: Challenge and solution theorem statement do not match: 'QuantumComputation.Specs.thc_correctness'
comparator exit 1 wall 319 s end 2026-11-26T11:46:51-08:00
VERDICT AnegH REJECTED

AnegT:
error: Challenge and solution theorem statement do not match: 'QuantumComputation.Specs.thc_t_cost'
comparator exit 1 wall 322 s end 2026-11-26T11:52:13-08:00
VERDICT AnegT REJECTED

SUMMARY Alit=ACCEPTED Apos=ACCEPTED AnegH=REJECTED AnegT=REJECTED
```

Local run on the Mac, 2026-11-26 11:17 to 11:22 PST, a copy of the 35,556-line solution with a `sorry` in a proof (sha256 0206dc9c37aa04ce…):

```
error: Illegal axiom detected: 'sorryAx'
comparator exit 1 (3 min)
```

Local comparator run on the unmodified 35,556-line file (sha256 af0404f95f7fc052…), against a challenge export of the untouched spec, 11:11 to 11:17 PST (local log `logs/g3p410_1126_1111.log`; the `sorry` run is `logs/g3p410neg_1126_1117.log`): `Your solution is okay!`, exit 0.

## Axioms and the per-step `#eval`

Local run on the Mac, 2026-11-26 11:10 PST, on the `THC.AssemblyCG` modules (the same proof before assembly into one file and before the Google-layout wrapping). Last lines of the local log `logs/p410ax_1126_1110.log`, with the prefix `info: THC/Debug/P410Ax.lean:<line>:0:` removed from the axiom lines:

```
info: THC/Debug/P410Skel.lean:5:0: [42684, 66728, 43868, 67944]
info: THC/Debug/P410Skel.lean:6:0: [9113, 14528, 7699, 13075]
'QC14.DecodeCS.runList_decodeOpen' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.DecodeCS.runList_decodeClose' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.DecodeCS.decodeOpen_count_T' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.DecodeCS.decodeClose_count_T' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.LiveCG.selLiveCG' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.PairProgramCG.cgFwd' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.PairProgramCG.cgInv' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.PairProgramCG.pair_catKetCG' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.PairProgramCG.pair_countCG' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.AssemblyCG.realizes_CG' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.AssemblyCG.count_CG' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.AssemblyCG.thc_correctness_CG' depends on axioms: [propext, Classical.choice, Quot.sound]
'QC14.AssemblyCG.thc_t_cost_CG' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The two `info` lines come from these commands in the same build:

```
#eval [stepTCG 54 350 10 16, stepTCG 76 450 10 20, stepTCF 54 350 10 16, stepTCF 76 450 10 20]
#eval [scratchCG 54 350 10 16, scratchCG 76 450 10 20, scratchCF 54 350 10 16, scratchCF 76 450 10 20]
```

`stepTCG` and `scratchCG` are this version; `stepTCF` and `scratchCF` are the P4.9 values, for comparison. The two spec theorems are proved by `exact QC14.AssemblyCG.thc_correctness_CG …` and `exact QC14.AssemblyCG.thc_t_cost_CG …`. The comparator enforces the stock config's permitted axioms (propext, Quot.sound, Classical.choice) and accepted. It does not print the axiom list.

## Numbers

These are Python evaluations of the Lean definitions in [lean/THCFactorization.lean](lean/THCFactorization.lean), not Lean evaluations. [numbers.py](numbers.py) ports `stepTCG`, `scratchCG`, `blockAncC`, `kappaC`, `qpeWalkSteps`, `tCostCG` and the definitions they use to exact integers and fractions, with π to 31 decimal places. Lines 1 to 38,455 of the file are identical to the P4.9 file, and P4.9's lines 38,458 to 42,556 reappear unchanged 593 lines later, so the shared definitions (including the generated decoder network) are the port from [../p49/numbers.py](../p49/numbers.py). It also ports P4.9's `stepTCF` and `scratchCF` for the comparison. It checks that its four values equal the Lean `#eval` values above. `thcTCost` itself cannot be evaluated in Lean, because `qpeWalkSteps` takes a real ε.

Output of `python3 -I numbers.py`:

```
Reiher: N=54 M=350 aleph=10 beth=16 lamMax=3063/10
  gC=28 dC=61479 kappaC=65536/61479 = 1.065990
  slotBitsS=16 wordBitsC=28 decoder ANDs=296 decodeTC=1184 decWorkC=1414
  aliasTCG=14348 (P4.9 aliasTCF=15532) 16*bIC=160 selTT=28176
  stepTCG=42684 (Lean #eval pin 42684); P4.9 stepTCF=43868 (pin 43868); difference 1184
  walk steps ceil(pi*kappa*lam/(2*0.001))=512886 (P4.9 512886)
  tCostCG=21892026024 = 2.1892e+10
  blockAncC=50 scratchCG=9113 (Lean #eval pin 9113); P4.9 scratchCF=7699 (pin 7699); difference +1414; catalyst=16
  coreWorkCF=4073 coreWorkCG=4073
  thcTotalLogicalQubits=9287 (P4.9 7873)
  Lee: steps=481135 T per step=44062.5 total T=2.120e+10 qubits=2142
  Lee minus stepTCG: 1378.5 T per step
  ratios to Lee: per step 0.9687, total 1.0326, qubits 4.336
  ratios to P4.9: per step 0.9730, total 0.9730, qubits 1.1796
  ratios to P4.4: per step 0.7397, total 0.7397, qubits 1.5207
Li: N=76 M=450 aleph=10 beth=20 lamMax=2403/2
  gC=29 dC=101551 kappaC=131072/101551 = 1.290701
  slotBitsS=17 wordBitsC=29 decoder ANDs=304 decodeTC=1216 decWorkC=1453
  aliasTCG=17504 (P4.9 aliasTCF=18720) 16*bIC=176 selTT=49048
  stepTCG=66728 (Lean #eval pin 66728); P4.9 stepTCF=67944 (pin 67944); difference 1216
  walk steps ceil(pi*kappa*lam/(2*0.001))=2435956 (P4.9 2435956)
  tCostCG=162546471968 = 1.6255e+11
  blockAncC=53 scratchCG=14528 (Lean #eval pin 14528); P4.9 scratchCF=13075 (pin 13075); difference +1453; catalyst=20
  coreWorkCF=8046 coreWorkCG=8046
  thcTotalLogicalQubits=14753 (P4.9 13300)
  Lee: steps=1887312 T per step=67821.3 total T=1.280e+11 qubits=2196
  Lee minus stepTCG: 1093.3 T per step
  ratios to Lee: per step 0.9839, total 1.2699, qubits 6.718
  ratios to P4.9: per step 0.9821, total 0.9821, qubits 1.1092
  ratios to P4.4: per step 0.7001, total 0.7001, qubits 1.2859
```

- What changed from P4.9: `aliasTCG` charges the decoder once (`decodeTC`) where `aliasTCF` charged it twice. The decoder's work register stays live through SELECT, and the PREPARE inverse uncomputes it by measurement at 0 T (`DecodeCS.decodeCloseSteps`) instead of decoding again. That saves 1,184 and 1,216 T per step. The price is width: `baseWidthCG` adds `decWorkC` (1,414 and 1,453 qubits) as its own region, where `coreWorkCF` shared it with other scratch inside a `max`.
- κ is unchanged from P4.9 and P4.4: `tCostCG` uses the same `kappaC N M aleph = 2^gC / (4·dC·2^ℵ)`, and `gC` is still 28 and 29. The walk-step counts 512,886 and 2,435,956 are the same as in both earlier versions.
- Qubits are `2N + thcBlockAncillas + thcScratchAncillas + thcCatalystQubits` with the solution's holes, the spec's `thcTotalLogicalQubits`. They exclude the phase-estimation register, which Lee et al.'s 2,142 and 2,196 include.
- Lee et al. (arXiv:2011.03494v3): Table III Toffolis 5.3e9 and 3.2e10, qubits 2,142 and 2,196, walk steps ⌈πλ/(2·0.001)⌉ = 481,135 and 1,887,312, per-step T = 4 × Toffolis / steps = 44,062.5 and 67,821.3.

## Not run

The hole check for computability of `thcCandidateProgram` and `thcTCost` was not run on this revision. The Lean build of the file in this folder was not rerun. `thcTotalLogicalQubits` and `blockAncC` were not evaluated in Lean for this revision.
