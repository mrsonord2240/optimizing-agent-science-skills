#!/usr/bin/env python
"""
SYNTHETIC data generator for the bio-splicing-qc audit (auditor-made, not real data).
Every read is simulated straight into a BAM (no aligner); ground truth is written to truth.json.
Contig chrS (700 kb), 60 genes x 4 exons (300 nt) -> 1200-nt transcripts, alternating strands.
Run:  asenv as-core python make_synth.py
"""
import os, sys, json, random
import numpy as np
import pysam

OUT = '/mnt/openscience/audits/bio-splicing-qc/run/data/synthetic'
os.makedirs(OUT, exist_ok=True)
SEED = 20260920
rng = np.random.default_rng(SEED)
random.seed(SEED)
CHROM, CLEN = 'chrS', 700000
NG, EXON, NEX = 60, 300, 4
RRNA = (650000, 655000)          # synthetic "rRNA locus"
MULTI_LOCI = [660000, 670000, 680000]

# ---------------------------------------------------------------- gene models
genes, pos = [], 5000
for i in range(NG):
    strand = '+' if i % 2 == 0 else '-'
    introns = [int(x) for x in rng.integers(1200, 2500, NEX - 1)]
    starts, p = [], pos
    for e in range(NEX):
        starts.append(p)
        p += EXON
        if e < NEX - 1:
            p += introns[e]
    genes.append(dict(id=f'G{i:02d}', strand=strand, starts=starts, ends=[s + EXON for s in starts]))
    pos = p + 3000
assert pos < RRNA[0], pos

with open(f'{OUT}/synth.bed12', 'w') as fh:
    for g in genes:
        s, e = g['starts'][0], g['ends'][-1]
        sizes = ','.join(str(EXON) for _ in range(NEX)) + ','
        rel = ','.join(str(x - s) for x in g['starts']) + ','
        fh.write('\t'.join(map(str, [CHROM, s, e, g['id'], 0, g['strand'], s, e, 0, NEX, sizes, rel])) + '\n')
# same model with the "X"-style (no chr prefix) contig name, to test naming mismatches
with open(f'{OUT}/synth_nochr.bed12', 'w') as fh, open(f'{OUT}/synth.bed12') as src:
    for line in src:
        fh.write(line.replace(CHROM, 'S', 1))
# BED6 (what a user gets from bedtools/awk for a "BED of canonical transcripts")
with open(f'{OUT}/synth.bed6', 'w') as fh:
    for g in genes:
        fh.write('\t'.join(map(str, [CHROM, g['starts'][0], g['ends'][-1], g['id'], 0, g['strand']])) + '\n')
# refFlat for Picard (CDS = exons 2..3 region so UTR/coding bases exist)
with open(f'{OUT}/synth.refFlat.txt', 'w') as fh:
    for g in genes:
        s, e = g['starts'][0], g['ends'][-1]
        cds_s, cds_e = g['starts'][0] + 100, g['ends'][-1] - 100
        fh.write('\t'.join([g['id'], g['id'] + '.t1', CHROM, g['strand'], str(s), str(e), str(cds_s), str(cds_e), str(NEX),
                            ','.join(map(str, g['starts'])) + ',', ','.join(map(str, g['ends'])) + ',']) + '\n')
with open(f'{OUT}/synth.rrna.interval_list', 'w') as fh:
    fh.write(f'@HD\tVN:1.6\tSO:coordinate\n@SQ\tSN:{CHROM}\tLN:{CLEN}\n')
    fh.write(f'{CHROM}\t{RRNA[0]+1}\t{RRNA[1]}\t+\trRNA_synth\n')
with open(f'{OUT}/synth.rrna.bed', 'w') as fh:
    fh.write(f'{CHROM}\t{RRNA[0]}\t{RRNA[1]}\trRNA_synth\n')

known_donors = {(g['id'], e) for g in genes for e in g['ends'][:-1]}
KD = {e for g in genes for e in g['ends'][:-1]}
KA = {s for g in genes for s in g['starts'][1:]}

# ---------------------------------------------------------------- junction catalogue
def catalogue():
    cat = []
    for gi, g in enumerate(genes):
        for i in range(NEX - 1):
            cat.append(dict(g=gi, cls='A', d=g['ends'][i], a=g['starts'][i + 1]))
        for i in range(NEX - 2):   # exon skipping i -> i+2: both sites known, junction itself not annotated
            cat.append(dict(g=gi, cls='SK', d=g['ends'][i], a=g['starts'][i + 2]))
    novel = []
    for gi, g in enumerate(genes):
        for i in range(NEX - 1):
            for _ in range(3):
                d0, a0 = g['ends'][i], g['starts'][i + 1]
                novel.append(dict(g=gi, cls='PA', d=d0, a=a0 - int(rng.integers(20, 300))))         # novel acceptor
                novel.append(dict(g=gi, cls='PD', d=d0 + int(rng.integers(20, 300)), a=a0))         # novel donor
                novel.append(dict(g=gi, cls='C', d=d0 + int(rng.integers(100, 400)), a=a0 - int(rng.integers(100, 400))))
    # de-duplicate and verify class semantics against the known-site sets
    seen, uniq = set(), []
    for j in novel:
        key = (j['d'], j['a'])
        if key in seen or j['a'] - j['d'] < 60:
            continue
        seen.add(key)
        dk, ak = j['d'] in KD, j['a'] in KA
        assert (j['cls'] == 'C' and not dk and not ak) or (j['cls'] == 'PA' and dk and not ak) or (j['cls'] == 'PD' and ak and not dk), j
        uniq.append(j)
    return cat, uniq

CAT, NOVEL = catalogue()
A_J = [j for j in CAT if j['cls'] == 'A']
SK_J = [j for j in CAT if j['cls'] == 'SK']
PA_J = [j for j in NOVEL if j['cls'] in ('PA', 'PD')]
C_J = [j for j in NOVEL if j['cls'] == 'C']
print('catalogue: A', len(A_J), 'SK', len(SK_J), 'partial', len(PA_J), 'complete', len(C_J))

HDR = {'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': CHROM, 'LN': CLEN}]}
BASES = np.array(list('ACGT'))

def seq(n):
    return ''.join(rng.choice(BASES, n))

def mk_read(name, start, cigar, flag, xs=None, mapq=255, nh=1, mate=None, tlen=0, hdr=None):
    r = pysam.AlignedSegment(hdr)
    r.query_name = name
    r.reference_id = 0
    r.reference_start = start
    r.cigartuples = cigar
    ql = sum(l for o, l in cigar if o in (0, 1, 4))
    r.query_sequence = seq(ql)
    r.query_qualities = pysam.qualitystring_to_array('I' * ql)
    r.flag = flag
    r.mapping_quality = mapq
    if mate is not None:
        r.next_reference_id = 0
        r.next_reference_start = mate
        r.template_length = tlen
    tags = [('NH', nh), ('HI', 1)]
    if xs:
        tags.append(('XS', xs))
    r.set_tags(tags)
    return r

def write_sorted(path, recs, hdr):
    tmp = path + '.tmp.bam'
    with pysam.AlignmentFile(tmp, 'wb', header=hdr) as fh:
        for r in recs:
            fh.write(r)
    pysam.sort('-o', path, tmp)
    os.remove(tmp)
    pysam.index(path)

def strand_xs(gi):
    return genes[gi]['strand']

# ---------------------------------------------------------------- SE junction datasets
def se_junction_bam(path, lam, readlen=100, tag='x'):
    """lam: dict class -> (list_of_junctions, mean reads/junction (Poisson, min 1 for retained), keep_fraction)"""
    hdr = pysam.AlignmentHeader.from_dict(HDR)
    recs, truth_j = [], []
    n = 0
    for cls, (jl, mean, keep) in lam.items():
        for j in jl:
            if rng.random() > keep:
                continue
            c = max(1, int(rng.poisson(mean)))
            truth_j.append(dict(cls=cls, d=j['d'], a=j['a'], reads=c))
            intron = j['a'] - j['d']
            for _ in range(c):
                a = int(rng.integers(8, readlen - 8 + 1))
                cig = [(0, a), (3, intron), (0, readlen - a)]
                n += 1
                recs.append(mk_read(f'{tag}{n}', j['d'] - a, cig, int(rng.choice([0, 16])), xs=strand_xs(j['g']), hdr=hdr))
    # unspliced exon reads for realism (20% of the total)
    for _ in range(int(0.25 * len(recs))):
        g = genes[int(rng.integers(NG))]
        e = int(rng.integers(NEX))
        n += 1
        recs.append(mk_read(f'{tag}{n}', g['starts'][e] + int(rng.integers(0, EXON - readlen)), [(0, readlen)], int(rng.choice([0, 16])), hdr=hdr))
    recs.sort(key=lambda r: r.reference_start)
    write_sorted(path, recs, hdr)
    # truth
    tot = sum(t['reads'] for t in truth_j)
    by = {}
    for t in truth_j:
        by.setdefault(t['cls'], [0, 0])
        by[t['cls']][0] += 1
        by[t['cls']][1] += t['reads']
    known_reads = sum(v[1] for k, v in by.items() if k in ('A', 'SK'))
    known_juncs = sum(v[0] for k, v in by.items() if k in ('A', 'SK'))
    tj = sum(v[0] for v in by.values())
    return dict(by_class={k: dict(junctions=v[0], reads=v[1]) for k, v in by.items()}, total_junction_reads=tot,
                total_junctions=tj,
                rseqc_known_read_frac=known_reads / tot, rseqc_known_junction_frac=known_juncs / tj,
                strict_annotated_read_frac=by.get('A', [0, 0])[1] / tot,
                partial_novel_read_frac=(by.get('PA', [0, 0])[1] + by.get('PD', [0, 0])[1]) / tot,
                complete_novel_read_frac=by.get('C', [0, 0])[1] / tot,
                junction_list=truth_j)

TRUTH = {}
# D1: clean library. annotated junctions well covered, some skipping, few novel
TRUTH['clean'] = se_junction_bam(f'{OUT}/se_clean.bam', {
    'A': (A_J, 60, 1.0), 'SK': (SK_J, 12, 0.5), 'PA': (PA_J, 1.6, 0.3), 'C': (C_J, 1.4, 0.3)}, tag='cl')
# D2: novel-rich library (biology-like: many low-count novel junctions)
TRUTH['novelrich'] = se_junction_bam(f'{OUT}/se_novelrich.bam', {
    'A': (A_J, 14, 1.0), 'SK': (SK_J, 3, 0.5), 'PA': (PA_J, 6, 1.0), 'C': (C_J, 5, 1.0)}, tag='nr')
# Saturation series: annotated junctions at three depths, plus singleton novel junctions in all
for nm, lam_a in [('sat_deep', 40), ('sat_mid', 3), ('sat_shallow', 1.5)]:
    TRUTH[nm] = se_junction_bam(f'{OUT}/se_{nm}.bam', {'A': (A_J, lam_a, 1.0), 'PA': (PA_J, 1.0, 0.5), 'C': (C_J, 1.0, 0.5)}, tag=nm[:5])
    TRUTH[nm]['lambda_A'] = lam_a
    TRUTH[nm]['n_A'] = len(A_J)

# ---------------------------------------------------------------- multi-junction / microexon reads (overhang truth)
hdr = pysam.AlignmentHeader.from_dict(HDR)
recs = []
mj_truth = []
# read type 1: 30M 1000N 4M 800N 66M   -> micro-exon of 4 nt: true adjacent overhang of BOTH junctions = 4
# read type 2: 20M 700N 10M 900N 70M   -> adjacent overhang 10 (>=8)
# read type 3: 6M 500N 94M             -> single junction overhang 6
# read type 4: 50M 600N 50M            -> overhang 50
shapes = [('mj_micro4', [(0, 30), (3, 1000), (0, 4), (3, 800), (0, 66)], [(30 + 1000 - 1000, 4), ]),
          ('mj_micro10', [(0, 20), (3, 700), (0, 10), (3, 900), (0, 70)], []),
          ('one_ov6', [(0, 6), (3, 500), (0, 94)], []),
          ('one_ov50', [(0, 50), (3, 600), (0, 50)], [])]
n = 0
for nm, cig, _ in shapes:
    for k in range(12):
        n += 1
        recs.append(mk_read(f'{nm}_{k}', 100000 + 5000 * shapes.index((nm, cig, _)), cig, 0, xs='+', hdr=hdr))
recs.sort(key=lambda r: r.reference_start)
write_sorted(f'{OUT}/se_overhang.bam', recs, hdr)
TRUTH['overhang'] = dict(note='true adjacent-exon-block overhang: mj_micro4 -> 4 and 4 for both junctions; mj_micro10 -> 10,10; one_ov6 -> 6; one_ov50 -> 50; 12 reads each')

# ---------------------------------------------------------------- PE stranded datasets
def spliced_blocks(g, off, length):
    """map [off, off+length) in spliced (genome-order) coordinates to genomic cigar; returns ref_start, cigar"""
    starts, ends = g['starts'], g['ends']
    cig, ref_start, remaining, cur = [], None, length, off
    acc = 0
    for s, e in zip(starts, ends):
        elen = e - s
        if cur >= acc + elen:
            acc += elen
            continue
        inner = cur - acc
        take = min(elen - inner, remaining)
        if ref_start is None:
            ref_start = s + inner
        else:
            cig.append((3, s - prev_end))
        cig.append((0, take))
        prev_end = s + inner + take
        remaining -= take
        cur += take
        acc += elen
        if remaining == 0:
            break
    return ref_start, cig

TLEN = NEX * EXON

def pe_bam(path, nfrag, protocol, leak=0.0, bias3=0.0, rrna_frac=0.0, unmapped_frac=0.0, multi_frac=0.0, tag='p', readlen=75):
    """protocol: 'dutp' (read1 antisense = fr-firststrand), 'fwd' (read1 sense = fr-secondstrand), 'unstr'.
       bias3: fraction of fragments drawn from the 3' 25% of the transcript. rrna_frac: fraction of fragments at the rRNA locus."""
    hdr = pysam.AlignmentHeader.from_dict(HDR)
    recs = []
    for i in range(nfrag):
        name = f'{tag}{i}'
        flen = int(rng.integers(220, 330))
        if unmapped_frac and rng.random() < unmapped_frac:
            for m in (1, 2):
                r = pysam.AlignedSegment(hdr)
                r.query_name = name
                r.query_sequence = seq(readlen)
                r.query_qualities = pysam.qualitystring_to_array('I' * readlen)
                r.flag = 77 if m == 1 else 141
                recs.append(r)
            continue
        if rrna_frac and rng.random() < rrna_frac:
            fs = RRNA[0] + int(rng.integers(0, RRNA[1] - RRNA[0] - flen))
            nmulti = 4 if (multi_frac and rng.random() < multi_frac) else 1
            for hi in range(nmulti):
                base = fs if hi == 0 else int(MULTI_LOCI[hi - 1]) + int(rng.integers(0, 3000))
                sec = 256 if hi > 0 else 0
                q = 255 if nmulti == 1 else 3
                l = mk_read(name, base, [(0, readlen)], 99 | sec, mapq=q, nh=nmulti, mate=base + flen - readlen, tlen=flen, hdr=hdr)
                rr = mk_read(name, base + flen - readlen, [(0, readlen)], 147 | sec, mapq=q, nh=nmulti, mate=base, tlen=-flen, hdr=hdr)
                l.set_tag('HI', hi + 1); rr.set_tag('HI', hi + 1)
                recs += [l, rr]
            continue
        g = genes[int(rng.integers(NG))]
        # position in transcript orientation
        if bias3 and rng.random() < bias3:
            u = rng.uniform(0.75, 1.0) * (TLEN - flen)
        else:
            u = rng.uniform(0, 1) * (TLEN - flen)
        u = int(u)
        off = u if g['strand'] == '+' else (TLEN - flen - u)   # spliced genome-order offset of fragment left end
        if g['strand'] == '-' and bias3 and False:
            pass
        left_start, left_cig = spliced_blocks(g, off, readlen)
        right_start, right_cig = spliced_blocks(g, off + flen - readlen, readlen)
        # which mate is on the left?
        gene_plus = g['strand'] == '+'
        read1_sense = {'dutp': False, 'fwd': True}.get(protocol, bool(rng.random() < 0.5))
        if protocol in ('dutp', 'fwd') and leak and rng.random() < leak:
            read1_sense = not read1_sense
        read1_strand_plus = (gene_plus == read1_sense)
        xs = g['strand']
        if read1_strand_plus:   # read1 maps + and is the left read; read2 maps - and is the right read
            f1, f2 = 99, 147
            r1 = mk_read(name, left_start, left_cig, f1, xs=xs if any(o == 3 for o, _ in left_cig) else None, mate=right_start, tlen=flen, hdr=hdr)
            r2 = mk_read(name, right_start, right_cig, f2, xs=xs if any(o == 3 for o, _ in right_cig) else None, mate=left_start, tlen=-flen, hdr=hdr)
        else:                    # read1 maps - (right read); read2 maps + (left read)
            f1, f2 = 83, 163
            r1 = mk_read(name, right_start, right_cig, f1, xs=xs if any(o == 3 for o, _ in right_cig) else None, mate=left_start, tlen=-flen, hdr=hdr)
            r2 = mk_read(name, left_start, left_cig, f2, xs=xs if any(o == 3 for o, _ in left_cig) else None, mate=right_start, tlen=flen, hdr=hdr)
        recs += [r1, r2]
    recs = [r for r in recs]
    recs.sort(key=lambda r: (r.reference_id if r.reference_id >= 0 else 10**9, r.reference_start))
    write_sorted(path, recs, hdr)
    return len(recs)

# mapping check for spliced_blocks
g0 = genes[0]
rs, cg = spliced_blocks(g0, 250, 100)
assert rs == g0['starts'][0] + 250 and cg[0] == (0, 50) and cg[1][0] == 3 and cg[2] == (0, 50), (rs, cg)

NF = 20000
pe = {}
pe['dutp'] = pe_bam(f'{OUT}/pe_dutp.bam', NF, 'dutp', tag='du')
pe['fwd'] = pe_bam(f'{OUT}/pe_fwd.bam', NF, 'fwd', tag='fw')
pe['unstr'] = pe_bam(f'{OUT}/pe_unstr.bam', NF, 'unstr', tag='un')
pe['dutp_leak20'] = pe_bam(f'{OUT}/pe_dutp_leak20.bam', NF, 'dutp', leak=0.20, tag='dl')
pe['dutp_leak40'] = pe_bam(f'{OUT}/pe_dutp_leak40.bam', NF, 'dutp', leak=0.40, tag='d4')
TRUTH['strand'] = dict(dutp='read1 antisense: 100% reverse-stranded (fr-firststrand)', fwd='100% forward (fr-secondstrand)',
                       unstr='50/50', dutp_leak20='80% reverse / 20% forward', dutp_leak40='60/40')
# 3' bias: 85% of fragments from the last 25% of the transcript
pe['bias3'] = pe_bam(f'{OUT}/pe_bias3.bam', NF, 'dutp', bias3=0.85, tag='b3')
# rRNA + multimappers + unmapped: truth defined on primary-mapped fragments
NR = 20000
pe['rrna'] = pe_bam(f'{OUT}/pe_rrna.bam', NR, 'dutp', rrna_frac=0.22, multi_frac=0.5, unmapped_frac=0.08, tag='rr')
TRUTH['rrna'] = dict(note='fragments: 20000; 8% unmapped pairs; of mapped fragments 22% rRNA (expected), half of rRNA fragments multi-map to 4 loci (3 secondary pairs, MAPQ 3)')
TRUTH['pe_record_counts'] = pe

json.dump(TRUTH, open(f'{OUT}/truth.json', 'w'), indent=1)
print('done', {k: (v['rseqc_known_read_frac'] if isinstance(v, dict) and 'rseqc_known_read_frac' in v else None) for k, v in TRUTH.items() if isinstance(v, dict)})
