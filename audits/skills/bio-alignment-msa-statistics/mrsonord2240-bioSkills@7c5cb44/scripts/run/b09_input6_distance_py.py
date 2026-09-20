"""INPUT 6 (Scope boundary) Python half: "I need distances for tree building from this protein alignment" ->
the Skill's DistanceCalculator('blosum62') snippet (SKILL.md block, run verbatim after the normalising import) and
kimura_protein_distance.py, checked against (a) a hand implementation of Bio's blosum62 distance formula,
(b) EMBOSS distmat -protmethod 2 (Kimura) from b09_wsl_distance_tools.sh, (c) IQ-TREE LG .mldist closest pair,
(d) scope: the Skill sends publication-grade work to ModelTest-NG / IQ-TREE and says hand-coded models are exploratory.
Run from run/ after b09_wsl_distance_tools.sh."""
import os, sys, itertools, json, re
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
from Bio.Align import substitution_matrices
from Bio.Phylo.TreeConstruction import DistanceCalculator
import kimura_protein_distance as KP, msa_utils
W = os.path.join(HERE, 'work_b09'); RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')

aln = msa_utils.load_alignment(os.path.join(W, 'alignment_aa.fasta')); N = len(aln)
calculator = DistanceCalculator('blosum62')          # SKILL.md snippet, verbatim
distance_matrix = calculator.get_distance(aln)
print('SKILL snippet ran; matrix names', len(distance_matrix.names))
B = substitution_matrices.load('BLOSUM62')
def hand(a, b):
    s = m1 = m2 = 0
    for x, y in zip(a, b):
        if x in '-*' or y in '-*': continue
        s += B[x, y]; m1 += B[x, x]; m2 += B[y, y]
    return 1 - s / max(m1, m2)
mx = max(abs(hand(str(aln[i].seq), str(aln[j].seq)) - distance_matrix[i, j]) for i, j in itertools.combinations(range(N), 2))
check('V1 DistanceCalculator(blosum62) == hand formula (28 pairs)', mx < 1e-9, f'max diff {mx:.1e}')
# EMBOSS distmat parse: rows "v v v ... \t name idx"; values are distance x 100
D = {}
for line in open(os.path.join(W, 'distmat_aa.txt')).read().splitlines():
    m = re.match(r'^[\s\t]*([-\d.\s\t]+)\t+(\S+)\s+(\d+)\s*$', line)
    if m and '\t' in line:
        vals = [float(t) for t in m.group(1).split()]; i = int(m.group(3)) - 1
        for k, v in enumerate(vals):
            D[(i, i + k)] = v / 100.0
diffs = []
for i, j in itertools.combinations(range(N), 2):
    sk = KP.kimura_protein_distance(str(aln[i].seq), str(aln[j].seq)); em = D[(i, j)]
    diffs.append((abs(sk - em) if np.isfinite(sk) else float('nan'), i, j, sk, em))
good = [d for d in diffs if np.isfinite(d[0])]; worst = max(good)
print(f'Skill Kimura vs EMBOSS distmat: {len(good)}/{len(diffs)} finite pairs, worst diff {worst[0]:.5f}: Skill {worst[3]:.4f} vs distmat {worst[4]:.4f}')
check('V2 Skill Kimura == EMBOSS distmat (finite pairs, 28/28)', worst[0] < 0.01 and len(good) == 28 and len(D) >= 28, f'max diff {worst[0]:.5f}; {len(good)} finite')
ml = open(os.path.join(W, 'alignment_aa.fasta.mldist')).read().split('\n')[1:1 + N]
names = [l.split()[0] for l in ml]; M = np.array([[float(x) for x in l.split()[1:]] for l in ml])
iu = np.triu_indices(N, 1); k = int(np.argmin(M[iu]))
kd = np.array([KP.kimura_protein_distance(str(aln[i].seq), str(aln[j].seq)) for i, j in zip(iu[0].tolist(), iu[1].tolist())])
kk = int(np.argmin(kd))
check('V3 closest pair (Skill Kimura) == closest pair in IQ-TREE LG .mldist', (iu[0][k], iu[1][k]) == (iu[0][kk], iu[1][kk]), f'{names[iu[0][k]]} / {names[iu[1][k]]}')
mt_nt = open(os.path.join(W, 'mt_nt.log')).read(); mt_aa = open(os.path.join(W, 'mt_aa.log')).read()
check('V4 modeltest-ng commands from SKILL.md produced a best model (nt K80+I by BIC, aa DAYHOFF+G4 by BIC)', re.search(r'BIC\s+K80\+I\s+2658', mt_nt) is not None and re.search(r'BIC\s+DAYHOFF\+G4\s+3268', mt_aa) is not None, '')
md = open(os.path.join(HERE, 'skill', 'SKILL.md'), encoding='utf-8').read()
check('V5 scope: SKILL.md says NOT to pick a model by rule of thumb, routes to ModelTest-NG + IQ-TREE/distmat, DistanceCalculator only exploratory', 'do NOT pick a model by rule of thumb' in md and 'ModelTest-NG' in md and 'only for exploratory work' in md, '')
json.dump({k: list(v) for k, v in RES.items()}, open(os.path.join(HERE, 'results_b09.json'), 'w'), indent=1)
print('SUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES))
