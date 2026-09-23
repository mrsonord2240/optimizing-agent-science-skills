"""Re-auditor fresh run 1/2 of SKILL.md's guarded 'Specificity Test (CellPhoneDB v5)' block, exactly
as written post-fix (def main(): ... / if __name__=='__main__':), with debug_seed=1337,
score_interactions=True, threads=4, on the same real PBMC data/DB used by the original audit
(counts_normalized.h5ad, meta.tsv, cpdb_db/cellphonedb.zip -- these are static inputs, not outputs,
being reused per AUDIT_BRIEF; the outputs below are freshly computed, not copied from the fixer).
"""
from cellphonedb.src.core.methods import cpdb_statistical_analysis_method

def main():
    results = cpdb_statistical_analysis_method.call(
        cpdb_file_path='run/cpdb_db/cellphonedb.zip',
        meta_file_path='run/meta.tsv',
        counts_file_path='run/counts_normalized.h5ad',
        counts_data='hgnc_symbol',
        threshold=0.1, iterations=1000, pvalue=0.05, debug_seed=1337,
        score_interactions=True, threads=4, output_path='run/cpdb_out_reaudit_run1')
    return results

if __name__ == '__main__':
    results = main()
    print('RUN1_COMPLETED_NO_CRASH')
    print('pvalues shape', results['pvalues'].shape)
    print('means shape', results['means'].shape)
    results['pvalues'].to_csv('run/reaudit_cpdb_pvalues_run1.csv', index=False)
    results['significant_means'].to_csv('run/reaudit_cpdb_sigmeans_run1.csv', index=False)
