"""Strong planted signal (beta=2.5 on 5 of 2000 features, n=120): recovery vs false stable, raw and rescaled. Usage: python -W error::FutureWarning stab_planted_strong.py <Skill dir>"""
import sys, os
sys.dont_write_bytecode = True
import numpy as np
sys.path.insert(0, os.path.join(sys.argv[1], 'scripts'))
from stability_selection import stability_selection
n, p, pi = 120, 2000, 0.6; q = int(np.sqrt(1 * (2*pi-1) * p))
for d in range(6):
    r = np.random.default_rng(4000+d); X = r.normal(size=(n, p)); beta = np.zeros(p); beta[:5] = 2.5
    lg = X @ beta + r.normal(size=n); y = (lg > np.median(lg)).astype(int)
    f, s = stability_selection(X, y, q=q, seed=0); st = np.flatnonzero(f > pi)
    u = np.exp(np.random.default_rng(d).normal(0, 2, p)); fu, _ = stability_selection(X * u + 5, y, q=q, seed=0)
    fp, _ = stability_selection(X, np.random.default_rng(d).permutation(y), q=q, seed=0)
    print(f'STRONG draw{d}: recovered {(st<5).sum()}/5 false {(st>=5).sum()} stable={st.tolist()} nogueira={s:.2f} | rescaled same set={set(st)==set(np.flatnonzero(fu>pi))} maxdiff={np.abs(f-fu).max():.2f} | permuted-label stable={(fp>pi).sum()} max={fp.max():.2f}', flush=True)
