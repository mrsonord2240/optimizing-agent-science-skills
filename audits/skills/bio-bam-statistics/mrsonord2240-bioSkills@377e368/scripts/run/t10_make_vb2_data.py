#!/usr/bin/env python3
"""SYNTHETIC input for an end-to-end VerifyBamID2 run (block 035): chr20 random reference (64,444,167 bp; panel ref alleles planted at the 204 panel markers on chr20) and a
coordinate-sorted BAM with 40 reads over every chr20 panel marker (genotype: ref/ref for 1/3, ref/alt for 1/3, alt/alt for 1/3 of markers, no contamination planted).
Purpose: show the command line runs to a FREEMIX value (not a biological result). Written to run/work/vb2/."""
import os, random
import pysam
random.seed(4242)
D = '/mnt/openscience/audit-envs/alignment-files/public-data/resources/1000g.phase3.10k.b38.vcf.gz.dat.bed'
OUT = '/mnt/openscience/audits/bio-bam-statistics/run/work/vb2'; os.makedirs(OUT, exist_ok=True)
L = 64444167
mk = [l.split() for l in open(D) if l.startswith('chr20\t')]
mk = [(int(a[1]), a[3], a[4]) for a in mk]     # (0-based pos, ref, alt)
seq = bytearray(random.choices(b'ACGT', k=L))
for p, r, a in mk: seq[p] = ord(r)
with open(f'{OUT}/chr20.fa', 'w') as fh:
    fh.write('>chr20\n')
    for i in range(0, L, 60): fh.write(seq[i:i + 60].decode() + '\n')
pysam.faidx(f'{OUT}/chr20.fa')
hdr = pysam.AlignmentHeader.from_dict({'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'chr20', 'LN': L}], 'RG': [{'ID': 'g1', 'SM': 'synthS'}]})
recs = []
for i, (p, r, a) in enumerate(mk):
    g = i % 3    # 0 ref/ref, 1 ref/alt, 2 alt/alt
    for k in range(40):
        st = max(0, p - random.randint(10, 89))
        s = bytearray(seq[st:st + 100])
        allele = r if g == 0 else a if g == 2 else (r if k % 2 == 0 else a)
        s[p - st] = ord(allele)
        x = pysam.AlignedSegment(hdr); x.query_name = f'm{i}_{k}'; x.flag = 0; x.reference_id = 0; x.reference_start = st
        x.mapping_quality = 60; x.cigarstring = '100M'; x.query_sequence = s.decode()
        x.query_qualities = pysam.qualitystring_to_array('I' * 100); x.set_tag('RG', 'g1'); recs.append(x)
recs.sort(key=lambda x: x.reference_start)
with pysam.AlignmentFile(f'{OUT}/vb2.bam', 'wb', header=hdr) as b:
    for x in recs: b.write(x)
pysam.index(f'{OUT}/vb2.bam')
print('markers', len(mk), 'reads', len(recs))
