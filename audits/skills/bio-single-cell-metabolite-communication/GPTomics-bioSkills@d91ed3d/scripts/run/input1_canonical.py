"""Input 1 (Canonical): "Run MEBOCOST on my annotated scRNA-seq data and filter on
permutation FDR" -- following the Skill's SKILL.md 'Run MEBOCOST' + 'Filter and
Summarize Results' code patterns verbatim (adapted only for our local paths).

NOTE (audit finding, P0): SKILL.md's own code block is a flat top-level script with
no `if __name__ == '__main__':` guard. Run exactly as documented, it crashes on
Windows with:
    RuntimeError: An attempt has been made to start a new process before the
    current process has finished its bootstrapping phase ...
because mebocost.infer_commu() -> crosstalk_calculator._shuffling_() calls
multiprocessing.Pool(thread) internally (thread=8 by default in the example), and
Windows' 'spawn' start method re-imports the top-level script in each worker,
re-triggering Pool() recursively. This is the same defect class flagged in
tools/mebocost-venv testing and matches a finding already recorded for
single-cell/cell-communication's cellphonedb example in this env's TOOLS.md.
The guard below is the auditor's fix to make the code runnable for scoring; it is
NOT how SKILL.md instructs the user to write the script.
"""
import time


def main():
    from mebocost import mebocost
    import scanpy as sc

    t0 = time.time()

    adata = sc.read_h5ad('adata_annotated.h5ad')   # log-normalized, gene SYMBOLS not Ensembl IDs

    # config_path points to mebocost.conf listing the metabolite-enzyme-sensor database paths
    # cutoff_prop=0.15: a gene must be expressed in >=15% of a group to count (dropout floor)
    # species MUST match the data: mouse data against the human enzyme/sensor DB returns almost nothing
    mebo = mebocost.create_obj(adata=adata, group_col='cell_type', condition_col=None,
                               met_est='mebocost', config_path='./mebocost.conf', species='human',
                               cutoff_exp='auto', cutoff_met='auto', cutoff_prop=0.15,
                               sensor_type='All', thread=8)

    # n_shuffle=1000: label-permutation null for FDR; min_cell_number=10 drops tiny groups
    commu_res = mebo.infer_commu(n_shuffle=1000, seed=12345, Return=True,
                                 min_cell_number=10, pval_method='permutation_test_fdr',
                                 pval_cutoff=0.05, thread=None)

    print('=== commu_res shape ===', commu_res.shape)
    print('=== columns ===', list(commu_res.columns))

    sig = commu_res[commu_res['permutation_test_fdr'] < 0.05].copy()
    print(f'\nTotal tested: {len(commu_res)}  Significant (FDR<0.05): {len(sig)}')

    sig['pair'] = sig['Sender'] + ' -> ' + sig['Receiver']
    print('\nTop metabolites:')
    print(sig['Metabolite_Name'].value_counts().head(10))
    print('\nTop sender -> receiver pairs:')
    print(sig['pair'].value_counts().head(10))

    print('\n--- Check for expected biology (adenosine Myeloid->TCell, PGE2 ->TCell) ---')
    check = sig[sig['Metabolite_Name'].isin(['Adenosine', 'Prostaglandin E2'])]
    print(check[['Sender', 'Receiver', 'Metabolite_Name', 'Sensor', 'Annotation',
                 'Commu_Score', 'permutation_test_fdr']].to_string())

    commu_res.to_csv('input1_full_result.csv', index=False)
    sig.to_csv('input1_significant.csv', index=False)
    print(f'\nElapsed: {time.time()-t0:.1f}s')


if __name__ == '__main__':
    main()
