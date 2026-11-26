/-
R008: diagonal case of Erdos problem 857.
Statement (below, `Erdos857`-style definitions copied from google-deepmind/formal-conjectures,
FormalConjectures/ErdosProblems/857.lean and FormalConjecturesForMathlib/.../Sunflower.lean):
  m n k = least t such that every family F of subsets of Fin n with t <= |F| contains k distinct sets
  forming a sunflower (pairwise intersections all equal; one member may equal the kernel).
Main theorem `R008.erdos857_diagonal`: for n >= 3, m n n = 2^n - n/2 - 1.
Plain English: the least family size forcing an n-sunflower on n points is 2^n - floor(n/2) - 1.
Not formalized: the classification of extremal families (secondary goal).
-/
import Mathlib

namespace R008
open Finset

variable {n : ℕ}

def FS (S : Finset (Finset (Fin n))) : Prop :=
  S.card = n ∧ ∃ C : Finset (Fin n), ∀ A ∈ S, ∀ B ∈ S, A ≠ B → A ∩ B = C

/-- type 2 -/
theorem fs_singletons : FS (n := n) (Finset.univ.image (fun v : Fin n => ({v} : Finset (Fin n)))) := by
  refine ⟨?_, ∅, ?_⟩
  · rw [Finset.card_image_of_injective _ (fun a b h => by simpa using h)]; simp
  · intro A hA B hB hAB
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at hA hB
    obtain ⟨a, rfl⟩ := hA; obtain ⟨b, rfl⟩ := hB
    have : a ≠ b := fun h => hAB (by rw [h])
    ext x; simp <;> grind

/-- type 1 -/
def T1 (i : Fin n) : Finset (Finset (Fin n)) :=
  insert {i} ((Finset.univ.erase i).image (fun j => ({i, j} : Finset (Fin n))))

theorem fs_T1 (i : Fin n) : FS (T1 i) := by
  refine ⟨?_, {i}, ?_⟩
  · unfold T1
    rw [Finset.card_insert_of_notMem, Finset.card_image_of_injOn]
    · have := i.pos; simp; omega
    · intro a ha b hb h
      simp only [Finset.coe_erase, Set.mem_sdiff, Finset.mem_coe, Finset.mem_univ, Set.mem_singleton_iff, true_and] at ha hb
      simp only at h
      have : b ∈ ({i, a} : Finset (Fin n)) := by rw [h]; simp
      simp at this; grind
    · simp only [Finset.mem_image, Finset.mem_erase, Finset.mem_univ, and_true, not_exists, not_and]
      intro j hj h
      have : j ∈ ({i, j} : Finset (Fin n)) := by simp
      rw [h] at this
      simp at this; grind
  · intro A hA B hB hAB
    unfold T1 at hA hB
    simp only [Finset.mem_insert, Finset.mem_image, Finset.mem_erase, Finset.mem_univ, and_true] at hA hB
    rcases hA with rfl | ⟨a, ha, rfl⟩ <;> rcases hB with rfl | ⟨b, hb, rfl⟩
    · exact absurd rfl hAB
    · ext x; simp <;> grind
    · ext x; simp <;> grind
    · ext x; simp <;> grind

/-- type 3 -/
def T3 (j : Fin n) : Finset (Finset (Fin n)) :=
  insert ∅ ((Finset.univ.erase j).image (fun v => ({v} : Finset (Fin n))))

theorem fs_T3 (j : Fin n) : FS (T3 j) := by
  refine ⟨?_, ∅, ?_⟩
  · unfold T3
    rw [Finset.card_insert_of_notMem, Finset.card_image_of_injective _ (fun a b h => by simpa using h)]
    · have := j.pos; simp; omega
    · simp
  · intro A hA B hB hAB
    unfold T3 at hA hB
    simp only [Finset.mem_insert, Finset.mem_image, Finset.mem_erase, Finset.mem_univ, and_true] at hA hB
    rcases hA with rfl | ⟨a, ha, rfl⟩ <;> rcases hB with rfl | ⟨b, hb, rfl⟩
    · exact absurd rfl hAB
    · simp
    · simp
    · have : a ≠ b := fun h => hAB (by rw [h])
      ext x; simp <;> grind

/-- type 4 -/
def T4 (a b : Fin n) : Finset (Finset (Fin n)) :=
  insert ∅ (insert {a, b} ((Finset.univ \ {a, b}).image (fun v => ({v} : Finset (Fin n)))))

theorem fs_T4 (a b : Fin n) (hab : a ≠ b) : FS (T4 a b) := by
  refine ⟨?_, ∅, ?_⟩
  · unfold T4
    rw [Finset.card_insert_of_notMem, Finset.card_insert_of_notMem, Finset.card_image_of_injective _ (fun a b h => by simpa using h)]
    · have : ({a, b} : Finset (Fin n)).card = 2 := Finset.card_pair hab
      rw [Finset.card_sdiff_of_subset (Finset.subset_univ _)]
      simp [this]; omega
    · simp only [Finset.mem_image, not_exists, not_and]
      intro v hv h
      have : v ∈ ({a, b} : Finset (Fin n)) := by rw [← h]; simp
      simp at hv; simp at this; grind
    · simp only [Finset.mem_insert, Finset.mem_image, not_or, not_exists, not_and]
      refine ⟨?_, ?_⟩
      · intro h; have : a ∈ (∅ : Finset (Fin n)) := by rw [h]; simp
        simp at this
      · intro v _ h; simpa using h
  · intro A hA B hB hAB
    unfold T4 at hA hB
    simp only [Finset.mem_insert, Finset.mem_image, Finset.mem_sdiff, Finset.mem_univ, true_and] at hA hB
    rcases hA with rfl | rfl | ⟨a', ha, rfl⟩ <;> rcases hB with rfl | rfl | ⟨b', hb, rfl⟩
    all_goals first | exact absurd rfl hAB | skip
    all_goals (try (ext x; simp <;> grind))

theorem upper (D : Finset (Finset (Fin n))) (hD : D.card ≤ n / 2 + 1) :
    ∃ S, FS S ∧ ∀ A ∈ S, A ∉ D := by
  by_contra hcon
  push_neg at hcon
  have H : ∀ S, FS S → ∃ A ∈ S, A ∈ D := hcon
  set Sset : Finset (Fin n) := Finset.univ.filter (fun v => ({v} : Finset (Fin n)) ∈ D) with hSset
  have hs1 : 1 ≤ Sset.card := by
    by_contra h0
    have h0' : Sset.card = 0 := by omega
    rw [Finset.card_eq_zero] at h0'
    obtain ⟨A, hA, hAD⟩ := H _ fs_singletons
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at hA
    obtain ⟨v, rfl⟩ := hA
    have : v ∈ Sset := by simp [hSset, hAD]
    rw [h0'] at this; simp at this
  have hcover : ∀ v : Fin n, v ∉ Sset → ∃ A ∈ D, A.card = 2 ∧ v ∈ A := by
    intro v hv
    obtain ⟨A, hA, hAD⟩ := H _ (fs_T1 v)
    unfold T1 at hA
    simp only [mem_insert, mem_image, mem_erase, mem_univ, and_true] at hA
    rcases hA with rfl | ⟨j, hj, rfl⟩
    · exact absurd (show v ∈ Sset by simp [hSset, hAD]) hv
    · exact ⟨_, hAD, Finset.card_pair hj.symm, by simp⟩
  set P := D.filter (fun A => A.card = 2) with hP
  set D0 := D.filter (fun A => A.card = 0) with hD0
  set D1 := D.filter (fun A => A.card = 1) with hD1def
  have hsum : D0.card + D1.card + P.card ≤ D.card := by
    have h01 : Disjoint D0 D1 := by
      exact Finset.disjoint_filter.2 (by intro A _ h1 h2; omega)
    have h012 : Disjoint (D0 ∪ D1) P := by
      rw [Finset.disjoint_union_left]
      constructor <;> exact Finset.disjoint_filter.2 (by intro A _ h1 h2; omega)
    have := Finset.card_le_card (show D0 ∪ D1 ∪ P ⊆ D by
      intro A hA; simp only [mem_union, hD0, hD1def, hP, mem_filter] at hA; tauto)
    rwa [Finset.card_union_of_disjoint h012, Finset.card_union_of_disjoint h01] at this
  have hD1 : Sset.card ≤ D1.card := by
    have hsub : (Sset.image (fun v => ({v} : Finset (Fin n)))) ⊆ D1 := by
      intro A hA; simp only [mem_image] at hA; obtain ⟨v, hv, rfl⟩ := hA
      simp [hD1def, hSset] at hv ⊢; exact hv
    calc Sset.card = (Sset.image (fun v => ({v} : Finset (Fin n)))).card :=
          (Finset.card_image_of_injective _ (fun a b h => by simpa using h)).symm
      _ ≤ _ := Finset.card_le_card hsub
  have hO : (Finset.univ \ Sset).card = n - Sset.card := by
    rw [Finset.card_univ_diff]; simp
  have hSn : Sset.card ≤ n := by simpa using Finset.card_le_univ Sset
  have hcov : (Finset.univ \ Sset).card ≤ P.card * 2 := by
    calc (Finset.univ \ Sset).card ≤ (P.biUnion id).card := Finset.card_le_card (by
          intro v hv; simp only [mem_sdiff, mem_univ, true_and] at hv
          obtain ⟨A, hA, h2, hvA⟩ := hcover v hv
          simp only [mem_biUnion, id]; exact ⟨A, by simp [hP, hA, h2], hvA⟩)
      _ ≤ P.card * 2 := Finset.card_biUnion_le_card_mul _ _ _ (fun A hA => by simp [hP] at hA ⊢; omega)
  by_cases he : (∅ : Finset (Fin n)) ∈ D
  · have : 1 ≤ D0.card := Finset.card_pos.2 ⟨∅, by simp [hD0, he]⟩
    omega
  · have hs2 : 2 ≤ Sset.card := by
      by_contra h
      have h1 : Sset.card = 1 := by omega
      obtain ⟨j, hj⟩ := Finset.card_eq_one.1 h1
      obtain ⟨A, hA, hAD⟩ := H _ (fs_T3 j)
      unfold T3 at hA
      simp only [mem_insert, mem_image, mem_erase, mem_univ, and_true] at hA
      rcases hA with rfl | ⟨v, hv, rfl⟩
      · exact he hAD
      · have : v ∈ Sset := by simp [hSset, hAD]
        rw [hj] at this; simp at this; exact hv this
    by_cases h2 : Sset.card = 2
    · obtain ⟨a, b, hab, hab'⟩ := Finset.card_eq_two.1 h2
      have hpair : ({a, b} : Finset (Fin n)) ∈ D := by
        obtain ⟨A, hA, hAD⟩ := H _ (fs_T4 a b hab)
        unfold T4 at hA
        simp only [mem_insert, mem_image, mem_sdiff, mem_univ, true_and] at hA
        rcases hA with rfl | rfl | ⟨v, hv, rfl⟩
        · exact absurd hAD he
        · exact hAD
        · exfalso
          have : v ∈ Sset := by simp [hSset, hAD]
          rw [hab'] at this; exact hv (by simpa using this)
      have hcov2 : (Finset.univ \ Sset).card ≤ (P.erase {a, b}).card * 2 := by
        calc (Finset.univ \ Sset).card ≤ ((P.erase {a, b}).biUnion id).card := Finset.card_le_card (by
              intro v hv; simp only [mem_sdiff, mem_univ, true_and] at hv
              obtain ⟨A, hA, h2', hvA⟩ := hcover v hv
              simp only [mem_biUnion, id]
              refine ⟨A, ?_, hvA⟩
              rw [Finset.mem_erase]
              refine ⟨?_, by simp [hP, hA, h2']⟩
              rintro rfl
              apply hv; rw [hab']; exact hvA)
          _ ≤ _ := Finset.card_biUnion_le_card_mul _ _ _ (fun A hA => by
              simp [hP] at hA ⊢; omega)
      have : (P.erase {a, b}).card + 1 = P.card :=
        Finset.card_erase_add_one (by simp [hP, hpair, Finset.card_pair hab])
      omega
    · omega


theorem lower (hn : 3 ≤ n) : ∃ D0 : Finset (Finset (Fin n)), D0.card ≤ n / 2 + 2 ∧
    ∀ S, FS S → ∃ A ∈ S, A ∈ D0 := by
  haveI : NeZero n := ⟨by omega⟩
  let mk : ℕ → Fin n := fun a => ⟨a % n, Nat.mod_lt _ (by omega)⟩
  let edge : ℕ → Finset (Fin n) := fun i => {mk (2 * i + 1), mk (2 * i + 2)}
  refine ⟨insert ∅ (insert {0} ((Finset.range (n / 2)).image edge)), ?_, ?_⟩
  · have h1 := Finset.card_insert_le (∅ : Finset (Fin n)) (insert {(0 : Fin n)} ((Finset.range (n / 2)).image edge))
    have h2 := Finset.card_insert_le ({0} : Finset (Fin n)) ((Finset.range (n / 2)).image edge)
    have h3 := Finset.card_image_le (s := Finset.range (n / 2)) (f := edge)
    simp only [Finset.card_range] at h3
    omega
  · rintro S ⟨hcard, C, hC⟩
    by_contra hcon
    have hcon' : ∀ A ∈ S, A ∉ insert ∅ (insert {0} ((Finset.range (n / 2)).image edge)) :=
      fun A hA h => hcon ⟨A, hA, h⟩
    have hn1 : ∀ A ∈ S, A ≠ ∅ := fun A hA h => hcon' A hA (by rw [h]; simp)
    have hn2 : ∀ A ∈ S, A ≠ {0} := fun A hA h => hcon' A hA (by rw [h]; simp)
    have hn3 : ∀ A ∈ S, ∀ i < n / 2, A ≠ edge i := fun A hA i hi h =>
      hcon' A hA (by
        rw [h]
        exact Finset.mem_insert_of_mem (Finset.mem_insert_of_mem
          (Finset.mem_image.2 ⟨i, Finset.mem_range.2 hi, rfl⟩)))
    have hedge : ∀ v : Fin n, v ≠ 0 → ∃ i < n / 2, v ∈ edge i := by
      intro v hv
      have hv0 : v.val ≠ 0 := fun h => hv (Fin.ext (by simpa using h))
      have hvn := v.isLt
      rcases Nat.even_or_odd' v.val with ⟨q, hq | hq⟩
      · refine ⟨q - 1, by omega, ?_⟩
        simp only [edge, Finset.mem_insert, Finset.mem_singleton]
        right
        apply Fin.ext
        show v.val = (_ : ℕ) % n
        rw [Nat.mod_eq_of_lt (by omega)]
        omega
      · refine ⟨q, by omega, ?_⟩
        simp only [edge, Finset.mem_insert, Finset.mem_singleton]
        left
        apply Fin.ext
        show v.val = (_ : ℕ) % n
        rw [Nat.mod_eq_of_lt (by omega)]
        omega
    have hsub : ∀ A ∈ S, C ⊆ A := by
      intro A hA
      obtain ⟨B, hB, hBA⟩ := Finset.exists_mem_ne (show 1 < S.card by omega) A
      rw [← hC A hA B hB (Ne.symm hBA)]
      exact Finset.inter_subset_left
    have hdisj : ∀ A ∈ S, ∀ B ∈ S, A ≠ B → Disjoint (A \ C) (B \ C) := by
      intro A hA B hB hAB
      rw [Finset.disjoint_left]
      intro x hxA hxB
      have : x ∈ A ∩ B :=
        Finset.mem_inter.2 ⟨(Finset.mem_sdiff.1 hxA).1, (Finset.mem_sdiff.1 hxB).1⟩
      rw [hC A hA B hB hAB] at this
      exact (Finset.mem_sdiff.1 hxA).2 this
    have hU : (S.biUnion (fun A => A \ C)).card = ∑ A ∈ S, (A \ C).card :=
      Finset.card_biUnion hdisj
    have hUle : S.biUnion (fun A => A \ C) ⊆ Finset.univ \ C := by
      intro x hx
      simp only [Finset.mem_biUnion] at hx
      obtain ⟨A, _, hxA⟩ := hx
      simp only [Finset.mem_sdiff] at hxA
      simp [hxA.2]
    have hUcard : (S.biUnion (fun A => A \ C)).card ≤ n - C.card := by
      have := Finset.card_le_card hUle
      rwa [Finset.card_univ_diff, Fintype.card_fin] at this
    have hpos : ∀ A ∈ S.erase C, 1 ≤ (A \ C).card := by
      intro A hA
      rw [Finset.mem_erase] at hA
      apply Finset.card_pos.2
      rw [Finset.sdiff_nonempty]
      intro h
      exact hA.1 (Finset.Subset.antisymm h (hsub A hA.2))
    have hSum : ∑ A ∈ S, (A \ C).card = ∑ A ∈ S.erase C, (A \ C).card :=
      (Finset.sum_erase S (by simp)).symm
    have hlow : (S.erase C).card ≤ ∑ A ∈ S.erase C, (A \ C).card := by
      have := Finset.card_nsmul_le_sum (S.erase C) (fun A => (A \ C).card) 1 hpos
      simpa using this
    have herase : n - 1 ≤ (S.erase C).card := by
      have := Finset.pred_card_le_card_erase (s := S) (a := C); omega
    have hkn : C.card ≤ n := by simpa using Finset.card_le_univ C
    -- the two cases for the core
    have hcases : (C.card = 0 ∧ C ∉ S) ∨ (C.card = 1 ∧ C ∈ S) := by
      by_cases hCS : C ∈ S
      · have h1 : (S.erase C).card = n - 1 := by rw [Finset.card_erase_of_mem hCS]; omega
        right
        have hk0 : C.card ≠ 0 := fun h => hn1 C hCS (Finset.card_eq_zero.1 h)
        refine ⟨by omega, hCS⟩
      · have h1 : (S.erase C).card = n := by rw [Finset.erase_eq_of_notMem hCS]; omega
        left
        refine ⟨by omega, hCS⟩
    have hEcard : (S.erase C).card = n - C.card := by
      rcases hcases with ⟨h0, hCS⟩ | ⟨h1, hCS⟩
      · rw [Finset.erase_eq_of_notMem hCS]; omega
      · rw [Finset.card_erase_of_mem hCS]; omega
    have hw1 : ∀ A ∈ S.erase C, (A \ C).card = 1 := by
      have heq : ∑ A ∈ S.erase C, (1 : ℕ) = ∑ A ∈ S.erase C, (A \ C).card := by
        simp only [Finset.sum_const, smul_eq_mul, mul_one]; omega
      exact fun A hA => ((Finset.sum_eq_sum_iff_of_le hpos).1 heq A hA).symm
    have hUeq : S.biUnion (fun A => A \ C) = Finset.univ \ C := by
      apply Finset.eq_of_subset_of_card_le hUle
      rw [Finset.card_univ_diff, Fintype.card_fin]; omega
    have hmem : ∀ x, x ∉ C → ∃ A ∈ S.erase C, x ∈ A \ C := by
      intro x hx
      have : x ∈ S.biUnion (fun A => A \ C) := by rw [hUeq]; simp [hx]
      simp only [Finset.mem_biUnion] at this
      obtain ⟨A, hA, hxA⟩ := this
      refine ⟨A, Finset.mem_erase.2 ⟨?_, hA⟩, hxA⟩
      rintro rfl
      simp at hxA
    rcases hcases with ⟨h0, hCS⟩ | ⟨h1, hCS⟩
    · have hC0 : C = ∅ := Finset.card_eq_zero.1 h0
      obtain ⟨A, hA, h0A⟩ := hmem 0 (by simp [hC0])
      have hAS := (Finset.mem_erase.1 hA).2
      have := hw1 A hA
      rw [hC0, Finset.sdiff_empty] at this h0A
      obtain ⟨a, rfl⟩ := Finset.card_eq_one.1 this
      have : a = 0 := (by simpa using h0A : (0 : Fin n) = a).symm
      exact hn2 _ hAS (by rw [this])
    · obtain ⟨c, hc⟩ := Finset.card_eq_one.1 h1
      by_cases hc0 : c = 0
      · exact hn2 C hCS (by rw [hc, hc0])
      · have hjS : ∀ j, ({c, j} : Finset (Fin n)) ∈ S := by
          intro j
          by_cases hjc : j = c
          · subst hjc; simpa [hc] using hCS
          · obtain ⟨A, hA, hjA⟩ := hmem j (by simp [hc, hjc])
            have hAS := (Finset.mem_erase.1 hA).2
            obtain ⟨j', hj'⟩ := Finset.card_eq_one.1 (hw1 A hA)
            have hjj : j = j' := by
              have : j ∈ ({j'} : Finset (Fin n)) := by rw [← hj']; exact hjA
              simpa using this
            have hAeq : A = {c, j} := by
              rw [← Finset.union_sdiff_of_subset (hsub A hAS), hj', hc, ← hjj]
              ext x; simp
            rw [← hAeq]; exact hAS
        obtain ⟨i, hi, hci⟩ := hedge c hc0
        have hcS : c ∈ edge i := hci
        simp only [edge, Finset.mem_insert, Finset.mem_singleton] at hcS
        rcases hcS with h | h
        · have : edge i = {c, mk (2 * i + 2)} := by
            simp only [edge]; rw [← h]
          exact hn3 (edge i) (by rw [this]; exact hjS _) i hi rfl
        · have : edge i = {c, mk (2 * i + 1)} := by
            simp only [edge]; rw [← h]; exact Finset.pair_comm _ _
          exact hn3 (edge i) (by rw [this]; exact hjS _) i hi rfl


/-! ### Statement, matching `FormalConjectures/ErdosProblems/857.lean` and
`FormalConjecturesForMathlib/Combinatorics/SetFamily/Sunflower.lean` -/

def IsSunflowerWithKernel {α : Type*} (F : Set (Set α)) (S : Set α) : Prop :=
  F.Pairwise (fun A B => A ∩ B = S)

def IsSunflower {α : Type*} (F : Set (Set α)) : Prop := ∃ S, IsSunflowerWithKernel F S

noncomputable def m (n k : ℕ) : ℕ :=
  sInf {t : ℕ | ∀ (F : Set (Set (Fin n))), t ≤ F.ncard →
    ∃ S ⊆ F, S.ncard = k ∧ IsSunflower S}

open Classical in
theorem sunf_of_FS {n : ℕ} (S : Finset (Finset (Fin n))) (h : FS S) :
    IsSunflower ((fun A : Finset (Fin n) => (A : Set (Fin n))) '' (S : Set (Finset (Fin n)))) ∧
    ((fun A : Finset (Fin n) => (A : Set (Fin n))) '' (S : Set (Finset (Fin n)))).ncard = n := by
  obtain ⟨hc, C, hC⟩ := h
  refine ⟨⟨(C : Set (Fin n)), ?_⟩, ?_⟩
  · rintro _ ⟨a, ha, rfl⟩ _ ⟨b, hb, rfl⟩ hne
    have : a ≠ b := fun h => hne (by rw [h])
    rw [← Finset.coe_inter, hC a ha b hb this]
  · rw [Set.ncard_image_of_injective _ Finset.coe_injective, Set.ncard_coe_finset, hc]

theorem card_univ_fs {n : ℕ} : (Finset.univ : Finset (Finset (Fin n))).card = 2 ^ n := by
  simp

open Classical in
theorem erdos857_diagonal (n : ℕ) (hn : 3 ≤ n) : m n n = 2 ^ n - n / 2 - 1 := by
  have hN : n < 2 ^ n := Nat.lt_two_pow_self
  have hcu : (Finset.univ : Finset (Finset (Fin n))).card = 2 ^ n := card_univ_fs
  have hmem : (2 ^ n - n / 2 - 1) ∈ {t : ℕ | ∀ (F : Set (Set (Fin n))), t ≤ F.ncard →
      ∃ S ⊆ F, S.ncard = n ∧ IsSunflower S} := by
    intro F hF
    set Fs : Finset (Finset (Fin n)) :=
      Finset.univ.filter (fun A : Finset (Fin n) => (A : Set (Fin n)) ∈ F) with hFs
    have hFsub : F ⊆ (fun A : Finset (Fin n) => (A : Set (Fin n))) '' (Fs : Set (Finset (Fin n))) := by
      intro B hB
      obtain ⟨A, hA⟩ := (Set.toFinite B).exists_finset_coe
      refine ⟨A, ?_, hA⟩
      simp [hFs, hA, hB]
    have hFle : F.ncard ≤ Fs.card := by
      have := Set.ncard_le_ncard hFsub (Set.toFinite _)
      rwa [Set.ncard_image_of_injective _ Finset.coe_injective, Set.ncard_coe_finset] at this
    have hDcard : (Finset.univ \ Fs).card ≤ n / 2 + 1 := by
      rw [Finset.card_univ_diff]
      have : Fs.card ≤ Fintype.card (Finset (Fin n)) := Finset.card_le_univ Fs
      simp only [Fintype.card_finset, Fintype.card_fin] at this ⊢
      omega
    obtain ⟨S, hS, hSD⟩ := upper (Finset.univ \ Fs) hDcard
    refine ⟨(fun A : Finset (Fin n) => (A : Set (Fin n))) '' (S : Set (Finset (Fin n))), ?_,
      (sunf_of_FS S hS).2, (sunf_of_FS S hS).1⟩
    rintro _ ⟨A, hA, rfl⟩
    have := hSD A hA
    simp [hFs] at this
    simpa [hFs] using this
  apply le_antisymm (Nat.sInf_le hmem)
  apply le_csInf ⟨_, hmem⟩
  intro t ht
  by_contra hlt
  push_neg at hlt
  obtain ⟨D0, hD0, hhit⟩ := lower (n := n) hn
  set Fs : Finset (Finset (Fin n)) := Finset.univ \ D0 with hFs
  set F : Set (Set (Fin n)) := (fun A : Finset (Fin n) => (A : Set (Fin n))) '' (Fs : Set (Finset (Fin n))) with hF
  have hFcard : F.ncard = Fs.card := by
    rw [hF, Set.ncard_image_of_injective _ Finset.coe_injective, Set.ncard_coe_finset]
  have hFs' : Fs.card = 2 ^ n - D0.card := by
    rw [hFs, Finset.card_univ_diff]; simp
  have hD0le : D0.card ≤ 2 ^ n := by
    simpa using Finset.card_le_univ D0
  obtain ⟨S, hSF, hScard, hSsun⟩ := ht F (by omega)
  set S0 : Finset (Finset (Fin n)) := Fs.filter (fun A => (A : Set (Fin n)) ∈ S) with hS0
  have hSeq : S = (fun A : Finset (Fin n) => (A : Set (Fin n))) '' (S0 : Set (Finset (Fin n))) := by
    ext B
    constructor
    · intro hB
      obtain ⟨A, hA, rfl⟩ := hSF hB
      exact ⟨A, Finset.mem_coe.2 (Finset.mem_filter.2 ⟨Finset.mem_coe.1 hA, hB⟩), rfl⟩
    · rintro ⟨A, hA, rfl⟩
      exact (Finset.mem_filter.1 (Finset.mem_coe.1 hA)).2
  have hFS : FS S0 := by
    refine ⟨?_, ?_⟩
    · have h := hScard
      rw [hSeq, Set.ncard_image_of_injective _ Finset.coe_injective, Set.ncard_coe_finset] at h
      exact h
    · obtain ⟨K, hK⟩ := hSsun
      obtain ⟨C, hCK⟩ := (Set.toFinite K).exists_finset_coe
      refine ⟨C, fun A hA B hB hAB => ?_⟩
      apply Finset.coe_injective
      rw [Finset.coe_inter, hCK]
      apply hK
      · rw [hSeq]; exact ⟨A, hA, rfl⟩
      · rw [hSeq]; exact ⟨B, hB, rfl⟩
      · intro h; exact hAB (Finset.coe_injective h)
  obtain ⟨A, hA, hAD⟩ := hhit S0 hFS
  have : A ∈ Fs := (Finset.mem_filter.1 hA).1
  rw [hFs] at this
  simp at this
  exact this hAD

end R008

#print axioms R008.erdos857_diagonal
