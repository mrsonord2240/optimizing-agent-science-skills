"""INPUT 3 (edge, terminal overhangs): the fixed PID1-PID4 against pwalign::pid (R) on the auditor's own 169 real
pairwise alignments (b03_pid_pwalign.R), plus hand-computed cases.
V0 = pwalign's aligned strings exactly as returned (22 of them carry end gaps: global mode with terminal gaps).
     pwalign::pid PID3/PID4 use the FULL sequence lengths (probed in b03b_pid4_probe.py), which V0 rows do not contain
     for local/overlap alignments, so V0 compares PID1/PID2 on all pairs and PID3/PID4 only where no flank exists.
V1 = the same pair as MSA rows with the unaligned flanks STAGGERED in (pattern flank, then subject flank, in their own
     columns) - the situation msa-statistics meets when two rows of a real MSA overhang each other. PID1 and PID2 must
     equal pwalign's, and here (rows hold the full sequences) PID3/PID4 must equal pwalign's too.
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b03_pid_compare.py"""
import os, sys, math, json
import numpy as np, pandas as pd
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import identity_matrix as IM
import ref

RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')

df = pd.read_csv(os.path.join(HERE, 'data', 'derived', 'pid_pairs_R.tsv'), sep='\t', keep_default_na=False)
print(len(df), 'pairs;', df.name.str.split('|').str[0].value_counts().to_dict())

def mk(a, b):
    return MultipleSeqAlignment([SeqRecord(Seq(a), id='a'), SeqRecord(Seq(b), id='b')])

def skill_all(a, b):
    aln = mk(a, b)
    f = [IM.pairwise_identity(a, b, m) * 100 for m in IM.METHODS]
    v = [IM.identity_matrix_vectorized(aln, m)[0, 1] * 100 for m in IM.METHODS]
    return f, v

def flanks(full, aligned):
    # residues of `full` outside the ungapped aligned string (pwalign's start()/end() ranges EXCLUDE end-gap residues
    # that are still present in the aligned string, so locate the string itself instead)
    ung = aligned.replace('-', ''); i = full.find(ung)
    assert i >= 0
    return full[:i], full[i + len(ung):]

def stagger(r):
    pfl, ptl = flanks(r.pfull, r.a)
    sfl, stl = flanks(r.sfull, r.b)
    A = pfl + '-' * len(sfl) + r.a + ptl + '-' * len(stl)
    B = '-' * len(pfl) + sfl + r.b + '-' * len(ptl) + stl
    return A, B

# ---- V0 ----
worst0 = 0; bad0 = []; worst_fv = 0
old_style_diff = []
for r in df.itertuples():
    f, v = skill_all(r.a, r.b)
    R = [r.PID1, r.PID2, r.PID3, r.PID4]
    has_flank = any(flanks(r.pfull, r.a)) or any(flanks(r.sfull, r.b))
    cols = [0, 1] if has_flank else [0, 1, 2, 3]
    d = max(abs(f[k] - R[k]) for k in cols); worst0 = max(worst0, d)
    worst_fv = max(worst_fv, max(abs(x - y) for x, y in zip(f, v)))
    if d > 0.01: bad0.append((r.name, [round(x, 2) for x in f], [round(x, 2) for x in R]))
    # what the OLD denominator (any-residue column anywhere) would have given
    den_old = sum(x != '-' or y != '-' for x, y in zip(r.a, r.b)); n_id = sum(x == y and x != '-' for x, y in zip(r.a, r.b))
    old_style_diff.append(abs(100 * n_id / den_old - r.PID1))
check('V0: Skill PID1/PID2 (all 169) and PID3/PID4 (pairs without flank) == pwalign::pid within 0.01 pts', not bad0, f'max diff {worst0:.5f}; mismatches {bad0[:3]}')
check('V0: function == vectorized matrix on all 169 pairs and 4 methods', worst_fv < 1e-9, f'max diff {worst_fv:.1e}')
n_end = int(sum(1 for r in df.itertuples() if r.a[0] == '-' or r.a[-1] == '-' or r.b[0] == '-' or r.b[-1] == '-'))
n_old_wrong = int(sum(1 for x in old_style_diff if x > 0.01))
print(f'   pairs with end gaps inside the aligned strings: {n_end}; pairs where the OLD (pre-fix) any-residue denominator would differ from pwalign: {n_old_wrong} (max {max(old_style_diff):.2f} pts)')
check('V0: the test discriminates - old denominator would have disagreed with pwalign on >= 5 pairs', n_old_wrong >= 5, f'{n_old_wrong}')

# ---- V1 ----
flank = df[[any(flanks(r.pfull, r.a)) or any(flanks(r.sfull, r.b)) for r in df.itertuples()]]
worst1 = 0; bad1 = []; worst34 = 0; old1 = []
for r in flank.itertuples():
    A, B = stagger(r)
    f, v = skill_all(A, B)
    d12 = max(abs(f[0] - r.PID1), abs(f[1] - r.PID2), abs(f[2] - r.PID3), abs(f[3] - r.PID4)); worst1 = max(worst1, d12)
    n_id = sum(x == y and x != '-' for x, y in zip(r.a, r.b))
    la, lb = len(A.replace('-', '')), len(B.replace('-', ''))
    e3 = 100 * n_id / min(la, lb); e4 = 100 * n_id / ((la + lb) / 2)
    worst34 = max(worst34, abs(f[2] - e3), abs(f[3] - e4), max(abs(x - y) for x, y in zip(f, v)))
    if d12 > 0.01: bad1.append((r.name, [round(x, 2) for x in f], [r.PID1, r.PID2, r.PID3, r.PID4]))
    den_old = sum(x != '-' or y != '-' for x, y in zip(A, B)); old1.append(abs(100 * n_id / den_old - r.PID1))
check(f'V1: staggered flanks ({len(flank)} pairs): Skill PID1, PID2, PID3, PID4 == pwalign within 0.01', not bad1, f'max diff {worst1:.5f}; bad {bad1[:3]}')
check('V1: PID3/PID4 == formula with full ungapped lengths; function == vectorized', worst34 < 1e-9, f'max diff {worst34:.1e}')
check('V1: old denominator would have been wrong on most of them', sum(1 for x in old1 if x > 0.01) >= 0.6 * len(flank), f'{sum(1 for x in old1 if x > 0.01)} of {len(flank)}; max {max(old1):.1f} pts')

# ---- the per-sequence "internal gap" definition (ref.pid_ref) on the same V1 rows: where do the two definitions part? ----
part = 0
for r in flank.itertuples():
    A, B = stagger(r)
    part += abs(ref.pid_ref(A, B)['PID1'] * 100 - r.PID1) > 0.01
print(f'   per-sequence "internal gap" PID1 (ref.pid_ref) differs from pwalign on {part} of {len(flank)} staggered pairs (Skill span definition: 0)')

# ---- hand-computed (before running) ----
hand = [
  ('s1/s2 AC-DEF-- / -CGDEFHK', 'AC-DEF--', '-CGDEFHK', (80.0, 100.0, 80.0, 200 / 3)),
  ('no aligned pair  AC-- / --GT', 'AC--', '--GT', (float('nan'), float('nan'), 0.0, 0.0)),
  ('one column, mismatch  A / C', 'A', 'C', (0.0, 0.0, 0.0, 0.0)),
  ('internal gap both ways  AB-CD / A-XCD', 'AB-CD', 'A-XCD', (75.0, 75.0, 75.0, 75.0)),  # ident A,C,D=3; aligned 3?? recomputed below
]
# recompute the last by hand: cols A/A ident; B/- gap; -/X gap; C/C ident; D/D ident -> aligned 3, ident 3, internal gaps 2 -> PID1 3/5=60, PID2 3/3=100, PID3 3/4=75, PID4 3/4=75
hand[3] = ('internal gap in both rows  AB-CD / A-XCD', 'AB-CD', 'A-XCD', (60.0, 100.0, 75.0, 75.0))
hand.append(('terminal overhangs only  XXABC-- / --ABCYY', 'XXABC--', '--ABCYY', (100.0, 100.0, 60.0, 60.0)))   # ident 3, aligned 3, span ABC=3; lengths 5,5
hand.append(('all-gap row vs residues', 'AC', '--', (float('nan'),) * 4))
for name, a, b, exp in hand:
    f, v = skill_all(a, b)
    ok = all((math.isnan(x) and math.isnan(y)) or abs(x - y) < 1e-9 for x, y in zip(f, exp)) and all((math.isnan(x) and math.isnan(y)) or abs(x - y) < 1e-9 for x, y in zip(v, exp))
    check(f'hand {name}', ok, f'skill {[round(x, 2) for x in f]} expected {[round(x, 2) for x in exp]}')
json.dump({k: list(v) for k, v in RES.items()}, open(os.path.join(HERE, 'results_b03.json'), 'w'), indent=1)
print('\nSUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'checks PASS')
