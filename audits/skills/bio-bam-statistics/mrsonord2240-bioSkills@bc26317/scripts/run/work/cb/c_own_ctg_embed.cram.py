import pysam

with pysam.AlignmentFile('/mnt/openscience/audits/bio-bam-statistics/run/data/new/own_ctg_embed.cram', 'rb', check_sq=False) as bam:
    primary = mapped = paired = proper = 0
    for read in bam:
        if read.is_secondary or read.is_supplementary or read.is_qcfail:
            continue
        primary += 1
        mapped += not read.is_unmapped
        paired += read.is_paired
        proper += read.is_proper_pair

if not primary:
    raise SystemExit('no QC-passed primary reads')
print(f'Primary QC-passed: {primary}')
print(f'Mapped: {mapped} ({mapped/primary*100:.2f}% of primary)')
if paired:
    print(f'Properly paired: {proper} ({proper/paired*100:.2f}% of primary paired)')
else:
    print('Single-end data: no paired reads')
