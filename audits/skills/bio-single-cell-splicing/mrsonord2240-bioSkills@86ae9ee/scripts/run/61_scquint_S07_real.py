"""INPUT 6c: SKILL.md block S07 (scQuint) run LITERALLY on REAL STARsolo SmartSeq SJ output (4 real chrX libraries as 4 'cells', made by 60_starsolo_real.sh), with the
real Ensembl GTF that the STAR index was built from. cell_types is defined first (2 GBR + 2 YRI). Only the input layout is staged (Solo.out/SJ/raw, annotation.gtf.gz).
Run in WSL as-sc from run/out/in6_scquint."""
import os, sys, shutil, gzip, numpy as np, pandas as pd
R = '/mnt/openscience/audits/bio-single-cell-splicing/run'; W = f'{R}/out/in6_scquint'; os.chdir(W)
shutil.rmtree('Solo.out', ignore_errors=True); shutil.copytree('ss_Solo.out', 'Solo.out')
src = os.environ['ASDATA'] + '/rnasplice/reference/genes_chrX.gtf'
with open(src, 'rb') as a, gzip.open('annotation.gtf.gz', 'wb') as b: shutil.copyfileobj(a, b)
print('junction features.tsv head:'); print(open('Solo.out/SJ/raw/features.tsv').read().split('\n')[0]); print('GTF contig of first line:', open(src).readline().split('\t')[0])
cell_types = ['GBR', 'GBR', 'YRI', 'YRI']
code = open(f'{R}/blocks/S07_python.py', encoding='utf-8').read().replace("'neuron'", "'GBR'").replace("'glia'", "'YRI'")
# literal except the two group labels (the block's labels are placeholders for the user's own)
ns = {'cell_types': cell_types}
try:
    exec(code, ns)
    print('S07 executed without error')
except Exception as e:
    import traceback; traceback.print_exc(); print('S07 FAILED:', type(e).__name__, str(e)[:200])
ad = ns.get('adata')
if ad is not None:
    print('adata', ad.shape, 'var columns', list(ad.var.columns)[:14])
    print('introns with a gene assigned:', int(ad.var['gene_id'].notna().sum()) if 'gene_id' in ad.var else 'no gene_id column', 'of', ad.n_vars)
    print('junction chromosome values:', ad.var.chromosome.unique()[:3])
ig = ns.get('intron_groups'); print('intron_groups rows', None if ig is None else len(ig), ' introns rows', None if ns.get('introns') is None else len(ns['introns']))
