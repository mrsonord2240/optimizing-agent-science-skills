#!/bin/bash
# Rsamtools bullet in SKILL.md ("R: scanBam() (Rsamtools)") through the env's r.sh (never bare Rscript). Run from Git Bash.
cd /f/OpenScience/audits/bio-sam-bam-basics/run
mkdir -p out
/f/OpenScience/audit-envs/alignment-files/r.sh regress/in1_rsamtools.R > out/in1_rsamtools.txt 2>&1
cat out/in1_rsamtools.txt
