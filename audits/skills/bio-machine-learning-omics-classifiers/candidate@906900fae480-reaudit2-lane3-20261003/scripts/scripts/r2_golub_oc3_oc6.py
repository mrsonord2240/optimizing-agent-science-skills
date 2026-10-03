"""OC-003 and OC-006 on real Golub (own splits 31, 32; 2,000 highest-variance probes). Executes the SKILL.md blocks 0, 1 (1-SE) and 2 (tree split + XGB) as written, then perturbs the held-out split
and checks that c_1se, the selected coefficients and XGB best round do not move. Usage: python r2_golub_oc3_oc6.py <Skill dir>"""
import re, sys, os, warnings, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
skill = sys.argv[1]; os.chdir(skill); warnings.simplefilter('error', FutureWarning)
blocks = re.findall(r'```python\n(.*?)```', open('SKILL.md', encoding='utf-8').read(), re.S)
G = pd.read_csv('F:/OpenScience/audit-envs/cheminformatics-hit-triage-analyst/public-data/expression/golub_leukemia_openml.csv')
y = pd.factorize(G.pop('label'))[0]; X = G.values.astype(float); X = X[:, np.argsort(-X.var(0))[:2000]]
for seed in (31, 32):
    res = {}
    for arm in ('base', 'perturbed-heldout'):
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=seed)
        if arm != 'base': Xte = np.random.default_rng(5).normal(size=Xte.shape) * 9; yte = np.random.default_rng(6).permutation(yte)
        g = {'X_train': Xtr, 'y_train': ytr}
        exec(blocks[0], g); dense = int((g['pipe']['clf'].coef_ != 0).sum())
        exec(blocks[1], g); sig = g['signature']; nz = int((sig['clf'].coef_ != 0).sum())
        auc = roc_auc_score(yte, sig.predict_proba(Xte)[:, 1]) if arm == 'base' else float('nan')
        # blocks[2]: three-way split on the whole X, y with test split fixed by train_test_split(random_state=0) inside the block; compare best round when y_te/X_te are corrupted AFTER the split
        g2 = {'X': X, 'y': y}
        code = blocks[2]
        if arm != 'base':
            code = code.replace("rf = RandomForestClassifier", "X_te = np.random.default_rng(5).normal(size=X_te.shape) * 9; y_te = np.random.default_rng(6).permutation(y_te)\nrf = RandomForestClassifier", 1)
        g2['np'] = np; exec(code, g2)
        res[arm] = (dense, g['c_1se'], nz, auc, g2['xgb'].best_iteration, float(g2['xgb'].best_score))
        print(f'seed {seed} {arm}: dense non-zero {dense}/2000; c_1se {g["c_1se"]:.4f}; lasso 1-SE non-zero {nz}; held-out AUC {auc:.3f}; xgb(block 2) best round {g2["xgb"].best_iteration} val score {g2["xgb"].best_score:.4f}', flush=True)
    print(f'seed {seed} selection identical under held-out perturbation:', res['base'][:3] == res['perturbed-heldout'][:3] and res['base'][4:] == res['perturbed-heldout'][4:])
