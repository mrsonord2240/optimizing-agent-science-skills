#!/usr/bin/env bash
set -euo pipefail
source /mnt/openscience/audit-envs/bio-atac-seq-allele-specific-accessibility/wsl_env.sh

AUDIT=/mnt/openscience/audits/bio-atac-seq-allele-specific-accessibility/reaudit2-opt10-20260928
RUN="$AUDIT/runs/fixtures"
LOG="$AUDIT/evidence/fixtures.txt"
PY=/home/sci/micromamba/envs/atac-core/bin/python
HELPER="$ASA_CANDIDATE/scripts/aggregate_peak_ase.py"
DRIVER="$ASA_CANDIDATE/scripts/run_rasqual_features.py"
PIPELINE="$ASA_CANDIDATE/scripts/wasp_ase_pipeline.sh"
CANDIDATE_SHA=275ff0a1b8d9bed7a80e8316f97fe421296cb081c837ed01aaa53a0f96e48ae2
rm -rf -- "$RUN"
mkdir -p "$RUN/path with spaces" "$RUN/wasp-stub/mapping" "$AUDIT/evidence"

{
  echo "run_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "candidate_sha256=$CANDIDATE_SHA"
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

# Canonical orientation and phase-set separation.
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

# Exact ASA-009 replay: same display label, disjoint coordinates.
printf 'chrAudit\t99\t150\tdup\nchrAudit\t199\t250\tdup\n' > "$RUN/duplicate-labels.bed"
"$PY" "$HELPER" --ase-counts "$RUN/counts.tsv" --peaks "$RUN/duplicate-labels.bed" \
  --haplotype-map "$RUN/haplotypes.tsv" --output "$RUN/duplicate-labels.tsv" >> "$LOG" 2>&1
"$PY" - "$ASA_CANDIDATE" "$RUN" >> "$LOG" <<'PY'
import csv, importlib.util, pathlib, sys
candidate = pathlib.Path(sys.argv[1]); run = pathlib.Path(sys.argv[2])
with (run / "duplicate-labels.tsv").open(encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
assert len(rows) == 2, rows
assert [row["peak"] for row in rows] == ["dup", "dup"]
assert [row["snp_count"] for row in rows] == ["1", "1"]
assert {row["status"] for row in rows} == {"underpowered_snp_count"}
assert not any(row["status"] == "significant_imbalance" for row in rows)

script = candidate / "scripts" / "aggregate_peak_ase.py"
spec = importlib.util.spec_from_file_location("aggregate_peak_ase_reaudit2", script)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
ase = module.read_ase(str(run / "counts.tsv")); phase = module.read_haplotype_map(str(run / "haplotypes.tsv"))
keys = ["contig", "position", "refAllele", "altAllele"]
ase = ase.loc[ase["totalCount"] >= 30].copy().merge(phase[keys + ["phaseSet", "haplotype1Allele"]], on=keys, how="left", validate="one_to_one")
ase["haplotype1Count"] = ase["refCount"].where(ase["haplotype1Allele"] == "REF", ase["altCount"])
ase["haplotype2Count"] = ase["altCount"].where(ase["haplotype1Allele"] == "REF", ase["refCount"])
mapped = module.map_variants_to_peaks(ase, module.read_peaks(str(run / "duplicate-labels.bed")))
observed = [(r.peak_chrom, int(r.peak_start), int(r.peak_end), r.peak, r.phaseSet) for r in mapped.itertuples()]
assert observed == [("chrAudit", 99, 150, "dup", "chrAudit:10"), ("chrAudit", 199, 250, "dup", "chrAudit:10")], observed
(run / "bed3.bed").write_text("chrAudit\t99\t150\nchrAudit\t199\t250\n", encoding="utf-8")
bed3 = module.evaluate_groups(module.map_variants_to_peaks(ase, module.read_peaks(str(run / "bed3.bed"))))
bed4 = module.evaluate_groups(mapped)
non_display = [c for c in module.OUTPUT_COLUMNS if c != "peak"]
assert bed3[non_display].equals(bed4[non_display])
assert list(bed3["peak"]) == ["chrAudit_99_150", "chrAudit_199_250"]
print("asa009_disjoint_duplicate_label_rows=2")
print("asa009_snp_counts=1,1")
print("asa009_statuses=underpowered_snp_count,underpowered_snp_count")
print("asa009_significant_calls=0")
print("intersection_coordinates=chrAudit:99-150,chrAudit:199-250")
print("coordinate_plus_phase_grouping=PASS")
print("bed3_bed4_non_display_equivalence=PASS")
PY

# Exact duplicate coordinates must fail closed even when labels differ.
printf 'chrAudit\t99\t150\tfirst\nchrAudit\t99\t150\tsecond\n' > "$RUN/duplicate-coordinates.bed"
set +e
"$PY" "$HELPER" --ase-counts "$RUN/counts.tsv" --peaks "$RUN/duplicate-coordinates.bed" \
  --haplotype-map "$RUN/haplotypes.tsv" --output "$RUN/duplicate-coordinates.tsv" \
  > "$RUN/duplicate-coordinates.stdout" 2> "$RUN/duplicate-coordinates.stderr"
duplicate_rc=$?
set -e
test "$duplicate_rc" -eq 2
grep -q 'peaks contain duplicate genomic intervals' "$RUN/duplicate-coordinates.stderr"
test ! -e "$RUN/duplicate-coordinates.tsv"
echo 'duplicate_coordinate_fail_closed=PASS' >> "$LOG"

# Stable empty/no-overlap/error surfaces.
head -1 "$RUN/counts.tsv" > "$RUN/empty.tsv"
"$PY" "$HELPER" --ase-counts "$RUN/empty.tsv" --peaks "$RUN/bed3.bed" \
  --haplotype-map "$RUN/haplotypes.tsv" --output "$RUN/empty-output.tsv" >> "$LOG" 2>&1
printf 'chrAudit\t900\t950\n' > "$RUN/no-overlap.bed"
"$PY" "$HELPER" --ase-counts "$RUN/counts.tsv" --peaks "$RUN/no-overlap.bed" \
  --haplotype-map "$RUN/haplotypes.tsv" --output "$RUN/no-overlap.tsv" >> "$LOG" 2>&1
test "$(wc -l < "$RUN/empty-output.tsv")" -eq 1
test "$(wc -l < "$RUN/no-overlap.tsv")" -eq 1
printf 'contig\tposition\trefCount\nchrAudit\t101\t90\n' > "$RUN/bad-counts.tsv"
set +e
"$PY" "$HELPER" --ase-counts "$RUN/bad-counts.tsv" --peaks "$RUN/bed3.bed" \
  --haplotype-map "$RUN/haplotypes.tsv" --output "$RUN/bad-output.tsv" > "$RUN/bad.stdout" 2> "$RUN/bad.stderr"
bad_rc=$?
set -e
test "$bad_rc" -eq 2
grep -q 'ASE table is missing required columns' "$RUN/bad.stderr"
test ! -e "$RUN/bad-output.tsv"
echo 'aggregate_empty_no_overlap_and_error_schema=PASS' >> "$LOG"

# RASQUAL driver contract boundaries and paths.
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
grep -q 'zero_feature' "$RUN/zero-plan.json"
head -c 8 "$RASQUAL_SRC/data/Y.bin" > "$RUN/short.bin"
set +e
"$PY" "$DRIVER" --features "$AUDIT/inputs/rasqual-two-features.tsv" \
  --counts "$RUN/short.bin" --offsets "$RASQUAL_SRC/data/K.bin" --vcf "$RASQUAL_SRC/data/chr11.gz" \
  --samples 24 --matrix-rows 2 --output-dir "$RUN/never" --dry-run > "$RUN/dim.stdout" 2> "$RUN/dim.stderr"
dim_rc=$?
set -e
test "$dim_rc" -eq 2
grep -q 'expected exactly 24 samples x 2 rows x 8 bytes = 384' "$RUN/dim.stderr"
echo 'rasqual_zero_feature_and_dimension_guards=PASS' >> "$LOG"

# Pipeline target-sample and output guards.
cat > "$RUN/tiny.sam" <<'EOF'
@HD	VN:1.6	SO:coordinate
@SQ	SN:chrAudit	LN:1000
@RG	ID:rg1	SM:NA12878	PL:ILLUMINA
r1	0	chrAudit	100	60	10M	*	0	0	AAAAAAAAAA	IIIIIIIIII	RG:Z:rg1
EOF
samtools view -bS -o "$RUN/tiny.bam" "$RUN/tiny.sam"
samtools index "$RUN/tiny.bam"
printf '>chrAudit\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n' > "$RUN/ref.fa"
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
bash "$PIPELINE" "$RUN/tiny.bam" "$RUN/multisample.vcf.gz" "$RUN/ref.fa" "$RUN/index" \
  "$RUN/peaks.bed" "$RUN/wasp-stub" "$RUN/target-filter-out" > "$RUN/target-filter.stdout" 2> "$RUN/target-filter.stderr"
target_rc=$?
set -e
test "$target_rc" -eq 65
grep -q 'target sample has no biallelic heterozygous SNPs' "$RUN/target-filter.stderr"
test ! -e "$RUN/target-filter-out"
if compgen -G "$RUN/target-filter-out.tmp.*" >/dev/null; then exit 1; fi
echo 'pipeline_target_only_filter_and_cleanup=PASS' >> "$LOG"

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
bash "$PIPELINE" "$RUN/tiny.bam" "$RUN/mismatch.vcf.gz" "$RUN/ref.fa" "$RUN/index" \
  "$RUN/peaks.bed" "$RUN/wasp-stub" "$RUN/mismatch-out" > "$RUN/mismatch.stdout" 2> "$RUN/mismatch.stderr"
mismatch_rc=$?
set -e
test "$mismatch_rc" -eq 65
grep -q 'must match exactly one VCF sample' "$RUN/mismatch.stderr"
mkdir -p "$RUN/existing-output"
set +e
bash "$PIPELINE" "$RUN/tiny.bam" "$RUN/multisample.vcf.gz" "$RUN/ref.fa" "$RUN/index" \
  "$RUN/peaks.bed" "$RUN/wasp-stub" "$RUN/existing-output" > "$RUN/reuse.stdout" 2> "$RUN/reuse.stderr"
reuse_rc=$?
set -e
test "$reuse_rc" -eq 73
grep -q 'output directory already exists' "$RUN/reuse.stderr"
echo 'pipeline_identity_and_reuse_guards=PASS' >> "$LOG"
echo 'fixture_reaudit2_complete=PASS' >> "$LOG"
cat "$LOG"
