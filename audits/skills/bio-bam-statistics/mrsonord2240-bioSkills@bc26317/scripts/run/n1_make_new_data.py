#!/usr/bin/env python3
"""NEW inputs of the second re-audit (2026-09-20), all SYNTHETIC, truth by construction (independent of every tool under test).
  own_ctg.bam/.cram    : 3 contigs (ctgA 20 kb, ctgB 5 kb with NO reads, ctgC 100 bp), tiled depth 10 + a 30x spike + 50x contig; extras that depth
                         excludes (7 QC-fail, 5 dup, 3 secondary) or counts (4 supplementary), 6 unmapped unplaced reads; BAM, CRAM (ref), CRAM (embed_ref), CRAM unindexed
  own_insert.bam       : proper pairs with template lengths 300 x10, 7000 x3, 7999, 8000, 8001, 8500 x2 (boundary of qc_report MAX_INSERT = 8000)
  own_del.bam          : 20 reads with a 20 bp deletion, 20 spliced reads (200 bp N), 10 overlapping pairs (frag 150, read 100); bcftools/mosdepth deletion + overlap claims
  bad inputs           : truncated BAM, text file named .bam, zero-byte .bam, CRAM decoded against a WRONG reference
"""
import os, re, random, json, subprocess, hashlib
import numpy as np
import pysam

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'data', 'new'); os.makedirs(OUT, exist_ok=True)
rng = random.Random(20260920)
def rseq(n): return ''.join(rng.choice('ACGT') for _ in range(n))

def write_bam(path, contigs, reads):
    hdr = {'HD': {'VN': '1.6', 'SO': 'coordinate'},
           'SQ': [{'SN': n, 'LN': len(s), 'M5': hashlib.md5(s.encode()).hexdigest()} for n, s in contigs.items()]}
    names = list(contigs)
    tmp = path + '.unsorted.bam'
    with pysam.AlignmentFile(tmp, 'wb', header=hdr) as out:
        for r in reads:
            a = pysam.AlignedSegment(out.header)
            a.query_name = r['name']; a.flag = r.get('flag', 0)
            if r.get('ctg') is not None:
                a.reference_id = names.index(r['ctg']); a.reference_start = r['pos']
                a.cigarstring = r['cigar']; a.mapping_quality = r.get('mapq', 60)
                q = ''; p = r['pos']
                for n_, op in re.findall(r'(\d+)([MIDNS=X])', r['cigar']):   # query = reference bases: zero mismatches
                    n_ = int(n_)
                    if op in 'M=X': q += contigs[r['ctg']][p:p + n_]; p += n_
                    elif op in 'DN': p += n_
                    elif op == 'S': q += 'A' * n_
            else:
                a.reference_id = -1; a.reference_start = -1; a.mapping_quality = 0
                q = rseq(100)
            a.query_sequence = q; a.query_qualities = pysam.qualitystring_to_array('I' * len(q))
            if 'mate' in r:
                a.next_reference_id = names.index(r['mate'][0]); a.next_reference_start = r['mate'][1]; a.template_length = r['tlen']
            out.write(a)
    pysam.sort('-o', path, tmp); os.remove(tmp); pysam.index(path)

def write_fa(path, contigs):
    with open(path, 'w') as fh:
        for n, s in contigs.items(): fh.write(f'>{n}\n{s}\n')
    pysam.faidx(path)

# ---------------------------------------------------------------- own_ctg
ctg = {'ctgA': rseq(20000), 'ctgB': rseq(5000), 'ctgC': rseq(100)}
write_fa(f'{OUT}/own_ctg.fa', ctg)
reads = []; k = 0
for st in range(0, 10000, 100):
    for _ in range(10): reads.append(dict(name=f't{k}', ctg='ctgA', pos=st, cigar='100M')); k += 1
for _ in range(30): reads.append(dict(name=f'spike{k}', ctg='ctgA', pos=15000, cigar='500M')); k += 1
for _ in range(50): reads.append(dict(name=f'c{k}', ctg='ctgC', pos=0, cigar='100M')); k += 1
for _ in range(7): reads.append(dict(name=f'qf{k}', ctg='ctgA', pos=0, cigar='100M', flag=512)); k += 1
for _ in range(5): reads.append(dict(name=f'dup{k}', ctg='ctgA', pos=2000, cigar='100M', flag=1024)); k += 1
for _ in range(3): reads.append(dict(name=f'sec{k}', ctg='ctgA', pos=2000, cigar='100M', flag=256)); k += 1
for _ in range(4): reads.append(dict(name=f'sup{k}', ctg='ctgA', pos=3000, cigar='50M50S', flag=2048)); k += 1
for _ in range(6): reads.append(dict(name=f'un{k}', flag=4)); k += 1
write_bam(f'{OUT}/own_ctg.bam', ctg, reads)
tot = {n: len(s) for n, s in ctg.items()}
d = {n: np.zeros(L, dtype=int) for n, L in tot.items()}
d['ctgA'][0:10000] += 10; d['ctgA'][15000:15500] += 30; d['ctgC'][:] += 50; d['ctgA'][3000:3050] += 4
allv = np.concatenate([d[n] for n in ctg]); L = len(allv)
nrec = len(reads)
truth = dict(note='SYNTHETIC, by construction', total_len=L, len_contigs_with_reads=tot['ctgA'] + tot['ctgC'],
             sum_depth=int(allv.sum()), mean_all=float(allv.sum()) / L, mean_reads_contigs_only=float(allv.sum()) / (tot['ctgA'] + tot['ctgC']),
             ge10_all_pct=100.0 * (allv >= 10).sum() / L, ge20_all_pct=100.0 * (allv >= 20).sum() / L, max=int(allv.max()),
             covered=int((allv > 0).sum()),
             flagstat=dict(records=nrec, secondary=3, supplementary=4, primary=nrec - 7, qcfail_primary=7,
                           passed_primary=nrec - 7 - 7, primary_mapped_passed=nrec - 7 - 7 - 6, primary_dup=5, unmapped=6))
json.dump(truth, open(f'{OUT}/own_ctg.truth.json', 'w'), indent=1)
for n in ctg: np.save(f'{OUT}/own_ctg.truth.{n}.npy', d[n])
B, F = f'{OUT}/own_ctg.bam', f'{OUT}/own_ctg.fa'
subprocess.run(['samtools', 'view', '-C', '-T', F, '-o', f'{OUT}/own_ctg.cram', B], check=True); pysam.index(f'{OUT}/own_ctg.cram')
subprocess.run(['samtools', 'view', '-C', '-T', F, '--output-fmt-option', 'embed_ref=1', '-o', f'{OUT}/own_ctg_embed.cram', B], check=True)
subprocess.run(['samtools', 'view', '-C', '-T', F, '-o', f'{OUT}/own_ctg_noidx.cram', B], check=True)
write_fa(f'{OUT}/wrong.fa', {n: rseq(len(s)) for n, s in ctg.items()})   # same names and lengths, different bases

# ---------------------------------------------------------------- own_insert
ins = {'ins': rseq(30000)}
reads = []; pos = 100; k = 0
tl = [300] * 10 + [7000] * 3 + [7999, 8000, 8001] + [8500] * 2
for t in tl:
    reads.append(dict(name=f'p{k}', ctg='ins', pos=pos, cigar='100M', flag=1 + 2 + 32 + 64, mate=('ins', pos + t - 100), tlen=t))
    reads.append(dict(name=f'p{k}', ctg='ins', pos=pos + t - 100, cigar='100M', flag=1 + 2 + 16 + 128, mate=('ins', pos), tlen=-t))
    k += 1; pos = (pos + 350) % 12000 + 50
write_bam(f'{OUT}/own_insert.bam', ins, reads)
json.dump(dict(tlens=tl, n_pairs=len(tl)), open(f'{OUT}/own_insert.truth.json', 'w'))

# ---------------------------------------------------------------- own_del
dl = {'del': rseq(3000)}
write_fa(f'{OUT}/own_del.fa', dl)
reads = []; k = 0
for _ in range(20): reads.append(dict(name=f'd{k}', ctg='del', pos=500, cigar='40M20D40M')); k += 1
for _ in range(20): reads.append(dict(name=f's{k}', ctg='del', pos=1000, cigar='40M200N40M')); k += 1
for _ in range(10):
    reads.append(dict(name=f'o{k}', ctg='del', pos=2000, cigar='100M', flag=1 + 2 + 32 + 64, mate=('del', 2050), tlen=150))
    reads.append(dict(name=f'o{k}', ctg='del', pos=2050, cigar='100M', flag=1 + 2 + 16 + 128, mate=('del', 2000), tlen=-150)); k += 1
write_bam(f'{OUT}/own_del.bam', dl, reads)
dd = np.zeros(3000, dtype=int); dd[500:540] += 20; dd[560:600] += 20; dd[1000:1040] += 20; dd[1240:1280] += 20
dd[2000:2100] += 10; dd[2050:2150] += 10
np.save(f'{OUT}/own_del.truth_default.npy', dd)
d1 = np.zeros(3000, dtype=int); d1[500:540] += 20; d1[560:600] += 20; d1[1000:1040] += 20; d1[1240:1280] += 20; d1[2000:2150] += 10
np.save(f'{OUT}/own_del.truth_matesonce.npy', d1)
dfast = dd.copy(); dfast[540:560] += 20; dfast[1040:1240] += 20   # what a tool counting D and N as covered would report
np.save(f'{OUT}/own_del.truth_dn_covered.npy', dfast)
print('own_del truth sums: default', dd.sum(), 'mates once', d1.sum(), 'D+N covered', dfast.sum(), 'len 3000')

# ---------------------------------------------------------------- bad inputs
H = os.environ['AFDATA'] + '/human/test.paired_end.sorted.bam'
raw = open(H, 'rb').read()
open(f'{OUT}/truncated.bam', 'wb').write(raw[: len(raw) // 2])
open(f'{OUT}/text_named.bam', 'w').write('this is not a bam file\nat all\n')
open(f'{OUT}/zero_byte.bam', 'wb').close()
print('wrote', sorted(os.listdir(OUT)))
