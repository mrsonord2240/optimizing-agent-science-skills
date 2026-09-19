#!/bin/bash
# Re-audit regression: independently re-run the original audit's Input 3 (out-of-reference
# synthetic ASVs, expected hard --min_align placement-abort) to confirm the corrected
# Common Errors table's split framing (hard abort vs post-hoc NSTI drop) still matches.
set -uo pipefail

WORK=/mnt/openscience/audits/bio-microbiome-functional-prediction/work/synthetic-edge
cd "$WORK"

eval "$(micromamba shell hook --shell bash)" 2>/dev/null
micromamba activate picrust2

picrust2_pipeline.py \
    -s asv_seqs.fna \
    -i asv_table.tsv \
    -o picrust2_out_reaudit \
    -p 4 \
    --hsp_method mp \
    --max_nsti 2 \
    --verbose > run_reaudit.log 2>&1
echo "EXIT_CODE=$?" >> run_reaudit.log
cat run_reaudit.log
ls picrust2_out_reaudit 2>&1 || echo "NO OUTPUT DIR (expected: hard placement abort before any output)"
