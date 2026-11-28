"""Check the [[162,8,17]] code of this entry, except the lower bound d >= 17.

Standard library only:  python3 -I verify.py            (checks, writes results/verify.txt)
                        python3 -I verify.py --write-data   (also regenerates data/H_X.txt, data/H_Z.txt)

Group C27 x C3 = <x> x <y>; the element x^i y^j has index 3*i + j. For a set P of group elements,
M(P) is the 81 x 81 matrix with M(P)[s*g, g] = 1 for s in P. H_X = (M(A) | M(B)) and
H_Z = (M(B)^T | M(A)^T). Qubits 0..80 are the left block, 81..161 the right block.
Rows are held as Python integers, bit q = qubit q.
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
L, M = 27, 3
O, N = L * M, 2 * L * M
A = [(0, 0), (1, 0), (5, 0)]                  # 1 + x + x^5
B = [(0, 0), (1, 1), (4, 2), (15, 1)]         # 1 + x y + x^4 y^2 + x^15 y
D = 17

lines = []
failed = []


def say(text):
    lines.append(text)
    print(text)


def check(name, ok, detail=''):
    say('%-4s %s%s' % ('ok' if ok else 'FAIL', name, ': ' + detail if detail else ''))
    if not ok:
        failed.append(name)


def shift(g, t, sign):
    """Index of g * t^sign."""
    i, j = divmod(g, M)
    return ((i + sign * t[0]) % L) * M + (j + sign * t[1]) % M


def bits(qubits):
    v = 0
    for q in qubits:
        v ^= 1 << q
    return v


def weight(v):
    return bin(v).count('1')


def rank(rows):
    pivots = {}
    for v in rows:
        while v:
            h = v.bit_length() - 1
            if h not in pivots:
                pivots[h] = v
                break
            v ^= pivots[h]
    return len(pivots)


def commutes(v, rows):
    return all(weight(v & r) % 2 == 0 for r in rows)


def text(rows):
    return ''.join(''.join('1' if r >> q & 1 else '0' for q in range(N)) + '\n' for r in rows)


def main():
    hx = [bits([shift(r, s, -1) for s in A] + [O + shift(r, t, -1) for t in B]) for r in range(O)]
    hz = [bits([shift(r, t, 1) for t in B] + [O + shift(r, s, 1) for s in A]) for r in range(O)]
    H = {'X': hx, 'Z': hz}

    say('[[162,8,17]] two-block group-algebra code over C27 x C3')
    say('A = 1 + x + x^5,  B = 1 + x y + x^4 y^2 + x^15 y')
    say('')
    if '--write-data' in sys.argv[1:]:
        (HERE / 'data').mkdir(exist_ok=True)
        for s in 'XZ':
            (HERE / 'data' / ('H_%s.txt' % s)).write_text(text(H[s]))
    for s in 'XZ':
        path = HERE / 'data' / ('H_%s.txt' % s)
        check('data/H_%s.txt equals the matrix built from A and B' % s,
              path.is_file() and path.read_text() == text(H[s]))

    check('n = 162', N == 162 and all(len(h) == 81 and all(r >> N == 0 for r in h) for h in H.values()),
          'H_X and H_Z are 81 x 162')
    for s in 'XZ':
        rw = sorted({weight(r) for r in H[s]})
        cw = [sum(r >> q & 1 for r in H[s]) for q in range(N)]
        check('every row of H_%s has weight 7' % s, rw == [7], 'row weights %s' % rw)
        check('column weights of H_%s are 3 and 4' % s, cw.count(3) == 81 and cw.count(4) == 81,
              '%d columns of weight 3, %d of weight 4' % (cw.count(3), cw.count(4)))
    check('H_X H_Z^T = 0 over GF(2)', all(commutes(r, hz) for r in hx), '81 x 81 row pairs')
    rx, rz = rank(hx), rank(hz)
    k = N - rx - rz
    check('k = 8', k == 8, 'rank H_X = %d, rank H_Z = %d, k = 162 - %d - %d = %d' % (rx, rz, rx, rz, k))

    say('')
    witnesses = json.loads((HERE / 'data' / 'witnesses.json').read_text())
    check('both sectors have a witness', {w['sector'] for w in witnesses} == {'X', 'Z'})
    for w in witnesses:
        s, sup = w['sector'], w['support']
        other = 'Z' if s == 'X' else 'X'
        v = bits(sup)
        tag = '%s witness (%s)' % (s, w['source'])
        check(tag + ' has weight 17', len(set(sup)) == len(sup) == D == weight(v)
              and all(0 <= q < N for q in sup), 'weight %d' % weight(v))
        check(tag + ' commutes with every row of H_%s' % other, commutes(v, H[other]))
        r0, r1 = rank(H[s]), rank(H[s] + [v])
        check(tag + ' is not in the row space of H_%s' % s, r1 == r0 + 1, 'rank %d -> %d' % (r0, r1))

    say('')
    say('Controls on the checks themselves (each must be detected):')
    for s in 'XZ':
        other = 'Z' if s == 'X' else 'X'
        v = bits(next(w['support'] for w in witnesses if w['sector'] == s))
        stab = H[s][0] ^ H[s][1]
        check('%s: a stabilizer is reported inside the row space' % s,
              commutes(stab, H[other]) and rank(H[s] + [stab]) == rank(H[s]))
        check('%s: a witness with one qubit flipped fails to commute' % s,
              not any(commutes(v ^ (1 << q), H[other]) for q in range(N)), 'all 162 single flips')

    say('')
    say('Link to the original certification logs (they number the group elements differently):')
    col = json.loads((HERE / 'data' / 'log_labelling.json').read_text())['log_column']
    record = json.loads((HERE / 'results' / 'exact' / 'original_record1.json').read_text())
    check('the relabelling is a permutation that keeps the two blocks',
          sorted(col) == list(range(N)) and all((c < O) == (q < O) for q, c in enumerate(col)))
    for s in 'XZ':
        mine = next(w['support'] for w in witnesses
                    if w['source'] == 'certification run' and w['sector'] == s)
        check('%s witness of the certification record maps to the published one' % s,
              sorted(col[q] for q in mine) == sorted(record['witness_' + s]))

    say('')
    fom = Fraction(k * D * D, N)
    say('k d^2 / n at d = 17: %s = %.4f; frozen-table value 96/7 = %.4f' % (fom, fom, Fraction(96, 7)))
    check('k d^2 / n at d = 17 exceeds 96/7', fom > Fraction(96, 7))
    say('')
    say('NOT checked here: d >= 17 (no nontrivial logical of weight <= 16). See results/RERUN.md.')
    say('The witnesses above give d_X <= 17 and d_Z <= 17.')
    say('RESULT: %s' % ('ALL CHECKS PASSED' if not failed else '%d CHECK(S) FAILED' % len(failed)))
    (HERE / 'results' / 'verify.txt').write_text('\n'.join(lines) + '\n')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
