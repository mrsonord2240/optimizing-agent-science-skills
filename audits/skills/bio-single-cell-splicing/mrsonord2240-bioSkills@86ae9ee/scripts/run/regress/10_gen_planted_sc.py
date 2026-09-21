"""SYNTHETIC single-cell splicing data with KNOWN per-group PSI (planted truth). Run in WSL env as-core (pysam).
Usage: python 10_gen_planted_sc.py <outdir> <mode: ss2|10x> <seed>
ss2 : 80 cells (40 A + 40 B), 75-nt single-end reads uniformly along the transcript (Smart-seq2-like), 15% low-coverage 'dropout' cells.
10x : 300 cells, 91-nt reads sampled only from the 3' end (<= 600 nt from poly(A)), CB/UR tags (10x 3' v3-like).
Events: 100 SE genes on contig chrS. Truth table -> truth.tsv (gene, class, psiA, psiB).
  class 'big'   : 20 genes, PSI 0.85 vs 0.15 (direction random)
  class 'mid'   : 10 genes, PSI 0.65 vs 0.35
  class 'null'  : 70 genes, same PSI in both groups (drawn 0.2-0.8)
Gene layout (+ strand): exon1 100 nt, intron 400, cassette exon 90 nt, intron 400, exon3 = LAST exon
   ss2 : exon3 = 100 nt.   10x: half the genes 'near3' with exon3 = 100 nt (cassette junction within ~190 nt of polyA), half 'far3' with exon3 = 1500 nt.
"""
import sys, os, numpy as np, pandas as pd, pysam

out, mode, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
ALLNULL = len(sys.argv) > 4 and sys.argv[4] == 'allnull'   # every gene null: pure false-positive-rate control
rng = np.random.default_rng(seed)
os.makedirs(out, exist_ok=True)
NG = 100
E1, I1, EC, I2 = 100, 400, 90, 400

genes = []
pos = 1000
for g in range(NG):
    cls = 'big' if g < 20 else ('mid' if g < 30 else 'null')
    if ALLNULL:
        cls = 'null'
    if mode == '10x':
        E3 = 100 if g % 2 == 0 else 1500
        lay = 'near3' if g % 2 == 0 else 'far3'
    else:
        E3, lay = 100, 'ss2'
    s1 = pos; e1 = s1 + E1 - 1
    sc_ = e1 + I1 + 1; ec = sc_ + EC - 1
    s3 = ec + I2 + 1; e3 = s3 + E3 - 1
    if cls == 'null':
        pa = pb = float(np.round(rng.uniform(0.2, 0.8), 2))
    elif cls == 'big':
        pa, pb = (0.85, 0.15) if rng.random() < 0.5 else (0.15, 0.85)
    else:
        pa, pb = (0.65, 0.35) if rng.random() < 0.5 else (0.35, 0.65)
    genes.append(dict(gene=f'SYNG{g:03d}', cls=cls, layout=lay, s1=s1, e1=e1, sc=sc_, ec=ec, s3=s3, e3=e3, psiA=pa, psiB=pb))
    pos = e3 + 2000
CHRLEN = pos + 1000
gdf = pd.DataFrame(genes)
gdf[['gene', 'cls', 'layout', 'psiA', 'psiB']].to_csv(f'{out}/truth.tsv', sep='\t', index=False)

# BRIE GFF3 (same layout as the shipped real 50-event file: gene / mRNA .in / mRNA .out)
with open(f'{out}/events.gff3', 'w') as f:
    f.write('#GFF3 synthetic\n')
    for g in genes:
        gid = g['gene']
        f.write(f"chrS\t.\tgene\t{g['s1']}\t{g['e3']}\t.\t+\t.\tID={gid};gene_id={gid};gene_name={gid};gene_type=protein_coding\n")
        f.write(f"chrS\t.\tmRNA\t{g['s1']}\t{g['e3']}\t.\t+\t.\tID={gid}.in;Parent={gid}\n")
        for i, (a, b) in enumerate([(g['s1'], g['e1']), (g['sc'], g['ec']), (g['s3'], g['e3'])], 1):
            f.write(f"chrS\t.\texon\t{a}\t{b}\t.\t+\t.\tID={gid}.in.{i};Parent={gid}.in\n")
        f.write(f"chrS\t.\tmRNA\t{g['s1']}\t{g['e3']}\t.\t+\t.\tID={gid}.out;Parent={gid}\n")
        for i, (a, b) in enumerate([(g['s1'], g['e1']), (g['s3'], g['e3'])], 1):
            f.write(f"chrS\t.\texon\t{a}\t{b}\t.\t+\t.\tID={gid}.out.{i};Parent={gid}.out\n")


def blocks_for(g, inc):
    """exon blocks (1-based inclusive) of the isoform"""
    ex = [(g['s1'], g['e1'])] + ([(g['sc'], g['ec'])] if inc else []) + [(g['s3'], g['e3'])]
    return ex


def read_cigar(blocks, tpos, rlen):
    """map transcript offset tpos (0-based) + rlen onto genome; return (ref_start0, cigartuples) or None"""
    total = sum(b - a + 1 for a, b in blocks)
    if tpos + rlen > total:
        return None
    cig = []; start0 = None; need = rlen; off = tpos; prev_end = None
    for a, b in blocks:
        L = b - a + 1
        if off >= L:
            off -= L; continue
        take = min(L - off, need)
        gs = a + off  # 1-based
        if start0 is None:
            start0 = gs - 1
        else:
            cig.append((3, gs - 1 - prev_end))  # N gap
        cig.append((0, take))
        prev_end = gs - 1 + take  # 0-based exclusive end
        need -= take; off = 0
        if need == 0:
            break
    return start0, cig


hdr = {'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'chrS', 'LN': int(CHRLEN)}]}
ncell = 80 if mode == 'ss2' else 300
RL = 75 if mode == 'ss2' else 91
cells = []
meta = []
per_cell_reads = {}
allreads = {}  # cell -> list of (start0, cig, tags)
BARC = []
for ci in range(ncell):
    grp = 'A' if ci < ncell // 2 else 'B'
    if mode == 'ss2':
        dropout = rng.random() < 0.15
        depth = 2.0 if dropout else 30.0   # mean reads per event (gene) per cell
        cid = f'cell{ci:03d}'
    else:
        dropout = False
        depth = 3.0
        cid = ''.join(rng.choice(list('ACGT'), 16)) + '-1'
    BARC.append(cid)
    meta.append(dict(cell=cid, group=grp, dropout=int(dropout)))
    reads = []
    for g in genes:
        psi_mean = g['psiA'] if grp == 'A' else g['psiB']
        # per-cell PSI: beta noise (concentration 20) around group mean
        psi_c = float(np.clip(rng.beta(max(psi_mean * 20, 0.5), max((1 - psi_mean) * 20, 0.5)), 0.001, 0.999))
        n = rng.negative_binomial(2, 2 / (2 + depth))
        for _ in range(n):
            # isoform allocation proportional to psi * len_in vs (1-psi) * len_out
            Lin = sum(b - a + 1 for a, b in blocks_for(g, True)); Lout = sum(b - a + 1 for a, b in blocks_for(g, False))
            p_in = psi_c * Lin / (psi_c * Lin + (1 - psi_c) * Lout)
            inc = rng.random() < p_in
            bl = blocks_for(g, inc)
            L = sum(b - a + 1 for a, b in bl)
            if mode == 'ss2':
                tpos = int(rng.integers(0, L - RL + 1))
            else:
                # 10x 3': read start within [L-600, L-RL] from the 3' end (fragment enriched near polyA)
                lo = max(0, L - 600)
                tpos = int(rng.integers(lo, L - RL + 1)) if L - RL + 1 > lo else 0
            r = read_cigar(bl, tpos, RL)
            if r:
                reads.append((r[0], r[1], inc))
    allreads[cid] = reads

pd.DataFrame(meta).to_csv(f'{out}/cells.tsv', sep='\t', index=False)
os.makedirs(f'{out}/bams', exist_ok=True)


def write_bam(path, reads_by_cell, tagged):
    items = []
    for cid, reads in reads_by_cell.items():
        for st, cig, inc in reads:
            items.append((st, cid, cig))
    items.sort(key=lambda x: x[0])
    with pysam.AlignmentFile(path, 'wb', header=hdr) as bam:
        for k, (st, cid, cig) in enumerate(items):
            a = pysam.AlignedSegment()
            a.query_name = f'r{k}'; a.query_sequence = 'A' * RL; a.flag = 0; a.reference_id = 0
            a.reference_start = st; a.mapping_quality = 60; a.cigartuples = cig
            a.query_qualities = pysam.qualitystring_to_array('I' * RL)
            tags = [('NH', 1)]
            if tagged:
                tags += [('CB', cid), ('UR', ''.join(rng.choice(list('ACGT'), 10)))]
            a.set_tags(tags)
            bam.write(a)
    pysam.index(path)


if mode == 'ss2':
    with open(f'{out}/cell_table.tsv', 'w') as f:
        for cid, reads in allreads.items():
            p = f'{out}/bams/{cid}.sorted.bam'
            write_bam(p, {cid: reads}, False)
            f.write(f'{p}\t{cid}\n')
    pd.DataFrame(meta).assign(grp01=lambda d: (d.group == 'B').astype(int)).set_index('cell')[['grp01']].to_csv(f'{out}/cellfeat.tsv', sep='\t')
else:
    write_bam(f'{out}/bams/synth10x.bam', allreads, True)
    with open(f'{out}/barcodes.tsv', 'w') as f:
        f.write('\n'.join(BARC) + '\n')
print('mode', mode, 'cells', ncell, 'genes', NG, 'reads', sum(len(v) for v in allreads.values()))
