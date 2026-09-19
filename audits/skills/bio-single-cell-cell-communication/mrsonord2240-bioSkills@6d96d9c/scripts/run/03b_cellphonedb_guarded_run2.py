"""Re-auditor fresh run 2/2 -- identical call, separate process, same debug_seed=1337."""
from cellphonedb.src.core.methods import cpdb_statistical_analysis_method

def main():
    results = cpdb_statistical_analysis_method.call(
        cpdb_file_path='run/cpdb_db/cellphonedb.zip',
        meta_file_path='run/meta.tsv',
        counts_file_path='run/counts_normalized.h5ad',
        counts_data='hgnc_symbol',
        threshold=0.1, iterations=1000, pvalue=0.05, debug_seed=1337,
        score_interactions=True, threads=4, output_path='run/cpdb_out_reaudit_run2')
    return results

if __name__ == '__main__':
    results = main()
    print('RUN2_COMPLETED_NO_CRASH')
    print('pvalues shape', results['pvalues'].shape)
    print('means shape', results['means'].shape)
    results['pvalues'].to_csv('run/reaudit_cpdb_pvalues_run2.csv', index=False)
    results['significant_means'].to_csv('run/reaudit_cpdb_sigmeans_run2.csv', index=False)
