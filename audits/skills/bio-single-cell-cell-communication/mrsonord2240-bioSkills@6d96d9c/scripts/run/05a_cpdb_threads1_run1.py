"""Isolate whether non-determinism is specific to threads=4 (the value SKILL.md actually documents)
by repeating at threads=1 (what the fixer's fix log tested), same debug_seed=1337, smaller
iterations=100 for speed -- this mirrors the fix log's own verification parameters exactly.
"""
from cellphonedb.src.core.methods import cpdb_statistical_analysis_method

def main():
    results = cpdb_statistical_analysis_method.call(
        cpdb_file_path='run/cpdb_db/cellphonedb.zip',
        meta_file_path='run/meta.tsv',
        counts_file_path='run/counts_normalized.h5ad',
        counts_data='hgnc_symbol',
        threshold=0.1, iterations=100, pvalue=0.05, debug_seed=1337,
        score_interactions=True, threads=1, output_path='run/cpdb_out_t1_run1')
    return results

if __name__ == '__main__':
    results = main()
    print('T1_RUN1_COMPLETED')
    results['pvalues'].to_csv('run/reaudit_cpdb_pvalues_t1_run1.csv', index=False)
