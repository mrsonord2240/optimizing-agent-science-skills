#!/bin/bash
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work
python $R/t11_basesmapped.py
echo "--- same fields on the real human BAM and the ARTIC BAM (stats vs CIGAR walk)"
for b in $AFDATA/human/test.paired_end.sorted.bam $AFDATA/sarscov2/sars-cov-2_v5.3.2.nanopore.bam; do samtools stats $b | grep -E '^SN\s+bases mapped' | cut -f2-3 | tr '\n' ' '; python - "$b" <<'PY'
import sys, pysam
q=c=0
with pysam.AlignmentFile(sys.argv[1]) as bam:
    for r in bam:
        if r.is_unmapped or r.is_secondary or r.is_supplementary or r.is_qcfail: continue
        q+=r.query_length; c+=sum(n for op,n in r.cigartuples if op in (0,7,8))
print(f'| walk: query bases of mapped primary = {q}, M/=/X bases = {c}')
PY
done
