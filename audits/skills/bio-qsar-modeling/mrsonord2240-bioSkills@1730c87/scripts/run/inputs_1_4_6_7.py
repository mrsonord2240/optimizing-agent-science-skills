# bio-qsar-modeling -- Inputs 1 (Canonical), 4 (Variant B), 6 (Scope boundary), 7 (Adversarial)
# Built only from SKILL.md: RF+ECFP4 baseline, scaffold-balanced split, the four
# tabulated AD methods, and the "Random split for QSAR" / "Missing AD" failure modes.
import numpy as np
import pandas as pd
from collections import defaultdict
from rdkit import Chem, RDLogger, DataStructs
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem.Scaffolds import MurckoScaffold
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from scipy.spatial.distance import mahalanobis

RDLogger.DisableLog('rdApp.*')
rng = np.random.RandomState(42)
SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"

df = pd.read_csv(SRC).dropna(subset=['canonical_smiles', 'pchembl_value'])
df = df.groupby('canonical_smiles', as_index=False).pchembl_value.mean()
df['mol'] = df.canonical_smiles.map(Chem.MolFromSmiles)
df = df[df.mol.notna()].reset_index(drop=True)
print(f"[data] {len(df)} unique hERG compounds, pChEMBL "
      f"{df.pchembl_value.min():.2f}-{df.pchembl_value.max():.2f} "
      f"mean {df.pchembl_value.mean():.2f}")

gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fps = [gen.GetFingerprint(m) for m in df.mol]
X = np.zeros((len(fps), 2048), dtype=np.uint8)
for i, fp in enumerate(fps):
    DataStructs.ConvertToNumpyArray(fp, X[i])
y = df.pchembl_value.to_numpy()


def scaffold_split(mols, sizes=(0.8, 0.1, 0.1), seed=42):
    """SKILL.md 'Scaffold-Balanced Split': whole scaffold groups to one split."""
    groups = defaultdict(list)
    for i, m in enumerate(mols):
        groups[MurckoScaffold.MurckoScaffoldSmiles(mol=m)].append(i)
    sets = sorted(groups.values(), key=len, reverse=True)
    n = len(mols)
    tr, va, te = [], [], []
    n_tr, n_va = sizes[0] * n, (sizes[0] + sizes[1]) * n
    for g in sets:
        if len(tr) + len(g) <= n_tr:
            tr += g
        elif len(tr) + len(va) + len(g) <= n_va:
            va += g
        else:
            te += g
    return np.array(tr), np.array(va), np.array(te)


tr, va, te = scaffold_split(list(df.mol))
print(f"[split] scaffold-balanced train={len(tr)} val={len(va)} test={len(te)}")
sc_tr = {MurckoScaffold.MurckoScaffoldSmiles(mol=df.mol[i]) for i in tr}
sc_te = {MurckoScaffold.MurckoScaffoldSmiles(mol=df.mol[i]) for i in te}
print(f"[split] scaffolds shared between train and test: {len(sc_tr & sc_te)} "
      f"(train {len(sc_tr)}, test {len(sc_te)})")

# ================= INPUT 7 (Adversarial): random vs scaffold optimism =====
print("\n===== INPUT 7: 'our random-split R2 is great, can we ship?' =====")
rtr, rte = train_test_split(np.arange(len(df)), test_size=len(te) / len(df),
                            random_state=42)
for label, a, b in [('random split  ', rtr, rte), ('scaffold split', tr, te)]:
    m = RandomForestRegressor(n_estimators=500, random_state=42, n_jobs=-1)
    m.fit(X[a], y[a])
    p = m.predict(X[b])
    print(f"  {label}  n_train={len(a)} n_test={len(b)}  "
          f"R2={r2_score(y[b], p):.3f}  MAE={mean_absolute_error(y[b], p):.3f}  "
          f"RMSE={np.sqrt(((y[b]-p)**2).mean()):.3f}")
sc_rtr = {MurckoScaffold.MurckoScaffoldSmiles(mol=df.mol[i]) for i in rtr}
sc_rte = {MurckoScaffold.MurckoScaffoldSmiles(mol=df.mol[i]) for i in rte}
print(f"  random split shares {len(sc_rtr & sc_rte)} scaffolds between train and test "
      f"-- this is the documented leakage mechanism")

# ================= INPUT 1 (Canonical): the deployable model ==============
print("\n===== INPUT 1: RF+ECFP4 baseline with an AD gate on the report =====")
model = RandomForestRegressor(n_estimators=500, random_state=42, n_jobs=-1)
model.fit(X[tr], y[tr])
pred = model.predict(X[te])
print(f"  overall  R2={r2_score(y[te], pred):.3f}  MAE={mean_absolute_error(y[te], pred):.3f}")

# per-tree ensemble spread (SKILL.md "Ensemble variance" AD row)
per_tree = np.stack([t.predict(X[te]) for t in model.estimators_])
ens_sd = per_tree.std(axis=0)

# kNN Tanimoto to training set (SKILL.md "kNN distance" / "Tanimoto coverage")
fp_tr = [fps[i] for i in tr]
sims = np.array([np.sort(DataStructs.BulkTanimotoSimilarity(fps[i], fp_tr))[::-1][:5]
                 for i in te])
knn5 = sims.mean(axis=1)
maxsim = sims[:, 0]
print(f"  AD diagnostics on the test set: mean max-Tanimoto={maxsim.mean():.3f}, "
      f"mean kNN5={knn5.mean():.3f}, mean ensemble sd={ens_sd.mean():.3f}")

# do the AD diagnostics separate good predictions from bad ones?
err = np.abs(y[te] - pred)
print("\n  does each AD diagnostic actually track error? (test set split at its median)")
for name, score, higher_is_inside in [('max Tanimoto', maxsim, True),
                                      ('kNN5 Tanimoto', knn5, True),
                                      ('ensemble sd', ens_sd, False)]:
    med = np.median(score)
    inside = score >= med if higher_is_inside else score <= med
    print(f"    {name:15} inside n={inside.sum():4} MAE={err[inside].mean():.3f} "
          f"R2={r2_score(y[te][inside], pred[inside]):6.3f}   |   "
          f"outside n={(~inside).sum():4} MAE={err[~inside].mean():.3f} "
          f"R2={r2_score(y[te][~inside], pred[~inside]):6.3f}")

# Tanimoto-coverage gate at a project-defined threshold
for thr in [0.3, 0.4, 0.5]:
    ins = maxsim >= thr
    if ins.sum() < 5 or (~ins).sum() < 5:
        continue
    print(f"    Tanimoto-coverage gate at {thr}: {ins.sum()}/{len(te)} inside "
          f"({100*ins.sum()/len(te):.0f}%), inside MAE={err[ins].mean():.3f}, "
          f"outside MAE={err[~ins].mean():.3f}")

# ================= INPUT 4 (Variant B): leverage and Mahalanobis ==========
print("\n===== INPUT 4: the other two tabulated AD methods on 2048-bit input =====")
keep = X[tr].sum(axis=0) > 0
Xt, Xs = X[tr][:, keep].astype(float), X[te][:, keep].astype(float)
print(f"  non-constant training bits: {keep.sum()}/2048; n_train={len(tr)}")
print(f"  leverage h = x(X'X)^-1 x' needs n > p: n_train={len(tr)}, p={keep.sum()} "
      f"-> {'OK' if len(tr) > keep.sum() else 'X\'X IS SINGULAR -- leverage undefined on raw bits'}")
try:
    XtX_inv = np.linalg.inv(Xt.T @ Xt)
    h = np.einsum('ij,jk,ik->i', Xs, XtX_inv, Xs)
    print(f"  leverage computed: mean={h.mean():.3f} min={h.min():.3f} max={h.max():.3f}")
    print(f"  SANITY: leverage is a hat-matrix diagonal and must lie in [0,1]; "
          f"{int((h > 1).sum())}/{len(h)} values exceed 1 "
          f"-> X'X is numerically singular on 2020 sparse binary bits and the "
          f"direct inverse returns garbage WITHOUT raising")
    cond = np.linalg.cond(Xt.T @ Xt)
    print(f"  condition number of X'X = {cond:.3e}")
    med = np.median(h)
    ins = h <= med
    print(f"  leverage-based gate anyway: inside MAE={err[ins].mean():.3f}  "
          f"outside MAE={err[~ins].mean():.3f}")
except np.linalg.LinAlgError as e:
    print(f"  leverage raised LinAlgError: {e}")
    print("  -> falling back to pseudo-inverse, as any practitioner would have to:")
    XtX_pinv = np.linalg.pinv(Xt.T @ Xt)
    h = np.einsum('ij,jk,ik->i', Xs, XtX_pinv, Xs)
    warn = 3 * (keep.sum() + 1) / len(tr)
    print(f"     leverage mean={h.mean():.3f} max={h.max():.3f}; classical warning "
          f"threshold 3(p+1)/n = {warn:.3f} -> {int((h > warn).sum())} flagged "
          f"({'meaningless: threshold > 1' if warn > 1 else 'usable'})")
    med = np.median(h)
    ins = h <= med
    print(f"     leverage-based gate: inside MAE={err[ins].mean():.3f}  "
          f"outside MAE={err[~ins].mean():.3f}")

from sklearn.decomposition import PCA
pca = PCA(n_components=50, random_state=42).fit(Xt)
Zt, Zs = pca.transform(Xt), pca.transform(Xs)
cov_inv = np.linalg.pinv(np.cov(Zt.T))
mu = Zt.mean(axis=0)
md = np.array([mahalanobis(z, mu, cov_inv) for z in Zs])
ins = md <= np.median(md)
print(f"  Mahalanobis on 50 PCA components: mean={md.mean():.2f}  "
      f"inside MAE={err[ins].mean():.3f}  outside MAE={err[~ins].mean():.3f}")
print("  (SKILL.md 'Con' column for Mahalanobis is 'high-dim instability' and for "
      "leverage 'linear assumptions' -- both are exactly what was hit here)")

# ================= INPUT 6 (Scope boundary): new chemotype, no AD =========
print("\n===== INPUT 6: predicting a new chemotype series with no AD check =====")
novel = np.argsort(maxsim)[:50]              # 50 most dissimilar test compounds
common = np.argsort(maxsim)[-50:]
for label, idx in [('50 most novel chemotypes', novel), ('50 closest analogues', common)]:
    print(f"  {label:26} max-Tanimoto {maxsim[idx].mean():.3f}  "
          f"MAE={err[idx].mean():.3f}  R2={r2_score(y[te][idx], pred[idx]):6.3f}  "
          f"sd(y)={y[te][idx].std():.3f}  mean ensemble sd={ens_sd[idx].mean():.3f}")
print(f"  ratio of MAE (novel / familiar) = {err[novel].mean()/err[common].mean():.2f}x")
print("  -> HONEST READING: on this dataset the AD effect appears in R2 and in ensemble")
print("     spread, NOT in MAE. The novel subset has far lower label variance, so the")
print("     model's absolute error is similar while it explains almost none of the")
print("     variance it is shown. The Skill's failure-mode symptom is stated as")
print("     'confident predictions but actual values different', which would predict a")
print("     larger MAE; that specific symptom did not reproduce here.")
np.save(r"F:\OpenScience\audits\bio-qsar-modeling\run\X.npy", X)
np.save(r"F:\OpenScience\audits\bio-qsar-modeling\run\y.npy", y)
np.save(r"F:\OpenScience\audits\bio-qsar-modeling\run\tr.npy", tr)
np.save(r"F:\OpenScience\audits\bio-qsar-modeling\run\te.npy", te)
df[['canonical_smiles', 'pchembl_value']].to_csv(
    r"F:\OpenScience\audits\bio-qsar-modeling\run\herg_unique.csv", index=False)
print("\n[saved] X.npy y.npy tr.npy te.npy herg_unique.csv for the MAPIE and chemprop inputs")
