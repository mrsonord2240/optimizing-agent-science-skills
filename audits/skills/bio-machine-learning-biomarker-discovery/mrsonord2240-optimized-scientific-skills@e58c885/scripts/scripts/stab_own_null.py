"""Independent null/planted/invariance/determinism test of scripts/stability_selection.py on self-built synthetic data.
Usage: python -W error::FutureWarning stab_own_null.py <Skill dir>"""
import sys, os, time
sys.dont_write_bytecode = True
import numpy as np
sys.path.insert(0, os.path.join(sys.argv[1], 'scripts'))
from stability_selection import stability_selection
pi, EV = 0.6, 1
def q_of(p): return int(np.sqrt(EV * (2*pi-1) * p))
n, p = 100, 2000; q = q_of(p); print(f'n={n} p={p} q={q}', flush=True)
# 1. pure-noise features, pure-noise labels: false stable count over 8 independent draws
fs = []
for d in range(8):
    r = np.random.default_rng(1000+d); X = r.normal(size=(n, p)); y = r.integers(0, 2, n)
    f, s = stability_selection(X, y, q=q, seed=0); fs.append(int((f > pi).sum()))
    print(f'NOISE draw{d}: stable={fs[-1]} maxfreq={f.max():.2f}', flush=True)
print('NOISE SUMMARY: stable counts', fs, 'mean', np.mean(fs), 'expected bound EV =', EV)
# 2. planted: 5 true features among 2000, 6 draws; recovered / false stable
rec = []; fal = []
for d in range(6):
    r = np.random.default_rng(2000+d); X = r.normal(size=(n, p))
    lg = X[:, :5].sum(1) * 1.0 + r.normal(size=n); y = (lg > 0).astype(int)
    f, s = stability_selection(X, y, q=q, seed=0); st = np.flatnonzero(f > pi)
    rec.append(int((st < 5).sum())); fal.append(int((st >= 5).sum()))
    print(f'PLANTED draw{d}: recovered {rec[-1]}/5 false {fal[-1]} stable={st.tolist()} nogueira={s:.2f}', flush=True)
    # permuted labels of the same planted data
    f0, _ = stability_selection(X, np.random.default_rng(3000+d).permutation(y), q=q, seed=0)
    print(f'   permuted-label null of this draw: stable={int((f0>pi).sum())} maxfreq={f0.max():.2f}', flush=True)
print('PLANTED SUMMARY recovered', rec, 'false', fal)
# 3. unit invariance on planted draw 0
r = np.random.default_rng(2000); X = r.normal(size=(n, p)); lg = X[:, :5].sum(1) + r.normal(size=n); y = (lg > 0).astype(int)
units = np.exp(np.random.default_rng(5).normal(0, 2, p))
fr, _ = stability_selection(X, y, q=q, seed=0)
fz, _ = stability_selection((X - X.mean(0)) / X.std(0), y, q=q, seed=0)
fu, _ = stability_selection(X * units + 5, y, q=q, seed=0)
fk, _ = stability_selection(X * 1000.0, y, q=q, seed=0)
for nm, ff in (('standardized', fz), ('rescaled exp(N(0,2))*X+5', fu), ('x1000', fk)):
    print(f'INVARIANCE raw vs {nm}: maxdiff freq={np.abs(fr-ff).max():.2f} stable sets equal={set(np.flatnonzero(fr>pi))==set(np.flatnonzero(ff>pi))}', flush=True)
# 4. determinism
a, sa = stability_selection(X, y, q=q, seed=0); b, sb = stability_selection(X, y, q=q, seed=0); c, sc = stability_selection(X, y, q=q, seed=7)
print(f'DETERMINISM seed0 twice identical={np.array_equal(a,b) and sa==sb}; seed0 vs seed7 differ={not np.array_equal(a,c)} maxdiff={np.abs(a-c).max():.2f}')
# 5. degenerate: q=0 -> nothing selected -> NaN index (documented guard); constant column ok
f, s = stability_selection(X, y, q=0, seed=0); print(f'DEGENERATE q=0: stable={int((f>pi).sum())} nogueira={s}')
Xc = X.copy(); Xc[:, 7] = 3.0; f, s = stability_selection(Xc, y, q=q, seed=0); print(f'CONSTANT COLUMN: freq[7]={f[7]} nogueira={s:.2f}')
# 6. standardization is per-subsample: a feature whose scale differs hugely between halves must not change the result vs ground truth permutation -> checked via invariance above
