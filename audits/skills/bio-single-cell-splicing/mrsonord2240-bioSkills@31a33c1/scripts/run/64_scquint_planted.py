"""INPUT 6c: scQuint block S07 on PLANTED data (SYNTHETIC) laid out exactly like real STARsolo SJ output (Solo.out/SJ/raw: matrix.mtx, barcodes.tsv, 9-column features.tsv, strand 1/2),
junction contigs 'chrN' and an Ensembl-style GTF ('N') = variant C of 62_*, the only naming combination that worked on real data. Source counts: the auditor's planted MARVEL set
(out/in4_planted: 120 SE events, 20 minus-strand, 40 cells, 25% low coverage; truth.tsv). Run in WSL as-sc from run/out/in6_planted.
Also: the same block with the Skill's default thresholds (30/30) to check the 'most groups filtered' claim, and the NULL set (out/in4_null)."""
import os, sys, glob, gzip, warnings, numpy as np, pandas as pd
from scipy import io, sparse
warnings.filterwarnings('ignore')
R = '/mnt/openscience/audits/bio-single-cell-splicing/run'

def build(src, dst):
    os.makedirs(f'{dst}/Solo.out/SJ/raw', exist_ok=True)
    truth = pd.read_csv(f'{src}/truth.tsv', sep='\t', keep_default_na=False); strand = {}
    ex = []
    for _, r in truth.iterrows():
        parts = [p.split(':') for p in r.tran_id.split('@')]; chrom = parts[0][0]
        e = [(int(p[1]), int(p[2])) for p in parts]
        if r.strand == '-': e = e[::-1]     # genomic order
        gid = 'SYNG%03d' % (list(truth.tran_id).index(r.tran_id) + 1)
        for a, b in e: ex.append((chrom[3:], 'SYN', 'exon', a, b, '.', r.strand, '.', f'gene_id "{gid}"; gene_name "Gene{gid[4:]}";'))
        strand[(chrom, e[0][1] + 1, e[1][0] - 1)] = r.strand; strand[(chrom, e[1][1] + 1, e[2][0] - 1)] = r.strand; strand[(chrom, e[0][1] + 1, e[2][0] - 1)] = r.strand
    pd.DataFrame(ex).to_csv(f'{dst}/annotation.gtf.gz', sep='\t', header=False, index=False, quoting=3)
    files = sorted(glob.glob(f'{src}/star_pass2/*_SJ.out.tab')); cells = [os.path.basename(f).replace('_SJ.out.tab', '') for f in files]
    d = {}
    for ci, f in enumerate(files):
        t = pd.read_csv(f, sep='\t', header=None)
        for _, r in t.iterrows(): d.setdefault((r[0], int(r[1]), int(r[2])), {})[ci] = int(r[6])
    keys = sorted(d); rows, cols, vals = [], [], []
    for ki, k in enumerate(keys):
        for ci, v in d[k].items(): rows.append(ki); cols.append(ci); vals.append(v)
    io.mmwrite(f'{dst}/Solo.out/SJ/raw/matrix.mtx', sparse.coo_matrix((vals, (rows, cols)), shape=(len(keys), len(cells))), field='integer')
    open(f'{dst}/Solo.out/SJ/raw/barcodes.tsv', 'w').write('\n'.join(cells) + '\n')
    with open(f'{dst}/Solo.out/SJ/raw/features.tsv', 'w') as f:
        for k in keys:
            tot = sum(d[k].values()); f.write(f'{k[0]}\t{k[1]}\t{k[2]}\t{1 if strand[k] == "+" else 2}\t1\t1\t{tot}\t0\t30\n')
    return truth, cells

def run(tag, src, thr):
    dst = f'{R}/out/in6_planted_{tag}'; truth, cells = build(src, dst); os.chdir(dst)
    cell_types = ['neuron'] * 20 + ['glia'] * 20
    code = open(f'{R}/blocks/S07_python.py', encoding='utf-8').read()
    if thr != 10: code = code.replace('min_cells_per_intron_group=10, min_total_cells_per_intron=10', f'min_cells_per_intron_group={thr}, min_total_cells_per_intron={thr}')
    ns = {'cell_types': cell_types}; exec(code, ns)
    ig, it = ns['intron_groups'], ns['introns']
    print(f'[{tag}, thresholds {thr}] adata {ns["adata"].shape}; intron groups tested {len(ig)}; introns {len(it)}; cols {list(ig.columns)[:8]}')
    hits = ns['hits']; g = it.copy(); g['gene'] = g.get('gene_id', pd.Series(index=g.index, dtype=object))
    return truth, ig, it, ns

truth, ig, it, ns = run('big', f'{R}/out/in4_planted', 10)
print('introns cols', it.columns.tolist()); print('intron_groups cols', ig.columns.tolist())
gcol = 'gene_id' if 'gene_id' in it.columns else None
truth['gene'] = ['SYNG%03d' % (i + 1) for i in range(len(truth))]
sig = it[it.p_value_adj < 0.05] if 'p_value_adj' in it.columns else it.merge(ig[['p_value_adj']], left_on='intron_group', right_index=True)[lambda d: d.p_value_adj < 0.05]
sig_genes = set(sig[gcol]) if gcol else set()
tt = truth.assign(hit=truth.gene.isin(sig_genes))
print(tt.groupby('cls').hit.agg(['sum', 'size']).T)
print('minus-strand events hit:', int(tt[tt.strand == '-'].hit.sum()), '/', int((tt.strand == '-').sum()), ' plus:', int(tt[tt.strand == '+'].hit.sum()), '/', int((tt.strand == '+').sum()))
# direction: delta_psi of the intron sharing the 3' site with the skip junction is not unique; check psi_a - psi_b sign for sig planted 'big' events on the SKIP intron (longest intron of the gene)
s2 = sig.copy(); s2['len'] = s2.end - s2.start; skip = s2.loc[s2.groupby(gcol).len.idxmax()]; skip = skip.merge(truth[['gene', 'cls', 'psiA_neuron', 'psiB_glia']], left_on=gcol, right_on='gene'); skip = skip[skip.cls != 'null']
# group a = neuron, b = glia; skip-intron usage = 1 - PSI_inclusion ; delta_psi = psi_a - psi_b (neuron - glia) expected sign = -(psiA_neuron - psiB_glia)
print('sign check on skip intron (delta_psi = a-b vs -(inclusion PSI neuron - glia)):', (np.sign(skip.delta_psi) == -np.sign(skip.psiA_neuron - skip.psiB_glia)).mean().round(3), 'n', len(skip))
try: run('default30', f'{R}/out/in4_planted', 30)
except Exception as e: print('[default 30/30 thresholds on 40 cells] RAISED', type(e).__name__, str(e)[:100], '(SKILL says both tables come back empty)')
try:
    t2, ig2, it2, ns2 = run('null', f'{R}/out/in4_null', 10)
    print('NULL set: intron GROUPS tested', len(ig2), ' p_value_adj<0.05:', int((ig2.p_value_adj < 0.05).sum()), ' raw p<0.05:', int((ig2.p_value < 0.05).sum()))
except Exception as e: print('null run error', type(e).__name__, str(e)[:120])
