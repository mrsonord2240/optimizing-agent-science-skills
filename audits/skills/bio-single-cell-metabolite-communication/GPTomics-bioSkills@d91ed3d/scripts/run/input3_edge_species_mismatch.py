"""Input 3 (Edge/boundary): user runs MEBOCOST with gene symbols in mouse casing
(e.g. 'Nt5e', 'Adora2a') against species='human' -- the exact failure mode the
Skill's Common Errors table documents ("Almost no metabolites detected... species
does not match the data"). Confirms the Skill's documented diagnosis actually
matches the tool's real behavior. Wrapped in main()/__main__ guard defensively
(this path fails before reaching multiprocessing, but keep the pattern consistent).
"""
import time
from mebocost import mebocost
import scanpy as sc


def main():
    t0 = time.time()
    adata = sc.read_h5ad('adata_mouse_labeled.h5ad')  # var_names are 'Nt5e', 'Adora2a', etc.

    try:
        mebo = mebocost.create_obj(adata=adata, group_col='cell_type', condition_col=None,
                                   met_est='mebocost', config_path='./mebocost.conf', species='human',
                                   cutoff_exp='auto', cutoff_met='auto', cutoff_prop=0.15,
                                   sensor_type='All', thread=8)
        commu_res = mebo.infer_commu(n_shuffle=1000, seed=12345, Return=True,
                                     min_cell_number=10, pval_method='permutation_test_fdr',
                                     pval_cutoff=0.05, thread=None)
        sig = commu_res[commu_res['permutation_test_fdr'] < 0.05]
        print(f'Total tested: {len(commu_res)}  Significant: {len(sig)}')
        print('STATUS: ran to completion (no hard error) -- check whether output is near-empty as documented')
    except KeyError as e:
        print(f'STATUS: raised KeyError as expected by low gene overlap: {e}')
    except Exception as e:
        print(f'STATUS: raised {type(e).__name__}: {e}')

    print(f'\nElapsed: {time.time()-t0:.1f}s')


if __name__ == '__main__':
    main()
