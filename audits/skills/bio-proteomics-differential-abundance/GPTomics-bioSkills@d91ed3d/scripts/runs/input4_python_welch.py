"""INPUT 4 (Variant B): 12 vs 12 plasma, Python only. SKILL.md "Python Workflow" functions copied verbatim,
then the Skill's own reporting rule for on/off proteins ("undetected in group X"), scored against truth."""
import warnings
import numpy as np
import pandas as pd
import scipy, statsmodels
from scipy import stats
from statsmodels.stats.multitest import multipletests

warnings.simplefilter('default')
print('pandas', pd.__version__, '| numpy', np.__version__, '| scipy', scipy.__version__, '| statsmodels', statsmodels.__version__)
D = 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data/'


# ---- SKILL.md Python block (verbatim) ----
def preprocess(intensities):
    log2_data = np.log2(intensities.replace(0, np.nan))  # zeros -> NaN to avoid -inf
    sample_medians = log2_data.median(axis=0)
    return log2_data - sample_medians + sample_medians.median()

def differential_abundance(normalized, case_cols, ctrl_cols):
    rows = []
    for protein in normalized.index:
        case, ctrl = normalized.loc[protein, case_cols].dropna(), normalized.loc[protein, ctrl_cols].dropna()
        if len(case) >= 2 and len(ctrl) >= 2:
            _, pval = stats.ttest_ind(case, ctrl, equal_var=False)  # Welch; scipy defaults to Student's True
            rows.append({'protein': protein, 'log2fc': case.mean() - ctrl.mean(), 'pvalue': pval})
    df = pd.DataFrame(rows)
    df['padj'] = multipletests(df['pvalue'], method='fdr_bh')[1]  # default is Holm-Sidak; pass fdr_bh explicitly
    return df
# ---- end Skill block ----

intensities = pd.read_csv(D + 'plasma_12v12.csv', index_col=0)
truth = pd.read_csv(D + 'plasma_truth.csv', index_col=0, keep_default_na=False)  # 'null' class must not parse as NaN
case_cols = [c for c in intensities.columns if c.startswith('case')]
ctrl_cols = [c for c in intensities.columns if c.startswith('ctrl')]
print('matrix', intensities.shape, '| missing', round(intensities.isna().mean().mean(), 3))

normalized = preprocess(intensities)
print('per-sample median after normalization (range):', normalized.median().round(3).agg(['min', 'max']).tolist())
res = differential_abundance(normalized, case_cols, ctrl_cols)
res['class'] = truth.loc[res['protein'], 'class'].values
sig = res[res['padj'] < 0.05]
print(f"tested {len(res)} of {len(intensities)} | called {len(sig)} | null FP {int((sig['class']=='null').sum())} "
      f"| realized FDR {100*(sig['class']=='null').mean():.1f}% | TP up {int((sig['class']=='up').sum())}/35 down {int((sig['class']=='down').sum())}/35 "
      f"| on/off in table {int((res['class']=='on_off').sum())}/8")

# Skill guidance: report on/off proteins as 'undetected in group X' (no code given; written here)
nc, nt = normalized[ctrl_cols].notna().sum(axis=1), normalized[case_cols].notna().sum(axis=1)
dropped = normalized.index[~normalized.index.isin(res['protein'])]
onoff = pd.DataFrame({'n_ctrl_detected': nc[dropped], 'n_case_detected': nt[dropped],
                      'ctrl_mean_log2': normalized.loc[dropped, ctrl_cols].mean(axis=1).round(2),
                      'class': truth.loc[dropped, 'class']})
report = onoff[(onoff['n_ctrl_detected'] >= 9) & (onoff['n_case_detected'] == 0) |
               (onoff['n_case_detected'] >= 9) & (onoff['n_ctrl_detected'] == 0)]
print(f'\nProteins silently dropped by the <2-per-group rule: {len(dropped)} (truth: {onoff["class"].value_counts().to_dict()})')
print("Reported as 'undetected in one group' (>=9/12 in one group, 0/12 in the other):")
print(report.sort_values('ctrl_mean_log2', ascending=False).to_string())

# sanity: does Welch control FDR at n=12? compare to Student and to naive unadjusted
res_s = []
for p in normalized.index:
    a, b = normalized.loc[p, case_cols].dropna(), normalized.loc[p, ctrl_cols].dropna()
    if len(a) >= 2 and len(b) >= 2:
        res_s.append(stats.ttest_ind(a, b).pvalue)
print('\nStudent t (equal_var default) calls at BH 0.05:', int((multipletests(res_s, method='fdr_bh')[1] < 0.05).sum()),
      '| Holm-Sidak default (method omitted) calls:', int((multipletests(res['pvalue'])[1] < 0.05).sum()))
res.sort_values('padj').to_csv('F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/input4_welch_results.csv', index=False)
print(res.sort_values('padj').head(6).to_string(index=False))
