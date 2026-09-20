#!/bin/bash
# Whole re-audit, in order. Usage (Git Bash):
#   F:/OpenScience/audit-envs/alignment-files/wsl_run.sh 'bash /mnt/openscience/audits/bio-sam-bam-basics/run/run_all.sh'
# then: bash run/run_rsamtools.sh   (Windows R via r.sh)
# Skill under test = the COPY in run/skill (from worktree wt/af-sambam @ 35712f5), never the worktree or the external/ clone.
cd /mnt/openscience/audits/bio-sam-bam-basics/run
export PYTHONIOENCODING=utf-8
bash run_regress.sh
python -u new/dedup_check.py > out/dedup_check.txt 2>&1
python -u new/misc_claims.py > out/misc_claims.txt 2>&1
bash new/in5c_mapdamage.sh > out/in5c_mapdamage.txt 2>&1
python -u new/tags_check.py > out/tags_check.txt 2>&1
python -u new/in6.py > out/in6.txt 2>&1
python -u new/in7.py > out/in7.txt 2>&1
python -u new/in8.py > out/in8.txt 2>&1
rm -rf skill/examples/__pycache__
echo done
