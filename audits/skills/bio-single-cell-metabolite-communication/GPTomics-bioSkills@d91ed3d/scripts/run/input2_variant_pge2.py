"""Input 2 (Variant A): "Which cells express the enzymes for prostaglandin E2 and which
express its sensors?" -- follows SKILL.md 'Run MEBOCOST' then the usage-guide's
analyze_specific_metabolite() pattern from examples/metabolite_communication.py.
"""
import time
from mebocost import mebocost
import scanpy as sc

# NOTE (audit): wrapped in main()/if __name__=='__main__' -- see input1_canonical.py
# header for why: mebocost.infer_commu() uses multiprocessing.Pool internally and
# SKILL.md's own examples do not guard against Windows spawn re-import.


def analyze_specific_metabolite(commu_res, metabolite, fdr_threshold=0.05):
    sig = commu_res[(commu_res['Metabolite_Name'] == metabolite) &
                    (commu_res['permutation_test_fdr'] < fdr_threshold)]
    if len(sig) == 0:
        print(f'No significant {metabolite} communication')
        return None
    print(f'\n{metabolite}: machinery consistent with sender -> receiver flow')
    for _, row in sig.iterrows():
        print(f"  {row['Sender']} -> {row['Receiver']} via {row['Sensor']} "
              f"(score {row['Commu_Score']:.3f}, FDR {row['permutation_test_fdr']:.4f})")
    return sig

def main():
    t0 = time.time()
    adata = sc.read_h5ad('adata_annotated.h5ad')

    mebo = mebocost.create_obj(adata=adata, group_col='cell_type', condition_col=None,
                               met_est='mebocost', config_path='./mebocost.conf', species='human',
                               cutoff_exp='auto', cutoff_met='auto', cutoff_prop=0.15,
                               sensor_type='All', thread=8)

    commu_res = mebo.infer_commu(n_shuffle=1000, seed=12345, Return=True,
                                 min_cell_number=10, pval_method='permutation_test_fdr',
                                 pval_cutoff=0.05, thread=None)

    result = analyze_specific_metabolite(commu_res, 'Prostaglandin E2')
    if result is not None:
        result.to_csv('input2_pge2_significant.csv', index=False)

    print(f'\nElapsed: {time.time()-t0:.1f}s')


if __name__ == '__main__':
    main()
