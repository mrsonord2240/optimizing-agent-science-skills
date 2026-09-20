#!/usr/bin/env python3
"""NEW input 7 data (SYNTHETIC, seed 7707): planted-depth BAM with zero-coverage regions, a contig with NO reads,
a contig-end stack, deletions, spliced (N) reads, excluded-by-default reads and overlapping proper pairs.
Truth is written BY CONSTRUCTION with explicit interval additions (not by parsing the BAM back).
Writes run/data/planted_depth.bam(+.bai), planted_depth.fa(+.fai), planted_depth.truth.json, planted_depth.regions.bed"""
import json, os, random
import numpy as np
import pysam

random.seed(7707)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUT, exist_ok=True)
CONTIGS = {'chrA': 10000, 'chrB': 5000, 'chrC': 3000, 'chrD': 4000}   # chrC gets no reads at all
REF = {c: ''.join(random.choice('ACGT') for _ in range(l)) for c, l in CONTIGS.items()}
with open(f'{OUT}/planted_depth.fa', 'w') as fh:
    for c, s in REF.items():
        fh.write(f'>{c}\n{s}\n')
pysam.faidx(f'{OUT}/planted_depth.fa')
hdr = pysam.AlignmentHeader.from_dict({'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': c, 'LN': l} for c, l in CONTIGS.items()]})
TID = {c: i for i, c in enumerate(CONTIGS)}
T_default = {c: np.zeros(l, dtype=np.int64) for c, l in CONTIGS.items()}   # samtools depth defaults (mates both counted; excluded flags dropped; D/N not counted)
T_once = {c: np.zeros(l, dtype=np.int64) for c, l in CONTIGS.items()}      # mates counted once
recs = []
n_qcfail = n_dup = n_sec = n_unm = 0


def read(name, contig, pos, cigar, flag=0, mapq=60, bq=30, mate=None, tlen=0):
    """cigar is a list of (op, len); sequence length = sum of M/I/S."""
    qlen = sum(n for op, n in cigar if op in 'MIS')
    a = pysam.AlignedSegment(hdr)
    a.query_name = name; a.flag = flag; a.reference_id = TID[contig]; a.reference_start = pos
    a.mapping_quality = mapq
    a.cigarstring = ''.join(f'{n}{op}' for op, n in cigar)
    a.query_sequence = ''.join(random.choice('ACGT') for _ in range(qlen))
    a.query_qualities = pysam.qualitystring_to_array(chr(33 + bq) * qlen)
    if mate is not None:
        a.next_reference_id = TID[contig]; a.next_reference_start = mate; a.template_length = tlen
    a.set_tag('NM', 0)
    recs.append(a)


def stack(contig, s, e, depth, tag, step=100, **kw):
    """exact depth over [s,e): `depth` reads of 100M at every start s, s+100, ... (e-s multiple of 100). Counted."""
    for st in range(s, e, step):
        for k in range(depth):
            read(f'{tag}_{st}_{k}', contig, st, [('M', 100)], **kw)
    T_default[contig][s:e] += depth
    T_once[contig][s:e] += depth


stack('chrA', 1000, 2000, 30, 'a30')
stack('chrA', 3000, 3500, 8, 'a8')
stack('chrA', 5000, 5100, 100, 'a100')
# MAPQ 0 and low-BQ reads ARE counted by samtools depth (-q 0 -Q 0), mosdepth (-Q 0) and coverage; plant 3 + 4 at [3000,3100)
for k in range(3):
    read(f'mq0_{k}', 'chrA', 3000, [('M', 100)], mapq=0)
for k in range(4):
    read(f'lbq_{k}', 'chrA', 3000, [('M', 100)], bq=2)
T_default['chrA'][3000:3100] += 7; T_once['chrA'][3000:3100] += 7
# excluded by default (UNMAP 4 | SECONDARY 256 | QCFAIL 512 | DUP 1024): must not change any tool's depth
for k in range(5):
    read(f'qcf_{k}', 'chrA', 1000, [('M', 100)], flag=512); n_qcfail += 1
for k in range(7):
    read(f'dup_{k}', 'chrA', 1000, [('M', 100)], flag=1024); n_dup += 1
for k in range(3):
    read(f'sec_{k}', 'chrA', 1000, [('M', 100)], flag=256, mapq=0); n_sec += 1
read('unm_0', 'chrA', 2000, [('M', 100)], flag=4); n_unm += 1
# overlapping proper pairs: read1 fwd at 7000, read2 rev at 7050 (overlap 50 bp), 10 pairs
for k in range(10):
    read(f'ov_{k}', 'chrA', 7000, [('M', 100)], flag=99, mate=7050, tlen=150)
    read(f'ov_{k}', 'chrA', 7050, [('M', 100)], flag=147, mate=7000, tlen=-150)
T_default['chrA'][7000:7100] += 10; T_default['chrA'][7050:7150] += 10
T_once['chrA'][7000:7150] += 10
# chrB: [0,500) depth 12, and a stack at the very end [4900,5000) depth 3
stack('chrB', 0, 500, 12, 'b12')
stack('chrB', 4900, 5000, 3, 'b3')
# chrC: no reads
# chrD: 20 reads 50M10D50M at 500 (deleted ref 550-560 not counted), 15 spliced reads 50M500N50M at 1000 (skipped 1050-1550 not counted)
for k in range(20):
    read(f'del_{k}', 'chrD', 500, [('M', 50), ('D', 10), ('M', 50)])
T_default['chrD'][500:550] += 20; T_default['chrD'][560:610] += 20
for k in range(15):
    read(f'spl_{k}', 'chrD', 1000, [('M', 50), ('N', 500), ('M', 50)])
T_default['chrD'][1000:1050] += 15; T_default['chrD'][1550:1600] += 15
T_once['chrD'] += T_default['chrD'] - T_once['chrD'] - 0  # single-end reads: identical
recs.sort(key=lambda a: (a.reference_id, a.reference_start))
path = f'{OUT}/planted_depth.bam'
with pysam.AlignmentFile(path, 'wb', header=hdr) as bam:
    for a in recs:
        bam.write(a)
pysam.index(path)
# T_once for chrB/chrD single-end pieces equals T_default: fix arrays built only from stack() (already added to both) and chrD (copied)
tot = int(sum(v.sum() for v in T_default.values())); L = sum(CONTIGS.values())
allv = np.concatenate([T_default[c] for c in CONTIGS])
allv1 = np.concatenate([T_once[c] for c in CONTIGS])
truth = {
    'note': 'SYNTHETIC; truth by construction', 'total_bases': L, 'contigs': CONTIGS,
    'records': len(recs), 'excluded_qcfail': n_qcfail, 'excluded_dup': n_dup, 'excluded_secondary': n_sec, 'unmapped_placed': n_unm,
    'sum_depth_default': tot, 'mean_depth_default_all_contigs': tot / L,
    'covered_default': int((allv > 0).sum()), 'ge10_default': int((allv >= 10).sum()), 'ge20_default': int((allv >= 20).sum()), 'max_default': int(allv.max()),
    'mean_depth_mates_once': float(allv1.sum()) / L, 'ge10_once': int((allv1 >= 10).sum()), 'ge20_once': int((allv1 >= 20).sum()),
    'per_contig': {c: {'len': l, 'sum': int(T_default[c].sum()), 'mean': float(T_default[c].sum()) / l, 'covered': int((T_default[c] > 0).sum())} for c, l in CONTIGS.items()},
    'covered_contigs_only_len': sum(l for c, l in CONTIGS.items() if T_default[c].sum() > 0),
}
truth['mean_depth_default_read_contigs_only'] = tot / truth['covered_contigs_only_len']
json.dump(truth, open(f'{OUT}/planted_depth.truth.json', 'w'), indent=1)
for c in CONTIGS:
    np.save(f'{OUT}/planted_depth.truth.{c}.npy', T_default[c])
# BED used by the coverage-loop / depth -b tests: 0-based half-open; extra columns; a region on the read-less chrC; one at the contig end; start=0
with open(f'{OUT}/planted_depth.regions.bed', 'w') as fh:
    fh.write('chrA\t1000\t2000\tR1\t0\t+\n')
    fh.write('chrA\t3000\t3500\tR2\n')
    fh.write('chrB\t0\t500\tR3\n')
    fh.write('chrB\t4900\t5000\tR4\n')
    fh.write('chrC\t100\t400\tR5_noreads\n')
    fh.write('chrD\t500\t610\tR6_deletion\n')
    fh.write('chrD\t1000\t1600\tR7_spliced\n')
print(json.dumps(truth, indent=1))
