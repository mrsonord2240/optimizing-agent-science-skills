#!/bin/bash
# Regression run: the 5 pre-fix inputs re-run against the FIXED Skill copy in run/skill. Judge by out/results.jsonl, not exit codes.
# Usage: F:/OpenScience/audit-envs/alignment-files/wsl_run.sh 'bash /mnt/openscience/audits/bio-sam-bam-basics/run/run_regress.sh'
cd /mnt/openscience/audits/bio-sam-bam-basics/run
mkdir -p out data
rm -f out/results.jsonl
export PYTHONIOENCODING=utf-8
bash regress/00_probe.sh > out/00_probe.txt 2>&1
python -u regress/in1.py > out/in1.txt 2>&1
python -u regress/in1b.py > out/in1b.txt 2>&1
python -u regress/in2.py > out/in2.txt 2>&1
bash regress/in2_diff.sh > out/in2_diff.txt 2>&1
python -u regress/in3.py > out/in3.txt 2>&1
python -u regress/in4.py > out/in4.txt 2>&1
python -u regress/in4b.py > out/in4b.txt 2>&1
bash regress/in5.sh > out/in5_sh.txt 2>&1
python -u regress/in5.py > out/in5.txt 2>&1
echo done
grep -c . out/results.jsonl
