"""INPUT 5: SKILL.md blocks S12 (pseudobulk_junctions) and S13 (call + write leafcutter tables) run LITERALLY via exec, on the auditor's replicate-structured planted matrix.
Then: conservation, hand-check of one pseudobulk column, name-keyed join (shuffled metadata rows), and the loud-failure checks (RangeIndex, missing cells, NaN, too few replicates).
Run in WSL as-sc from run/out/in5 :  asenv as-sc python ../../41_pb_S12_S13.py"""
import numpy as np, pandas as pd, os, sys
R = '/mnt/openscience/audits/bio-single-cell-splicing/run'; D = f'{R}/data/pb_v2'
os.makedirs(f'{R}/out/in5', exist_ok=True); os.chdir(f'{R}/out/in5')
junction_counts = pd.read_csv(f'{D}/junction_counts.tsv', sep='\t', index_col=0)
cell_metadata = pd.read_csv(f'{D}/cell_metadata.tsv', sep='\t', index_col=0)
exec(open(f'{R}/blocks/S12_python.py', encoding='utf-8').read())          # defines pseudobulk_junctions
exec(open(f'{R}/blocks/S13_python.py', encoding='utf-8').read())          # pb, groups = ...; writes pb_counts.txt.gz, pb_groups.txt
print('pb shape', pb.shape, ' groups:', groups.group.value_counts().to_dict())
assert pb.shape == (450, 14) and int(pb.values.sum()) == int(junction_counts.values.sum())
print('ASSERT OK: 14 pseudobulks (7 donors x 2 types), total reads conserved =', int(pb.values.sum()))
m = ((cell_metadata.cell_type == 'T2') & (cell_metadata['sample'] == 'd3')).values
assert (junction_counts.loc[:, m].sum(1).values == pb['T2__d3'].values).all(); print('ASSERT OK: column T2__d3 == numpy mask sum over its', int(m.sum()), 'cells')
# name-keyed join: shuffle the metadata rows -> same pseudobulk
shuf = cell_metadata.sample(frac=1, random_state=1); pb2, g2 = pseudobulk_junctions(junction_counts, shuf)
assert pb2.equals(pb) and g2.equals(groups); print('ASSERT OK: shuffled metadata order gives identical pseudobulk (join is by cell id)')
# also shuffled COLUMN order of the matrix
pb3, _ = pseudobulk_junctions(junction_counts[junction_counts.columns[::-1]], cell_metadata); assert pb3[pb.columns].equals(pb); print('ASSERT OK: reversed matrix column order gives identical pseudobulk')
def expect_error(label, f):
    try: f(); print('NO ERROR (bad):', label)
    except Exception as e: print(f'raises {type(e).__name__}: {label}: {str(e)[:110]}')
expect_error('default RangeIndex metadata', lambda: pseudobulk_junctions(junction_counts, cell_metadata.reset_index()))
expect_error('metadata missing 10 cells', lambda: pseudobulk_junctions(junction_counts, cell_metadata.iloc[10:]))
mm = cell_metadata.copy(); mm.loc[mm.index[:3], 'sample'] = np.nan
expect_error('NaN sample for 3 cells', lambda: pseudobulk_junctions(junction_counts, mm))
mm = cell_metadata.copy(); mm['sample'] = mm['sample'].replace({f'd{i}': 'd1' for i in range(2, 8)})
expect_error('only 1 sample (donor) per type', lambda: pseudobulk_junctions(junction_counts, mm))
mm = cell_metadata.copy(); mm.index = [c.lower() + ' ' for c in mm.index]
expect_error('metadata ids differ from matrix ids (case/space)', lambda: pseudobulk_junctions(junction_counts, mm))
mm = cell_metadata[~cell_metadata.index.duplicated()].copy(); mm.loc['T1_d1_c1x'] = ['T1', 'd1']
print('extra metadata rows (cells absent from the matrix) tolerated:', pseudobulk_junctions(junction_counts, mm)[0].shape == pb.shape)
# what a user gets when the metadata has a sample column but a DUPLICATED index (two rows per cell)
dup = pd.concat([cell_metadata, cell_metadata.iloc[:2]])
expect_error('duplicated cell ids in metadata', lambda: pseudobulk_junctions(junction_counts, dup))
