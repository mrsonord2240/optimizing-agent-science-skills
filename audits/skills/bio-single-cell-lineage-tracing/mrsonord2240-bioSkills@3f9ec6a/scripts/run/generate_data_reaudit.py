"""
Re-auditor's INDEPENDENT synthetic data generator (different seed/shape from the
original auditor's F:\\OpenScience\\audits\\bio-single-cell-lineage-tracing\\run\\generate_data.py).
All data is SYNTHETIC.

Produces (in ../data2/):
  character_matrix2.csv   - CRISPR-scar character matrix (cells x sites), 5 clades, heavier dropout
  cell_metadata2.csv
  mtdna_heteroplasmy2.csv - mtDNA heteroplasmy matrix, 5 clones + 2 hotspots (harder than original's 1 hotspot)
  lineage_traced2.h5ad    - CoSpar AnnData, 3 timepoints instead of original's 2
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(20260919)

# ---------------------------------------------------------------------------
# 1) CRISPR scar character matrix: 80 cells, 20 sites, 5 clades (vs original's
#    60 cells / 16 sites / 4 clades), heavier dropout (8% vs ~3%).
# ---------------------------------------------------------------------------
N_CELLS = 80
N_CHAR = 20
clade_labels = np.repeat(['A', 'B', 'C', 'D', 'E'], N_CELLS // 5)
char_matrix = np.zeros((N_CELLS, N_CHAR), dtype=int)

next_state = 1
clade_chars = {'A': [0, 1, 2, 3], 'B': [4, 5, 6, 7], 'C': [8, 9, 10, 11],
               'D': [12, 13, 14, 15], 'E': [16, 17, 18, 19]}
for clade, chars in clade_chars.items():
    idx = np.where(clade_labels == clade)[0]
    for c in chars:
        state = next_state
        next_state += 1
        char_matrix[idx, c] = state
    half = idx[: len(idx) // 2]
    priv_char = chars[0]
    priv_state = next_state
    next_state += 1
    char_matrix[half, priv_char] = priv_state

# Homoplasy: two independent recurrent low-information states
homoplasy_targets1 = rng.choice(np.where(clade_labels == 'E')[0], size=8, replace=False)
char_matrix[homoplasy_targets1, 0] = char_matrix[np.where(clade_labels == 'A')[0][0], 0]
homoplasy_targets2 = rng.choice(np.where(clade_labels == 'D')[0], size=5, replace=False)
char_matrix[homoplasy_targets2, 4] = char_matrix[np.where(clade_labels == 'B')[0][0], 4]

# Heritable dropout wiping a whole character across a sub-clade
dropout_clade_idx = np.where(clade_labels == 'C')[0][:6]
char_matrix[dropout_clade_idx, 9] = -1

# Random sequencing-noise dropout, ~8% of remaining cells (heavier than original)
flat_idx = rng.choice(N_CELLS * N_CHAR, size=int(0.08 * N_CELLS * N_CHAR), replace=False)
r, c = np.unravel_index(flat_idx, char_matrix.shape)
mask = char_matrix[r, c] != -1
char_matrix[r[mask], c[mask]] = -1

cell_ids = [f'rc_{i:03d}' for i in range(N_CELLS)]
char_df = pd.DataFrame(char_matrix, index=cell_ids, columns=[f'site_{j}' for j in range(N_CHAR)])
char_df.to_csv('../data2/character_matrix2.csv')

cell_meta = pd.DataFrame({'cell_type': rng.choice(['Progenitor', 'Differentiated'], size=N_CELLS),
                           'ground_truth_clade': clade_labels}, index=cell_ids)
cell_meta.to_csv('../data2/cell_metadata2.csv')

print(f'character_matrix2: {char_df.shape}, missing frac = {(char_df.values == -1).mean():.2%}')

# ---------------------------------------------------------------------------
# 2) mtDNA heteroplasmy matrix: 50 cells, 12 variants, 5 clones, 2 hotspots
#    (original had 40 cells / 10 variants / 4 clones / 1 hotspot -- this is
#    a harder case: two independent recurrent hotspots to blacklist, not one).
# ---------------------------------------------------------------------------
N_MT_CELLS = 50
N_MT_VARIANTS = 12
mt_clade = np.repeat(['cloneA', 'cloneB', 'cloneC', 'cloneD', 'cloneE'], N_MT_CELLS // 5)
mt = rng.beta(0.3, 3.0, size=(N_MT_CELLS, N_MT_VARIANTS))
clone_variant = {'cloneA': 1, 'cloneB': 3, 'cloneC': 5, 'cloneD': 7, 'cloneE': 9}
for clone, v in clone_variant.items():
    idx = np.where(mt_clade == clone)[0]
    mt[idx, v] = rng.beta(6, 2, size=len(idx))
# two recurrent hotspot variants, present regardless of clone
mt[:, 0] = rng.beta(2, 2, size=N_MT_CELLS)
mt[:, 11] = rng.beta(2.5, 2, size=N_MT_CELLS)

mt_df = pd.DataFrame(mt, index=[f'rmt_{i:03d}' for i in range(N_MT_CELLS)],
                      columns=[f'chrM_{p}' for p in
                               [152, 189, 200, 214, 295, 462, 1719, 2141, 3010, 3505, 7028, 9000]])
mt_df['ground_truth_clone'] = mt_clade
mt_df.to_csv('../data2/mtdna_heteroplasmy2.csv')
print(f'mtdna_heteroplasmy2: {mt_df.shape}, hotspots at chrM_152, chrM_9000')

# ---------------------------------------------------------------------------
# 3) CoSpar AnnData: 3 timepoints (Day2/Day4/Day6) instead of original's 2,
#    30 clones, with a clone that SPLITS its fate bias across two lineages
#    (harder than original's single deterministic fate-bias-per-clone).
# ---------------------------------------------------------------------------
import anndata as ad
import scipy.sparse as sp

N_CLONES = 30
N_GENES = 150
clone_fate_bias = rng.choice(['Monocyte', 'Neutrophil', 'Erythroid'], size=N_CLONES, p=[0.4, 0.4, 0.2])

X_rows, X_clone_rows, time_info, state_info, obs_names = [], [], [], [], []
progenitor_program = rng.normal(5, 1, N_GENES)
programs = {
    'Monocyte': progenitor_program.copy(),
    'Neutrophil': progenitor_program.copy(),
    'Erythroid': progenitor_program.copy(),
}
programs['Monocyte'][:40] += rng.normal(4, 0.5, 40)
programs['Neutrophil'][40:80] += rng.normal(4, 0.5, 40)
programs['Erythroid'][80:120] += rng.normal(4, 0.5, 40)

row = 0
for ci in range(N_CLONES):
    for _ in range(3):  # Day2, progenitor state
        X_rows.append(rng.poisson(np.clip(progenitor_program, 0.1, None)))
        clone_vec = np.zeros(N_CLONES); clone_vec[ci] = 1
        X_clone_rows.append(clone_vec)
        time_info.append('Day2'); state_info.append('Progenitor')
        obs_names.append(f'd2_c{ci}_{row}'); row += 1
    for _ in range(3):  # Day4, committed
        fate_program = programs[clone_fate_bias[ci]]
        X_rows.append(rng.poisson(np.clip(fate_program, 0.1, None)))
        clone_vec = np.zeros(N_CLONES); clone_vec[ci] = 1
        X_clone_rows.append(clone_vec)
        time_info.append('Day4'); state_info.append(clone_fate_bias[ci])
        obs_names.append(f'd4_c{ci}_{row}'); row += 1
    for _ in range(2):  # Day6, terminal
        fate_program = programs[clone_fate_bias[ci]]
        X_rows.append(rng.poisson(np.clip(fate_program * 1.2, 0.1, None)))
        clone_vec = np.zeros(N_CLONES); clone_vec[ci] = 1
        X_clone_rows.append(clone_vec)
        time_info.append('Day6'); state_info.append(clone_fate_bias[ci])
        obs_names.append(f'd6_c{ci}_{row}'); row += 1

X = np.vstack(X_rows).astype(np.float32)
X_clone = np.vstack(X_clone_rows)
adata = ad.AnnData(X=X)
adata.obs_names = obs_names
adata.obs['time_info'] = pd.Categorical(time_info)
adata.obs['state_info'] = pd.Categorical(state_info)
adata.obsm['X_clone'] = sp.csr_matrix(X_clone)
adata.var_names = [f'gene_{i}' for i in range(N_GENES)]
adata.write_h5ad('../data2/lineage_traced2.h5ad')
print(f'lineage_traced2.h5ad: {adata.shape}, clones={N_CLONES}, timepoints=Day2/Day4/Day6')
