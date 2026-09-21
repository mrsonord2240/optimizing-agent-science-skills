"""SYNTHETIC Smart-seq-like BAMs with KNOWN per-group PSI: the auditor's own design (differs from the pre-fix set).
   asenv as-core python 20_gen_planted_v2.py <outdir> <seed> [null]
 - 60 SE events, half on the MINUS strand (pre-fix set was plus-only), varied exon/intron lengths
 - classes: 'big' 12 events PSI 0.80 vs 0.30 (dPSI 0.5), 'small' 8 events 0.60 vs 0.40 (dPSI 0.2), 'null' 40 events (same PSI, drawn 0.25-0.75); 'null' arg -> all 60 null
 - 100 cells (50 A / 50 B); 30% low-coverage cells (mean 1.5 reads/event vs 25); per-cell PSI = Beta noise (concentration 15)
 - unstranded uniform 100-nt single-end reads over the isoform; contig chrT
Outputs: events.gff3 (BRIE layout), truth.tsv, cell_table.tsv (absolute BAM paths), cell_metadata.tsv (grp01), cells.tsv"""
import sys, os, numpy as np, pandas as pd, pysam
out, seed = os.path.abspath(sys.argv[1]), int(sys.argv[2]); ALLNULL = len(sys.argv) > 3 and sys.argv[3] == 'null'
rng = np.random.default_rng(seed); os.makedirs(out + '/bams', exist_ok=True)
NG, RL, NC = 60, 100, 100
genes = []; pos = 5000
for g in range(NG):
    cls = 'big' if g < 12 else ('small' if g < 20 else 'null')
    if ALLNULL: cls = 'null'
    e1, i1, ec, i2, e3 = [int(rng.integers(*r)) for r in [(120, 260), (300, 900), (60, 160), (300, 900), (120, 260)]]
    s1 = pos; en1 = s1 + e1 - 1; sc_ = en1 + i1 + 1; enc = sc_ + ec - 1; s3 = enc + i2 + 1; en3 = s3 + e3 - 1
    if cls == 'null': pa = pb = round(float(rng.uniform(.25, .75)), 2)
    elif cls == 'big': pa, pb = (.8, .3) if rng.random() < .5 else (.3, .8)
    else: pa, pb = (.6, .4) if rng.random() < .5 else (.4, .6)
    genes.append(dict(gene=f'TG{g:03d}', cls=cls, strand='-' if g % 2 else '+', s1=s1, e1=en1, sc=sc_, ec=enc, s3=s3, e3=en3, psiA=pa, psiB=pb)); pos = en3 + 3000
pd.DataFrame(genes)[['gene', 'cls', 'strand', 'psiA', 'psiB']].to_csv(out + '/truth.tsv', sep='\t', index=False)
with open(out + '/events.gff3', 'w') as f:
    f.write('#GFF3 synthetic v2\n')
    for g in genes:
        gid, st = g['gene'], g['strand']
        f.write(f"chrT\t.\tgene\t{g['s1']}\t{g['e3']}\t.\t{st}\t.\tID={gid};gene_id={gid};gene_name={gid};gene_type=protein_coding\n")
        for tag, exs in [('in', [(g['s1'], g['e1']), (g['sc'], g['ec']), (g['s3'], g['e3'])]), ('out', [(g['s1'], g['e1']), (g['s3'], g['e3'])])]:
            f.write(f"chrT\t.\tmRNA\t{g['s1']}\t{g['e3']}\t.\t{st}\t.\tID={gid}.{tag};Parent={gid}\n")
            for i, (a, b) in enumerate(exs, 1): f.write(f"chrT\t.\texon\t{a}\t{b}\t.\t{st}\t.\tID={gid}.{tag}.{i};Parent={gid}.{tag}\n")
def blocks(g, inc): return [(g['s1'], g['e1'])] + ([(g['sc'], g['ec'])] if inc else []) + [(g['s3'], g['e3'])]
def read_at(bl, tpos):
    cig = []; start0 = None; need = RL; off = tpos; prev = None
    for a, b in bl:
        L = b - a + 1
        if off >= L: off -= L; continue
        take = min(L - off, need); gs = a + off
        if start0 is None: start0 = gs - 1
        else: cig.append((3, gs - 1 - prev))
        cig.append((0, take)); prev = gs - 1 + take; need -= take; off = 0
        if need == 0: break
    return start0, cig
hdr = {'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'chrT', 'LN': int(pos + 1000)}]}
meta = []; rows = []
for ci in range(NC):
    cid = f'c{ci:03d}'; grp = 'A' if ci < NC // 2 else 'B'; low = rng.random() < .3; depth = 1.5 if low else 25.0
    meta.append(dict(cell=cid, group=grp, lowcov=int(low))); reads = []
    for g in genes:
        pm = g['psiA'] if grp == 'A' else g['psiB']; pc = float(np.clip(rng.beta(max(pm * 15, .5), max((1 - pm) * 15, .5)), .001, .999))
        for _ in range(rng.negative_binomial(2, 2 / (2 + depth))):
            Li = sum(b - a + 1 for a, b in blocks(g, True)); Lo = sum(b - a + 1 for a, b in blocks(g, False))
            inc = rng.random() < pc * Li / (pc * Li + (1 - pc) * Lo); bl = blocks(g, inc); L = sum(b - a + 1 for a, b in bl)
            if L < RL: continue
            reads.append(read_at(bl, int(rng.integers(0, L - RL + 1))))
    reads.sort(key=lambda x: x[0]); p = f'{out}/bams/{cid}.sorted.bam'
    with pysam.AlignmentFile(p, 'wb', header=hdr) as bam:
        for k, (st, cig) in enumerate(reads):
            a = pysam.AlignedSegment(); a.query_name = f'{cid}r{k}'; a.query_sequence = 'A' * RL; a.flag = 0; a.reference_id = 0; a.reference_start = st
            a.mapping_quality = 60; a.cigartuples = cig; a.query_qualities = pysam.qualitystring_to_array('I' * RL); a.set_tags([('NH', 1)]); bam.write(a)
    pysam.index(p); rows.append((p, cid))
pd.DataFrame(meta).to_csv(out + '/cells.tsv', sep='\t', index=False)
open(out + '/cell_table.tsv', 'w').write(''.join(f'{p}\t{c}\n' for p, c in rows))
pd.DataFrame(meta).assign(grp01=lambda d: (d.group == 'B').astype(int)).set_index('cell')[['grp01']].to_csv(out + '/cell_metadata.tsv', sep='\t')
print('cells', NC, 'events', NG, 'null-only' if ALLNULL else 'planted', 'low-cov cells', sum(m['lowcov'] for m in meta))
