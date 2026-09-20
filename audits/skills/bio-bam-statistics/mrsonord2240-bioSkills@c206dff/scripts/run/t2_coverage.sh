#!/bin/bash
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
python t2_coverage.py work/test.paired_end.sorted.bam chr22 40001 > out/t2_coverage.txt 2>&1
cat out/t2_coverage.txt
