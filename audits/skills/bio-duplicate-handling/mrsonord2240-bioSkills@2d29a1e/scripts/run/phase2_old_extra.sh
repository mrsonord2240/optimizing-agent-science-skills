#!/usr/bin/env bash
# Remaining old Input 7 coverage: Picard UMI-aware marking and mapDamage rescaling.
set -euo pipefail

ROOT=/mnt/openscience
source "$ROOT/audit-envs/alignment-files/wsl_env.sh"
SKILL="$ROOT/wt/alignment-files-duplicate-handling/alignment-files/duplicate-handling"
RUN="$ROOT/audits/bio-duplicate-handling/run"
DATA="$ROOT/audit-envs/alignment-files/public-data"
WORK="$RUN/work/old_extra"
rm -rf "$WORK"
mkdir -p "$WORK"

echo 'OLD INPUT 7A — Picard UmiAwareMarkDuplicatesWithMateCigar'
samtools sort -n -o "$WORK/umi_name.bam" "$DATA/human/test.paired_end.umi_unsorted.bam"
samtools fixmate -m "$WORK/umi_name.bam" "$WORK/umi_fixmate.bam"
samtools sort -o "$WORK/umi_coord.bam" "$WORK/umi_fixmate.bam"
picard UmiAwareMarkDuplicatesWithMateCigar I="$WORK/umi_coord.bam" O="$WORK/umi_picard.bam" M="$WORK/umi.metrics.txt" UMI_METRICS="$WORK/umi.umi_metrics.txt" UMI_TAG_NAME=RX VALIDATION_STRINGENCY=SILENT >"$WORK/umi_picard.out" 2>"$WORK/umi_picard.err"
flagged=$(samtools view -c -f 1024 "$WORK/umi_picard.bam")
[ "$flagged" = 10127 ] || { echo "ASSERT_FAIL Picard UMI flags=$flagged expected=10127" >&2; exit 99; }
[ -s "$WORK/umi.metrics.txt" ] || { echo 'ASSERT_FAIL missing Picard metrics' >&2; exit 99; }
echo "Picard UMI flagged=$flagged"

echo 'OLD INPUT 7B — mapDamage --rescale after documented markdup workflow'
ASSAY=wgs bash "$SKILL/examples/markdup_pipeline.sh" "$DATA/human/test.paired_end.sorted.bam" "$WORK/human_marked.bam" 2 >"$WORK/markdup.out" 2>"$WORK/markdup.err"
mapDamage -i "$WORK/human_marked.bam" -r "$DATA/human/genome.fasta" --rescale -d "$WORK/mapdamage" >"$WORK/mapdamage.out" 2>"$WORK/mapdamage.err"
rescaled="$WORK/mapdamage/human_marked.rescaled.bam"
[ -s "$rescaled" ] || { echo "ASSERT_FAIL missing rescaled BAM: $rescaled" >&2; exit 99; }
in_count=$(samtools view -c "$WORK/human_marked.bam")
out_count=$(samtools view -c "$rescaled")
[ "$in_count" = "$out_count" ] || { echo "ASSERT_FAIL mapDamage records=$out_count expected=$in_count" >&2; exit 99; }
[ -s "$WORK/mapdamage/misincorporation.txt" ] || { echo 'ASSERT_FAIL missing mapDamage evidence table' >&2; exit 99; }
echo "mapDamage rescaled records=$out_count"
echo 'OLD_EXTRA_ASSERTIONS_PASSED'
