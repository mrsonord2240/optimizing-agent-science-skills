#!/bin/bash
# Verify: pysam pileup.n counts deletion columns (explains 69.97 vs 68.84 on the ARTIC nanopore BAM)
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
D=/mnt/openscience/audit-envs/alignment-files/public-data/sarscov2
mkdir -p work/t4c && cp $D/sars-cov-2_v5.3.2.nanopore.bam work/t4c/a.bam && samtools index work/t4c/a.bam
python - > out/t4c_deletions.txt 2>&1 <<'PY'
import pysam
tot_n = tot_aligned = 0
with pysam.AlignmentFile('work/t4c/a.bam') as f:
    for c in f.pileup('MN908947.3', 0, 29903, truncate=True, max_depth=1000000, min_base_quality=0):
        tot_n += c.n
        tot_aligned += sum(1 for p in c.pileups if not p.is_del and not p.is_refskip)
print('sum of pileup.n =', tot_n, ' mean =', round(tot_n/29903, 3))
print('sum of pileup reads that are not deletion/refskip =', tot_aligned, ' mean =', round(tot_aligned/29903, 3), '(truth 68.8373)')
PY
cat out/t4c_deletions.txt; rm -rf work/t4c
