#!/bin/bash
# qc_report.py insert-size window: `0 < template_length < 1000` in the shipped script vs the Skill text.
export LC_ALL=C
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work; D=$R/data
echo "--- qc_report.py on rf.bam (proper flag SET, all inserts 2000; stats says average 2000.0)"; python $R/skill/examples/qc_report.py $D/rf.bam
echo "--- block 030 snippet on rf.bam"; sed "s#'input.bam'#'$D/rf.bam'#" $R/blocks/030_python.py > ins.py; python ins.py
grep -n '1000' $R/skill/examples/qc_report.py; grep -n -i 'less than 1000\|< 1000\|1000 bp\|insert.*cap\|window' $R/skill/SKILL.md | head
