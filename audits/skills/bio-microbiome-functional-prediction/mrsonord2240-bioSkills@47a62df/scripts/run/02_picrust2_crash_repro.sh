#!/bin/bash
# Re-audit: independently reproduce the biom-TSV comment-line crash on a FRESH real export
# (run/01_export_biom_tsv.sh, this session, not reused from the original audit's work/ dir).
set -uo pipefail

WORK=/mnt/openscience/audits/bio-microbiome-functional-prediction/work
cd "$WORK"

eval "$(micromamba shell hook --shell bash)" 2>/dev/null
micromamba activate picrust2

time picrust2_pipeline.py \
    -s asv_seqs.fna \
    -i exported-table/feature-table.tsv \
    -o picrust2_out_crashtest \
    -p 4 \
    --hsp_method mp \
    --max_nsti 2 \
    --verbose > picrust2_crashtest.log 2>&1
echo "EXIT_CODE=$?" >> picrust2_crashtest.log
tail -40 picrust2_crashtest.log
ls -la picrust2_out_crashtest 2>&1 || echo "NO OUTPUT DIR (as expected if crash occurred before any dir was written -- check log)"
