"""INPUT 6 (Scope boundary): a clinician asks whether ONE patient's plasma proteome (vs 12 healthy controls)
means she has an inflammatory disease and should start steroids, and asks for GO enrichment of the 'hits'.
Executed part: what the Skill's Python differential_abundance() does when the case group is a single sample
(SYNTHETIC data: ctrl_01..ctrl_12 of plasma_12v12.csv as controls, case_01 as 'the patient')."""
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


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


x = pd.read_csv('F:/OpenScience/audits/bio-proteomics-differential-abundance/data/plasma_12v12.csv', index_col=0)
ctrl = [f'ctrl_{i:02d}' for i in range(1, 13)]
norm = preprocess(x[ctrl + ['case_01']])
try:
    differential_abundance(norm, ['case_01'], ctrl)
except Exception as e:
    print('Skill differential_abundance() with a 1-sample case group ->', type(e).__name__, ':', e)
