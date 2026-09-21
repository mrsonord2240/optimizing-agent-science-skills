"""Input 3: droplet (10x 3'-like) planted data through the example script's count_splicing_reads() (brie-count -s -b), then quantify
junction-read yield per cell per event for events whose cassette exon is near vs far from the poly(A) end; then brie-quant."""
import sys, os, subprocess, numpy as np, pandas as pd, scanpy as sc
sys.path.insert(0,'/mnt/openscience/audits/bio-single-cell-splicing/run/skill/examples')
import sc_splicing_brie2 as ex
R='/mnt/openscience/audits/bio-single-cell-splicing/run'; D=f'{R}/data/synth_10x'; O=f'{R}/out/planted_10x'
os.makedirs(O, exist_ok=True)
ex.count_splicing_reads(f'{D}/bams/synth10x.bam', f'{D}/events.gff3', O+'/counts', f'{D}/barcodes.tsv', n_proc=8)
a = sc.read_h5ad(f'{O}/counts/brie_count.h5ad'); print(a)
truth = pd.read_csv(f'{D}/truth.tsv', sep='\t', keep_default_na=False).set_index('gene').loc[a.var_names]
dense = lambda m: np.asarray(m.todense() if hasattr(m,'todense') else m)
i1, i2, amb, poor = [dense(a.layers[k]) for k in ['isoform1','isoform2','ambiguous','poorQual']]
junc = i1 + i2  # brie unique reads = reads that discriminate the isoforms
for lay in ['near3','far3']:
    m = (truth.layout==lay).values
    print(f'{lay}: n events {m.sum()}, mean unique(isoform1+isoform2) reads per cell per event {junc[:,m].mean():.4f}; '
          f'frac cell-event >=5 unique {((junc[:,m])>=5).mean():.4f}; ambiguous mean {amb[:,m].mean():.3f}; poorQual mean {poor[:,m].mean():.3f}')
assert junc[:, (truth.layout=='far3').values].sum() == 0, 'far-3prime events unexpectedly have discriminating reads'
print('ASSERT: far3 events (cassette exon >1.5 kb from polyA) yield 0 discriminating reads with 10x-3 style reads')
# quantify with defaults + the Skill flags; cell feature = planted group
cells = pd.read_csv(f'{D}/cells.tsv', sep='\t').set_index('cell')
cf = pd.DataFrame({'grp01': (cells.group=='B').astype(int)}); cf.to_csv(f'{O}/cellfeat.tsv', sep='\t')
try:
    p = subprocess.run(['brie-quant','-i',f'{O}/counts/brie_count.h5ad','-c',f'{O}/cellfeat.tsv','-o',f'{O}/quant.h5ad','--interceptMode','gene','--LRTindex','All','--testBase','null','-p','8'],capture_output=True,text=True)
    print('brie-quant rc', p.returncode); print((p.stdout+p.stderr).replace('\r','\n')[-600:])
except Exception as e:
    print('ERR', e)
if os.path.exists(f'{O}/quant.h5ad'):
    q = sc.read_h5ad(f'{O}/quant.h5ad'); print(q)
    t = truth.loc[q.var_names]
    print(t.groupby(['layout','cls']).size())
    f = q.varm['fdr'][:,0]
    res = pd.DataFrame({'layout':t.layout,'cls':t.cls,'fdr':f})
    print(res.groupby(['layout','cls']).agg(n=('fdr','size'), n_fdr05=('fdr',lambda x:(x<0.05).sum())))
else:
    print('no quant output written: brie-quant filtered all genes or failed')
