import numpy as np

def assess_missingness(matrix, sample_cols):
    miss_per_protein = matrix[sample_cols].isna().sum(axis=1)
    miss_per_sample = matrix[sample_cols].isna().sum(axis=0)
    total_pct = 100 * matrix[sample_cols].isna().sum().sum() / matrix[sample_cols].size
    mean_abund = matrix[sample_cols].mean(axis=1)  # negative corr with missingness => MNAR / left-censored
    mnar_corr = mean_abund.corr(miss_per_protein)
    return {'per_protein': miss_per_protein, 'per_sample': miss_per_sample, 'total_pct': total_pct, 'abundance_missing_corr': mnar_corr}
