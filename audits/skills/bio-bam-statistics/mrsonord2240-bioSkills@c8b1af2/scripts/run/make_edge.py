#!/usr/bin/env python3
"""NEW input 8 data (SYNTHETIC, seed 88): edge-case BAMs for the pysam counters and examples/qc_report.py.
Expected QC-passed-column counts are written BY CONSTRUCTION (not from flagstat) to data/edge/expected.json.
BAMs: unmapped_only, ubam_no_sq, supp_sec_heavy, qcfail_heavy, all_qcfail, all_dup_pe, se_dup, mixed_pairs, se_reverse_only."""
import json, os, random
import pysam

random.seed(88)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'edge')
os.makedirs(OUT, exist_ok=True)
SQ = [{'SN': 'c1', 'LN': 50000}, {'SN': 'c2', 'LN': 30000}]
REF = {c['SN']: ''.join(random.choice('ACGT') for _ in range(c['LN'])) for c in SQ}
HDR = pysam.AlignmentHeader.from_dict({'HD': {'VN': '1.6', 'SO': 'unsorted'}, 'SQ': SQ})
HDR_NOSQ = pysam.AlignmentHeader.from_dict({'HD': {'VN': '1.6'}, 'RG': [{'ID': 'x', 'SM': 's'}]})
TID = {'c1': 0, 'c2': 1}
expected = {}


def rec(hdr, name, flag, contig=None, pos=-1, cigar=None, mapq=0, mate_contig=None, mate_pos=-1, tlen=0, qlen=100):
    a = pysam.AlignedSegment(hdr)
    a.query_name = name; a.flag = flag
    a.reference_id = TID[contig] if contig else -1
    a.reference_start = pos if contig else -1
    a.mapping_quality = mapq
    if cigar:
        a.cigarstring = cigar
    a.query_sequence = ''.join(random.choice('ACGT') for _ in range(qlen))
    a.query_qualities = pysam.qualitystring_to_array('I' * qlen)
    a.next_reference_id = TID[mate_contig] if mate_contig else -1
    a.next_reference_start = mate_pos if mate_contig else -1
    a.template_length = tlen
    return a


def write(name, hdr, recs, exp):
    path = f'{OUT}/{name}.bam'
    with pysam.AlignmentFile(path, 'wb', header=hdr) as bam:
        for r in recs:
            bam.write(r)
    expected[name] = exp


def pair(i, flags, pos, contig='c1', ins=300, mapq=60):
    p2 = pos + ins - 100
    return [rec(HDR, f'p{i}', flags[0], contig, pos, '100M', mapq, contig, p2, ins), rec(HDR, f'p{i}', flags[1], contig, p2, '100M', mapq, contig, pos, -ins)]


# 1 unmapped only: 50 PE pairs, no coordinates (flags 77/141) + 20 SE unmapped (4)
r = []
for i in range(50):
    r += [rec(HDR, f'u{i}', 77), rec(HDR, f'u{i}', 141)]
for i in range(20):
    r.append(rec(HDR, f'v{i}', 4))
write('unmapped_only', HDR, r, dict(records=120, primary=120, secondary=0, supplementary=0, qcfail_primary=0, passed=120, mapped=0, paired=100, proper=0, dup=0))
# 2 uBAM without @SQ (SE unmapped)
write('ubam_no_sq', HDR_NOSQ, [rec(HDR_NOSQ, f'w{i}', 4) for i in range(30)], dict(records=30, primary=30, secondary=0, supplementary=0, qcfail_primary=0, passed=30, mapped=0, paired=0, proper=0, dup=0))
# 3 long-read style: 100 primary SE mapped (60 fwd, 40 rev), 300 supplementary (2048/2064), 200 secondary (256/272), 10 primary unmapped
r = []
for i in range(100):
    r.append(rec(HDR, f'L{i}', 0 if i < 60 else 16, 'c1', 1000 + i * 300, '100M', 60))
for i in range(300):
    r.append(rec(HDR, f'L{i % 100}', 2048 if i % 2 else 2064, 'c2', 500 + i * 50, '60M40S', 20))
for i in range(200):
    r.append(rec(HDR, f'L{i % 100}', 256 if i % 2 else 272, 'c2', 20000 + i * 40, '100M', 0))
for i in range(10):
    r.append(rec(HDR, f'Lu{i}', 4))
write('supp_sec_heavy', HDR, r, dict(records=610, primary=110, secondary=200, supplementary=300, qcfail_primary=0, passed=110, mapped=100, paired=0, proper=0, dup=0))
# 4 QC-fail heavy: 100 proper PE pairs (200 rec) QC-passed with 20 duplicates pairs; 100 pairs (200 rec) QC-failed (half also duplicate, 30 pairs not proper); 20 QC-failed secondary records
r = []
for i in range(100):
    fl = (99 | (1024 if i < 20 else 0), 147 | (1024 if i < 20 else 0))
    r += pair(i, fl, 1000 + i * 400)
for i in range(100, 200):
    dup = 1024 if i % 2 else 0
    proper = 2 if i >= 130 else 0
    r += pair(i, ((97 | proper | 512 | dup), (145 | proper | 512 | dup)), 1000 + i * 400)
for i in range(20):
    r.append(rec(HDR, f'q{i}', 256 | 512 | 1, 'c2', 100 + i * 50, '100M', 0))
write('qcfail_heavy', HDR, r, dict(records=420, primary=400, secondary=20, supplementary=0, qcfail_primary=200, passed=200, mapped=200, paired=200, proper=200, dup=40))
# 5 all QC-fail (10 SE mapped reads, all 0x200)
write('all_qcfail', HDR, [rec(HDR, f'z{i}', 512, 'c1', 100 + i * 200, '100M', 60) for i in range(10)], dict(records=10, primary=10, secondary=0, supplementary=0, qcfail_primary=10, passed=0, mapped=0, paired=0, proper=0, dup=0))
# 6 all duplicates PE (30 pairs) + one supplementary flagged duplicate
r = []
for i in range(30):
    r += pair(i, (99 | 1024, 147 | 1024), 2000 + i * 500)
r.append(rec(HDR, 'p0', 2048 | 1024 | 1 | 64, 'c2', 10, '50M50S', 30))
write('all_dup_pe', HDR, r, dict(records=61, primary=60, secondary=0, supplementary=1, qcfail_primary=0, passed=60, mapped=60, paired=60, proper=60, dup=60))
# 7 SE duplicates: 40 reads, 15 dup
write('se_dup', HDR, [rec(HDR, f's{i}', 1024 if i < 15 else 0, 'c1', 500 + i * 150, '100M', 60) for i in range(40)], dict(records=40, primary=40, secondary=0, supplementary=0, qcfail_primary=0, passed=40, mapped=40, paired=0, proper=0, dup=15))
# 8 mixed pairs: 10 proper; 10 both mapped not proper; 10 mate unmapped (singleton); 10 mate on other chr; 5 proper-flag on read1 only (inconsistent mate flags)
r = []
for i in range(10):
    r += pair(f'a{i}', (99, 147), 1000 + i * 500)
for i in range(10):
    r += pair(f'b{i}', (97, 145), 6000 + i * 500)
for i in range(10):
    r += [rec(HDR, f'c{i}', 73, 'c1', 12000 + i * 300, '100M', 60, 'c1', 12000 + i * 300), rec(HDR, f'c{i}', 133, 'c1', 12000 + i * 300, None, 0, 'c1', 12000 + i * 300)]
for i in range(10):
    r += [rec(HDR, f'd{i}', 97, 'c1', 20000 + i * 300, '100M', 60, 'c2', 500 + i * 300), rec(HDR, f'd{i}', 145, 'c2', 500 + i * 300, '100M', 60, 'c1', 20000 + i * 300)]
for i in range(5):
    r += [rec(HDR, f'e{i}', 99, 'c1', 30000 + i * 500, '100M', 60, 'c1', 30300 + i * 500, 400), rec(HDR, f'e{i}', 145, 'c1', 30300 + i * 500, '100M', 60, 'c1', 30000 + i * 500, -400)]
# expected (QC-passed col): records 10*2 (a) + 10*2 (b) + 10*2 (c) + 10*2 (d) + 5*2 (e) = 90; mapped = 90 - 10 unmapped mates = 80; paired 90; proper = 20 (a) + 5 (e read1 only) = 25
write('mixed_pairs', HDR, r, dict(records=90, primary=90, secondary=0, supplementary=0, qcfail_primary=0, passed=90, mapped=80, paired=90, proper=25, dup=0))
# 9 single-end reverse-only mapped, MAPQ 0 (multi-mappers), 25 reads
write('se_reverse_only', HDR, [rec(HDR, f'r{i}', 16, 'c2', 1000 + i * 120, '100M', 0) for i in range(25)], dict(records=25, primary=25, secondary=0, supplementary=0, qcfail_primary=0, passed=25, mapped=25, paired=0, proper=0, dup=0))
json.dump(expected, open(f'{OUT}/expected.json', 'w'), indent=1)
for n in expected:
    p = f'{OUT}/{n}.bam'
    if n != 'ubam_no_sq':
        # sort + index so coordinate-based tools (idxstats, mosdepth, coverage) can run
        pysam.sort('-o', f'{OUT}/{n}.sorted.bam', p)
        os.replace(f'{OUT}/{n}.sorted.bam', p)
        pysam.index(p)
print(json.dumps(expected))
