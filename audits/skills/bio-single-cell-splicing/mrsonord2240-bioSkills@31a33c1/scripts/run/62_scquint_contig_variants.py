"""INPUT 6c follow-up: which contig-naming combinations make SKILL.md block S07 work on the REAL STARsolo output?
 A junctions 'X'    + GTF 'X'      (self-consistent STAR run; result of 61)
 B junctions 'X'    + GTF 'chrX'   (self-consistent chr-style run)
 C junctions 'chrX' + GTF 'X'      (what the SKILL text describes: 'Ensembl-style contigs ... scQuint prepends chr to match the junctions')
Run in WSL as-sc from run/out/in6_scquint."""
import os, shutil, gzip, re, sys, warnings; warnings.filterwarnings('ignore')
R = '/mnt/openscience/audits/bio-single-cell-splicing/run'; W = f'{R}/out/in6_scquint'; os.chdir(W)
src = os.environ['ASDATA'] + '/rnasplice/reference/genes_chrX.gtf'
code = open(f'{R}/blocks/S07_python.py', encoding='utf-8').read().replace("'neuron'", "'GBR'").replace("'glia'", "'YRI'")
def variant(name, junc_chr, gtf_chr):
    d = f'var_{name}'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d + '/Solo.out/SJ/raw')
    for f in ['matrix.mtx', 'barcodes.tsv']: shutil.copy(f'ss_Solo.out/SJ/raw/{f}', f'{d}/Solo.out/SJ/raw/{f}')
    with open('ss_Solo.out/SJ/raw/features.tsv') as a, open(f'{d}/Solo.out/SJ/raw/features.tsv', 'w') as b:
        for l in a: b.write(('chr' if junc_chr else '') + l)
    with open(src) as a, gzip.open(f'{d}/annotation.gtf.gz', 'wt') as b:
        for l in a: b.write(('chr' if gtf_chr else '') + l)
    cwd = os.getcwd(); os.chdir(d); ns = {'cell_types': ['GBR', 'GBR', 'YRI', 'YRI']}
    try: exec(code, ns); r = 'S07 ran; adata %s, intron_groups %d rows, introns %d rows' % (ns['adata'].shape, len(ns['intron_groups']), len(ns['introns']))
    except Exception as e: r = f'S07 FAILED {type(e).__name__}: {str(e)[:90]} (adata after annotation: {ns["adata"].shape if "adata" in ns else "n/a"})'
    os.chdir(cwd); print(f'variant {name} (junctions chr={junc_chr}, GTF chr={gtf_chr}):', r)
variant('A', False, False); variant('B', False, True); variant('C', True, False)
