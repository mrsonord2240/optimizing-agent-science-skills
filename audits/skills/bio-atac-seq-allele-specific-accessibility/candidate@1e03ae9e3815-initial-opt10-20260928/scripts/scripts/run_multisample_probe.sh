#!/bin/bash
set -euo pipefail

source /mnt/openscience/audit-envs/bio-atac-seq-allele-specific-accessibility/wsl_env.sh

AUDIT=/mnt/openscience/audits/bio-atac-seq-allele-specific-accessibility/initial-opt10-20260928
RUN="$AUDIT/runs/multisample"
EVIDENCE="$AUDIT/evidence/multisample.txt"
INPUT="$AUDIT/inputs/multisample-target-hom.vcf"
REF="$PUBLIC_DATA/reference/hg38.chr1.fa"
BAM="$AUDIT/runs/candidate-merge/control.sorted.rg.bam"

rm -rf "$RUN"
mkdir -p "$RUN" "$(dirname "$EVIDENCE")"

# Candidate expression: the record survives because any retained sample is
# heterozygous, while all sample columns remain present.
bcftools view -m2 -M2 -v snps -i 'GT="het"' "$INPUT" -Ov -o "$RUN/candidate-filtered.vcf"
candidate_records=$(bcftools view -H "$RUN/candidate-filtered.vcf" | wc -l)
candidate_samples=$(bcftools query -l "$RUN/candidate-filtered.vcf" | paste -sd, -)
candidate_gts=$(bcftools query -f '[%SAMPLE=%GT,]\n' "$RUN/candidate-filtered.vcf")

# Sample-scoped control: after retaining only NA12878, the homozygous target
# record is correctly excluded.
bcftools view -s NA12878 -Ou "$INPUT" | \
  bcftools view -i 'GT="het"' -Ov -o "$RUN/target-filtered.vcf"
target_records=$(bcftools view -H "$RUN/target-filtered.vcf" | wc -l)

bgzip -c "$RUN/candidate-filtered.vcf" > "$RUN/candidate-filtered.vcf.gz"
tabix -f -p vcf "$RUN/candidate-filtered.vcf.gz"
gatk ASEReadCounter \
  -I "$BAM" -V "$RUN/candidate-filtered.vcf.gz" -R "$REF" \
  -O "$RUN/candidate-filtered.ase.tsv" --output-format TABLE \
  --min-mapping-quality 30 --min-base-quality 20 \
  > "$RUN/gatk.stdout" 2> "$RUN/gatk.stderr"
gatk_rows=$(awk 'NR>1 {n++} END {print n+0}' "$RUN/candidate-filtered.ase.tsv")
gatk_first=$(awk -F '\t' 'NR==2 {print "variant=" $3 ";ref=" $6 ";alt=" $7 ";total=" $8}' "$RUN/candidate-filtered.ase.tsv")

{
  echo "candidate_filter_records=$candidate_records"
  echo "candidate_filter_samples=$candidate_samples"
  echo "candidate_filter_genotypes=$candidate_gts"
  echo "target_scoped_control_records=$target_records"
  echo "gatk_rows_from_candidate_filter=$gatk_rows"
  echo "gatk_first_row=$gatk_first"
} > "$EVIDENCE"

cat "$EVIDENCE"
