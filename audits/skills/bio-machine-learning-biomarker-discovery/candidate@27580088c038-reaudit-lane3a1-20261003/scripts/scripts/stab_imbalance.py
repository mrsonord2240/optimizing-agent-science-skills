"""Imbalanced labels: subsamples are not stratified; does stability_selection fail loudly or silently? Usage: python stab_imbalance.py <Skill dir>"""
import sys, os
sys.dont_write_bytecode = True
import numpy as np
sys.path.insert(0, os.path.join(sys.argv[1], 'scripts'))
from stability_selection import stability_selection
for npos in (20, 8, 4, 2):
    r = np.random.default_rng(0); n, p = 72, 300; X = r.normal(size=(n, p)); y = np.zeros(n, int); y[:npos] = 1; X[:npos, :3] += 2
    try:
        f, s = stability_selection(X, y, q=7, seed=0); print(f'npos={npos}: ok stable={np.flatnonzero(f>.6).tolist()} nogueira={s:.2f}')
    except Exception as e:
        print(f'npos={npos}: {type(e).__name__}: {str(e)[:120]}')
