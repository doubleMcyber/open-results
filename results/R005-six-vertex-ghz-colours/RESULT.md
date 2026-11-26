# Six vertices and any number of colors at least three

## Exact statement and source

For every natural number D ≥ 3, there is no complex weighting of the endpoint-colored edges of the complete graph on six vertices whose perfect-matching sum is 1 on each constant vertex coloring and 0 on each other coloring. Every ordered pair of endpoint colors on each edge may have its own complex weight. Two colors are attainable.

This is the statement of `eqSystem6_no_solution_ge3` on lines 464–467 of the local source for INDEX.tsv row 131, `../src/misc/fc/FormalConjectures__Paper__MonochromaticQuantumGraph.lean` relative to the index directory. The source marks that statement open. Lines 414–424 mark the unrestricted three-color case solved and cite an external Lean certificate. The deduction below uses exactly that base case.

## Proof

For a coloring x, write its matching sum as

    H_W(x) = Σ_M ∏_{uv ∈ M, u < v} W(u,v,x(u),x(v)),

where M runs over the perfect matchings on the six labeled vertices. Suppose W solves the D-color equations. Choose an injection f from the three colors into the D colors. Define V(u,v,i,j) = W(u,v,f(i),f(j)) for every edge and every ordered pair of three-color indices.

For every three-coloring x and matching M, the three factors of its product under V at x equal the corresponding three factors under W at f ∘ x. Summing gives H_V(x) = H_W(f ∘ x). Injectivity gives that f ∘ x is constant exactly when x is constant. Thus V satisfies all the three-color equations. This contradicts the cited three-color theorem and proves the statement for every D ≥ 3.

The two-color witness in the same source assigns weight 1 to equal-color pairs on edges 01, 23, 45 for color 0 and 05, 12, 34 for color 1. All other entries have weight 0. The support is a six-cycle. Choosing either incident edge at vertex 0 forces the rest of the perfect matching. Its two matchings produce the two constant colorings, each with weight 1.

## Exact check

Run `python3 check.py` in this folder. The checker represents each edge/color weight by a separate formal variable. It compares full monomial multisets, with integer multiplicities, from two matching enumerations for all 729 three-colorings. The three distinct names for the image colors are symbolic, so the computation uses no chosen values of the complex weights. It also evaluates the stated two-color witness on all 64 colorings.

Local run on 2026-11-25 PDT with Python 3.11.9 completed without an assertion failure. It compared 10,935 matching products across 729 profiles, including three constant profiles. The two-color witness gave exactly two ones and 62 zeros.

## Reviewer checks and status

1. Independently verify the three-color base at the pinned external commit and compare the weight domain, endpoint order, right-hand side, and normalization with the local definitions. The external proof and its kernel verification are UNVERIFIED here. The local statement contains a proof placeholder. [Cited three-color certificate](https://github.com/algal/krenn-gu-6x3-certificate/blob/c04696e515e0c02be140353fb52ea60c62e827b1/KrennGuCertificate/Unrestricted.lean#L201-L222)
2. Rerun the Python checker. Inspect that restriction covers unequal endpoint indices and that equality of image colors reflects equality of their preimages.
3. Compile `Restriction.lean` against the matching FormalConjectures snapshot on the cluster. Its lemma takes the three-color obstruction as an explicit argument. With the verified base theorem in scope, the proof body of the original target is `exact WaveSix.six_of_three eqSystem6_no_solution_d3`. Lean elaboration and this integration are UNVERIFIED.
4. Novelty is UNVERIFIED. The local source already credits the fixed three-color obstruction and the two-color witness. The result here is the deduction for the separately indexed all-D statement.
