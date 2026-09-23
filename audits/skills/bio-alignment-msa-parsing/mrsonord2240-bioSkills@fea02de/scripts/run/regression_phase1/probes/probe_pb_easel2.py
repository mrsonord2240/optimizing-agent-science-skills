"""Probe 2: try to reproduce Easel pb exactly (canonical residues only, consensus columns by n/(n+m)>=0.5, fragments)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, pyhmmer
from common import *
with pyhmmer.easel.MSAFile(PFAM_STO, digital=True) as f:
    msa = f.read()
pb = np.array(msa.compute_weights(method='pb'), dtype=float)
seqs = {}
for line in open(PFAM_STO, encoding='utf-8'):
    if line.startswith('#') or line.startswith('//') or not line.strip(): continue
    n, s = line.split(); seqs[n] = s
arr = np.array([list(s.upper()) for s in seqs.values()])
N, L = arr.shape
canon = set('ACDEFGHIKLMNPQRSTVWY')
iscan = np.vectorize(lambda c: c in canon)(arr)
isres = np.isin(arr, ['-', '.', '_', '~'], invert=True)     # residue incl degenerate
def run(cons_mode, rl_mode, frag):
    # consensus column: residues / (residues+gaps)
    frac = isres.sum(0) / N
    cons = frac >= 0.5
    w = np.zeros(N)
    for c in range(L):
        if cons_mode == 'cons' and not cons[c]: continue
        col = arr[:, c]; m = iscan[:, c]
        u, cnt = np.unique(col[m], return_counts=True)
        if len(u) == 0: continue
        d = dict(zip(u, cnt))
        for i in np.where(m)[0]: w[i] += 1.0 / (len(u) * d[col[i]])
    rl = {'canon_all': iscan.sum(1), 'canon_cons': iscan[:, cons].sum(1), 'res_all': isres.sum(1)}[rl_mode]
    w = w / rl
    return w * N / w.sum()
for cm in ('cons', 'all'):
    for rm in ('canon_all', 'canon_cons', 'res_all'):
        w = run(cm, rm, False)
        print(f'{cm:5s} {rm:11s} max abs diff {np.abs(w - pb).max():.6f}  spearman-ish corr {np.corrcoef(w, pb)[0,1]:.4f}')
