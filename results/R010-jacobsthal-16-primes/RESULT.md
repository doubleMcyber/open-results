# Which moduli attain the 16-prime Jacobsthal maximum?

Entry 021, “A quadratic bound for Jacobsthal’s function”, occurs on line
290 of `INDEX.tsv`. The local source (`src/openai_math/CONTENTS.md`,
lines 570–579) defines the worst-case interval length over moduli with at
most $k$ distinct prime divisors. This follow-up determines which moduli
attain that worst case for each $k$ through 16. Novelty is UNVERIFIED.

## Theorem

Let $n$ be a positive integer with at most 16 distinct prime divisors.
Every interval of 106 consecutive integers contains an integer coprime to
$n$. An interval of 105 consecutive integers all sharing a factor with
$n$ exists if and only if the following three conditions hold.

1. $n$ has exactly 16 distinct prime divisors.
2. Every prime from 2 through 29 divides $n$.
3. At least two of 31, 37 and 43 divide $n$.

Thus, once a qualifying pair and the ten mandatory primes are fixed,
any four further distinct primes suffice. Prime exponents are arbitrary.
Call a set of at most $k$ primes sufficient if every choice of exactly $k$
prime divisors containing it attains the longest run possible for that $k$.
The first positive $k$ with more than one inclusion-minimal sufficient set
is 16.

## Witnesses for all three pairs

Let $M$ be the product of the primes through 29 and the indicated pair.
The last column lists every $j$ in $0\le j<105$ with $\gcd(a+j,M)=1$.
All entries can be checked using ordinary integer gcd.

| Pair | $M$ | $a$ | Surviving offsets $j$ |
|---|---:|---:|---|
| 31, 37 | 7420738134810 | 4783380817184 | 27, 47, 65, 99 |
| 31, 43 | 8624101075590 | 74651409074 | 39, 47, 65, 75 |
| 37, 43 | 10293281928930 | 2095238757854 | 39, 47, 53, 75 |

For the four remaining prime divisors choose a bijection $j\mapsto q_j$
from the surviving offsets. By the Chinese remainder theorem (CRT) there
is a positive $x\equiv a\pmod M$ satisfying $x\equiv-j\pmod {q_j}$ for
every survivor. Each $x+j$ in the interval now has a common prime factor
with $n$.

## Exhaustive upper bound and necessity

Fix a length $L$, a budget $k$, and an arbitrary set $P$ of exactly
$k$ primes. A run beginning at $x$ covers the offsets $0,\ldots,L-1$
by one class modulo each $p\in P$, namely $-x\bmod p$. Conversely any
choice of one class per prime is realized by CRT. Every prime $p\ge L$
can cover at most one offset, and it can cover any chosen one.

The script `check.py` processes every prime below $L$ in increasing order.
Its state consists of the next prime, uncovered offsets $U$, and the
tuple $S$ of primes already used. There are $b=k-|S|$ slots left.

* If $|U|\le b$, record $S$. Every $k$-prime set containing $S$
  suffices. Assign a distinct remaining prime to each uncovered position.
* For the next prime, branch over its classes that hit at least two
  currently uncovered offsets. Also branch over skipping the prime.
  To see completeness, follow any given cover in increasing prime order,
  taking its specified class whenever that class hits at least two.
  Every skipped prime of the cover then accounts for at most one final
  uncovered offset, since the uncovered set only shrinks. Once all small
  primes have been processed, there are enough free slots to finish.
* For early rejection, let $m_p$ be the largest number of offsets of
  $U$ lying in one class modulo each unprocessed prime $p<L$. Count
  one position per remaining slot. Each such prime can contribute at
  most $m_p-1$ more. If $b$ plus the sum of the largest $b$ of
  these nonnegative savings is less than $|U|$, this branch cannot finish.
  A skipped prime is available here only as a singleton. Overlaps between
  contributions only decrease the number covered.

Discard each recorded set that strictly contains another. The resulting
list characterizes every $P$. An $L$-run exists exactly when $P$
contains a set on the list. It also gives all inclusion-minimal sufficient
sets. Indeed, for any proposed sufficient set of at most $k$ primes,
fill its unassigned slots with fresh primes larger than $L$. Any list
member contained in this completion had to belong to the proposed set.

## Exact computation

Write $P_t$ for the first $t$ primes, with $P_0$ empty. Each row
gives the longest run $L$ and all inclusion-minimal sufficient sets at
that length. In every row the same search returned no set at $L+1$.
Any longer run would contain an $L+1$ subinterval.

| $k$ | $L$ | Minimal sufficient sets |
|---:|---:|---|
| 1 | 1 | $P_0$ |
| 2 | 3 | $P_1$ |
| 3 | 5 | $P_1$ |
| 4 | 9 | $P_2$ |
| 5 | 13 | $P_3$ |
| 6 | 21 | $P_4$ |
| 7 | 25 | $P_5$ |
| 8 | 33 | $P_6$ |
| 9 | 39 | $P_6$ |
| 10 | 45 | $P_8$ |
| 11 | 57 | $P_9$ |
| 12 | 65 | $P_9$ |
| 13 | 73 | $P_{11}$ |
| 14 | 89 | $P_9\cup\{31\}$ |
| 15 | 99 | $P_{12}$ |
| 16 | 105 | $P_{10}\cup T$, for each two-element $T\subset\{31,37,43\}$ |

The modulus $1$ has no positive-length run. Together with the rows
through 15 this accounts for every modulus with fewer than 16 primes.

## Second computation for $k=16$

`crosscheck.py` tests the exclusions by a different branching rule. With
2 absent, it rules out covering 105 positions using 16 slots. With 2
present, deleting its chosen parity class from 106 positions leaves 53
positions in a progression of step two. For 105 positions at least 52
remain. Since 2 is invertible modulo every odd prime, a class modulo an
odd prime restricts to one class on the consecutive progression indices.

The second search rules out 53 consecutive indices with 15 odd primes
and 52 with only 14. At length 52 with 15 odd primes, it rules out each
case omitting one of the nine mandatory odd primes or two of 31, 37 and
43. It also tests the three feasible pairs and the witness gcd values.

To decide coverability, the second search picks an uncovered offset.
Either its prime serves it alone or the prime also covers another
remaining offset. In the second case the prime divides their difference
and is smaller than the length. Choosing the prime fixes its class at the
pivot. Remove that entire class and spend one slot. The singleton case
may use a fresh prime larger than the length.

For pruning, sum the largest single-class capacities of distinct available
primes up to the slot limit, filling spare slots with capacity one. This
sum bounds coverage from above. If omitting the largest-capacity prime
already falls short, that prime is forced. Branch on its classes first.
It must cover at least two offsets, since a singleton could be replaced
by a fresh prime. This verifier uses Python sets and imports no code
from the main search.

On 2026-11-25 both scripts passed locally under Python 3.11.9 on macOS.
The main search used 8.96 CPU seconds and the second used 0.51 CPU seconds.
Each process peaked below 16 MiB of resident memory.

## Reviewer checks

1. Run `python3 -B check.py` in this folder. Verify the sufficient sets
   at $L$ and the empty lists at $L+1$ against the table.
2. Run `python3 -B crosscheck.py` for the witness gcd values and parity-based
   exclusions. Check the change of indices on the odd progression and the
   pairwise coprimality of the moduli in each use of CRT.
3. Check the skip branch for primes hitting at most one current offset,
   the direction of the savings bound and the argument allowing arbitrary
   large primes. These steps justify the exhaustive claim.
4. Check prior tables of extremal Jacobsthal coverings for the full
   equality classification, including whether they record all three
   sufficient sets at 16. Novelty, independent lead review and Lean
   verification are UNVERIFIED.
