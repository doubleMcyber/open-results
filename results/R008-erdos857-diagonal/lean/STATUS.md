PROVED

Main theorem: `R008.erdos857_diagonal (n : ℕ) (hn : 3 ≤ n) : m n n = 2 ^ n - n / 2 - 1`, in Main.lean.
Covers the value formula for all n >= 3, both directions (upper bound `R008.upper`: any deletion set of
size <= n/2+1 misses an n-sunflower; lower bound `R008.lower`: an explicit deletion set of size <= n/2+2
meets every n-sunflower). Not formalized: the classification of extremal families (secondary goal).

Definitions `IsSunflowerWithKernel`, `IsSunflower`, `m` copy google-deepmind/formal-conjectures
(FormalConjectures/ErdosProblems/857.lean, FormalConjecturesForMathlib/Combinatorics/SetFamily/Sunflower.lean):
sunflower = pairwise intersections of distinct members all equal a kernel (one member may equal the kernel),
`m n k = sInf {t | ∀ F : Set (Set (Fin n)), t ≤ F.ncard → ∃ S ⊆ F, S.ncard = k ∧ IsSunflower S}`.

Axioms (`#print axioms R008.erdos857_diagonal`): [propext, Classical.choice, Quot.sound].
No sorry, no new axiom, no native_decide.

Check (2026-11-25): cd ~/dev/quantum/QS_hundred/lean && PATH=$HOME/.elan/bin:$PATH lake env lean OpenResults/R008/Main.lean
Output: only linter/deprecation warnings, zero errors, and the axioms line above.
