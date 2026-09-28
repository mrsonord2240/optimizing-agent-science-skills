#!/bin/bash
set -u

source /mnt/openscience/audit-envs/bio-atac-seq-allele-specific-accessibility/wsl_env.sh

AUDIT=/mnt/openscience/audits/bio-atac-seq-allele-specific-accessibility/initial-opt10-20260928
SOURCE="$ASA_ROOT/runs/wasp-real"
RUN="$AUDIT/runs/candidate-merge"
EVIDENCE="$AUDIT/evidence/candidate-merge.txt"
REF="$PUBLIC_DATA/reference/hg38.chr1.fa"
VCF="$SOURCE/NA12878.het.vcf.gz"

rm -rf "$RUN"
mkdir -p "$RUN" "$(dirname "$EVIDENCE")"
: > "$EVIDENCE"

set +e
samtools merge -f "$RUN/candidate.wasp.bam" \
  "$SOURCE/kept.bam" "$SOURCE/map/NA12878.keep.bam" \
  > "$RUN/merge.stdout" 2> "$RUN/merge.stderr"
merge_rc=$?

samtools index "$RUN/candidate.wasp.bam" \
  > "$RUN/index.stdout" 2> "$RUN/index.stderr"
index_rc=$?

samtools view -H "$RUN/candidate.wasp.bam" > "$RUN/candidate.header.sam"
header_rc=$?
set -e

rg_count=$(grep -c '^@RG' "$RUN/candidate.header.sam" || true)
sort_order=$(awk -F '\t' '$1=="@HD" {for(i=1;i<=NF;i++) if($i ~ /^SO:/) print substr($i,4)}' "$RUN/candidate.header.sam")
read_count=$(samtools view -c "$RUN/candidate.wasp.bam")

printf 'candidate_exact_merge_rc=%s\n' "$merge_rc" >> "$EVIDENCE"
printf 'candidate_exact_index_rc=%s\n' "$index_rc" >> "$EVIDENCE"
printf 'candidate_header_rc=%s\n' "$header_rc" >> "$EVIDENCE"
printf 'candidate_header_sort_order=%s\n' "${sort_order:-missing}" >> "$EVIDENCE"
printf 'candidate_header_read_groups=%s\n' "$rg_count" >> "$EVIDENCE"
printf 'candidate_merged_reads=%s\n' "$read_count" >> "$EVIDENCE"
printf 'candidate_index_stderr=%s\n' "$(tr '\n' ' ' < "$RUN/index.stderr")" >> "$EVIDENCE"

# The candidate cannot reach GATK when its own index step fails. Sort only to
# isolate the independent read-group boundary; this is not credited as a
# candidate execution success.
samtools sort -o "$RUN/control.sorted.no-rg.bam" "$RUN/candidate.wasp.bam"
samtools index "$RUN/control.sorted.no-rg.bam"
set +e
gatk ASEReadCounter \
  -I "$RUN/control.sorted.no-rg.bam" -V "$VCF" -R "$REF" \
  -O "$RUN/no-rg.ase.tsv" --output-format TABLE \
  --min-mapping-quality 30 --min-base-quality 20 \
  > "$RUN/no-rg.gatk.stdout" 2> "$RUN/no-rg.gatk.stderr"
no_rg_gatk_rc=$?
set -e
no_rg_rows=0
if test -f "$RUN/no-rg.ase.tsv"; then
  no_rg_rows=$(awk 'NR>1 {n++} END {print n+0}' "$RUN/no-rg.ase.tsv")
fi
printf 'sorted_without_read_group_gatk_rc=%s\n' "$no_rg_gatk_rc" >> "$EVIDENCE"
printf 'sorted_without_read_group_rows=%s\n' "$no_rg_rows" >> "$EVIDENCE"
printf 'sorted_without_read_group_stderr_tail=%s\n' "$(tail -3 "$RUN/no-rg.gatk.stderr" | tr '\n' ' ')" >> "$EVIDENCE"

# Positive control: the same real reads become countable after adding the
# missing read group. This confirms the failure is candidate orchestration,
# not the public input or the prepared tools.
samtools addreplacerg -r ID:atac -r SM:NA12878 -r PL:ILLUMINA \
  -o "$RUN/control.sorted.rg.bam" "$RUN/control.sorted.no-rg.bam"
samtools index "$RUN/control.sorted.rg.bam"
gatk ASEReadCounter \
  -I "$RUN/control.sorted.rg.bam" -V "$VCF" -R "$REF" \
  -O "$RUN/control.ase.tsv" --output-format TABLE \
  --min-mapping-quality 30 --min-base-quality 20 \
  > "$RUN/control.gatk.stdout" 2> "$RUN/control.gatk.stderr"
control_rows=$(awk 'NR>1 {n++} END {print n+0}' "$RUN/control.ase.tsv")
control_depth30=$(awk -F '\t' 'NR>1 && $8>=30 {n++} END {print n+0}' "$RUN/control.ase.tsv")
printf 'sorted_with_read_group_gatk_rc=0\n' >> "$EVIDENCE"
printf 'sorted_with_read_group_rows=%s\n' "$control_rows" >> "$EVIDENCE"
printf 'sorted_with_read_group_depth30_rows=%s\n' "$control_depth30" >> "$EVIDENCE"

cat "$EVIDENCE"
