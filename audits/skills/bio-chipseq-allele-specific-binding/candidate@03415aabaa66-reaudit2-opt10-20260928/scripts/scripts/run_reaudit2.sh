#!/usr/bin/env bash
set -euo pipefail

ROOT=/mnt/openscience/audit-envs/bio-chipseq-allele-specific-binding
CANDIDATE=/mnt/openscience/wt/opt10-chipseq-asb/skills/bio-chipseq-allele-specific-binding
AUDIT=/mnt/openscience/audits/bio-chipseq-allele-specific-binding/reaudit2-opt10-20260928
FIXTURE=/mnt/openscience/fixes/bio-chipseq-allele-specific-binding/focused-regressions
PRIOR_DELTA="$ROOT/delta-20260928"
EVIDENCE="$AUDIT/evidence"
RUNROOT="$EVIDENCE/run-artifacts"
SECONDARY="$EVIDENCE/secondary-artifacts"
RSCRIPT="$ROOT/env/bin/Rscript"
R="$ROOT/env/bin/R"
PYTHON="$ROOT/env/bin/python"
SAMTOOLS="$ROOT/env/bin/samtools"
TABIX="$ROOT/env/bin/tabix"
RASQUAL="$ROOT/fixtures/rasqual-build/rasqual"
WORKFLOW="$CANDIDATE/scripts/baalchip_workflow.R"
SOURCE_TAR="$ROOT/sources/BaalChIP_1.36.0.tar.gz"
SOURCE_DIR="$ROOT/sources/BaalChIP-1.36.0"

case "$RUNROOT" in
  "$AUDIT"/evidence/run-artifacts) rm -rf -- "$RUNROOT" ;;
  *) printf 'unsafe run path: %s\n' "$RUNROOT" >&2; exit 98 ;;
esac
case "$SECONDARY" in
  "$AUDIT"/evidence/secondary-artifacts) rm -rf -- "$SECONDARY" ;;
  *) printf 'unsafe secondary path: %s\n' "$SECONDARY" >&2; exit 98 ;;
esac
mkdir -p "$RUNROOT" "$SECONDARY" "$EVIDENCE"
exec > >(tee "$EVIDENCE/execution.log") 2>&1

export PATH="$ROOT/env/bin:/usr/bin:/bin"
export R_LIBS_USER="$ROOT/r-lib"
export PYTHONDONTWRITEBYTECODE=1

pass() { printf 'PASS\t%s\t%s\n' "$1" "${2:-}"; }

run_baal() {
  "$RSCRIPT" --vanilla "$WORKFLOW" \
    --samples "$FIXTURE/baal-fixture/samples.tsv" \
    --hets "$FIXTURE/baal-fixture/hets-raf.tsv" \
    --group TUMOR \
    --blacklist "$FIXTURE/baal-fixture/blacklist.bed" \
    --imprinted "$FIXTURE/baal-fixture/imprinted.bed" \
    --sex female \
    --assembly GRCh38 \
    --samples-assembly GRCh38 \
    --hets-assembly GRCh38 \
    --blacklist-assembly GRCh38 \
    --imprinted-assembly GRCh38 \
    --correction raf \
    --samtools "$SAMTOOLS" \
    --out "$RUNROOT/default" \
    "$@"
}

expect_baal_failure() {
  local label=$1
  local expected=$2
  shift 2
  set +e
  local output
  output=$(run_baal "$@" 2>&1)
  local status=$?
  set -e
  if [[ $status -eq 0 ]] || ! grep -Fq "$expected" <<<"$output"; then
    printf 'FAIL\t%s\tstatus=%s expected=%s\n%s\n' "$label" "$status" "$expected" "$output" >&2
    exit 80
  fi
  printf '%s\n' "$output" >"$RUNROOT/${label}.stderr.txt"
  pass "$label" "exit=$status expected=$expected"
}

"$PYTHON" -B - "$CANDIDATE" "$EVIDENCE/candidate-manifest.tsv" "$EVIDENCE/candidate-identity.txt" <<'PY'
from hashlib import sha256
from pathlib import Path
import sys

root = Path(sys.argv[1])
paths = sorted(
    (path for path in root.rglob("*") if path.is_file()),
    key=lambda path: path.relative_to(root).as_posix().encode(),
)
rows = [
    f"{path.relative_to(root).as_posix()}\t{sha256(path.read_bytes()).hexdigest()}"
    for path in paths
]
manifest_bytes = "\n".join(rows).encode()
digest = sha256(manifest_bytes).hexdigest()
expected = "03415aabaa66de0ef1b747e3fc664dae6d2868e42bf52a2c104d990db5e6057f"
if len(rows) != 8 or len(manifest_bytes) != 750 or digest != expected:
    raise SystemExit(
        f"candidate mismatch: rows={len(rows)} bytes={len(manifest_bytes)} "
        f"digest={digest} expected={expected}"
    )
Path(sys.argv[2]).write_text("\n".join(rows) + "\n", encoding="utf-8")
Path(sys.argv[3]).write_text(digest + "\n", encoding="utf-8")
print(f"PASS\tcandidate_identity\trows=8 bytes=750 digest={digest}")
PY

{
  printf 'python\t%s\n' "$("$PYTHON" --version 2>&1)"
  printf 'r\t%s\n' "$("$R" --version | head -n 1)"
  printf 'bioconductor\t3.22\n'
  printf 'samtools\t%s\n' "$("$SAMTOOLS" --version | head -n 1)"
  printf 'tabix\t%s\n' "$("$TABIX" --version 2>&1 | head -n 1)"
  printf 'wasp_commit\t%s\n' "$(git -C "$ROOT/sources/WASP" rev-parse HEAD)"
  printf 'rasqual_commit\t%s\n' "$(git -C "$ROOT/sources/rasqual" rev-parse HEAD)"
  printf 'alleleseq_remote\t%s\n' "$(git -C "$ROOT/sources/AlleleSeq2" remote get-url origin)"
  printf 'alleleseq_commit\t%s\n' "$(git -C "$ROOT/sources/AlleleSeq2" rev-parse HEAD)"
  printf 'environment_lock_sha256\t%s\n' "$(sha256sum "$ROOT/environment-explicit.lock" | awk '{print $1}')"
  printf 'r_packages_sha256\t%s\n' "$(sha256sum "$ROOT/r-packages.tsv" | awk '{print $1}')"
} >"$EVIDENCE/environment.tsv"
pass environment "pinned tool and lock identities captured"

test "$(sha256sum "$SOURCE_TAR" | awk '{print $1}')" = f3d033913484173f5ae6bcdb62d199f122736e634b3861c8f165b32c475a227e
grep -Fxq 'Version: 1.36.0' "$SOURCE_DIR/DESCRIPTION"
grep -Fxq 'git_branch: RELEASE_3_22' "$SOURCE_DIR/DESCRIPTION"
grep -Fxq 'Repository: Bioconductor 3.22' "$SOURCE_DIR/DESCRIPTION"
grep -A8 '^Package: BaalChIP$' "$ROOT/delta3-20260928/PACKAGES.3.22" >"$EVIDENCE/baalchip-packages-entry.txt"
grep -Fxq 'Version: 1.36.0' "$EVIDENCE/baalchip-packages-entry.txt"
METHODS="$SOURCE_DIR/R/BaalChIP-methods.R"
grep -Fq 'BaalChIP <- function(samplesheet = NULL, hets = NULL, CorrectWithgDNA = list())' "$METHODS"
grep -Fq 'function(.Object, Iter = 5000, conf_level = 0.95, cores = 4, RMcorrection = TRUE,' "$METHODS"
grep -Fq 'RAFcorrection = TRUE, verbose = TRUE)' "$METHODS"
grep -Fq 'setMethod("BaalChIP.get", "BaalChIP"' "$METHODS"
grep -Fq 'setMethod("BaalChIP.report", "BaalChIP"' "$METHODS"
grep -Fq 'names(query) <- group_names' "$METHODS"
grep -Fq 'BAALCHIP_CONTRACT_VERSION <- "1.36.0"' "$CANDIDATE/scripts/baalchip_contracts.R"
grep -Fq 'BAALCHIP_CONTRACT_BIOCONDUCTOR <- "3.22"' "$CANDIDATE/scripts/baalchip_contracts.R"
grep -Fq 'assert_baalchip_version(packageVersion("BaalChIP"))' "$WORKFLOW"
grep -Fq 'BaalChIP 1.36.0 from Bioconductor 3.22 on R 4.5' "$CANDIDATE/SKILL.md"
grep -Fq "stopifnot(as.character(packageVersion('BaalChIP')) == '1.36.0')" "$CANDIDATE/references/methods-and-commands.md"
{
  printf 'package\tBaalChIP\nversion\t1.36.0\nbioconductor\t3.22\nr\t4.5\n'
  printf 'tar_sha256\tf3d033913484173f5ae6bcdb62d199f122736e634b3861c8f165b32c475a227e\n'
  printf 'api\tCorrectWithgDNA,Iter,RMcorrection,RAFcorrection,mergedCounts,named-group-reports\n'
  printf 'status\tPASS\n'
} >"$EVIDENCE/baalchip-source-binding.tsv"
pass baalchip_binding "official Bioconductor 3.22 / BaalChIP 1.36.0 / R 4.5 and used APIs"

alleleseq_url=$(git -C "$ROOT/sources/AlleleSeq2" remote get-url origin)
alleleseq_head=$(git -C "$ROOT/sources/AlleleSeq2" rev-parse HEAD)
test "$alleleseq_url" = 'https://github.com/trgaleev/AlleleSeq2.git'
test "$alleleseq_head" = 'cfe8acf88989922da841e71238b360f8f57e813a'
grep -Fq '[`trgaleev/AlleleSeq2`](https://github.com/trgaleev/AlleleSeq2)' "$CANDIDATE/SKILL.md"
grep -Fq 'Canonical method: [Rozowsky et al., Molecular Systems Biology]' "$CANDIDATE/references/methods-and-commands.md"
grep -Fq 'tested implementation: [`trgaleev/AlleleSeq2`](https://github.com/trgaleev/AlleleSeq2)' "$CANDIDATE/references/methods-and-commands.md"
printf 'remote\t%s\nhead\t%s\ncanonical_method\tRozowsky et al. 2011; separate from tested implementation\nclassification\texternal-only legacy implementation\nstatus\tPASS\n' \
  "$alleleseq_url" "$alleleseq_head" >"$EVIDENCE/alleleseq-binding.tsv"
pass alleleseq_binding "trgaleev/AlleleSeq2@cfe8acf; canonical paper separate"

"$RSCRIPT" --vanilla -e "invisible(parse(file='$WORKFLOW')); invisible(parse(file='$CANDIDATE/scripts/baalchip_contracts.R'))"
"$RSCRIPT" --vanilla "$CANDIDATE/tests/test_baalchip_contracts.R" "$CANDIDATE/scripts/baalchip_contracts.R"
"$PYTHON" -B -m unittest discover -s "$CANDIDATE/tests" -p 'test_*.py'
"$RSCRIPT" --vanilla -e "source('$CANDIDATE/scripts/baalchip_contracts.R'); assert_baalchip_version('1.36.0'); tryCatch(assert_baalchip_version('1.38.0'), error=function(e) { stopifnot(startsWith(conditionMessage(e), '[version_mismatch]')); cat('expected version mismatch:', conditionMessage(e), '\n') })"
pass candidate_tests "R helper/version suite and Python 3/3"

mkdir -p "$RUNROOT/install-probe-lib"
set +e
R_LIBS_USER="$RUNROOT/install-probe-lib:$ROOT/r-lib" "$R" CMD INSTALL --library="$RUNROOT/install-probe-lib" "$SOURCE_TAR" >"$EVIDENCE/package-install-probe.log" 2>&1
install_status=$?
set -e
test "$install_status" -ne 0
grep -Fq 'dependencies' "$EVIDENCE/package-install-probe.log"
grep -Eq 'Rsamtools|GenomicAlignments' "$EVIDENCE/package-install-probe.log"
pass bounded_install_probe "exit=$install_status; exact source blocked by missing compiled dependencies"

"$SAMTOOLS" quickcheck -v "$FIXTURE/baal-fixture/rep1.wasp.bam"
test -f "$FIXTURE/baal-fixture/rep1.wasp.bam.bai"
run_baal --preflight-only --out "$RUNROOT/raf-preflight"
grep -Eq '^preflight_passed[[:space:]]+GRCh38[[:space:]]+TUMOR[[:space:]]+raf[[:space:]]+1\.36\.0$' "$RUNROOT/raf-preflight/run-status.tsv"
grep -Fq $'raf\t' "$RUNROOT/raf-preflight/correction-provenance.tsv"
grep -Fq $'bam_1\tchr' "$RUNROOT/raf-preflight/contig-contract.tsv"
run_baal --correction gdna --gdna-bam "$FIXTURE/baal-fixture/rep1.wasp.bam" --preflight-only --out "$RUNROOT/gdna-preflight"
grep -Fq $'gdna_bam\tchr' "$RUNROOT/gdna-preflight/contig-contract.tsv"
grep -Fq "$FIXTURE/baal-fixture/rep1.wasp.bam" "$RUNROOT/gdna-preflight/correction-provenance.tsv"
pass raf_gdna_preflights "real indexed BAM; 1.36.0 status; measured RAF and gDNA provenance"

expect_baal_failure af_not_raf '[missing_raf]' --hets "$FIXTURE/baal-fixture/hets-af.tsv" --out "$RUNROOT/af-not-raf"
expect_baal_failure missing_alt '[schema_mismatch]' --hets "$PRIOR_DELTA/hets-missing-alt.tsv" --out "$RUNROOT/missing-alt"
expect_baal_failure assembly_mismatch '[assembly_mismatch]' --hets-assembly hg19 --out "$RUNROOT/assembly-mismatch"
expect_baal_failure contig_mismatch '[contig_mismatch]' --blacklist "$PRIOR_DELTA/blacklist-bare.bed" --out "$RUNROOT/contig-mismatch"
expect_baal_failure sample_mismatch '[sample_mismatch]' --group OTHER --out "$RUNROOT/sample-mismatch"
expect_baal_failure empty_intervals '[empty_intervals]' --blacklist "$PRIOR_DELTA/blacklist-empty.bed" --out "$RUNROOT/empty-intervals"
expect_baal_failure missing_bam '[missing_input]' --samples "$PRIOR_DELTA/samples-missing-bam.tsv" --out "$RUNROOT/missing-bam"
expect_baal_failure missing_bed '[missing_input]' --samples "$PRIOR_DELTA/samples-missing-bed.tsv" --out "$RUNROOT/missing-bed"
expect_baal_failure existing_output '[output_exists]' --preflight-only --out "$RUNROOT/raf-preflight"
expect_baal_failure missing_gdna '[missing_gdna]' --correction gdna --out "$RUNROOT/missing-gdna"
pass negative_baal_boundaries "ten expected structured failures"

mkdir "$RUNROOT/unrelated.partial-keep"
printf 'preserve\n' >"$RUNROOT/unrelated.partial-keep/sentinel.txt"
set +e
cleanup_output=$(run_baal --hets "$PRIOR_DELTA/hets-all-excluded.tsv" --out "$RUNROOT/atomic-cleanup" 2>&1)
cleanup_status=$?
set -e
printf '%s\n' "$cleanup_output" >"$RUNROOT/atomic-cleanup.stderr.txt"
test "$cleanup_status" -ne 0
grep -Eq "there is no package called .BaalChIP.|package .BaalChIP. is not available" <<<"$cleanup_output"
test ! -e "$RUNROOT/atomic-cleanup"
test "$(find "$RUNROOT" -maxdepth 1 -name 'atomic-cleanup.partial-*' -print | wc -l)" -eq 0
test "$(cat "$RUNROOT/unrelated.partial-keep/sentinel.txt")" = preserve
pass atomic_cleanup "missing-package exit=$cleanup_status; no final/partial; unrelated sentinel preserved"

WASP="$ROOT/sources/WASP"
WRUN="$RUNROOT/wasp"
mkdir -p "$WRUN/snps" "$WRUN/out"
cp "$WASP/examples/example_data/test_genome.fa" "$WRUN/genome.fa"
cp "$WASP/examples/example_data/test_reads1.fq" "$WRUN/reads1.fq"
cp "$WASP/examples/example_data/test_reads2.fq" "$WRUN/reads2.fq"
cp "$WASP/examples/example_data/test_chr1.snps.txt.gz" "$WRUN/snps/test_chr1.snps.txt.gz"
cp "$WASP/examples/example_data/test_chr2.snps.txt.gz" "$WRUN/snps/test_chr2.snps.txt.gz"
bowtie2-build --quiet "$WRUN/genome.fa" "$WRUN/genome"
bowtie2 --quiet -x "$WRUN/genome" -1 "$WRUN/reads1.fq" -2 "$WRUN/reads2.fq" -S "$WRUN/input.sam"
samtools view -bS "$WRUN/input.sam" | samtools sort -o "$WRUN/input.bam"
samtools index "$WRUN/input.bam"
python "$WASP/mapping/find_intersecting_snps.py" --is_paired_end --is_sorted --output_dir "$WRUN/out" --snp_dir "$WRUN/snps" "$WRUN/input.bam" >"$WRUN/find.stdout" 2>"$WRUN/find.stderr"
bowtie2 --quiet -x "$WRUN/genome" -1 "$WRUN/out/input.remap.fq1.gz" -2 "$WRUN/out/input.remap.fq2.gz" | samtools view -b -o "$WRUN/input.remap.bam"
python "$WASP/mapping/filter_remapped_reads.py" "$WRUN/out/input.to.remap.bam" "$WRUN/input.remap.bam" "$WRUN/input.remap.keep.bam" >"$WRUN/filter.stdout" 2>"$WRUN/filter.stderr"
samtools merge -f "$WRUN/merged.bam" "$WRUN/out/input.keep.bam" "$WRUN/input.remap.keep.bam"
samtools sort -o "$WRUN/final.wasp.bam" "$WRUN/merged.bam"
samtools index "$WRUN/final.wasp.bam"
input_alignments=$(samtools view -c "$WRUN/input.bam")
direct_keep=$(samtools view -c "$WRUN/out/input.keep.bam")
remap_keep=$(samtools view -c "$WRUN/input.remap.keep.bam")
final_alignments=$(samtools view -c "$WRUN/final.wasp.bam")
final_paired=$(samtools view -c -f 1 "$WRUN/final.wasp.bam")
fq1_records=$(( $(gzip -dc "$WRUN/out/input.remap.fq1.gz" | wc -l) / 4 ))
fq2_records=$(( $(gzip -dc "$WRUN/out/input.remap.fq2.gz" | wc -l) / 4 ))
test "$fq1_records" -gt 0
test "$fq1_records" -eq "$fq2_records"
test "$final_alignments" -eq $((direct_keep + remap_keep))
test "$final_paired" -eq "$final_alignments"
test "$final_alignments" -le "$input_alignments"
printf 'input_alignments\t%s\ndirect_keep_alignments\t%s\nremap_fastq1_records\t%s\nremap_fastq2_records\t%s\nremap_keep_alignments\t%s\nfinal_alignments\t%s\nfinal_paired_alignments\t%s\npaired_output_names\tinput.remap.fq1.gz,input.remap.fq2.gz\nstatus\tPASS\n' \
  "$input_alignments" "$direct_keep" "$fq1_records" "$fq2_records" "$remap_keep" "$final_alignments" "$final_paired" >"$EVIDENCE/wasp-live.tsv"
pass wasp_live "paired names/count invariants; final=$final_alignments input=$input_alignments"

RASRUN="$RUNROOT/rasqual"
mkdir -p "$RASRUN/input"
cp "$PRIOR_DELTA/rasqual-binaries/Y.txt" "$RASRUN/input/Y.txt"
cp "$PRIOR_DELTA/rasqual-binaries/K.txt" "$RASRUN/input/K.txt"
cp "$PRIOR_DELTA/rasqual-binaries/X.txt" "$RASRUN/input/X.txt"
cp "$FIXTURE/rasqual-features.tsv" "$RASRUN/features.tsv"
"$PYTHON" -B "$CANDIDATE/scripts/rasqual_cohort.py" prepare \
  --rasqual-source "$ROOT/sources/rasqual" --r "$R" \
  --y "$RASRUN/input/Y.txt" --k "$RASRUN/input/K.txt" --x "$RASRUN/input/X.txt" \
  --out "$RASRUN/binaries"
"$PYTHON" -B "$CANDIDATE/scripts/rasqual_cohort.py" run \
  --manifest "$RASRUN/features.tsv" --feature-count 2 --covariates 4 \
  --y "$RASRUN/binaries/Y.bin" --k "$RASRUN/binaries/K.bin" --x "$RASRUN/binaries/X.bin" \
  --vcf "$ROOT/sources/rasqual/data/chr11.gz" --tabix "$TABIX" --rasqual "$RASQUAL" \
  --output "$RASRUN/cohort.tsv"
test "$(wc -l < "$RASRUN/cohort.tsv")" -eq 3
test "$(awk -F '\t' 'NR>1 && $1=="C11orf21"{n++} END{print n+0}' "$RASRUN/cohort.tsv")" -eq 1
test "$(awk -F '\t' 'NR>1 && $1=="TSPAN32"{n++} END{print n+0}' "$RASRUN/cohort.tsv")" -eq 1
test "$(awk -F '\t' 'NR>1 && $23==0{n++} END{print n+0}' "$RASRUN/cohort.tsv")" -eq 2
awk -F '\t' 'NR>1 {if ($14<0 || $14>1 || $26<0 || $26>1 || $27<0 || $27>1) exit 1}' "$RASRUN/cohort.tsv"
set +e
rasqual_existing=$("$PYTHON" -B "$CANDIDATE/scripts/rasqual_cohort.py" run \
  --manifest "$RASRUN/features.tsv" --feature-count 2 --covariates 4 \
  --y "$RASRUN/binaries/Y.bin" --k "$RASRUN/binaries/K.bin" --x "$RASRUN/binaries/X.bin" \
  --vcf "$ROOT/sources/rasqual/data/chr11.gz" --tabix "$TABIX" --rasqual "$RASQUAL" \
  --output "$RASRUN/cohort.tsv" 2>&1)
rasqual_existing_status=$?
set -e
test "$rasqual_existing_status" -eq 2
grep -Fq 'refusing to overwrite output' <<<"$rasqual_existing"
printf '%s\n' "$rasqual_existing" >"$RASRUN/existing-output.stderr.txt"
cp "$RASRUN/binaries/binary-contract.tsv" "$EVIDENCE/rasqual-binary-contract.tsv"
cp "$RASRUN/cohort.tsv" "$EVIDENCE/rasqual-cohort.tsv"
pass rasqual_live "public 2-feature cohort; exact binary sizes; converged rows; finite phi/p/q; overwrite refused"

IRUN="$SECONDARY/intervals"
mkdir -p "$IRUN"
printf 'chr1\t9\t10\tA\tG\nchr1\t19\t20\tC\tT\nchrX\t29\t30\tG\tA\n' >"$IRUN/hetSNPs.bed"
printf 'chr1\t8\t11\tIMPRINTED_A\n' >"$IRUN/imprinted_loci_hg38.bed"
bedtools intersect -v -a "$IRUN/hetSNPs.bed" -b "$IRUN/imprinted_loci_hg38.bed" >"$IRUN/non_imprinted.bed"
awk '$1 != "chrX"' "$IRUN/hetSNPs.bed" >"$IRUN/autosomal.bed"
test "$(wc -l < "$IRUN/non_imprinted.bed")" -eq 2
test "$(wc -l < "$IRUN/autosomal.bed")" -eq 2
printf 'input_rows\t3\nnon_imprinted_rows\t2\nautosomal_rows\t2\nstatus\tPASS\n' >"$EVIDENCE/interval-live.tsv"
pass interval_filters "2/3 non-imprinted; 2/3 autosomal"

BUILD="$SECONDARY/wasp-snp2h5-build"
HRUN="$SECONDARY/wasp-hdf5"
cp -a "$WASP/snp2h5" "$BUILD"
mkdir -p "$HRUN"
make -C "$BUILD" HDF_INSTALL="$ROOT/env" CC="$ROOT/env/bin/x86_64-conda-linux-gnu-cc" \
  CFLAGS="-std=gnu89 -DH5_USE_16_API -I$ROOT/env/include -Wall -g" \
  >"$SECONDARY/wasp-snp2h5-build.log" 2>&1
DATA="$WASP/examples/example_data"
"$BUILD/snp2h5" \
  --chrom "$DATA/chromInfo.hg19.txt" --format impute \
  --snp_index "$HRUN/snp_index.h5" --geno_prob "$HRUN/geno_probs.h5" \
  --snp_tab "$HRUN/snp_tab.h5" --haplotype "$HRUN/haps.h5" \
  --samples "$DATA/genotypes/YRI_samples.txt" \
  "$DATA/genotypes/chr22.hg19.impute2.gz" "$DATA/genotypes/chr22.hg19.impute2_haps.gz"
"$PYTHON" -B - "$HRUN" "$EVIDENCE/wasp-hdf5-live.tsv" <<'PY'
from pathlib import Path
import sys
import tables

root = Path(sys.argv[1])
expected = {
    "snp_index.h5": (51304566,),
    "snp_tab.h5": (247303,),
    "haps.h5": (247303, 120),
    "geno_probs.h5": (247303, 180),
}
rows = []
for name, shape in expected.items():
    with tables.open_file(root / name) as handle:
        actual = handle.root.chr22.shape
    if actual != shape:
        raise SystemExit(f"{name}: expected {shape}, got {actual}")
    rows.append(f"{name}\t/chr22\t{actual}")
rows.append("status\tPASS")
Path(sys.argv[2]).write_text("\n".join(rows) + "\n", encoding="utf-8")
PY
pass wasp_hdf5 "provider chr22 IMPUTE2/HAPS shapes verified"

set +e
make -f "$ROOT/sources/AlleleSeq2/PIPELINE.mk" -n \
  PGENOME_DIR="$SECONDARY/personalized" REFGENOME_VERSION=GRCh38 ALIGNMENT_MODE=ASB NTHR=1 \
  >"$EVIDENCE/alleleseq-make-dryrun.stdout" 2>"$EVIDENCE/alleleseq-make-dryrun.stderr"
make_status=$?
set -e
{
  printf 'remote\t%s\n' "$alleleseq_url"
  printf 'commit\t%s\n' "$alleleseq_head"
  printf 'make_dryrun_exit\t%s\n' "$make_status"
  for tool in python2 STAR picard; do
    if command -v "$tool" >/dev/null 2>&1; then printf '%s\tAVAILABLE\n' "$tool"; else printf '%s\tUNAVAILABLE\n' "$tool"; fi
  done
  if find "$ROOT/sources/AlleleSeq2" -iname 'vcf2diploid*.jar' -print -quit | grep -q .; then
    printf 'official_vcf2diploid_jar\tFOUND\n'
  else
    printf 'official_vcf2diploid_jar\tUNAVAILABLE\n'
  fi
  printf 'classification\tUNAVAILABLE_FULL_TOOLCHAIN_EXTERNAL_ONLY_NOT_CREDITED\n'
} >"$EVIDENCE/alleleseq-boundary.tsv"
pass alleleseq_boundary "exact implementation bound; full legacy runtime remains unavailable and uncredited"

set +e
"$RSCRIPT" --vanilla -e 'quit(status=ifelse(requireNamespace("BaalChIP", quietly=TRUE), 0L, 1L))'
baal_installed=$?
"$RSCRIPT" --vanilla -e 'quit(status=ifelse(requireNamespace("Rsamtools", quietly=TRUE), 0L, 1L))'
rsamtools_installed=$?
"$RSCRIPT" --vanilla -e 'quit(status=ifelse(requireNamespace("GenomicAlignments", quietly=TRUE), 0L, 1L))'
genomic_alignments_installed=$?
"$RSCRIPT" --vanilla -e 'quit(status=ifelse(requireNamespace("rtracklayer", quietly=TRUE), 0L, 1L))'
rtrack_installed=$?
set -e
test "$baal_installed" -eq 1
test "$rsamtools_installed" -eq 1
test "$genomic_alignments_installed" -eq 1
test "$rtrack_installed" -eq 1
printf 'BaalChIP_requireNamespace_exit\t%s\nRsamtools_requireNamespace_exit\t%s\nGenomicAlignments_requireNamespace_exit\t%s\nrtracklayer_requireNamespace_exit\t%s\ninstall_probe_exit\t%s\nclassification\tRESOURCE_INFEASIBLE_BOUNDED_NOT_CREDITED\n' \
  "$baal_installed" "$rsamtools_installed" "$genomic_alignments_installed" "$rtrack_installed" "$install_status" >"$EVIDENCE/baalchip-runtime-boundary.tsv"
pass baalchip_runtime_boundary "full model/all-excluded/no-call unavailable after bounded exact-source probe; no credit"

printf 'ALL_REAUDIT2_CONTRACTS_PASS\n'
