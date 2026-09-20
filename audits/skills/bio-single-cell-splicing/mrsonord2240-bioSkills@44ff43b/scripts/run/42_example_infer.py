"""Call the example module's run_brie2_inference() and prepare_splicing_events() as shipped (from the COPY)."""
import sys, os, subprocess
sys.path.insert(0,'/mnt/openscience/audits/bio-single-cell-splicing/run/skill/examples')
import sc_splicing_brie2 as ex
R='/mnt/openscience/audits/bio-single-cell-splicing/run'
a = ex.run_brie2_inference(f'{R}/out/planted_ss2/counts/brie_count.h5ad', f'{R}/data/synth_ss2/cellfeat.tsv', f'{R}/out/example_quant.h5ad')
print('returned', type(a), a.shape, 'layers', list(a.layers.keys()))
assert 'Psi' in a.layers; print('ASSERT OK: example run_brie2_inference returns AnnData with Psi layer')
try:
    ex.prepare_splicing_events('nonexistent.gtf', f'{R}/out/ev.gff3')
except Exception as e:
    print('prepare_splicing_events ->', type(e).__name__, str(e)[:160])
