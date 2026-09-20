#!/bin/bash
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
python t2b_pysam_defaults.py > out/t2b_pysam_defaults.txt 2>&1; cat out/t2b_pysam_defaults.txt
