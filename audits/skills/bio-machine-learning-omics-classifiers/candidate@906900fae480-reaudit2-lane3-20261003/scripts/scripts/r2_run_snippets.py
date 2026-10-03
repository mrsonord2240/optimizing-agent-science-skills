"""Execute every python block of SKILL.md as written (cwd = Skill dir), on Golub or synthetic data."""
import re, sys, os, time, warnings
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
skill = sys.argv[1]; mode = sys.argv[2]
os.chdir(skill)
blocks = re.findall(r'```python\n(.*?)```', open('SKILL.md', encoding='utf-8').read(), re.S)
print(len(blocks), 'blocks')
if mode == 'golub':
    G = pd.read_csv('F:/OpenScience/audit-envs/cheminformatics-hit-triage-analyst/public-data/expression/golub_leukemia_openml.csv')
    y = pd.factorize(G.pop('label'))[0]; X = G.values.astype(float)
    X = X[:, np.argsort(-X.var(0))[:2000]]
else:
    rng = np.random.default_rng(0); X = rng.normal(size=(400, 300)); b = np.zeros(300); b[:15] = 0.8
    y = (rng.random(400) < 1/(1+np.exp(-(X @ b - 1.5)))).astype(int)
g = {'X': X, 'y': y}
g['X_train'], _, g['y_train'], _ = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
g['batch_labels'] = np.random.default_rng(1).integers(0, 3, len(y))
g['X_cal'] = g['y_cal'] = None
for i, code in enumerate(blocks):
    t = time.time()
    if 'recalibrate(' in code:
        # calibration set disjoint from train/val/test: reuse the validation split on Golub, a fresh pool on synthetic
        if mode == 'golub': g['X_cal'], g['y_cal'] = g['X_val'], g['y_val']
        else:
            r = np.random.default_rng(5); g['X_cal'] = r.normal(size=(1200, 300)); g['y_cal'] = (r.random(1200) < 1/(1+np.exp(-(g['X_cal'] @ b - 1.5)))).astype(int)
        g['X_te_orig'] = g['X_te']
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always'); warnings.simplefilter('error', FutureWarning)
            exec(code, g)
        fw = [str(x.message)[:80] for x in w if issubclass(x.category, FutureWarning)]
        print(f'--- block {i} OK {time.time()-t:.0f}s  warnings: {[x.category.__name__ for x in w]} {fw}')
    except Exception as e:
        print(f'--- block {i} FAILED: {type(e).__name__}: {e}'); print(code[:200])
