# Exactly three blue-to-red flips in Exoo’s cyclic colouring

**The minimum number of monochromatic five-sets is 11.** Label the vertices of the complete graph by residues modulo 43. Give an edge the shorter of its two cyclic lengths. Initially the red lengths are 1, 2, 7, 10, 12, 13, 14, 16, 18, 20 and 21. All other edges are blue. Choose exactly three distinct initially blue edges and recolour them red. Independently recolour any subset of the initially red edges blue. The minimum counts five-vertex subsets spanning a clique of either colour, each counted once.

The starting point is row 661, `ramsey_5_5_17`, of the supplied index. Its source `src/rstation/md/p17.md`, section “Allowing two changes in the opposite direction”, proves a lower bound of three when one or two initially blue edges change to red. The theorem here gives the exact minimum for the next case. The supplied index ends at physical line 669. Novelty is UNVERIFIED.

## A colouring attaining 11

Recolour {13,30}, {0,26} and {10,29} red. Recolour the unit edges {i,i+1} blue for i in the inclusive ranges 0–3, 9–12, 18–20, 26–29 and 35–37. The script checks all 962,598 five-sets directly against the resulting edge colours. Exactly 11 are red and none are blue.

## Lower bound

Fix the three additions F. A private witness for an initially red edge e is a five-set whose only initially red edge is e and whose other nine edges avoid F. If e is deleted, every such witness is blue. Write w(e) for their number. Witnesses for distinct edges are disjoint as collections of five-sets, since the sole initially red edge determines e.

Consider the five-sets with just one initially blue edge, belonging to F. Each is red immediately after the additions. Choose a family of p such sets so that each initially red edge e belongs to at most w(e) members. For each occurrence of e reserve a different private witness at e. This makes p disjoint groups of five-sets. Each group contains its chosen set and nine reserved witnesses, one for each initially red edge of the chosen set. In every final colouring, at least one five-set in each group is monochromatic. If no edge of the chosen set is deleted, it is red. Otherwise a reserved witness at any deleted edge is blue. Thus any such family certifies at least p defects.

The script builds a family greedily, accepting a set when all nine edges have unused witnesses. For each initially red edge it computes the initial witnesses as triangles in the common blue neighbourhood of its endpoints, then drops witnesses hit by F. For each addition it finds candidate sets by the same triangle enumeration with the colours exchanged. An attained packing of 11 suffices. A smaller greedy packing goes to the following check.

Suppose a colouring has at most 10 defects. Write b = 10−p. Besides the guaranteed defect in each group, at most b defects can occur outside the groups. If e has more than b unreserved private witnesses, e must stay red. All three additions are also fixed red. All initially blue edges outside F are fixed blue. Call the remaining edges undetermined.

For each colour enumerate all five-cliques among that colour’s fixed edges and the undetermined edges. In each clique record the set of undetermined edges as a bit mask. Its multiplicity counts distinct five-sets with the same mask. A red term counts that multiplicity if every edge in its mask is red, and a blue term counts it if all are blue. Remove one red term occurrence for each chosen set. A blue term with singleton mask {e} is exactly a surviving private witness at e, since every fixed blue edge is initially blue and outside F. Keep only the unreserved multiplicity at each singleton. A reserved witness at an edge already fixed red cannot occur among the blue candidates. All five-sets outside the groups that can become monochromatic are now represented.

The remaining terms are allowed total cost at most b. On assigning colours to edges, discard terms containing an opposite-colour edge and erase matching edges from the other masks. Charge empty masks immediately. A negative budget excludes the branch. If a singleton’s multiplicity exceeds the budget, its edge must have the opposite colour. Otherwise the checker branches on both colours of one undecided edge. It also recognizes a feasible constant-colour completion when all remaining terms of that colour fit the budget. Every branch fixes at least one new edge, so the search exhausts the possibilities. Infeasibility of these residual terms suffices, since the removed groups already cost at least p.

## Enumeration and reproduction

Index the blue edges by increasing length d and within each length by the start s of the edge {s,s+d}, with 0 ≤ s < 43. A shortest addition can be rotated to start 0. Its index f is then the least of the three indices and is a multiple of 43. Enumerating f < g < h for each such f covers every placement. This gives 352,395 normalized triples, counting possible repeats under symmetry. After the greedy test, the checker identifies congruent remaining triples by allowing both orientations and rotating each shortest edge in turn to start 0. Reflection changes start s to −s−d. The least sorted triple of indices is a representative. These maps preserve both initial colours and arbitrary deletions.

Run `python3 -B check.py` from this folder. The initial scan reaches 11 on 347,905 normalized triples. The remaining 4,490 reduce to 1,266 symmetry classes. On rerunning the greedy pass in the representative orientation, seven more reach 11. The residual decision procedure rejects the other 1,259 at a cap of 10. The script raises an error on any unresolved class. The upper witness and lower bound together establish the exact minimum.

The completed macOS run used Python 3.15.2, 39.82 CPU seconds and 21,250,048 bytes peak resident memory. Additional local checks compared the decision procedure with full truth tables on 300 small weighted instances and checked all 86 dihedral images of 60 sampled triples. The residual check rejected a cap of 10 and accepted 11 on the displayed witness’s symmetry class.

## Reviewer checks

1. Match the starting colour classes and both allowed directions of change against the local source. Recount both colours of the displayed witness.
2. Check disjointness of the reserved witnesses, the unreserved-witness forcing inequality, and the subtraction of selected red sets and blue singleton multiplicities.
3. Verify coverage by rotations, the reflected start formula, and the two branches of the residual decision procedure. Rerun the standalone standard-library Python script on the cluster.
4. Independent cluster replay and literature novelty review are pending. The computation is local and has no external data dependencies.
