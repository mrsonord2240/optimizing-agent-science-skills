#!/usr/bin/env bash
set -euo pipefail
source /mnt/openscience/audit-envs/bio-atac-seq-allele-specific-accessibility/wsl_env.sh

AUDIT=/mnt/openscience/audits/bio-atac-seq-allele-specific-accessibility/reaudit-opt10-20260928
RUN="$AUDIT/runs/fixtures"
LOG="$AUDIT/evidence/fixtures.txt"
PY=/home/sci/micromamba/envs/atac-core/bin/python
HELPER="$ASA_CANDIDATE/scripts/aggregate_peak_ase.py"
DRIVER="$ASA_CANDIDATE/scripts/run_rasqual_features.py"
PIPELINE="$ASA_CANDIDATE/scripts/wasp_ase_pipeline.sh"
rm -rf -- "$RUN"
mkdir -p "$RUN/path with spaces" "$RUN/wasp-stub/mapping" "$AUDIT/evidence"

{
  echo "run_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "candidate_sha256=4310ddfa1d9ed178f033ad42e77e0772ddadd3c4905dd1e9bcef8b6289a24103"
  bash -n "$PIPELINE"
  echo 'pipeline_bash_syntax=PASS'
  "$PY" -W error::ResourceWarning -m unittest discover -s "$ASA_CANDIDATE/tests" -v
} > "$LOG" 2>&1

cat > "$RUN/counts.tsv" <<'EOF'
contig	position	variantID	refAllele	altAllele	refCount	altCount	totalCount	lowMAPQDepth	lowBaseQDepth	rawDepth	otherBases	improperPairs
chrAudit	101	a	A	G	90	10	100	0	0	100	0	0
chrAudit	201	b	C	T	10	90	100	0	0	100	0	0
chrAudit	301	c	G	A	18	12	30	0	0	30	0	0
chrAudit	401	d	T	C	17	13	30	0	0	30	0	0
EOF
cat > "$RUN/haplotypes.tsv" <<'EOF'
contig	position	refAllele	altAllele	phaseSet	haplotype1Allele
chrAudit	101	A	G	chrAudit:10	REF
chrAudit	201	C	T	chrAudit:10	ALT
chrAudit	301	G	A	chrAudit:20	REF
chrAudit	401	T	C	chrAudit:20	REF
EOF
printf 'chrAudit\t99\t250\tpeak oriented\nchrAudit\t299\t450\tpeak neutral\n' > "$RUN/path with spaces/peaks.bed"
"$PY" "$HELPER" --ase-counts "$RUN/counts.tsv" \
  --peaks "$RUN/path with spaces/peaks.bed" --haplotype-map "$RUN/haplotypes.tsv" \
  --output "$RUN/path with spaces/oriented.tsv" >> "$LOG" 2>&1
"$PY" - "$RUN/path with spaces/oriented.tsv" >> "$LOG" <<'PY'
import csv, math, sys
with open(sys.argv[1], encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
assert len(rows) == 2, rows
by_peak = {row["peak"]: row for row in rows}
assert by_peak["peak oriented"]["phase_set"] == "chrAudit:10"
assert by_peak["peak oriented"]["haplotype1_count"] == "180"
assert by_peak["peak oriented"]["haplotype2_count"] == "20"
assert by_peak["peak oriented"]["status"] == "significant_imbalance"
assert by_peak["peak neutral"]["phase_set"] == "chrAudit:20"
assert by_peak["peak neutral"]["snp_count"] == "2"
assert by_peak["peak neutral"]["status"] == "non_significant"
assert all(math.isfinite(float(row["p_value"])) for row in rows)
print("aggregate_orientation_phase_status=PASS")
print("aggregate_path_with_spaces=PASS")
PY

head -1 "$RUN/counts.tsv" > "$RUN/empty.tsv"
"$PY" "$HELPER" --ase-counts "$RUN/empty.tsv" \
  --peaks "$RUN/path with spaces/peaks.bed" --haplotype-map "$RUN/haplotypes.tsv" \
  --output "$RUN/empty-output.tsv" >> "$LOG" 2>&1
"$PY" - "$RUN/empty-output.tsv" >> "$LOG" <<'PY'
import csv, sys
expected = ["peak", "phase_set", "haplotype1_count", "haplotype2_count", "total_count", "haplotype1_frac", "snp_count", "p_value", "adj_p", "status"]
with open(sys.argv[1], encoding="utf-8") as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    assert reader.fieldnames == expected
    assert list(reader) == []
print("aggregate_empty_schema=PASS")
PY

printf 'chrAudit\t900\t950\n' > "$RUN/no-overlap.bed"
"$PY" "$HELPER" --ase-counts "$RUN/counts.tsv" --peaks "$RUN/no-overlap.bed" \
  --haplotype-map "$RUN/haplotypes.tsv" --output "$RUN/no-overlap.tsv" >> "$LOG" 2>&1
test "$(wc -l < "$RUN/no-overlap.tsv")" -eq 1
echo 'aggregate_no_overlap_schema=PASS' >> "$LOG"

printf 'contig\tposition\trefCount\nchrAudit\t101\t90\n' > "$RUN/bad-counts.tsv"
set +e
"$PY" "$HELPER" --ase-counts "$RUN/bad-counts.tsv" \
  --peaks "$RUN/path with spaces/peaks.bed" --haplotype-map "$RUN/haplotypes.tsv" \
  --output "$RUN/bad-output.tsv" > "$RUN/bad.stdout" 2> "$RUN/bad.stderr"
bad_rc=$?
set -e
test "$bad_rc" -eq 2
grep -q 'ASE table is missing required columns' "$RUN/bad.stderr"
test ! -e "$RUN/bad-output.tsv"
echo 'aggregate_schema_error=PASS' >> "$LOG"

# Fresh adversarial case: distinct genomic peaks are permitted to share a BED4
# label. A safe helper must keep their coordinate identities separate or reject
# duplicate labels rather than pooling them by the display label alone.
printf 'chrAudit\t99\t150\tdup\nchrAudit\t199\t250\tdup\n' > "$RUN/duplicate-names.bed"
"$PY" "$HELPER" --ase-counts "$RUN/counts.tsv" --peaks "$RUN/duplicate-names.bed" \
  --haplotype-map "$RUN/haplotypes.tsv" --output "$RUN/duplicate-names.tsv" >> "$LOG" 2>&1
"$PY" - "$RUN/duplicate-names.tsv" >> "$LOG" <<'PY'
import csv, sys
with open(sys.argv[1], encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
if len(rows) == 2 and all(row["snp_count"] == "1" for row in rows):
    print("aggregate_duplicate_peak_identity=PASS")
elif len(rows) == 1 and rows[0]["snp_count"] == "2":
    print("aggregate_duplicate_peak_identity=FAIL distinct coordinates pooled under duplicate BED4 name")
else:
    print(f"aggregate_duplicate_peak_identity=FAIL unexpected_rows={rows!r}")
PY

cp "$RASQUAL_SRC/data/Y.bin" "$RUN/path with spaces/Y.bin"
cp "$RASQUAL_SRC/data/K.bin" "$RUN/path with spaces/K.bin"
cp "$RASQUAL_SRC/data/chr11.gz" "$RUN/path with spaces/chr11.gz"
"$PY" "$DRIVER" --features "$AUDIT/inputs/rasqual-two-features.tsv" \
  --counts "$RUN/path with spaces/Y.bin" --offsets "$RUN/path with spaces/K.bin" \
  --vcf "$RUN/path with spaces/chr11.gz" --samples 24 --matrix-rows 2 \
  --output-dir "$RUN/path with spaces/rasqual" --dry-run > "$RUN/rasqual-plan.json"
"$PY" - "$RUN/rasqual-plan.json" >> "$LOG" <<'PY'
import json, sys
plan = json.load(open(sys.argv[1], encoding="utf-8"))
assert [item["index"] for item in plan["features"]] == [1, 2]
assert [item["rasqual"][item["rasqual"].index("-j") + 1] for item in plan["features"]] == ["1", "2"]
assert "path with spaces" in plan["features"][0]["rasqual"][2]
assert "BH" in plan["multiplicity"]
print("rasqual_two_feature_row_mapping=PASS")
print("rasqual_path_argument_safety=PASS")
print("rasqual_bh_contract=PASS")
PY

"$PY" "$DRIVER" --features "$AUDIT/inputs/rasqual-zero-feature.tsv" \
  --counts "$RASQUAL_SRC/data/Y.bin" --offsets "$RASQUAL_SRC/data/K.bin" \
  --vcf "$RASQUAL_SRC/data/chr11.gz" --samples 24 --matrix-rows 2 \
  --output-dir "$RUN/zero-plan" --dry-run > "$RUN/zero-plan.json"
"$PY" - "$RUN/zero-plan.json" >> "$LOG" <<'PY'
import json, sys
plan = json.load(open(sys.argv[1], encoding="utf-8"))
assert plan["skipped_zero_feature_snps"] == ["zero_feature"]
assert [item["index"] for item in plan["features"]] == [1]
print("rasqual_zero_feature_skip_plan=PASS")
PY

head -c 8 "$RASQUAL_SRC/data/Y.bin" > "$RUN/short.bin"
set +e
"$PY" "$DRIVER" --features "$AUDIT/inputs/rasqual-two-features.tsv" \
  --counts "$RUN/short.bin" --offsets "$RASQUAL_SRC/data/K.bin" \
  --vcf "$RASQUAL_SRC/data/chr11.gz" --samples 24 --matrix-rows 2 \
  --output-dir "$RUN/never" --dry-run > "$RUN/dim.stdout" 2> "$RUN/dim.stderr"
dim_rc=$?
set -e
test "$dim_rc" -eq 2
grep -q 'expected exactly 24 samples x 2 rows x 8 bytes = 384' "$RUN/dim.stderr"
echo 'rasqual_matrix_dimension_validation=PASS' >> "$LOG"

# Build a valid tiny BAM and a two-sample VCF in which the BAM target is
# homozygous while another sample is heterozygous. The pipeline must stop after
# target-only filtering, before WASP, and clean its stage.
cat > "$RUN/tiny.sam" <<'EOF'
@HD	VN:1.6	SO:coordinate
@SQ	SN:chrAudit	LN:1000
@RG	ID:rg1	SM:NA12878	PL:ILLUMINA
r1	0	chrAudit	100	60	10M	*	0	0	AAAAAAAAAA	IIIIIIIIII	RG:Z:rg1
EOF
samtools view -bS -o "$RUN/tiny.bam" "$RUN/tiny.sam"
samtools index "$RUN/tiny.bam"
printf '>chrAudit\n' > "$RUN/ref.fa"
printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n' >> "$RUN/ref.fa"
samtools faidx "$RUN/ref.fa"
printf 'chrAudit\t0\t500\tpeak\n' > "$RUN/peaks.bed"
cat > "$RUN/multisample.vcf" <<'EOF'
##fileformat=VCFv4.2
##contig=<ID=chrAudit,length=1000>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=PS,Number=1,Type=Integer,Description="Phase set">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	NA12878	donor2
chrAudit	101	rsTargetHom	A	G	.	PASS	.	GT:PS	0|0:10	0|1:10
EOF
bgzip -c "$RUN/multisample.vcf" > "$RUN/multisample.vcf.gz"
tabix -f -p vcf "$RUN/multisample.vcf.gz"
touch "$RUN/wasp-stub/mapping/find_intersecting_snps.py" "$RUN/wasp-stub/mapping/filter_remapped_reads.py"
set +e
bash "$PIPELINE" "$RUN/tiny.bam" "$RUN/multisample.vcf.gz" "$RUN/ref.fa" \
  "$RUN/index" "$RUN/peaks.bed" "$RUN/wasp-stub" "$RUN/target-filter-out" \
  > "$RUN/target-filter.stdout" 2> "$RUN/target-filter.stderr"
target_rc=$?
set -e
test "$target_rc" -eq 65
grep -q 'target sample has no biallelic heterozygous SNPs' "$RUN/target-filter.stderr"
test ! -e "$RUN/target-filter-out"
if compgen -G "$RUN/target-filter-out.tmp.*" >/dev/null; then exit 1; fi
echo 'pipeline_target_only_genotype_filter=PASS' >> "$LOG"
echo 'pipeline_early_failure_cleanup=PASS' >> "$LOG"

cat > "$RUN/mismatch.vcf" <<'EOF'
##fileformat=VCFv4.2
##contig=<ID=chrAudit,length=1000>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	donor2
chrAudit	101	rsMismatch	A	G	.	PASS	.	GT	0|1
EOF
bgzip -c "$RUN/mismatch.vcf" > "$RUN/mismatch.vcf.gz"
tabix -f -p vcf "$RUN/mismatch.vcf.gz"
set +e
bash "$PIPELINE" "$RUN/tiny.bam" "$RUN/mismatch.vcf.gz" "$RUN/ref.fa" \
  "$RUN/index" "$RUN/peaks.bed" "$RUN/wasp-stub" "$RUN/mismatch-out" \
  > "$RUN/mismatch.stdout" 2> "$RUN/mismatch.stderr"
mismatch_rc=$?
set -e
test "$mismatch_rc" -eq 65
grep -q 'must match exactly one VCF sample' "$RUN/mismatch.stderr"
echo 'pipeline_sample_identity_mismatch=PASS' >> "$LOG"

mkdir -p "$RUN/existing-output"
set +e
bash "$PIPELINE" "$RUN/tiny.bam" "$RUN/multisample.vcf.gz" "$RUN/ref.fa" \
  "$RUN/index" "$RUN/peaks.bed" "$RUN/wasp-stub" "$RUN/existing-output" \
  > "$RUN/reuse.stdout" 2> "$RUN/reuse.stderr"
reuse_rc=$?
set -e
test "$reuse_rc" -eq 73
grep -q 'output directory already exists' "$RUN/reuse.stderr"
echo 'pipeline_output_reuse_refusal=PASS' >> "$LOG"
echo 'fixture_reaudit_complete=PASS' >> "$LOG"
cat "$LOG"
