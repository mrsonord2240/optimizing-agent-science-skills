#!/bin/bash
# A1: scripts/run_abc.sh EXACTLY as shipped on chr22 K562 example; chr22 real-K562 avg-format Hi-C SUBSTITUTE (not the cross-cell-type average).
source /mnt/openscience/audits/bio-atac-seq-enhancer-gene-linking/initial-audit-20260930/scripts/common.sh
stage_inputs $RUN/outputs/a1_shipped; date -Is
bash $SKILL/scripts/run_abc.sh atac.bam h3k27ac.bam $EG/work/avg dummy.fa chr22.sizes $E/RefSeqCurated.170308.bed.CollapsedGeneBounds.chr22.hg38.bed $R K562 abc_out
echo "run_abc.sh rc=$?"
