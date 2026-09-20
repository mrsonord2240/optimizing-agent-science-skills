#!/bin/bash
# INPUT 4b (REAL deep amplicon, ARTIC nanopore): all depth tools vs block-based truth
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
samtools index work/batch/artic_nanopore.bam; python t2_coverage.py work/batch/artic_nanopore.bam MN908947.3 29903 > out/t4b_artic.txt 2>&1
cat out/t4b_artic.txt
echo "--- pysam max_depth effect on real ARTIC"
python - <<'PY' >> out/t4b_artic.txt 2>&1
import pysam, numpy as np
for kw in ({}, {'max_depth': 1000000}):
    d = np.zeros(29903, int)
    with pysam.AlignmentFile('work/batch/artic_nanopore.bam') as f:
        for c in f.pileup('MN908947.3', 0, 29903, truncate=True, **kw): d[c.reference_pos] = c.n
    print('pysam pileup', kw or 'DEFAULT', 'max =', d.max(), 'mean =', round(d.sum()/29903, 3), 'covered =', (d>0).sum())
PY
tail -3 out/t4b_artic.txt
