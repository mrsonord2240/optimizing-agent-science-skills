#!/bin/bash
# The Skill's LeafcutterMD block, verbatim except: python leafcutter_cluster_regtools.py -> wrapper on PATH (script lives in the leafcutter repo).
cd /mnt/openscience/audits/bio-outlier-splicing-detection/run/lmd
for bam in *.bam; do
    regtools junctions extract -a 8 -m 50 -s XS "$bam" -o "${bam%.bam}.junc"
done
ls *.junc > juncfiles.txt
wc -l juncfiles.txt; head -3 S05.junc
leafcutter_cluster_regtools.py -j juncfiles.txt -o leafcutter -m 50 -l 500000
ls leafcutter_* 
leafcutterMD.R \
    --num_threads 4 \
    --output_prefix patient_outlier \
    leafcutter_perind_numers.counts.gz
ls patient_outlier_*
