#!/bin/bash
# Edge-case input: run PICRUSt2 on the synthetic DADA2 fixture ASVs (11 ASVs, not real 16S
# biology). Expect the tool's own quality gate (--min_align 0.8) to refuse them -- this is
# the auditor independently reproducing what TOOLS.md documented from the tooling pass.
set -uo pipefail  # no -e: we want to capture and report a non-zero exit, not abort the script

BASE=/mnt/openscience/audit-envs/microbiome-metagenomics-analyst
WORK=/mnt/openscience/audits/bio-microbiome-functional-prediction/work/synthetic-edge
mkdir -p "$WORK"
cd "$WORK"

cp "$BASE/datagen/amplicon/asv_seqs.fna" .
cp "$BASE/datagen/amplicon/asv_table.tsv" .

eval "$(micromamba shell hook --shell bash)"
micromamba activate picrust2

picrust2_pipeline.py \
    -s asv_seqs.fna \
    -i asv_table.tsv \
    -o picrust2_out \
    -p 4 \
    --hsp_method mp \
    --max_nsti 2 \
    --verbose > run.log 2>&1
echo "EXIT_CODE=$?" >> run.log
tail -40 run.log
