"""Functions transcribed verbatim from bio-crispr-screens-screen-qc SKILL.md
(crispr-screens/screen-qc), as an agent following the Skill's inline code
patterns would write them. Copied into the auditor's own run/ folder per the
audit brief (never import the external clone in place).
"""
import pandas as pd
import numpy as np


def library_representation(counts_df):
    '''Per-sample library coverage diagnostics.
    counts_df: rows = sgRNAs, columns = samples (numeric counts).'''
    out = pd.DataFrame(index=counts_df.columns)
    out['n_sgrnas_detected'] = (counts_df > 0).sum()
    out['pct_zero'] = (counts_df == 0).sum() / len(counts_df) * 100
    out['pct_lowcount'] = (counts_df < 30).sum() / len(counts_df) * 100
    out['median_count'] = counts_df.median()
    out['p10_count'] = counts_df.quantile(0.10)
    out['p90_count'] = counts_df.quantile(0.90)
    out['skew_ratio'] = out['p90_count'] / out['p10_count'].replace(0, np.nan)
    return out


def stage_specific_thresholds():
    '''Stage conventions: Joung 2017 (zero-count, skew) + MAGeCK-VISPR (Gini).'''
    return {
        'plasmid':  {'pct_zero_max': 0.5, 'skew_max': 2.0, 'gini_max': 0.10},
        'day_0':    {'pct_zero_max': 1.0, 'skew_max': 2.5, 'gini_max': 0.12},
        'endpoint': {'pct_zero_max': 5.0, 'skew_max': 10.0, 'gini_max': 0.30},
    }


def gini(x):
    '''Gini coefficient: 0 = perfect equality, 1 = maximal inequality.
    Uses non-zero counts only; zero-count sgRNAs handled separately by % zero.'''
    x = np.sort(x[x > 0].astype(float))
    if x.size == 0:
        return np.nan
    n = x.size
    cumx = np.cumsum(x)
    return (n + 1 - 2 * np.sum(cumx) / cumx[-1]) / n


def replicate_concordance(counts_df, condition_map):
    '''condition_map: {condition_name: [sample_col1, sample_col2, ...]}.'''
    log_counts = np.log10(counts_df + 1)
    rows = []
    for cond, samples in condition_map.items():
        if len(samples) < 2:
            continue
        for i in range(len(samples)):
            for j in range(i + 1, len(samples)):
                r_pearson = log_counts[[samples[i], samples[j]]].corr().iloc[0, 1]
                r_spearman = counts_df[[samples[i], samples[j]]].corr(method='spearman').iloc[0, 1]
                rows.append({'condition': cond, 'rep1': samples[i], 'rep2': samples[j],
                             'pearson_log': r_pearson, 'spearman': r_spearman})
    return pd.DataFrame(rows)


def essentialome_recovery(gene_lfc_df, cegv2_set, negv1_set):
    '''gene_lfc_df: must have ["gene", "lfc"] columns (gene-level mean LFC, negative = depleted).
    cegv2_set, negv1_set: sets of gene symbols from Hart 2017.'''
    from sklearn.metrics import precision_recall_curve, auc, roc_auc_score
    labeled = gene_lfc_df[gene_lfc_df['gene'].isin(cegv2_set | negv1_set)].copy()
    labeled['is_essential'] = labeled['gene'].isin(cegv2_set).astype(int)
    y_score = -labeled['lfc']
    precision, recall, _ = precision_recall_curve(labeled['is_essential'], y_score)
    return {
        'pr_auc': auc(recall, precision),
        'roc_auc': roc_auc_score(labeled['is_essential'], y_score),
        'n_essential_detected': labeled['is_essential'].sum(),
        'n_nonessential_detected': (1 - labeled['is_essential']).sum(),
    }


def cn_bias_diagnostic(gene_lfc_df, cn_df):
    '''cn_df: per-gene copy number (from WGS/SNP-array/matched ASCAT).
    Tests whether amplified genes show systematically lower LFC.'''
    from scipy.stats import spearmanr
    merged = gene_lfc_df.merge(cn_df, on='gene')
    bins = pd.qcut(merged['copy_number'], q=5, duplicates='drop')
    bin_lfc = merged.groupby(bins, observed=True)['lfc'].agg(['mean', 'median', 'std', 'count'])
    rho, p = spearmanr(merged['copy_number'], merged['lfc'])
    return {'cn_vs_lfc_rho': rho, 'cn_vs_lfc_p': p,
            'amplified_mean_lfc': merged[merged['copy_number'] > 4]['lfc'].mean(),
            'diploid_mean_lfc': merged[(merged['copy_number'] >= 1.5) & (merged['copy_number'] <= 2.5)]['lfc'].mean(),
            'per_bin': bin_lfc}


def depth_audit(counts_df):
    '''Verify depth: Joung 2017 recommends >100 reads/sgRNA for plasmid QC and
    >500 for screening; MAGeCK-VISPR uses 300x.'''
    total = counts_df.sum()
    n_sgrnas = len(counts_df)
    depth = total / n_sgrnas
    cv = total.std() / total.mean()
    return pd.DataFrame({'total_reads': total, 'reads_per_sgrna': depth,
                          'depth_grade': np.where(depth < 100, 'FAIL',
                                          np.where(depth < 300, 'CAUTION',
                                          np.where(depth < 500, 'OK', 'EXCELLENT')))}).assign(across_sample_cv=cv)


def screen_pca(counts_df, metadata_df, condition_col='condition'):
    '''metadata_df: rows = samples, columns include condition_col, batch (optional).'''
    from sklearn.decomposition import PCA
    log_counts = np.log10(counts_df + 1).T
    pca = PCA(n_components=3)
    pcs = pca.fit_transform(log_counts)
    out = pd.DataFrame(pcs, columns=['PC1', 'PC2', 'PC3'], index=counts_df.columns)
    out = out.join(metadata_df)
    return out, pca.explained_variance_ratio_


def composite_qc_score(per_sample_qc):
    '''per_sample_qc: one row per sample, joining library_representation() output
    (n_sgrnas_detected, reads_per_sgrna) with gini, pearson_min_replicate, pr_auc
    and n_sgrnas_total.'''
    metrics = {
        'gini_inv': 1 - per_sample_qc['gini'],
        'pearson': per_sample_qc['pearson_min_replicate'],
        'pr_auc': per_sample_qc['pr_auc'],
        'depth_log': np.log10(per_sample_qc['reads_per_sgrna']),
        'detected_frac': per_sample_qc['n_sgrnas_detected'] / per_sample_qc['n_sgrnas_total'],
    }
    return pd.DataFrame(metrics).mean(axis=1)
