"""
Synthetic data generator for the bio-single-cell-lineage-tracing audit.
All data below is SYNTHETIC, generated with fixed seeds for reproducibility.

Produces:
  data/character_matrix.csv   - CRISPR-scar character matrix (cells x sites)
  data/cell_metadata.csv      - cell_type + ground-truth clade for the scar cells
  data/lineage_traced.h5ad    - AnnData for CoSpar (X_clone, time_info, state_info)
  data/mtdna_heteroplasmy.csv - synthetic mtDNA variant heteroplasmy matrix
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# 1) CRISPR scar character matrix with an explicit ground-truth binary tree,
#    plus injected homoplasy (recurrent scars) and dropout (-1).
# ---------------------------------------------------------------------------
N_CELLS = 60
N_CHAR = 16

# Ground truth: a balanced binary clade structure, 4 top-level clades (A-D),
# each edited on a disjoint set of characters early, then further edits later.
clade_labels = np.repeat(['A', 'B', 'C', 'D'], N_CELLS // 4)
char_matrix = np.zeros((N_CELLS, N_CHAR), dtype=int)

next_state = 1
clade_chars = {'A': [0, 1, 2, 3], 'B': [4, 5, 6, 7], 'C': [8, 9, 10, 11], 'D': [12, 13, 14, 15]}
for clade, chars in clade_chars.items():
    idx = np.where(clade_labels == clade)[0]
    for c in chars:
        # within-clade cells mostly share the same scar state at their clade's sites
        state = next_state
        next_state += 1
        char_matrix[idx, c] = state
    # add some within-clade private mutations (later, sub-clade splits)
    half = idx[: len(idx) // 2]
    priv_char = chars[0]
    priv_state = next_state
    next_state += 1
    char_matrix[half, priv_char] = priv_state

# Homoplasy: force a frequent low-information indel state (state value 1) to
# recur independently in an unrelated clade (classic Cas9 recurrent-indel case).
homoplasy_targets = rng.choice(np.where(clade_labels == 'D')[0], size=6, replace=False)
char_matrix[homoplasy_targets, 0] = char_matrix[np.where(clade_labels == 'A')[0][0], 0]

# Dropout: heritable excision dropout wipes a whole character across a random
# sub-clade (should NOT be coded as 0/unedited).
dropout_clade_idx = np.where(clade_labels == 'B')[0][:5]
char_matrix[dropout_clade_idx, 5] = -1

# Random sequencing-noise dropout, sparse, across the rest of the matrix
flat_idx = rng.choice(N_CELLS * N_CHAR, size=20, replace=False)
r, c = np.unravel_index(flat_idx, char_matrix.shape)
mask = char_matrix[r, c] != -1
char_matrix[r[mask], c[mask]] = -1

cell_ids = [f'cell_{i:03d}' for i in range(N_CELLS)]
char_df = pd.DataFrame(char_matrix, index=cell_ids, columns=[f'site_{j}' for j in range(N_CHAR)])
char_df.to_csv('../data/character_matrix.csv')

cell_meta = pd.DataFrame({'cell_type': rng.choice(['Progenitor', 'Differentiated'], size=N_CELLS),
                           'ground_truth_clade': clade_labels}, index=cell_ids)
cell_meta.to_csv('../data/cell_metadata.csv')

print(f'character_matrix: {char_df.shape}, missing frac = {(char_df.values == -1).mean():.2%}')

# ---------------------------------------------------------------------------
# 2) Synthetic mtDNA heteroplasmy matrix (cells x variant sites, 0-1 continuous)
#    for the "group clonally related cells from mtDNA" scenario.
# ---------------------------------------------------------------------------
N_MT_CELLS = 40
N_MT_VARIANTS = 10
mt_clade = np.repeat(['clone1', 'clone2', 'clone3', 'clone4'], N_MT_CELLS // 4)
mt = rng.beta(0.3, 3.0, size=(N_MT_CELLS, N_MT_VARIANTS))  # background low heteroplasmy noise
clone_variant = {'clone1': 0, 'clone2': 2, 'clone3': 5, 'clone4': 7}
for clone, v in clone_variant.items():
    idx = np.where(mt_clade == clone)[0]
    mt[idx, v] = rng.beta(6, 2, size=len(idx))  # high heteroplasmy = clone-defining variant
# one hotspot variant recurrent across clones (homoplasy in mtDNA)
mt[:, 9] = rng.beta(2, 2, size=N_MT_CELLS)

mt_df = pd.DataFrame(mt, index=[f'mtcell_{i:03d}' for i in range(N_MT_CELLS)],
                      columns=[f'chrM_{p}' for p in [73, 150, 263, 310, 750, 1438, 2706, 3107, 4769, 8860]])
mt_df['ground_truth_clone'] = mt_clade
mt_df.to_csv('../data/mtdna_heteroplasmy.csv')
print(f'mtdna_heteroplasmy: {mt_df.shape}')

# ---------------------------------------------------------------------------
# 3) Synthetic LARRY-style AnnData for CoSpar: two timepoints, clonal barcodes,
#    and a deliberate "state does not predict fate" structure -- within one
#    transcriptomic cluster at day 2, cells from different clones are biased
#    toward different day-4 fates despite indistinguishable day-2 expression.
# ---------------------------------------------------------------------------
import anndata as ad
import scipy.sparse as sp

N_CLONES = 25
CELLS_PER_CLONE_D2 = 4
CELLS_PER_CLONE_D4 = 4
n_cells_total = N_CLONES * (CELLS_PER_CLONE_D2 + CELLS_PER_CLONE_D4)
N_GENES = 200

clone_fate_bias = rng.choice(['Monocyte', 'Neutrophil'], size=N_CLONES, p=[0.5, 0.5])

X = np.zeros((n_cells_total, N_GENES))
X_clone = np.zeros((n_cells_total, N_CLONES))
time_info = []
state_info = []
obs_names = []

row = 0
# shared "progenitor" expression program for ALL day-2 cells regardless of fate bias
# (this is the point: day-2 state is indistinguishable across clones)
progenitor_program = rng.normal(5, 1, N_GENES)
mono_program = progenitor_program.copy()
mono_program[:50] += rng.normal(4, 0.5, 50)
neut_program = progenitor_program.copy()
neut_program[50:100] += rng.normal(4, 0.5, 50)

for ci in range(N_CLONES):
    for _ in range(CELLS_PER_CLONE_D2):
        X[row] = rng.poisson(np.clip(progenitor_program, 0.1, None))
        X_clone[row, ci] = 1
        time_info.append('Day2')
        state_info.append('Progenitor')
        obs_names.append(f'd2_clone{ci}_{row}')
        row += 1
    fate_program = mono_program if clone_fate_bias[ci] == 'Monocyte' else neut_program
    for _ in range(CELLS_PER_CLONE_D4):
        X[row] = rng.poisson(np.clip(fate_program, 0.1, None))
        X_clone[row, ci] = 1
        time_info.append('Day4')
        state_info.append(clone_fate_bias[ci])
        obs_names.append(f'd4_clone{ci}_{row}')
        row += 1

adata = ad.AnnData(X=X.astype(np.float32))
adata.obs_names = obs_names
adata.obs['time_info'] = pd.Categorical(time_info)
adata.obs['state_info'] = pd.Categorical(state_info)
adata.obsm['X_clone'] = sp.csr_matrix(X_clone)
adata.var_names = [f'gene_{i}' for i in range(N_GENES)]
adata.write_h5ad('../data/lineage_traced.h5ad')
print(f'lineage_traced.h5ad: {adata.shape}, clones={N_CLONES}, '
      f'day2 cells={sum(t=="Day2" for t in time_info)}, day4 cells={sum(t=="Day4" for t in time_info)}')
print('clone fate bias ground truth (first 10):', dict(list(zip(range(10), clone_fate_bias[:10]))))
