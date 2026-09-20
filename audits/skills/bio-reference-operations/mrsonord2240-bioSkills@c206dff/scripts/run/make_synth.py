#!/usr/bin/env python
"""SYNTHETIC data with planted truth for the bio-reference-operations audit.
Everything written here is synthetic (random seed 42), not real sequence.

Outputs (data/synthetic/):
  synth.fa          3 contigs, mixed line widths (80/60/70), soft-masked (lowercase) block, N run, descriptions in headers
  synth_chr.bam     reads on chr1 / chr2 with planted truth (see TRUTH below), coordinate sorted + indexed
  truth.json        planted truth used by the checkers
  synth_numeric.fa  the same sequences with contigs renamed chr1->1, chr2->2, chrM->MT (Ensembl style)
  variants.vcf.gz   phased VCF (+.tbi) for bcftools consensus
"""
import json, os, random, sys
import pysam

OUT = sys.argv[1] if len(sys.argv) > 1 else 'data/synthetic'
os.makedirs(OUT, exist_ok=True)
random.seed(42)


def rnd(n):
    return ''.join(random.choice('ACGT') for _ in range(n))


contigs = {'chr1': (rnd(5000), 80), 'chr2': (rnd(3007), 60), 'chrM': (rnd(1000), 70)}
c1 = list(contigs['chr1'][0])
for i in range(2000, 2050):
    c1[i] = 'N'                       # N run
contigs['chr1'] = (''.join(c1), 80)
# make sure planted-SNP positions are not N / are the base we expect
seqs = {k: v[0] for k, v in contigs.items()}
descr = {'chr1': 'synthetic contig one', 'chr2': 'synthetic contig two', 'chrM': 'synthetic mito'}


def write_fa(path, names):
    with open(path, 'w', newline='\n') as f:
        for k, (s, w) in contigs.items():
            s2 = s
            if k == 'chr1':                       # soft-mask 1000..1300 (0-based) in file only
                s2 = s[:1000] + s[1000:1300].lower() + s[1300:]
            f.write('>%s %s\n' % (names.get(k, k), descr[k]))
            for i in range(0, len(s2), w):
                f.write(s2[i:i + w] + '\n')


write_fa(f'{OUT}/synth.fa', {})
write_fa(f'{OUT}/synth_numeric.fa', {'chr1': '1', 'chr2': '2', 'chrM': 'MT'})

# ---------------- reads --------------------
header = {'HD': {'VN': '1.6', 'SO': 'coordinate'},
          'SQ': [{'SN': k, 'LN': len(s)} for k, s in seqs.items()]}
reads = []          # (tid, pos, seq, cigar_tuples, name)
S1 = seqs['chr1']
S2 = seqs['chr2']


def other(b):
    return {'A': 'C', 'C': 'G', 'G': 'T', 'T': 'A'}[b]


# chr1 planted truth (0-based positions)
HOM = 200      # every read carries alt
HET50 = 400    # every 2nd read carries alt
HET20 = 600    # every 5th read carries alt (fraction ~0.2 > default het-fract 0.15)
ERR1 = 800     # exactly one read carries alt (fraction ~3%)
LOW = 1550     # depth-2 region, both reads carry alt
alt = {p: other(S1[p]) for p in (HOM, HET50, HET20, ERR1, LOW)}
n = 0
for start in range(0, 901, 3):                  # depth ~33 across 100..900
    s = list(S1[start:start + 100])
    idx = n
    for p in range(start, start + 100):
        b = None
        if p == HOM:
            b = alt[p]
        elif p == HET50 and idx % 2 == 1:
            b = alt[p]
        elif p == HET20 and idx % 5 == 0:
            b = alt[p]
        elif p == ERR1 and idx == 100:
            b = alt[p]
        if b:
            s[p - start] = b
    reads.append((0, start, ''.join(s), [(0, 100)], 'c1_%04d' % n))
    n += 1
for st in (1500, 1500, 1600, 1600):             # depth 2 in 1500..1700 (gap 1000..1500 uncovered)
    s = list(S1[st:st + 100])
    if st <= LOW < st + 100:
        s[LOW - st] = alt[LOW]
    reads.append((0, st, ''.join(s), [(0, 100)], 'c1_low%d_%d' % (st, n)))
    n += 1

# chr2: all 31 reads (200 bp) carry a 3-base deletion (ref 550..552) and a 2-base insertion "GT" after ref 600
DEL = (550, 3)
INS_AFTER = 600
truth_c2 = None
for k, st in enumerate(range(420, 451)):
    # ref bases [st, 550) M, 3D, [553, 601) M -> ref consumed through position 600 inclusive, then 2I 'GT', then M
    a = 550 - st
    b = 601 - 553
    rest = 200 - a - b
    seq = S2[st:550] + S2[553:601] + 'GT' + S2[601:601 + rest - 2]
    cig = [(0, a), (2, 3), (0, b), (1, 2), (0, rest - 2)]
    assert len(seq) == 200 - 0, (len(seq), a, b, rest)
    reads.append((1, st, seq, cig, 'c2_%03d' % k))
# truth haplotype for chr2 over [420, 650): ref[420:550]+ref[553:601]+GT+ref[601:...]
# last read start 450 -> its ref end = 450 + (200-2) + 3 = 651 (exclusive), first read start 420
hap2 = S2[420:550] + S2[553:601] + 'GT' + S2[601:651]

with pysam.AlignmentFile(f'{OUT}/synth_chr.unsorted.bam', 'wb', header=header) as out:
    for tid, pos, seq, cig, name in reads:
        r = pysam.AlignedSegment(out.header)
        r.query_name = name
        r.query_sequence = seq
        r.flag = 0
        r.reference_id = tid
        r.reference_start = pos
        r.mapping_quality = 60
        r.cigartuples = cig
        r.query_qualities = pysam.qualitystring_to_array('I' * len(seq))   # Q40
        out.write(r)
pysam.sort('-o', f'{OUT}/synth_chr.bam', f'{OUT}/synth_chr.unsorted.bam')
pysam.index(f'{OUT}/synth_chr.bam')
os.remove(f'{OUT}/synth_chr.unsorted.bam')

# phased VCF for bcftools consensus
vcf_lines = ['##fileformat=VCFv4.2'] + ['##contig=<ID=%s,length=%d>' % (k, len(s)) for k, s in seqs.items()]
vcf_lines += ['##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">',
              '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1']
vcf_lines.append('chr1\t%d\t.\t%s\t%s\t50\tPASS\t.\tGT\t1|1' % (HOM + 1, S1[HOM], alt[HOM]))
vcf_lines.append('chr1\t%d\t.\t%s\t%s\t50\tPASS\t.\tGT\t1|0' % (HET50 + 1, S1[HET50], alt[HET50]))
vcf_lines.append('chr1\t%d\t.\t%s\t%s\t50\tPASS\t.\tGT\t0|1' % (HET20 + 1, S1[HET20], alt[HET20]))
# deletion of 3 bp after 550 (VCF anchor = base before), insertion GT after 600
vcf_lines.append('chr2\t%d\t.\t%s\t%s\t50\tPASS\t.\tGT\t1|1' % (DEL[0], S2[DEL[0] - 1:DEL[0] + 3], S2[DEL[0] - 1]))
vcf_lines.append('chr2\t%d\t.\t%s\t%s\t50\tPASS\t.\tGT\t1|1' % (INS_AFTER + 1, S2[INS_AFTER], S2[INS_AFTER] + 'GT'))
open(f'{OUT}/variants.vcf', 'w', newline='\n').write('\n'.join(vcf_lines) + '\n')
pysam.tabix_index(f'{OUT}/variants.vcf', preset='vcf', force=True)   # bgzips + indexes, removes plain vcf

json.dump({'HOM': HOM, 'HET50': HET50, 'HET20': HET20, 'ERR1': ERR1, 'LOW': LOW,
           'alt': {str(k): v for k, v in alt.items()},
           'ref_at': {str(k): S1[k] for k in alt},
           'hap2_start': 420, 'hap2': hap2,
           'seqs': seqs, 'widths': {k: v[1] for k, v in contigs.items()}},
          open(f'{OUT}/truth.json', 'w'), indent=1)
print('synthetic data written to', OUT)
print('chr1 alt bases:', alt, 'ref:', {k: S1[k] for k in alt})
print('reads:', len(reads))
