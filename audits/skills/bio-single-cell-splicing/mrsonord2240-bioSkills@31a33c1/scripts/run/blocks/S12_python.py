import numpy as np
import pandas as pd

def pseudobulk_junctions(junction_counts, cell_metadata, groupby='cell_type',
                         sample_col='sample', min_replicates=3):
    """junction_counts: junctions x cells. cell_metadata: one row per cell, INDEXED BY CELL ID,
    with columns groupby and sample_col. Returns (counts, groups): junctions x (cell type, sample)
    pseudobulks and a leafcutter groups table."""
    missing = junction_counts.columns.difference(cell_metadata.index)
    if len(missing):
        raise ValueError(f'{len(missing)} cells not in cell_metadata.index (set index=cell id): {list(missing[:3])}')
    meta = cell_metadata.loc[junction_counts.columns, [groupby, sample_col]]
    if meta.isna().any().any():
        raise ValueError(f'NaN in {groupby!r} or {sample_col!r}: those cells would be dropped')
    pb = junction_counts.T.groupby([meta[groupby].to_numpy(), meta[sample_col].to_numpy()]).sum().T
    assert pb.to_numpy().sum() == junction_counts.to_numpy().sum()   # every read kept
    groups = pd.DataFrame({'sample': [f'{g}__{s}' for g, s in pb.columns],
                           'group': [g for g, _ in pb.columns]})
    n_rep = groups.group.value_counts()
    if (n_rep < min_replicates).any():
        raise ValueError(f'need >= {min_replicates} samples per {groupby}; got {n_rep.to_dict()}')
    pb.columns = groups['sample']
    return pb, groups
