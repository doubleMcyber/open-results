Nine-input T-state factory, ideal acceptance 1/4. Balada Gaggioli and Marecek (arXiv:2610.31115, Proposition 7) give a nine-input stabilizer protocol with output error 27/2 p^2 + O(p^3) that accepts an ideal batch with probability 1/128. Applying an outcome-dependent Clifford correction instead of discarding nontrivial syndromes gives ideal acceptance 1/8 (four checks measured first) and 1/4 (a depth-five adaptive tree over symmetry images of the code), with the output error identical, as a rational function of p, to the published one. The correction principle is Bravyi and Kitaev 2005; the new part is its application to Proposition 7.

Cost: at p = 0.01 the tree needs 38.7 inputs per output, against 17.4 for Bravyi-Kitaev 15-to-1, so the gain is acceptance at the minimum input count, not a cheaper factory.

Upper bound: for nine inputs, independent Z faults and ideal Clifford operations, no protocol with quadratic suppression has ideal acceptance above 32407/65536 = 0.4945, so none reaches 1/2. This bound is computer-assisted, one implementation, not independently reproduced, not formalised. The exact values (1/128, 1/8, 1/4 and the error function) were computed in exact arithmetic by two implementations.

[RESULT.md](RESULT.md) has the construction, the proof parts and the rerun table. Run the scripts from this folder with numpy, sympy and numba.
