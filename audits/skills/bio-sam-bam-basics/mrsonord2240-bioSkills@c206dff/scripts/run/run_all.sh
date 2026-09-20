#!/bin/bash
# Reproduce the whole audit from a clean run dir. Usage (Git Bash):
#   F:/OpenScience/audit-envs/alignment-files/wsl_run.sh 'bash /mnt/openscience/audits/bio-sam-bam-basics/run/run_all.sh'
# Skill under test is the COPY in run/skill (never the clone under external/).
cd /mnt/openscience/audits/bio-sam-bam-basics/run
mkdir -p out data
rm -f out/results.jsonl
bash 00_probe.sh > out/00_probe.txt 2>&1
python -u in1.py > out/in1.txt 2>&1
python -u in1b.py > out/in1b.txt 2>&1
python -u in2.py > out/in2.txt 2>&1
bash in2_diff.sh > out/in2_diff.txt 2>&1
python -u in3.py > out/in3.txt 2>&1
python -u in4.py > out/in4.txt 2>&1
python -u in4b.py > out/in4b.txt 2>&1
bash in5.sh > out/in5_sh.txt 2>&1
python -u in5.py > out/in5.txt 2>&1
echo done
grep -c . out/results.jsonl
