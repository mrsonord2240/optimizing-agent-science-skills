"""Functions copied VERBATIM from proteomics-qc/SKILL.md code blocks (upstream commit d91ed3d).
Only the imports are gathered at the top; function bodies are unchanged. Audit 2026-09-11."""
import pandas as pd
import numpy as np
from itertools import combinations
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.stats import f_oneway

# --- SKILL.md lines 85-100 ---
contaminant_flags = ['Potential contaminant', 'Reverse', 'Only identified by site']

def strip_contaminant_rows(protein_groups):
    keep = pd.Series(True, index=protein_groups.index)
    for col in contaminant_flags:
        match = next((c for c in protein_groups.columns if c.lower() == col.lower()), None)  # MaxQuant casing varies by version -- match case-insensitively
        if match is not None:
            keep &= protein_groups[match].fillna('') != '+'  # MaxQuant marks flagged rows with a literal '+'
    return protein_groups[keep]

def raw_sample_qc(raw_intensities):
    return pd.DataFrame({
        'n_quantified': raw_intensities.notna().sum(),
        'total_signal': raw_intensities.sum(),
        'median_intensity': raw_intensities.median(),
        'missing_pct': 100 * raw_intensities.isna().sum() / len(raw_intensities)})

# --- SKILL.md lines 114-121 ---
def replicate_correlation(log2_intensities, sample_groups):
    corr = log2_intensities.corr(method='pearson')  # log2 first: Pearson on raw is a high-abundance artifact
    rows = []
    for group in sample_groups.unique():
        members = sample_groups[sample_groups == group].index
        for s1, s2 in combinations(members, 2):
            rows.append({'group': group, 's1': s1, 's2': s2, 'r': corr.loc[s1, s2]})
    return pd.DataFrame(rows)

# --- SKILL.md lines 133-143 ---
def median_cv_linear(linear_intensities, sample_groups):
    rows = []
    for group in sample_groups.unique():
        block = linear_intensities[sample_groups[sample_groups == group].index]
        per_protein_cv = block.std(axis=1) / block.mean(axis=1)  # base CV formula REQUIRES linear scale
        rows.append({'group': group, 'median_cv_pct': 100 * per_protein_cv.median()})
    return pd.DataFrame(rows)

def geometric_cv_from_log(log_intensities):
    sigma = log_intensities.std(axis=1) * np.log(2)  # convert log2 SD to natural-log SD
    return 100 * np.sqrt(np.expm1(sigma ** 2))  # gCV = sqrt(exp(sigma^2) - 1)

# --- SKILL.md lines 155-167 ---
def missingness_profile(log2_intensities, n_bins=20):
    observed = log2_intensities.stack()
    abundance_bins = pd.qcut(observed, n_bins, duplicates='drop')
    present_per_protein = log2_intensities.notna().mean(axis=1)
    mean_abundance = log2_intensities.mean(axis=1)
    return mean_abundance, present_per_protein  # plot present-fraction vs abundance: rising-with-abundance = MNAR

def completeness_filter(log2_intensities, sample_groups, min_valid_frac=0.7):
    keep = pd.Series(False, index=log2_intensities.index)
    for group in sample_groups.unique():
        block = log2_intensities[sample_groups[sample_groups == group].index]
        keep |= block.notna().mean(axis=1) >= min_valid_frac  # valid in >=70% of >=1 condition
    return log2_intensities[keep]

# --- SKILL.md lines 183-192 ---
def pca_batch_check(normalized_log2, sample_info, batch_col='batch'):
    imputed = normalized_log2.apply(lambda r: r.fillna(r.median()), axis=1)  # temporary, for PCA only
    pcs = PCA(n_components=5).fit(StandardScaler().fit_transform(imputed.T))
    coords = pd.DataFrame(pcs.transform(StandardScaler().fit_transform(imputed.T)),
                          columns=[f'PC{i+1}' for i in range(5)], index=normalized_log2.columns).join(sample_info)
    for pc in ['PC1', 'PC2', 'PC3']:
        groups = [coords[coords[batch_col] == b][pc] for b in coords[batch_col].unique()]
        _, p = f_oneway(*groups)
        print(f'{pc} ~ {batch_col}: p={p:.4f}')
    return coords, pcs.explained_variance_ratio_
