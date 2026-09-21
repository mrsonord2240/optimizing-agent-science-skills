"""INPUT 1 (real): pysam cross-check of S05 brie-count output: inspect brie-count output on real Smart-seq2 and cross-check the counts with pysam (independent method).
Run inside WSL env as-sc:  asenv as-sc python 02_brie_real_check.py
"""
import sys, os, json
import numpy as np, pandas as pd, anndata as ad, pysam

R = '/mnt/openscience/audits/bio-single-cell-splicing/run'
a = ad.read_h5ad(f'{R}/out/in1/brie_counts/brie_count.h5ad')
print(a)
print('layers', list(a.layers.keys()))
print('var cols', list(a.var.columns))
print(a.var.head(3))

# events from the GFF3: SE event = gene with .in (3 exons) and .out (2 exons)
gff = pd.read_csv(f'/mnt/openscience/audit-envs/alternative-splicing/public-data/singlecell/mouse_SE.lenient_50events.gff3', sep='\t', comment='#', header=None)
ev = {}
for _, r in gff.iterrows():
    if r[2] != 'exon':
        continue
    attrs = dict(kv.split('=') for kv in r[8].split(';'))
    tid = attrs['Parent']
    ev.setdefault(tid, []).append((r[0], int(r[3]), int(r[4]), r[6]))
genes = sorted({t.rsplit('.', 1)[0] for t in ev})
print('n genes', len(genes))

# pysam: count reads with a N gap exactly matching each junction (1-based exon coords -> 0-based intron [e1_end, e3_start-1))
cells = list(a.obs_names)
inc1 = np.zeros((len(cells), len(genes))); inc2 = np.zeros_like(inc1); skip = np.zeros_like(inc1)
gi = {g: i for i, g in enumerate(genes)}
for ci, c in enumerate(cells):
    bam = pysam.AlignmentFile(f'/mnt/openscience/audit-envs/alternative-splicing/public-data/singlecell/bams_SS2/{c}.sorted.bam')
    for g in genes:
        ex_in = sorted(ev[g + '.in'], key=lambda x: x[1])
        chrom = ex_in[0][0]
        (s1, e1), (s2, e2), (s3, e3) = [(x[1], x[2]) for x in ex_in]
        J = {'inc1': (e1, s2 - 1), 'inc2': (e2, s3 - 1), 'skip': (e1, s3 - 1)}  # (intron start 1-based = e1+1 -> 0-based e1 ; end 0-based excl = s2-1)
        for rd in bam.fetch(chrom, s1 - 1, e3):
            if rd.is_unmapped or rd.is_secondary or rd.is_supplementary:
                continue
            pos = rd.reference_start
            for op, ln in rd.cigartuples:
                if op == 3:
                    j = (pos, pos + ln)
                    for k, jj in J.items():
                        if j == jj:
                            {'inc1': inc1, 'inc2': inc2, 'skip': skip}[k][ci, gi[g]] += 1
                if op in (0, 2, 3, 7, 8):
                    pos += ln
    bam.close()
print('pysam total: inc1', inc1.sum(), 'inc2', inc2.sum(), 'skip', skip.sum())
for l in a.layers.keys():
    print('brie layer', l, 'total', np.asarray(a.layers[l].sum()))
# align gene order
order = [list(a.var_names).index(g) for g in genes]
from scipy.stats import spearmanr
sk = np.asarray(a.layers['isoform2'].todense() if hasattr(a.layers['isoform2'],'todense') else a.layers['isoform2'])[:, order]
i1 = np.asarray(a.layers['isoform1'].todense() if hasattr(a.layers['isoform1'],'todense') else a.layers['isoform1'])[:, order]
r_sk = spearmanr(sk.ravel(), skip.ravel())[0]
r_in = spearmanr(i1.ravel(), (inc1+inc2).ravel())[0]
print('Spearman brie isoform2 vs pysam skip-junction count (cell x event):', round(r_sk,3))
print('Spearman brie isoform1 vs pysam inc-junction count:', round(r_in,3))
print('brie isoform2 total', sk.sum(), 'pysam skip-junction total', skip.sum(), 'ratio', round(sk.sum()/skip.sum(),3))
# per-cell PSI-ish crude: fraction of cells with >=1 junction read per event (data sparsity of real Smart-seq2)
tot = i1+sk
print('median unique reads per cell per event', np.median(tot), 'mean', tot.mean().round(2), 'frac cell-event with >=5 reads', (tot>=5).mean().round(3))
assert r_sk > 0.9, 'brie skip counts do not track pysam junction counts'
assert r_in > 0.8
print('ASSERT OK: brie-count tracks independent pysam junction counts on real data')
