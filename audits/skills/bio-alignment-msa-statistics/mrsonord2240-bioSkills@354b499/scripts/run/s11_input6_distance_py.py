"""INPUT 6 (Scope boundary) Python half: "I need distances for tree building from this protein alignment" ->
the Skill's DistanceCalculator('blosum62') snippet + kimura_protein_distance.py, checked against (a) a hand implementation of
Bio's blosum62 distance formula, (b) EMBOSS distmat (Kimura) from s10_wsl_distance_tools.sh, (c) IQ-TREE .mldist ordering sanity.
Run from run/ after s10."""
import os, sys, itertools, math, json
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
from Bio import AlignIO
from Bio.Align import substitution_matrices
from Bio.Phylo.TreeConstruction import DistanceCalculator
import kimura_protein_distance as KP
W = os.path.join(HERE, 'work_in6'); RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')

aln = AlignIO.read(os.path.join(W, 'alignment_aa.fasta'), 'fasta'); N = len(aln)
# --- verbatim SKILL.md snippet ---
calculator = DistanceCalculator('blosum62')
distance_matrix = calculator.get_distance(aln)
print('SKILL snippet ran; matrix shape', len(distance_matrix.names), 'names[0]=', distance_matrix.names[0])
# (a) hand implementation of Bio's formula: d = 1 - sum B[a,b] / max(sum B[a,a], sum B[b,b]) over ungapped columns
B = substitution_matrices.load('BLOSUM62')
def hand(a, b):
    s = m1 = m2 = 0
    for x, y in zip(a, b):
        if x in '-*' or y in '-*': continue
        s += B[x, y]; m1 += B[x, x]; m2 += B[y, y]
    return 1 - s / max(m1, m2)
mx = max(abs(hand(str(aln[i].seq), str(aln[j].seq)) - distance_matrix[i, j]) for i, j in itertools.combinations(range(N), 2))
check('V1 DistanceCalculator(blosum62) == hand formula (28 pairs)', mx < 1e-9, f'max diff {mx:.1e}')
# (b) Skill kimura vs EMBOSS distmat -protmethod 2
txt = [l for l in open(os.path.join(W, 'distmat_aa.txt')).read().splitlines() if '\t' in l and any(ch.isdigit() for ch in l)]
D = {}
for line in txt:
    toks = line.split()
    idx = int(toks[-1]); name = toks[-2]
    vals = [float(t) for t in toks[:-2]]
    i = idx - 1
    for k, v in enumerate(vals):
        D[(i, i + k)] = v / 100.0
diffs = []
for i, j in itertools.combinations(range(N), 2):
    sk = KP.kimura_protein_distance(str(aln[i].seq), str(aln[j].seq)); em = D[(i, j)]
    diffs.append((abs(sk - em) if np.isfinite(sk) else float('nan'), i, j, sk, em))
good = [d for d in diffs if np.isfinite(d[0])]
worst = max(good)
print(f'Skill Kimura vs EMBOSS distmat: {len(good)}/{len(diffs)} finite pairs, worst diff {worst[0]:.4f} at pair ({worst[1]},{worst[2]}): Skill {worst[3]:.4f} vs distmat {worst[4]:.4f}')
print('  pairs Skill calls saturated (inf):', sum(1 for d in diffs if not np.isfinite(d[3])), '; distmat values there:', [round(d[4], 3) for d in diffs if not np.isfinite(d[3])])
check('V2 Skill Kimura == EMBOSS distmat (finite pairs)', worst[0] < 0.01, f'max diff {worst[0]:.4f}')
# ordering sanity vs IQ-TREE LG mldist: closest pair must agree
ml = open(os.path.join(W, 'alignment_aa.fasta.mldist')).read().split('\n')[1:1 + N]
names = [l.split()[0] for l in ml]; M = np.array([[float(x) for x in l.split()[1:]] for l in ml])
iu = np.triu_indices(N, 1); k = np.argmin(M[iu]); print('IQ-TREE closest pair:', names[iu[0][k]], names[iu[1][k]], f'{M[iu][k]:.4f}')
kd = np.array([KP.kimura_protein_distance(str(aln[i].seq), str(aln[j].seq)) for i, j in zip(iu[0].tolist(), iu[1].tolist())])
kk = int(np.argmin(kd)); print('Skill Kimura closest pair:', names[iu[0][kk]], names[iu[1][kk]], f'{kd[kk]:.4f}')
check('V3 closest pair agrees with IQ-TREE LG distances', (iu[0][k], iu[1][k]) == (iu[0][kk], iu[1][kk]), '')
json.dump(RES, open(os.path.join(HERE, 'results_in6.json'), 'w'), indent=1)
print('SUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES))
