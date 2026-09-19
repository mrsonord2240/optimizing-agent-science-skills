"""Input 4 (Variant B): "Compare metabolite communication between tumor and normal
tissue" -- follows SKILL.md 'Compare Conditions' pattern (per-condition subset loop).

NOTE (audit): wrapped in main()/if __name__=='__main__' -- see input1_canonical.py
header for why (mebocost.infer_commu uses multiprocessing.Pool internally; SKILL.md's
own code is a flat top-level script and is not Windows-safe as written).
"""
import time
from mebocost import mebocost
import scanpy as sc


def main():
    t0 = time.time()
    adata = sc.read_h5ad('adata_annotated.h5ad')

    results = {}
    for cond in adata.obs['condition'].unique():
        sub = adata[adata.obs['condition'] == cond].copy()
        obj = mebocost.create_obj(adata=sub, group_col='cell_type', met_est='mebocost',
                                  config_path='./mebocost.conf', species='human',
                                  cutoff_prop=0.15, thread=8)
        results[cond] = obj.infer_commu(n_shuffle=1000, seed=12345, Return=True,
                                        min_cell_number=10, pval_cutoff=0.05)

    for cond, res in results.items():
        sig = res[res['permutation_test_fdr'] < 0.05]
        print(f'\n=== Condition: {cond} ===  tested={len(res)} significant={len(sig)}')
        check = sig[sig['Metabolite_Name'].isin(['Adenosine', 'Prostaglandin E2'])]
        print(check[['Sender', 'Receiver', 'Metabolite_Name', 'Sensor', 'Commu_Score',
                     'permutation_test_fdr']].to_string())
        res.to_csv(f'input4_{cond}_full.csv', index=False)

    # Differential framing: significant in tumor only = hypothesis for metabolomics follow-up
    tumor_sig = set(results['tumor'][results['tumor']['permutation_test_fdr'] < 0.05]
                    .apply(lambda r: (r['Sender'], r['Receiver'], r['Metabolite_Name']), axis=1))
    normal_sig = set(results['normal'][results['normal']['permutation_test_fdr'] < 0.05]
                     .apply(lambda r: (r['Sender'], r['Receiver'], r['Metabolite_Name']), axis=1))
    tumor_only = tumor_sig - normal_sig
    print(f'\nTumor-only significant triples (Sender, Receiver, Metabolite): {len(tumor_only)}')
    for t in sorted(tumor_only):
        print(' ', t)

    print(f'\nElapsed: {time.time()-t0:.1f}s')


if __name__ == '__main__':
    main()
