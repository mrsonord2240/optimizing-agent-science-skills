#!/bin/bash
# NEW: exact pysam error strings quoted in the Skill's pysam paragraph, and block 028 (per-chromosome counts) on a uBAM / unindexed BAM.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; N=$R/data/new; cd $R/work
U=$R/data/edge/ubam_no_sq.bam
python - <<PY 2>&1 | grep -v cram_index | cut -c1-200
import pysam
try:
    pysam.AlignmentFile('$U','rb').close(); print('plain open OK (unexpected)')
except Exception as e: print('plain AlignmentFile(uBAM,"rb") ->', type(e).__name__+':', e)
with pysam.AlignmentFile('$U','rb',check_sq=False) as b: print('check_sq=False: records', sum(1 for _ in b))
try:
    with pysam.AlignmentFile('$N/own_ctg.cram','rb') as b: print('CRAM w/o reference_filename, UR intact, reads:', sum(1 for _ in b))
except Exception as e: print('CRAM no ref ->', type(e).__name__+':', e)
PY
for f in $U $N/own_ctg.bam $R/data/noindex.bam; do echo "--- block 028 on $(basename $f)"; sed "s#'input.bam'#'$f'#" $R/blocks/028_python.py > pc.py; python pc.py 2>&1 | tail -3 | cut -c1-160; done
