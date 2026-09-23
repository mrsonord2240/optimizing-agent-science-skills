"""Probe: what does Easel's pb weighting actually compute? pyhmmer docstring + numeric variants vs pyhmmer output on the REAL Pfam seed."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, pyhmmer
from common import *
print((pyhmmer.easel.MSA.compute_weights.__doc__ or '')[:1800])
with pyhmmer.easel.MSAFile(PFAM_STO, digital=True) as f:
    msa = f.read()
pb = np.array(msa.compute_weights(method='pb'), dtype=float)
print('pb sum', pb.sum(), 'min', pb.min(), 'max', pb.max())
# raw text parse (independent of Biopython): sequences from the Stockholm text
seqs = {}
for line in open(PFAM_STO, encoding='utf-8'):
    if line.startswith('#') or line.startswith('//') or not line.strip(): continue
    n, s = line.split(); seqs[n] = s
names = [n for n in seqs]
arr = np.array([list(seqs[n].upper()) for n in names])
isgap = np.isin(arr, ['-', '.', '_', '~'])
N, L = arr.shape
def weights(use_cols, divide, cons_frac=None):
    w = np.zeros(N)
    rl = (~isgap).sum(1)
    for c in range(L):
        col = arr[:, c]; res = col[~isgap[:, c]]
        if len(res) == 0: continue
        if cons_frac is not None and len(res) / N < cons_frac: continue
        u, cnt = np.unique(res, return_counts=True)
        d = dict(zip(u, cnt)); nd = len(u)
        for i in range(N):
            if not isgap[i, c]: w[i] += 1.0 / (nd * d[col[i]])
    if divide: w = w / rl
    return w * N / w.sum()
for label, kw in [('all cols, no divide', dict(use_cols=None, divide=False)), ('all cols, /rlen', dict(use_cols=None, divide=True)),
                  ('cons>=0.5, no divide', dict(use_cols=None, divide=False, cons_frac=0.5)), ('cons>=0.5, /rlen', dict(use_cols=None, divide=True, cons_frac=0.5))]:
    w = weights(**kw)
    print(f'{label:24s} max abs diff vs pyhmmer pb (sum-to-N units): {np.abs(w-pb).max():.6f}')
