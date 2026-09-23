'''Transcribed verbatim from SKILL.md's "Run All Five on the Same Data (Consensus Strategy)"
code block, crispr-screens/hit-calling, commit 6847328. Not imported from the fork clone --
hand-copied exactly as an agent following SKILL.md would produce it.'''
import pandas as pd
from scipy.stats import hypergeom

def _check_comparable(merged, hit_cols):
    '''Warn if any pair of method hit-sets shows no statistical enrichment for
    overlap -- the signature of merging results that answer different questions
    (e.g. a real essentiality MAGeCK+BAGEL2 pair merged against a drugZ table from
    an unrelated drug-vs-vehicle screen) rather than genuine method disagreement on
    the same comparison. Verified on real data: matched MAGeCK/BAGEL2 hit sets give
    p=0 (highly enriched overlap); a mismatched drugZ table against either gives
    p=1.0 (no enrichment) -- see the Failure Modes entry below.'''
    n = len(merged)
    warnings = []
    for i, col_a in enumerate(hit_cols):
        for col_b in hit_cols[i + 1:]:
            a, b = merged[col_a].fillna(False), merged[col_b].fillna(False)
            k, K, N = int((a & b).sum()), int(a.sum()), int(b.sum())
            if K == 0 or N == 0:
                continue
            p = hypergeom.sf(k - 1, n, K, N)
            if p > 0.05:
                warnings.append(f'{col_a} vs {col_b}: overlap not enriched above chance '
                                 f'(observed={k}, expected~{K * N / n:.1f}, p={p:.3f}) -- '
                                 'check these came from the SAME experimental comparison '
                                 'before trusting consensus.')
    for w in warnings:
        print(f'WARNING: {w}')
    return warnings

def consensus_hits(mageck_path, bagel_path, drugz_path,
                   mageck_fdr_thresh=0.05, bagel_bf_thresh=6, drugz_fdr_thresh=0.05):
    '''Build consensus across MAGeCK / BAGEL2 / drugZ on the same screen.
    Each hit gets a count of supporting methods. Defaults match the Quantitative
    Thresholds table below -- keep this function and examples/consensus_hits.py in
    sync with that table, not with each other.'''
    mageck = pd.read_csv(mageck_path, sep='\t')[['id', 'neg|fdr']].rename(columns={'id': 'gene', 'neg|fdr': 'mageck_neg_fdr'})
    bagel = pd.read_csv(bagel_path, sep='\t')[['GENE', 'BF']].rename(columns={'GENE': 'gene', 'BF': 'bagel_bf'})
    drugz = pd.read_csv(drugz_path, sep='\t')[['GENE', 'fdr_synth']].rename(columns={'GENE': 'gene', 'fdr_synth': 'drugz_synth_fdr'})
    merged = mageck.merge(bagel, on='gene', how='outer').merge(drugz, on='gene', how='outer')
    merged['mageck_hit'] = merged['mageck_neg_fdr'] < mageck_fdr_thresh
    merged['bagel_hit'] = merged['bagel_bf'] > bagel_bf_thresh
    merged['drugz_hit'] = merged['drugz_synth_fdr'] < drugz_fdr_thresh
    _check_comparable(merged, ['mageck_hit', 'bagel_hit', 'drugz_hit'])
    merged['consensus_count'] = (merged[['mageck_hit', 'bagel_hit', 'drugz_hit']].astype(int)).sum(axis=1)
    return merged.sort_values('consensus_count', ascending=False)

def second_best_lfc(sgrna_lfc_df, genes_series, direction='neg'):
    '''Return per-gene LFC of the second-best sgRNA in the direction of interest,
    and flag genes with fewer than 2 sgRNAs.'''
    results = []
    for gene in genes_series.unique():
        gene_lfc = sgrna_lfc_df[genes_series == gene].sort_values()
        n = len(gene_lfc)
        if n >= 2:
            second = gene_lfc.iloc[1] if direction == 'neg' else gene_lfc.iloc[-2]
            single = False
        else:
            second = float('nan')
            single = True
        results.append({'gene': gene, 'second_best_lfc': second, 'single_guide': single})
    return pd.DataFrame(results)
