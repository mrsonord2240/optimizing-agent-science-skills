"""INPUT 1/3: every helper in skill/examples/sc_splicing_brie2.py, run from the clean copy (no __pycache__: PYTHONDONTWRITEBYTECODE=1) on REAL data.
Run in WSL as-sc:  asenv as-sc python 13_in1_example_helpers.py"""
import sys, os, subprocess, numpy as np, pandas as pd, anndata as ad
R = '/mnt/openscience/audits/bio-single-cell-splicing/run'
S = os.environ['ASDATA'] + '/singlecell'
sys.path.insert(0, f'{R}/skill/examples')
import sc_splicing_brie2 as ex
O = f'{R}/out/ex_helpers'; os.makedirs(O, exist_ok=True)

# 1. fetch_splicing_events (network) + failure on bad species
ex.fetch_splicing_events('mouse', f'{O}/SE.gold.gff3', tier='gold')
n = sum(1 for l in open(f'{O}/SE.gold.gff3') if not l.startswith('#') and l.split('\t')[2] == 'gene')
print('fetch: gene rows', n); assert n > 1000 and open(f'{O}/SE.gold.gff3').read(200).startswith('#GFF3')
try: ex.fetch_splicing_events('zebrafish', f'{O}/x.gff3'); print('NO ERROR on bad species (bad)')
except KeyError as e: print('bad species -> KeyError', e)
os.remove(f'{O}/SE.gold.gff3')

# 2. count_splicing_reads on REAL 10x subset (droplet mode)
ex.count_splicing_reads(f'{S}/10xData/neuron_1k_v3_possorted_genome_bam.50events.bam', f'{S}/mouse_SE.lenient_50events.gff3', f'{O}/c10x', f'{S}/10xData/barcodes.tsv.gz', n_proc=8)
a10 = ad.read_h5ad(f'{O}/c10x/brie_count.h5ad'); u = (a10.layers['isoform1'] + a10.layers['isoform2']); u = np.asarray(u.todense() if hasattr(u, 'todense') else u)
print('10x cells x events', a10.shape, 'mean unique reads/cell/event %.4f' % u.mean())
assert a10.shape[1] == 50 and u.mean() < 0.1     # SKILL claim: < 0.1 per cell per event

# 3. run_brie2_inference on REAL Smart-seq2 (uses out/in1 counts + metadata)
q = ex.run_brie2_inference(f'{R}/out/in1/brie_counts/brie_count.h5ad', f'{R}/out/in1/cell_metadata.tsv', f'{O}/quant.h5ad')
print('run_brie2_inference ->', q.shape, 'Psi' in q.layers)
assert 'Psi' in q.layers and q.shape[0] == 130

# 4. find_variable_splicing (labels are ARBITRARY on real cells: only the mechanics are checked) vs hand computation
rng = np.random.default_rng(3); q.obs['cell_type'] = rng.choice(['t1', 't2'], q.n_obs)
var, mp = ex.find_variable_splicing(q, 'cell_type', 40)
ev0 = var.index[0]; i0 = list(q.var_names).index(ev0)
hand = {ct: float(np.nanmean(q.layers['Psi'][(q.obs.cell_type == ct).values, i0])) for ct in ['t1', 't2']}
print('find_variable_splicing top event', ev0, 'helper', mp.loc[ev0].round(6).to_dict(), 'hand', {k: round(v, 6) for k, v in hand.items()})
assert all(abs(mp.loc[ev0, k] - hand[k]) < 1e-6 for k in hand)

# 5. differential_splicing_per_cell on REAL cells with arbitrary labels: null -> expect ~no fdr<0.05
d = ex.differential_splicing_per_cell(q, (q.obs.cell_type == 't1').values, (q.obs.cell_type == 't2').values)
print('per-cell MWU on random labels: tested', len(d), 'fdr<0.05', int((d.fdr < 0.05).sum()), 'raw p<0.05', int((d.pvalue < 0.05).sum()))

# 6. pseudobulk_by_celltype on brie-count h5ad (sparse layers), REAL cells, arbitrary labels; conservation vs numpy
a = ad.read_h5ad(f'{R}/out/in1/brie_counts/brie_count.h5ad')
a.obs['cell_type'] = np.where(np.arange(a.n_obs) % 2 == 0, 'A', 'B'); a.obs['sample'] = [f's{(i // 2) % 4}' for i in range(a.n_obs)]
pb = ex.pseudobulk_by_celltype(a, 'cell_type', 'sample', min_cells=5, min_replicates=3, layer='isoform2')
tot = np.asarray(a.layers['isoform2'].sum()); print('pb shape', pb.shape, 'sum', pb.values.sum(), 'layer sum', tot)
assert pb.shape == (50, 8) and pb.values.sum() == tot
m = ((a.obs.cell_type == 'A') & (a.obs['sample'] == 's1')).values
assert (np.asarray(a.layers['isoform2'][m].sum(0)).ravel() == pb['A__s1'].values).all()
for kw, why in [(dict(min_replicates=5), 'too few replicates'), (dict(min_cells=100), 'min_cells too high')]:
    try: ex.pseudobulk_by_celltype(a, 'cell_type', 'sample', **{**dict(min_cells=5, min_replicates=3, layer='isoform2'), **kw}); print('NO ERROR', why)
    except ValueError as e: print('raises ValueError:', why)
try: ex.pseudobulk_by_celltype(a, 'cell_type', 'nosuch', layer='isoform2'); print('NO ERROR missing col')
except KeyError as e: print('raises KeyError missing column')
print('ALL HELPER ASSERTIONS OK')
