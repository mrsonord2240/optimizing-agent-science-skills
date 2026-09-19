#!/bin/bash
# Canonical input: run PICRUSt2 on REAL ASVs denoised from the public moving-pictures 16S dataset
# (770 ASVs, 34 gut samples). This is real human-gut 16S data - PICRUSt2's best-case environment.
set -uo pipefail

WORK=/mnt/openscience/audits/bio-microbiome-functional-prediction/work
cd "$WORK"

eval "$(micromamba shell hook --shell bash)" 2>/dev/null
micromamba activate picrust2

time picrust2_pipeline.py \
    -s exported-rep-seqs/dna-sequences.fasta \
    -i exported-table/feature-table.tsv \
    -o picrust2_out_real \
    -p 4 \
    --hsp_method mp \
    --max_nsti 2 \
    --verbose > picrust2_real_run.log 2>&1
echo "EXIT_CODE=$?" >> picrust2_real_run.log
tail -60 picrust2_real_run.log

# add_descriptions on the MetaCyc pathway table (per SKILL.md's documented step)
add_descriptions.py \
    -i picrust2_out_real/pathways_out/path_abun_unstrat.tsv.gz \
    -m METACYC \
    -o picrust2_out_real/pathways_out/path_abun_described.tsv.gz
echo "add_descriptions EXIT_CODE=$?"

ls -la picrust2_out_real/
