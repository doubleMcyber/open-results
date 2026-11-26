import FormalConjectures.Paper.MonochromaticQuantumGraph

namespace WaveSix
open MonochromaticQuantumGraph

/-- The three-color obstruction implies the source's full six-vertex statement. -/
theorem six_of_three
    (base : ¬ ∃ W : WeightsN 6 3 ℂ, EqSystemN 6 3 W) :
    ∀ D : Nat, D ≥ 3 →
      ¬ ∃ W : WeightsN 6 D ℂ, EqSystemN 6 D W := by
  intro D hD
  rintro ⟨W, hW⟩
  let f : Fin 3 → Fin D := fun x => ⟨x.val, Nat.lt_of_lt_of_le x.isLt hD⟩
  have hf : Function.Injective f := by
    intro i j hij
    exact Fin.ext (congrArg (fun k : Fin D => k.val) hij)
  let V' : WeightsN 6 3 ℂ := fun e => W (mkEdge e.u e.v (f e.i) (f e.j))
  apply base
  refine ⟨V', ?_⟩
  intro x
  have rel : (fun v w : V 6 => f (x v) = f (x w)) =
      (fun v w : V 6 => x v = x w) := by
    funext v w
    exact propext ⟨fun h => hf h, congrArg f⟩
  have hconst : allEqual (fun v => f (x v)) ↔ allEqual x := by
    unfold allEqual allEqualList
    rw [rel]
  have hsum : pmSumN 6 3 V' x = pmSumN 6 D W (fun v => f (x v)) := by
    rfl
  rw [hsum]
  simpa only [hconst] using hW (fun v => f (x v))

end WaveSix
