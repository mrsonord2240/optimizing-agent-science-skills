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
    if not rows:
        raise ValueError('No protein has >= 2 non-missing values in both groups; a two-sample test is not possible')
    df = pd.DataFrame(rows)
    df['padj'] = multipletests(df['pvalue'], method='fdr_bh')[1]  # default is Holm-Sidak; pass fdr_bh explicitly
    return df
