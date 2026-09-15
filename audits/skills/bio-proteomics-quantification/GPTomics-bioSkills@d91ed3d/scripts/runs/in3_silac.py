"""Input 3 (Edge) - SILAC H/L ratios with on/off proteins, SKILL.md lines 172-186, then a pandas/limma downstream.
SYNTHETIC data generated here (seeded): 400 proteins x 3 forward-label replicates (heavy = treatment).
Truth: 30 up (+1.5 log2), 30 down (-1.5), 6 heavy-only (on in treatment), 6 light-only (off in treatment).
Heavy labeling incorporation = 93% (the researcher's pilot number): 7% of heavy-sample protein appears in L.
"""
import os
import numpy as np
import pandas as pd

D = 'F:/OpenScience/audits/bio-proteomics-quantification/data'
rng = np.random.default_rng(3)
n = 400
prot = [f'SILP{i:03d}' for i in range(n)]
cls = np.array(['unchanged'] * n, dtype=object)
cls[:30], cls[30:60], cls[60:66], cls[66:72] = 'up', 'down', 'heavy_only', 'light_only'
eff = np.where(cls == 'up', 1.5, np.where(cls == 'down', -1.5, 0.0))
base = rng.normal(24, 1.8, n)
INC = 0.93
rows = []
for r in (1, 2, 3):
    light_true = 2 ** (base + rng.normal(0, 0.2, n))
    heavy_total = 2 ** (base + eff + rng.normal(0, 0.2, n) + 0.15 * (r - 2))  # small per-replicate mixing error
    heavy_total[cls == 'light_only'] = 0.0             # off in treatment: only the light (control) channel has signal
    light_true[cls == 'heavy_only'] = 0.0              # on in treatment: only the heavy channel has signal
    H = INC * heavy_total
    L = light_true + (1 - INC) * heavy_total               # incomplete labeling leaks heavy-sample protein into L
    det_thr = 2 ** 20.5                                    # below this the peak is not quantified -> 0
    H[H < det_thr] = 0.0
    L[L < det_thr] = 0.0
    rows.append(pd.DataFrame({f'Intensity H rep{r}': H, f'Intensity L rep{r}': L}, index=prot))
silac = pd.concat(rows, axis=1)
silac.index.name = 'protein'
silac.to_csv(os.path.join(D, 'silac_proteins.csv'))
pd.DataFrame({'protein': prot, 'class': cls, 'true_log2fc': eff}).to_csv(os.path.join(D, 'silac_truth.csv'), index=False)

# ---------------- the Skill's code, verbatim
SILAC_SHIFTS = {'Arg10': 10.008269, 'Lys8': 8.014199, 'Arg6': 6.020129, 'Lys6': 6.020129}


def silac_log2_ratio(heavy, light):
    if heavy > 0 and light > 0:
        return np.log2(heavy / light)
    if heavy > 0 and light == 0:
        return np.inf     # present only in heavy: real on/off biology, do NOT discard as NaN
    if light > 0 and heavy == 0:
        return -np.inf
    return np.nan


# (a) naive column-wise call, the way an agent would first try it
try:
    silac_log2_ratio(silac['Intensity H rep1'], silac['Intensity L rep1'])
except Exception as e:
    print(f'(a) column-wise call -> {type(e).__name__}: {e}')

# (b) element-wise, as the scalar function requires
ratios = pd.DataFrame({f'rep{r}': [silac_log2_ratio(h, l) for h, l in zip(silac[f'Intensity H rep{r}'], silac[f'Intensity L rep{r}'])]
                       for r in (1, 2, 3)}, index=silac.index)
print('(b) element-wise: +inf cells', int(np.isposinf(ratios.values).sum()), '| -inf cells', int(np.isneginf(ratios.values).sum()),
      '| NaN cells', int(ratios.isna().sum().sum()))
truth = pd.read_csv(os.path.join(D, 'silac_truth.csv'), index_col=0)
print('heavy_only proteins -> ratios:\n', ratios[truth['class'] == 'heavy_only'].round(2).to_string())
print('light_only proteins -> ratios:\n', ratios[truth['class'] == 'light_only'].round(2).to_string())

# ---------------- downstream, pandas
med = ratios.median()                                    # per-replicate median normalization (standard for SILAC)
print('\nper-replicate medians (inf included):', med.round(3).to_dict())
norm = ratios - med
print('mean over replicates, heavy_only rows:', norm[truth['class'] == 'heavy_only'].mean(axis=1).round(2).tolist())
print('std over replicates, heavy_only rows:', norm[truth['class'] == 'heavy_only'].std(axis=1).round(2).tolist())
mixed = norm[np.isinf(norm).any(axis=1) & np.isfinite(norm).any(axis=1)]
print('rows mixing finite and inf values:', len(mixed), '-> mean', mixed.mean(axis=1).round(2).tolist()[:4])
print('global column mean (what a mean-centering step would use):', ratios.mean().round(3).to_dict())
print('global column std:', ratios.std().round(3).to_dict())
from scipy import stats
t = stats.ttest_1samp(norm, 0, axis=1)
print('scipy ttest_1samp on +inf rows -> p =', np.round(t.pvalue[(truth['class'] == 'heavy_only').values], 3).tolist())
norm.to_csv('F:/OpenScience/audits/bio-proteomics-quantification/runs/in3_silac_log2_norm.csv')

# ---------------- label-efficiency sanity: what does 93% incorporation do to unchanged proteins?
raw_null = ratios[truth['class'] == 'unchanged'].replace([np.inf, -np.inf], np.nan)
print(f'\nunchanged proteins: median raw log2 H/L = {np.nanmedian(raw_null.values):+.3f} (0 expected with 100% labeling; '
      f'log2(0.93) = {np.log2(0.93):+.3f})')
up = ratios[truth['class'] == 'up'].replace([np.inf, -np.inf], np.nan)
print(f'up proteins (true +1.5): median raw log2 H/L = {np.nanmedian(up.values):+.3f}; after median norm = '
      f'{np.nanmedian((ratios - med)[truth["class"] == "up"].replace([np.inf, -np.inf], np.nan).values):+.3f}')
