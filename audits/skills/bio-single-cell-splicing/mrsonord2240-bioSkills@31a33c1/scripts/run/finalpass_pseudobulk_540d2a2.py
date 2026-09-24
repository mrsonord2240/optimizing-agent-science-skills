import numpy as np
import pandas as pd

def pseudobulk_junctions(junction_counts, cell_metadata, groupby='cell_type', sample_col='sample', min_replicates=3):
    missing = junction_counts.columns.difference(cell_metadata.index)
    if len(missing):
        raise ValueError(f'{len(missing)} cells not in cell_metadata.index: {list(missing[:3])}')
    meta = cell_metadata.loc[junction_counts.columns, [groupby, sample_col]]
    if meta.isna().any().any():
        raise ValueError(f'NaN in {groupby!r} or {sample_col!r}: those cells would be dropped')
    pb = junction_counts.T.groupby([meta[groupby].to_numpy(), meta[sample_col].to_numpy()]).sum().T
    assert pb.to_numpy().sum() == junction_counts.to_numpy().sum()
    groups = pd.DataFrame({'sample': [f'{g}__{s}' for g, s in pb.columns],
                           'group': [g for g, _ in pb.columns]})
    n_rep = groups.group.value_counts()
    if (n_rep < min_replicates).any():
        raise ValueError(f'need >= {min_replicates} samples per {groupby}; got {n_rep.to_dict()}')
    pb.columns = groups['sample']
    return pb, groups

cells = [f'{group}_{sample}_{rep}' for group in 'AB' for sample in ('d1','d2','d3') for rep in (1,2)]
counts = pd.DataFrame(np.arange(36).reshape(3, 12), columns=cells)
meta = pd.DataFrame({
    'cell_type': [c.split('_')[0] for c in cells],
    'sample': [c.split('_')[1] for c in cells]}, index=cells).sample(frac=1, random_state=9)
pb, groups = pseudobulk_junctions(counts, meta)
assert pb.shape == (3, 6) and groups.groupby('group').size().to_dict() == {'A': 3, 'B': 3}
try:
    pseudobulk_junctions(counts, meta.reset_index(drop=True))
except ValueError:
    pass
else:
    raise AssertionError('RangeIndex must fail')
print('PASS pseudobulk reads=', counts.to_numpy().sum(), ' columns=', list(pb.columns), sep='')
