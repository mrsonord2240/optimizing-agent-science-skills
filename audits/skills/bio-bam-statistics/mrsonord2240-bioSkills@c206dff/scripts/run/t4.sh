#!/bin/bash
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
mkdir -p work
python t4_deep_cap.py > out/t4_deep_cap.txt 2>&1; cat out/t4_deep_cap.txt
