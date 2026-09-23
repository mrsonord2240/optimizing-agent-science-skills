#!/bin/bash
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work
python $R/n1_make_new_data.py
ls -la $R/data/new | awk '{print $5, $9}'
for f in own_ctg.bam own_ctg.cram own_del.bam own_insert.bam; do echo "== flagstat $f"; samtools flagstat $R/data/new/$f | head -3; done
