# The exact three-string ratio for maximum-overlap Greedy

## Question and statement

Physical row 393 of `out/INDEX.tsv` is OpenAI Math entry 128, *A factor-two approximation for shortest common superstring*. Its local abstract explicitly excludes classical maximum-overlap Greedy from its guarantee (`src/openai_math/chunks/c3.md`, lines 694–703). Both paths are relative to `~/dev/quantum/ideation/mine_20261125/`. This follow-up asks for the exact ratio on three strings, the first cardinality at which Greedy can lose.

Take three distinct nonempty strings, none a substring of another, of length at most \(L\). The directed overlap \(o(x,y)\) is the length of the longest suffix of \(x\) equal to a prefix of \(y\), allowing zero. Greedy chooses an ordered pair of distinct strings with maximum overlap, merges them with that overlap, then takes a shortest superstring of the two remaining strings. Ties may be resolved arbitrarily. Let \(T\) be the optimal length and \(G\) the Greedy length.

For integers \(L\ge1\) and \(0\le k\le L-1\), require that the chosen first overlap exceed or equal **each of the other five overlaps plus \(k\)**. The exact worst-case ratio over eligible inputs and choices, on any alphabet of at least three symbols, is

\[
\max G/T=1+\frac{\max(0,L-1-2k)}{L+k+2}.
\]

In particular, arbitrary ties give \((2L+1)/(L+2)\). For \(L\ge2\) a binary example already attains this value. A unique first choice corresponds to \(k=1\), giving \(2L/(L+3)\) for \(L\ge3\). If \(2k\ge L-1\), every eligible choice is optimal.

The same examples also attain the sharp additive loss \(\max(G-T)=\max(0,L-1-2k)\).

## Upper bound

Write \(x,y\) for the chosen ordered pair, \(z\) for the third string, \(a=o(x,y)\), and \(S=|x|+|y|+|z|\). All overlaps are proper in both words by substring-freeness. In particular \(a\le L-1\).

For two substring-free words, a shortest superstring merges the better of their two directed overlaps, as one sees by ordering their occurrences. This also describes the second Greedy step here. Indeed, if \(z\) occurred in the first merge, it would have to start before the start of \(y\) and end after the end of \(x\), since neither input contains it. The suffix of \(x\) starting there would be a prefix of \(z\) longer than \(a\), contradicting maximality. The first merge cannot occur inside \(z\) either, since it contains \(x\).

For an ordering of the three words let \(u,v\) be its two consecutive directed overlaps. Merging in order realizes length \(S-u-v\), since each partial merge ends with the entire word just appended. Conversely, choose an occurrence of each word in a shortest superstring and sort by start. Ends occur in the same strict order by substring-freeness. Each consecutive pair intersects in at most its directed overlap, and gaps only increase the span. Thus \(T\) is the minimum of \(S-u-v\) over the six orders. This argument allows a triple intersection.

Fix a minimizing order. If it uses the directed edge \(x\to y\), the merged word starts with \(x\) and ends with \(y\). Greedy's second step can therefore realize that ordering at its optimum length. Assume henceforth \(D=G-T>0\). The minimizing order omits \(x\to y\), so \(u,v\le a-k\). Greedy can always concatenate after its first merge, hence

\[
D\le(S-a)-(S-u-v)=u+v-a\le a-2k.
\]

Let \(m=\min(u,v)\) and \(M=\max(u,v)\). Each chosen endpoint word has length at least \(a+1\). The word \(z\) is incident to at least one overlap in the minimizing order, so \(|z|\ge m+1\). Consequently

\[
T=S-u-v\ge 2(a+1)+(m+1)-(M+m)=2a+3-M\ge a+k+3.
\]

Thus \(D/T\le (a-2k)/(a+k+3)\). This fraction is \(1-(3k+3)/(a+k+3)\), increasing in \(a\). Substituting \(L-1\) proves the upper bound. The case \(D=0\) is immediate.

## Sharp examples

Put \(a=L-1\). If \(a\le2k\), the bound is one. The triple \(0^L,0^{L-1}1,2\) has a first overlap of \(a\) and all five alternatives zero, so the eligible class is nonempty even at \(L=1\).

Now let \(a>2k\), put \(m=a-k\), and take the infinite periodic binary word \(W=(0^k1)^\infty\), indexed from zero. Write \(P=W[0:a]\) and \(Q=W[k:a+1]\) with half-open intervals. Choose a third symbol \(\#\) and set

\[
x=\#P,\qquad y=P\#,\qquad z=Q.
\]

Here \(|P|=a\) and \(|Q|=m+1\le L\). The first symbol of \(Q\) is 1, occurring only at indices congruent to \(k\) modulo \(k+1\). Its earliest possible occurrence in \(P\) starts at \(k\) and would end one symbol beyond \(P\). Thus \(Q\) occurs in neither marked word. The two distinct marked words have equal length, and neither can occur in \(Q\).

The six directed overlaps are as follows.

| edge | \(x\to y\) | \(x\to z\) | \(z\to y\) | \(y\to x\) | \(y\to z\) | \(z\to x\) |
|---|---:|---:|---:|---:|---:|---:|
| length | \(a\) | \(m\) | \(m\) | 1 | 0 | 0 |

For the two entries \(m\), the first \(m\) letters of \(Q\) end \(P\), and the last \(m\) letters of \(Q\) start at period boundary \(k+1\) in \(W\). An overlap of length \(m+1\) would contain all of \(Q\). The marker forces the last three entries. Since \(m\ge1\), the first choice \(x\to y\) has margin exactly \(k\).

The merge is \(\#P\#\), which neither contains nor overlaps \(Q\) in either direction. Hence \(G=(a+2)+(m+1)=2a-k+3\). Among orders using \(x\to y\), the total saving is \(a\). Among the others it is at most \(2m\), attained by \(x,z,y\). Since \(2m>a\), we get \(T=S-2m=a+k+3\). This gives equality. For \(k=0\) the construction uses only 1 and the marker.

For example, take \(L=4,k=1\). The unique first merge of `#010` and `010#` produces `#010#`, and appending `101` gives length 8. The optimal word `#01010#` has length 7 and places `101` between the other two occurrences.

## Verification and review

The script enumerates all substring-free unordered triples up to each stated cap and every first tie. For each triple it computes \(T\) by breadth-first search over letters. A state records which input words have occurred and the longest suffix of the current text that is a prefix of some input word. When a letter is appended, every newly completed word ends in that suffix. Keeping the suffix therefore preserves all future transitions, and the first state with all three words seen gives the shortest length.

| Alphabet | Length cap | Triples | First choices | Worst \(G/T\) by minimum margin \(k=0,1,\ldots,L-1\) |
|---|---:|---:|---:|---|
| Binary | 5 | 19,984 | 31,446 | 11/7, 11/9, 1, 1, 1 |
| Ternary | 4 | 216,769 | 387,336 | 3/2, 8/7, 1, 1 |

The oracle also checked the constructed witnesses for all 300 pairs \(1\le L\le24\), \(0\le k<L\). At \(L=5,k=1\) the binary maximum \(11/9\) lies strictly below the ternary value \(5/4\). The run exited successfully on 2026-11-25 (PST) with Python 3.11.9 on arm64 macOS, using 17.38 CPU seconds and 20,168,704 bytes peak RSS. The finite checks support the proof. Its inequalities and periodic construction cover all lengths.

The proof addresses exactly three substring-free inputs and every permitted first choice. The unrestricted Greedy question for arbitrary input cardinality remains open in this work. Novelty is UNVERIFIED. There is no Lean formalization or independent cluster check.

Reviewer checks:

1. Check the source pointer, the direction of overlaps, the minimum-margin convention, and the treatment of ties.
2. Check the ordered-occurrence proof when all three occurrences intersect, and the lower bound on \(|z|\) when \(z\) is an endpoint.
3. Check the periodic witness at \(k=0\), at \(a=2k+1\), and the zero-loss example at \(L=1\).
4. Re-run `python3 check.py` from this folder. Its shortest-superstring oracle searches words independently of the six-order argument. Search prior work before attributing novelty.
