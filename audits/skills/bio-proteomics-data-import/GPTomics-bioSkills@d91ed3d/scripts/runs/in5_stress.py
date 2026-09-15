"""Input 5 (Stress) - load BOTH the MaxQuant DDA table and the DIA-NN report, diagnose missingness in each, advise imputation.
Part A: Skill blocks verbatim (MaxQuant cleaning, DIA-NN import, assess_missingness).
Part B: what Claude-with-this-Skill tells the user (Decision Tree: DDA -> MNAR/left-censored; DIA -> 'closer to MCAR').
Part C: AUDITOR checks against the SYNTHETIC truth: is DIA missingness really MCAR-like here, and what does a
        'standard imputer' (row mean, KNN) do to DIA missing cells compared with a left-censored imputer (MinProb-style)?
"""
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

D = 'F:/OpenScience/audits/bio-proteomics-data-import/data/'

# ---------------- Part A: Skill blocks verbatim ----------------
pg = pd.read_csv(D + 'proteinGroups.txt', sep='\t', low_memory=False)
mask = (pg.get('Reverse', '') != '+') & (pg.get('Potential contaminant', '') != '+') & (pg.get('Only identified by site', '') != '+')
pg = pg[mask].copy()
pg['leading_protein'] = pg['Protein IDs'].str.split(';').str[0]
pg['leading_gene'] = pg['Gene names'].where(pg['Gene names'].notna(), '').str.split(';').str[0]
lfq_cols = [c for c in pg.columns if c.startswith('LFQ intensity ')]
matrix = pg[['leading_protein', 'leading_gene'] + lfq_cols].copy()
matrix[lfq_cols] = matrix[lfq_cols].replace(0, np.nan)
matrix[lfq_cols] = np.log2(matrix[lfq_cols])

report = pd.read_parquet(D + 'report.parquet')
raw_report = report.copy()
report = report[(report['Q.Value'] <= 0.01) & (report['PG.Q.Value'] <= 0.01)]
dia = report.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first')


def assess_missingness(matrix, sample_cols):
    miss_per_protein = matrix[sample_cols].isna().sum(axis=1)
    miss_per_sample = matrix[sample_cols].isna().sum(axis=0)
    total_pct = 100 * matrix[sample_cols].isna().sum().sum() / matrix[sample_cols].size
    mean_abund = matrix[sample_cols].mean(axis=1)  # negative corr with missingness => MNAR / left-censored
    mnar_corr = mean_abund.corr(miss_per_protein)
    return {'per_protein': miss_per_protein, 'per_sample': miss_per_sample, 'total_pct': total_pct, 'abundance_missing_corr': mnar_corr}


# ---------------- Part B: user-facing ----------------
dia_log = np.log2(dia.replace(0, np.nan))  # Claude applies the Skill's MaxQuant 0->NaN rule to PG.MaxLFQ too, then log2
runs = list(dia_log.columns)
res_dda = assess_missingness(matrix, lfq_cols)
res_dia = assess_missingness(dia_log, runs)
res_dia_rawscale = assess_missingness(dia, runs)  # verbatim Skill order: no 0->NaN, no log2
for name, r in (('DDA MaxQuant LFQ (log2)', res_dda), ('DIA-NN PG.MaxLFQ (log2, 0->NaN)', res_dia),
                ('DIA-NN PG.MaxLFQ as pivoted (linear, zeros kept)', res_dia_rawscale)):
    print(f'{name:<50} missing {r["total_pct"]:5.1f}% | corr(mean abundance, #missing) = {r["abundance_missing_corr"]:+.3f}')
print('DDA per-sample missing:', res_dda['per_sample'].to_dict())
print('DIA per-sample missing:', res_dia['per_sample'].to_dict())
print('DDA proteins with 0/8 valid values kept in matrix:', int((res_dda['per_protein'] == 8).sum()))
dda_ids = set(matrix.loc[matrix[lfq_cols].notna().any(axis=1), 'leading_protein'])
dia_ids = set(dia_log.index[dia_log.notna().any(axis=1)])
print(f'overlap: DDA {len(dda_ids)} | DIA {len(dia_ids)} | both {len(dda_ids & dia_ids)}')

# ---------------- Part C: auditor checks ----------------
truth = pd.read_csv(D + 'truth_proteins.csv', keep_default_na=False).set_index('protein')
print('\n[AUDIT] DIA missingness by TRUE abundance quartile (global-FDR-filtered matrix, 887 true groups):')
glob = raw_report[(raw_report['Q.Value'] <= 0.01) & (raw_report['PG.Q.Value'] <= 0.01) & (raw_report['Global.PG.Q.Value'] <= 0.01)]
diag = np.log2(glob.pivot_table(index='Protein.Group', columns='Run', values='PG.MaxLFQ', aggfunc='first').replace(0, np.nan))
diag = diag.reindex(truth.index[truth.index.isin(diag.index)])
tb = truth.loc[diag.index, 'base_log2']
q = pd.qcut(tb, 4, labels=['Q1 low', 'Q2', 'Q3', 'Q4 high'])
onoff = truth.loc[diag.index, 'class'].eq('on_off')
cells = diag[~onoff.to_numpy()]
print((cells.isna().mean(axis=1).groupby(q[~onoff]).mean() * 100).round(1).to_string())
r_glob = assess_missingness(diag[~onoff.to_numpy()], runs)
print(f'[AUDIT] Skill diagnostic on DIA without LOWCONF and on/off groups: missing {r_glob["total_pct"]:.1f}%, corr {r_glob["abundance_missing_corr"]:+.3f}')
print(f'[AUDIT] Skill diagnostic on DIA LOWCONF-free vs Skill-filtered matrix: corr {r_glob["abundance_missing_corr"]:+.3f} vs {res_dia["abundance_missing_corr"]:+.3f}')
# logistic regression-free check: P(missing) vs per-protein observed mean, binned
m_obs = cells.mean(axis=1)
bins = pd.qcut(m_obs, 5)
print('[AUDIT] DIA % missing by OBSERVED-mean quintile:', (cells.isna().mean(axis=1).groupby(bins, observed=True).mean() * 100).round(1).tolist())

# truth for each DIA cell (auditor only): base + effect for Treatment; batch shift (+0.3 mean in B2) is not in truth_proteins.csv
tv = pd.DataFrame({r: truth.loc[cells.index, 'base_log2'] + (truth.loc[cells.index, 'true_log2fc'] if r.startswith('T') else 0.0)
                   for r in runs})
miss = cells.isna()
obs_vals = cells.stack().dropna()
print(f'[AUDIT] DIA: true value of missing cells median {tv[miss].stack().dropna().median():.2f} vs observed cells median {obs_vals.median():.2f} log2')
# standard imputers
row_mean = cells.apply(lambda r: r.fillna(r.mean()), axis=1)
knn = pd.DataFrame(KNNImputer(n_neighbors=5).fit_transform(cells), index=cells.index, columns=runs)
rng = np.random.default_rng(1)
minprob = cells.copy()
for c in runs:
    mu, sd = cells[c].mean(), cells[c].std()
    idx = minprob[c].isna()
    minprob.loc[idx, c] = rng.normal(mu - 1.8 * sd, 0.3 * sd, idx.sum())
for name, imp in (('row mean', row_mean), ('KNN k=5', knn), ('MinProb-style downshift (1.8 SD, width 0.3)', minprob)):
    err = (imp[miss] - tv[miss]).stack().dropna()
    print(f'[AUDIT] DIA imputation bias on missing cells, {name:<44}: mean {err.mean():+.2f} log2, MAE {err.abs().mean():.2f} (n={err.size}; rows all-NaN skipped by row mean)')
# same check on DDA for reference
dm = matrix.set_index('leading_protein')[lfq_cols]
dm = dm[dm.index.isin(truth.index) & dm.notna().any(axis=1)]
dm = dm[~truth.loc[dm.index, 'class'].eq('on_off').to_numpy()]
tvd = pd.DataFrame({c: truth.loc[dm.index, 'base_log2'] + (truth.loc[dm.index, 'true_log2fc'] if ' T' in c else 0.0) for c in lfq_cols})
md = dm.isna()
knn_d = pd.DataFrame(KNNImputer(n_neighbors=5).fit_transform(dm), index=dm.index, columns=lfq_cols)
e = (knn_d[md] - tvd[md]).stack().dropna()
print(f'[AUDIT] DDA KNN bias on missing cells: mean {e.mean():+.2f} log2 (n={e.size})')

# downstream consequence (auditor): fold-change bias and false hits per imputer, DIA matrix without LOWCONF/on-off
from scipy import stats
cls = truth.loc[cells.index, 'class']
has_miss = miss.any(axis=1)
C = [r for r in runs if r.startswith('C')]; T = [r for r in runs if r.startswith('T')]
for name, imp in (('no imputation (complete-pair Welch)', cells), ('row mean', row_mean), ('KNN k=5', knn), ('MinProb-style', minprob)):
    lfc = imp[T].mean(axis=1) - imp[C].mean(axis=1)
    p = stats.ttest_ind(imp[T], imp[C], axis=1, equal_var=False, nan_policy='omit').pvalue
    p = pd.Series(np.asarray(p, dtype=float), index=imp.index)
    chg = cls.isin(['up', 'down']) & has_miss
    bias = (lfc[chg] - truth.loc[chg[chg].index, 'true_log2fc']).mean()
    shrink = (lfc[chg].abs() / truth.loc[chg[chg].index, 'true_log2fc'].abs()).median()
    nullm = cls.eq('null') & has_miss
    print(f'[AUDIT] {name:<36} changed-with-missing n={int(chg.sum())}: |est|/|true| median {shrink:.2f} | null-with-missing n={int(nullm.sum())}: p<0.01 {int((p[nullm] < 0.01).sum())}')
