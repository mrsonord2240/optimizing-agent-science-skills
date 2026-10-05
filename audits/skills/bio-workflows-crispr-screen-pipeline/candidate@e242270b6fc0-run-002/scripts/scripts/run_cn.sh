#!/bin/bash
export HOME=/home/sci
cd /mnt/openscience/fix-evidence/recut-crispr-pipeline/audit-initial/run-002/work/cn
time /home/sci/micromamba/envs/crispr-ccr/bin/Rscript /mnt/openscience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline/scripts/cn_correction.R a375.count.txt screen
echo EXIT=$?
# trap: qc.py on corrected table (non-integer)
