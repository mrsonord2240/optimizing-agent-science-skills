#!/usr/bin/env bash
set -euo pipefail

ROOT=/mnt/openscience/audit-envs/bio-chipseq-allele-specific-binding
CANDIDATE=/mnt/openscience/wt/opt10-chipseq-asb/skills/bio-chipseq-allele-specific-binding
AUDIT=/mnt/openscience/audits/bio-chipseq-allele-specific-binding/reaudit-opt10-20260928
FIXTURE=/mnt/openscience/fixes/bio-chipseq-allele-specific-binding/focused-regressions
PRIOR_DELTA="$ROOT/delta-20260928"
RUNROOT="$AUDIT/evidence/run-artifacts"
EVIDENCE="$AUDIT/evidence"
RSCRIPT="$ROOT/env/bin/Rscript"
R="$ROOT/env/bin/R"
PYTHON="$ROOT/env/bin/python"
SAMTOOLS="$ROOT/env/bin/samtools"
TABIX="$ROOT/env/bin/tabix"
RASQUAL="$ROOT/fixtures/rasqual-build/rasqual"
WORKFLOW="$CANDIDATE/scripts/baalchip_workflow.R"

case "$RUNROOT" in
  "$AUDIT"/evidence/run-artifacts) rm -rf -- "$RUNROOT" ;;
  *) printf 'unsafe run path: %s\n' "$RUNROOT" >&2; exit 98 ;;
esac
mkdir -p "$RUNROOT" "$EVIDENCE"
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
  label=$1
  expected=$2
  shift 2
  set +e
  output=$(run_baal "$@" 2>&1)
  status=$?
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
manifest = Path(sys.argv[2])
identity_file = Path(sys.argv[3])
paths = [
    "SKILL.md",
    "references/methods-and-commands.md",
    "references/pitfalls-and-troubleshooting.md",
    "scripts/baalchip_contracts.R",
    "scripts/baalchip_workflow.R",
    "scripts/rasqual_cohort.py",
    "tests/test_baalchip_contracts.R",
    "tests/test_rasqual_cohort.py",
]
rows = [f"{path}\t{sha256((root / path).read_bytes()).hexdigest()}" for path in paths]
digest = sha256("\n".join(rows).encode()).hexdigest()
expected = "944f852224538df92c581ab4a42889202ab10639f54974130f841782f5c90ead"
if digest != expected:
    raise SystemExit(f"candidate digest mismatch: {digest} != {expected}")
manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")
identity_file.write_text(digest + "\n", encoding="utf-8")
print(f"PASS\tcandidate_identity\t{digest}")
PY

{
  printf 'python\t%s\n' "$("$PYTHON" --version 2>&1)"
  printf 'r\t%s\n' "$("$R" --version | head -n 1)"
  printf 'samtools\t%s\n' "$("$SAMTOOLS" --version | head -n 1)"
  printf 'tabix\t%s\n' "$("$TABIX" --version 2>&1 | head -n 1)"
  printf 'wasp_commit\t%s\n' "$(git -C "$ROOT/sources/WASP" rev-parse HEAD)"
  printf 'rasqual_commit\t%s\n' "$(git -C "$ROOT/sources/rasqual" rev-parse HEAD)"
  printf 'alleleseq_commit\t%s\n' "$(git -C "$ROOT/sources/AlleleSeq2" rev-parse HEAD)"
  printf 'environment_lock_sha256\t%s\n' "$(sha256sum "$ROOT/environment-explicit.lock" | awk '{print $1}')"
  printf 'r_packages_sha256\t%s\n' "$(sha256sum "$ROOT/r-packages.tsv" | awk '{print $1}')"
} >"$EVIDENCE/environment.tsv"
pass environment "pinned tool and lock identities captured"

"$RSCRIPT" --vanilla -e "invisible(parse(file='$WORKFLOW')); invisible(parse(file='$CANDIDATE/scripts/baalchip_contracts.R'))"
"$RSCRIPT" --vanilla "$CANDIDATE/tests/test_baalchip_contracts.R" "$CANDIDATE/scripts/baalchip_contracts.R"
"$PYTHON" -B -m unittest discover -s "$CANDIDATE/tests" -p 'test_*.py'
pass candidate_tests "R parse/helper suite and Python 3/3"

"$SAMTOOLS" quickcheck -v "$FIXTURE/baal-fixture/rep1.wasp.bam"
test -f "$FIXTURE/baal-fixture/rep1.wasp.bam.bai"
header_contig=$("$SAMTOOLS" view -H "$FIXTURE/baal-fixture/rep1.wasp.bam" | awk -F '\t' '$1=="@SQ" {for(i=1;i<=NF;i++) if($i ~ /^SN:/) {sub(/^SN:/,"",$i); print $i; exit}}')
test "$header_contig" = chr1
pass real_indexed_bam "quickcheck; contig=$header_contig; BAI present"

run_baal --preflight-only --out "$RUNROOT/raf-preflight"
grep -Fq $'raf\t' "$RUNROOT/raf-preflight/correction-provenance.tsv"
grep -Fq $'bam_1\tchr' "$RUNROOT/raf-preflight/contig-contract.tsv"
pass raf_preflight "measured RAF provenance and chr contract"

run_baal --correction gdna --gdna-bam "$FIXTURE/baal-fixture/rep1.wasp.bam" --preflight-only --out "$RUNROOT/gdna-preflight"
grep -Fq $'gdna_bam\tchr' "$RUNROOT/gdna-preflight/contig-contract.tsv"
grep -Fq "$FIXTURE/baal-fixture/rep1.wasp.bam" "$RUNROOT/gdna-preflight/correction-provenance.tsv"
pass gdna_preflight "indexed gDNA provenance and chr contract"

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
test $cleanup_status -ne 0
grep -Eq "there is no package called .BaalChIP.|package .BaalChIP. is not available" <<<"$cleanup_output"
test ! -e "$RUNROOT/atomic-cleanup"
matching_partial_count=$(find "$RUNROOT" -maxdepth 1 -name 'atomic-cleanup.partial-*' -print | wc -l)
test "$matching_partial_count" -eq 0
test "$(cat "$RUNROOT/unrelated.partial-keep/sentinel.txt")" = preserve
pass missing_baalchip_atomic_cleanup "exit=$cleanup_status no final; matching partials=0; unrelated sentinel preserved"

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
samtools quickcheck -v "$WRUN/final.wasp.bam"
{
  printf 'input_alignments\t%s\n' "$input_alignments"
  printf 'direct_keep_alignments\t%s\n' "$direct_keep"
  printf 'remap_fastq1_records\t%s\n' "$fq1_records"
  printf 'remap_fastq2_records\t%s\n' "$fq2_records"
  printf 'remap_keep_alignments\t%s\n' "$remap_keep"
  printf 'final_alignments\t%s\n' "$final_alignments"
  printf 'final_paired_alignments\t%s\n' "$final_paired"
  printf 'paired_output_names\tinput.remap.fq1.gz,input.remap.fq2.gz\n'
  printf 'status\tPASS\n'
} >"$EVIDENCE/wasp-live.tsv"
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
pass rasqual_live "public 2-feature cohort; exact binary sizes; 2 converged rows; finite phi/p/q; overwrite refused"

{
  printf 'alleleseq_commit\t%s\n' "$(git -C "$ROOT/sources/AlleleSeq2" rev-parse HEAD)"
  for tool in python2 STAR picard; do
    if command -v "$tool" >/dev/null 2>&1; then printf '%s\tAVAILABLE\n' "$tool"; else printf '%s\tUNAVAILABLE\n' "$tool"; fi
  done
  if find "$ROOT/sources/AlleleSeq2" -iname 'vcf2diploid*.jar' -print -quit | grep -q .; then
    printf 'official_vcf2diploid_jar\tFOUND\n'
  else
    printf 'official_vcf2diploid_jar\tUNAVAILABLE\n'
  fi
  printf 'classification\tUNAVAILABLE_FULL_TOOLCHAIN_EXTERNAL_ONLY\n'
} >"$EVIDENCE/alleleseq-boundary.tsv"
pass alleleseq_boundary "official legacy runtime remains unavailable; no execution credited"

set +e
"$RSCRIPT" --vanilla -e 'quit(status=ifelse(requireNamespace("BaalChIP", quietly=TRUE), 0L, 1L))'
baal_installed=$?
"$RSCRIPT" --vanilla -e 'quit(status=ifelse(requireNamespace("rtracklayer", quietly=TRUE), 0L, 1L))'
rtrack_installed=$?
set -e
test "$baal_installed" -eq 1
test "$rtrack_installed" -eq 1
{
  printf 'BaalChIP_requireNamespace_exit\t%s\n' "$baal_installed"
  printf 'rtracklayer_requireNamespace_exit\t%s\n' "$rtrack_installed"
  printf 'prepared_install_log_sha256\t%s\n' "$(sha256sum "$ROOT/evidence/baalchip-install.log" | awk '{print $1}')"
  printf 'prepared_status_sha256\t%s\n' "$(sha256sum "$ROOT/evidence/baalchip-surface-status.txt" | awk '{print $1}')"
  printf 'observed_compile_failure\tRhtslib hts.c missing lzma.h; bounded retry timed out per retained status\n'
  printf 'classification\tRESOURCE_INFEASIBLE_BOUNDED\n'
} >"$EVIDENCE/baalchip-runtime-boundary.tsv"
pass baalchip_runtime_boundary "packages independently absent; retained bounded install evidence hashed; no model pass claimed"

printf 'ALL_FINAL_REAUDIT_CONTRACTS_PASS\n'
