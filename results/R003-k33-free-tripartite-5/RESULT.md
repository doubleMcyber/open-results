# The tripartite Zarankiewicz number on three parts of size five

**Theorem.** A simple tripartite graph with five vertices in each part and no
copy of the complete bipartite graph $K_{3,3}$ has at most 49 edges. There is
such a graph with 49 edges. Copies are ordinary subgraphs, so additional edges
among their six vertices are allowed.

This is a finite follow-up to INDEX.tsv row 40, arXiv 2608.11554, “Tripartite
Zarankiewicz numbers and norm graphs.” Its local abstract gives the asymptotic
value of the same extremal function. The result here is
$\operatorname{ex}(5,5,5,K_{3,3})=49$. Novelty is UNVERIFIED.

## Upper bound

Fix one part $A$. For each of the ten vertices $v$ outside $A$, let
$d_v$ count its neighbors in $A$, and put $D_A=\sum_v d_v$.
Every triple in $A$ has at most two common neighbors, since any three
common neighbors would complete a $K_{3,3}$. Counting pairs consisting of
a triple and a common neighbor gives

$$
\sum_{v\notin A}\binom{d_v}{3}\le 2\binom{5}{3}=20.
$$

For the integers $d=0,1,2,3,4,5$, the values of
$\binom d3-(3d-8)$ are $8,5,2,0,0,3$, respectively. Consequently
$3D_A-80\le20$, so $D_A\le33$ by integrality. The same holds for the
other two parts. Each edge is incident with two parts, whence
$2|E|=D_A+D_B+D_C\le99$ and $|E|\le49$.

## Construction

Number the vertices in each part from 0 to 4. Each column below lists the
rows of one adjacency matrix. A 1 joins the indicated row vertex in the first
part to the column vertex in the second part. The last block goes from C to A.

| Row | A to B | B to C | C to A |
|---:|:---:|:---:|:---:|
| 0 | 10101 | 10101 | 10101 |
| 1 | 11011 | 10110 | 11100 |
| 2 | 01110 | 11010 | 01111 |
| 3 | 11100 | 01111 | 11011 |
| 4 | 00111 | 10011 | 10110 |

The blocks contain 16, 16, and 17 edges. For a hand check, the common-neighbor
counts for the ten triples in each part, in lexicographic order, are

| Part | Counts |
|:---:|:---|
| A | 1 2 2 2 2 2 2 2 2 2 |
| B | 2 2 2 0 2 2 2 2 2 2 |
| C | 1 2 2 2 2 2 2 2 2 2 |

In a tripartite graph the two sides of a complete bipartite subgraph use
disjoint sets of parts. Thus at least one side of any $K_{3,3}$ lies wholly
in one part. The table rules out such a side. The accompanying script also
checks all $\binom{15}{3}=455$ triples directly. Running it locally under Python 3.11.9 gave 159 triples
with zero common neighbors, 161 with one, and 135 with two.

## Handoff 2026-11-25

1. Reproduce the certificate from this folder with
   `python3 check.py`. Use ordinary Python with
   assertions enabled. Check the three transcribed matrices against the table.
2. Audit the triple double count, its per-part integer rounding, and the final
   division by two. The upper bound applies to all graphs on these parts.
3. Check the full paper and finite tripartite Zarankiewicz literature before
   claiming priority. Only the local abstract was available for this source.
