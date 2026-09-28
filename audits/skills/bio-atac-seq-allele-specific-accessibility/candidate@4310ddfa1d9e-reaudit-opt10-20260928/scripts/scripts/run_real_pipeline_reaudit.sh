#!/usr/bin/env bash
set -euo pipefail
source /mnt/openscience/audit-envs/bio-atac-seq-allele-specific-accessibility/wsl_env.sh

AUDIT=/mnt/openscience/audits/bio-atac-seq-allele-specific-accessibility/reaudit-opt10-20260928
RUN="$AUDIT/runs/real-pipeline"
INPUT="$RUN/input with spaces"
OUT="$RUN/output with spaces"
FAILED_OUT="$RUN/ps-free-failed-output"
LOG="$AUDIT/evidence/real-pipeline.txt"
PIPELINE="$ASA_CANDIDATE/scripts/wasp_ase_pipeline.sh"
SOURCE="$ASA_ROOT/runs/wasp-real"
REF="$PUBLIC_DATA/reference/hg38.chr1.fa"
BT2="$PUBLIC_DATA/reference/bt2/hg38_chr1"
PUBLIC_VCF="$PUBLIC_DATA/variants/NA12878.chr1_1-30M.phased.vcf.gz"
rm -rf -- "$RUN"
mkdir -p "$INPUT/bin" "$AUDIT/evidence"

samtools addreplacerg -r ID:reaudit_NA12878 -r SM:NA12878 -r PL:ILLUMINA \
  -m orphan_only -o "$INPUT/NA12878.bam" "$SOURCE/NA12878.bam"
samtools index "$INPUT/NA12878.bam"

# The public VCF is chromosome-wide phased but lacks PS. This bounded test-only
# derivative adds a single declared PS=1 across chr1:1-5 Mb; the PS-free source
# is separately tested and must fail. This does not generalize PS inference.
bcftools view -r chr1:1-5000000 -m2 -M2 -v snps --samples NA12878 \
  -i 'GT="het"' -Ov "$PUBLIC_VCF" | \
awk 'BEGIN {OFS="\t"}
  /^##/ {print; next}
  /^#CHROM/ {print "##FORMAT=<ID=PS,Number=1,Type=Integer,Description=\"Bounded re-audit derivative; constant PS=1\">"; print; next}
  {$9=$9 ":PS"; for (i=10; i<=NF; i++) $i=$i ":1"; print}
' | bgzip -c > "$INPUT/NA12878.bounded.ps1.vcf.gz"
tabix -f -p vcf "$INPUT/NA12878.bounded.ps1.vcf.gz"
printf 'chr1\t0\t5000000\tchr1_1_5Mb\n' > "$INPUT/peaks.bed"

cat > "$INPUT/bin/python" <<'EOF'
#!/bin/bash
exec /home/sci/micromamba/envs/atac-wasp/bin/python "$@"
EOF
cat > "$INPUT/bin/python3" <<'EOF'
#!/bin/bash
exec /home/sci/micromamba/envs/atac-core/bin/python "$@"
EOF
chmod +x "$INPUT/bin/python" "$INPUT/bin/python3"
export PATH="$INPUT/bin:$PATH"
export ASE_THREADS=2

set +e
bash "$PIPELINE" "$INPUT/NA12878.bam" "$PUBLIC_VCF" "$REF" "$BT2" \
  "$INPUT/peaks.bed" "$WASP_SRC" "$FAILED_OUT" \
  > "$RUN/ps-free.stdout" 2> "$RUN/ps-free.stderr"
ps_free_rc=$?
set -e
test "$ps_free_rc" -ne 0
grep -Eq 'missing phase-set PS|FORMAT/PS' "$RUN/ps-free.stderr"
test ! -e "$FAILED_OUT"
if compgen -G "$FAILED_OUT.tmp.*" >/dev/null; then exit 1; fi

bash "$PIPELINE" "$INPUT/NA12878.bam" "$INPUT/NA12878.bounded.ps1.vcf.gz" \
  "$REF" "$BT2" "$INPUT/peaks.bed" "$WASP_SRC" "$OUT" \
  > "$RUN/pipeline.stdout" 2> "$RUN/pipeline.stderr"

FINAL_BAM="$OUT/wasp/NA12878.wasp.bam"
FILTERED="$OUT/wasp/NA12878.phased_het.vcf.gz"
ASE="$OUT/ase/NA12878.ase_counts.tsv"
HAP="$OUT/ase/NA12878.haplotype_map.tsv"
PEAK="$OUT/peak_aggregation/NA12878.peak_ase.tsv"
samtools quickcheck "$FINAL_BAM"
samtools idxstats "$FINAL_BAM" >/dev/null

set +e
bash "$PIPELINE" "$INPUT/NA12878.bam" "$INPUT/NA12878.bounded.ps1.vcf.gz" \
  "$REF" "$BT2" "$INPUT/peaks.bed" "$WASP_SRC" "$OUT" \
  > "$RUN/reuse.stdout" 2> "$RUN/reuse.stderr"
reuse_rc=$?
set -e
test "$reuse_rc" -eq 73
grep -q 'output directory already exists' "$RUN/reuse.stderr"

{
  echo "run_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo 'candidate_sha256=4310ddfa1d9ed178f033ad42e77e0772ddadd3c4905dd1e9bcef8b6289a24103'
  echo 'bounded_region=chr1:1-5000000'
  echo 'phase_derivative=constant PS=1 only for bounded chromosome-wide-phased public VCF test'
  echo "ps_free_source_rejected_rc=$ps_free_rc"
  echo 'ps_free_staged_cleanup=PASS'
  echo "wasp_commit=$(git -C "$WASP_SRC" rev-parse HEAD)"
  echo "filtered_samples=$(bcftools query -l "$FILTERED" | paste -sd, -)"
  echo "filtered_variants=$(bcftools index -n "$FILTERED")"
  echo "haplotype_map_rows=$(awk 'NR>1 {n++} END {print n+0}' "$HAP")"
  echo "final_sort_order=$(samtools view -H "$FINAL_BAM" | awk -F '\t' '$1=="@HD" {for(i=2;i<=NF;i++) if($i ~ /^SO:/) {sub(/^SO:/,"",$i); print $i}}')"
  echo "final_rg_samples=$(samtools view -H "$FINAL_BAM" | awk -F '\t' '$1=="@RG" {for(i=2;i<=NF;i++) if($i ~ /^SM:/) {sub(/^SM:/,"",$i); print $i}}' | sort -u | paste -sd, -)"
  echo "final_reads=$(samtools view -c "$FINAL_BAM")"
  echo 'final_index_readable=PASS'
  echo "gatk_rows=$(awk 'NR>1 && NF {n++} END {print n+0}' "$ASE")"
  echo "gatk_depth30_rows=$(awk -F '\t' 'NR>1 && $8>=30 {n++} END {print n+0}' "$ASE")"
  echo "peak_rows=$(awk 'NR>1 && NF {n++} END {print n+0}' "$PEAK")"
  echo "peak_header=$(head -1 "$PEAK")"
  echo 'path_with_spaces=PASS'
  echo 'output_reuse_refusal=PASS'
  echo 'real_pipeline_reaudit=PASS'
} > "$LOG"
cat "$LOG"
