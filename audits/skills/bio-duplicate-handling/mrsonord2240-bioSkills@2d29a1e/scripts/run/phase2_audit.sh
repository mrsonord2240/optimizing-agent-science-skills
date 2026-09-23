#!/usr/bin/env bash
# Fresh Phase 2 audit runner for bio-duplicate-handling.
# Run through audit-envs/alignment-files/wsl_run.sh so the documented side-tool wrappers are on PATH.
set -euo pipefail

ROOT=/mnt/openscience
SKILL="$ROOT/wt/alignment-files-duplicate-handling/alignment-files/duplicate-handling"
RUN="$ROOT/audits/bio-duplicate-handling/run"
DATA="$ROOT/audit-envs/alignment-files/public-data"
WORK="$RUN/work"
mkdir -p "$WORK"
rm -rf "$WORK"/*

fail() { echo "ASSERT_FAIL: $*" >&2; exit 99; }
eq() { [ "$1" = "$2" ] || fail "expected $2, got $1 ($3)"; }
count() { samtools view -c "$1"; }
dups() { samtools view -c -f 1024 "$1"; }
require_file() { [ -s "$1" ] || fail "missing or empty $1"; }
run_expected_failure() {
  local label=$1; shift
  set +e
  "$@" >"$WORK/$label.out" 2>"$WORK/$label.err"
  local rc=$?
  set -e
  [ "$rc" -ne 0 ] || fail "$label unexpectedly succeeded"
  echo "$label expected_failure_rc=$rc"
}

PLANTED="$DATA/derived/planted_dups.bam"
HUMAN="$DATA/human/test.paired_end.sorted.bam"
UMI="$DATA/human/test.paired_end.umi_unsorted.bam"
RNA="$DATA/human/test.rna.paired_end.sorted.bam"

echo 'INPUT 1 — old canonical workflow / Python regression'
mkdir -p "$WORK/in1"
samtools sort -n -o "$WORK/in1/n.bam" "$PLANTED"
samtools fixmate -m "$WORK/in1/n.bam" "$WORK/in1/f.bam"
samtools sort -o "$WORK/in1/c.bam" "$WORK/in1/f.bam"
samtools markdup "$WORK/in1/c.bam" "$WORK/in1/marked.bam"
samtools index "$WORK/in1/marked.bam"
eq "$(dups "$WORK/in1/marked.bam")" 100 'standard workflow duplicates'
require_file "$WORK/in1/marked.bam.bai"
python "$SKILL/scripts/pysam_markdup.py" "$PLANTED" "$WORK/in1/pysam.bam" | tee "$WORK/in1/pysam.txt"
grep -q 'flagged duplicate: 100' "$WORK/in1/pysam.txt" || fail 'pysam marked truth'
python "$SKILL/scripts/dup_rate.py" "$WORK/in1/pysam.bam" | tee "$WORK/in1/rate.txt"
grep -q 'Rate: 20.00%' "$WORK/in1/rate.txt" || fail 'pysam rate'
eq "$(samtools view -c -F 1024 "$WORK/in1/marked.bam")" 400 'nonduplicate filter count'
picard MarkDuplicates I="$PLANTED" O="$WORK/in1/picard.bam" M="$WORK/in1/picard.metrics.txt" VALIDATION_STRINGENCY=SILENT >"$WORK/in1/picard.out" 2>"$WORK/in1/picard.err"
eq "$(dups "$WORK/in1/picard.bam")" 100 'Picard duplicates'
grep -q 'READ_PAIR_DUPLICATES' "$WORK/in1/picard.metrics.txt" || fail 'Picard metrics'

echo 'INPUT 2 — old piped/example and phase-1 cleanup regression'
mkdir -p "$WORK/in2"
ASSAY=wgs bash "$SKILL/examples/markdup_pipeline.sh" "$PLANTED" "$WORK/in2/out.bam" 2 | tee "$WORK/in2/example.txt"
eq "$(dups "$WORK/in2/out.bam")" 100 'example duplicates'
require_file "$WORK/in2/out.markdup_stats.txt"
run_expected_failure no_assay bash "$SKILL/examples/markdup_pipeline.sh" "$PLANTED" "$WORK/in2/no_assay.bam"
[ ! -e "$WORK/in2/no_assay.bam" ] || fail 'no-assay BAM left behind'
[ ! -e "$WORK/in2/no_assay.markdup_stats.txt" ] || fail 'no-assay stats left behind'
run_expected_failure rna_refusal env ASSAY=wgs bash "$SKILL/examples/markdup_pipeline.sh" "$RNA" "$WORK/in2/rna.bam"
grep -q 'looks like RNA-seq' "$WORK/rna_refusal.err" || fail 'RNA heuristic message'
[ ! -e "$WORK/in2/rna.bam" ] || fail 'RNA refusal BAM left behind'
ALLOW_SPLICED=1 ASSAY=wgs bash "$SKILL/examples/markdup_pipeline.sh" "$RNA" "$WORK/in2/rna_override.bam" 2 >"$WORK/in2/rna_override.txt"
require_file "$WORK/in2/rna_override.bam"

echo 'INPUT 3 — old common-error and pre-marked regression'
mkdir -p "$WORK/in3"
run_expected_failure fixmate_coordinate samtools fixmate "$PLANTED" "$WORK/in3/bad_fixmate.bam"
grep -q 'Coordinate sorted, require grouped/sorted by queryname' "$WORK/fixmate_coordinate.err" || fail 'fixmate error wording'
samtools sort -n -o "$WORK/in3/n.bam" "$PLANTED"
samtools fixmate "$WORK/in3/n.bam" "$WORK/in3/no_ms.bam"
samtools sort -o "$WORK/in3/no_ms_coord.bam" "$WORK/in3/no_ms.bam"
run_expected_failure markdup_no_ms samtools markdup "$WORK/in3/no_ms_coord.bam" "$WORK/in3/no_ms_out.bam"
grep -q 'no ms score tag' "$WORK/markdup_no_ms.err" || fail 'no-ms error wording'
run_expected_failure markdup_queryname samtools markdup "$WORK/in3/n.bam" "$WORK/in3/qn_out.bam"
grep -q 'queryname sorted, must be sorted by coordinate' "$WORK/markdup_queryname.err" || fail 'queryname error wording'
samtools markdup "$WORK/in1/c.bam" "$WORK/in3/first.bam"
samtools markdup "$WORK/in3/first.bam" "$WORK/in3/re_mark.bam"
samtools markdup -c "$WORK/in3/first.bam" "$WORK/in3/re_mark_clear.bam"
eq "$(dups "$WORK/in3/re_mark_clear.bam")" 100 'clear previous duplicate flags'

echo 'INPUT 4 — old UMI / fgbio regression'
mkdir -p "$WORK/in4"
bash "$SKILL/scripts/umi_tools_dedup.sh" bulk-paired "$UMI" "$WORK/in4/bulk.bam" | tee "$WORK/in4/bulk.txt"
eq "$(count "$WORK/in4/bulk.bam")" 5689 'seeded bulk UMI output'
bash "$SKILL/scripts/fgbio_consensus.sh" single "$UMI" "$WORK/in4/single.bam" | tee "$WORK/in4/single.txt"
eq "$(count "$WORK/in4/single.bam")" 5646 'single consensus output'
bash "$SKILL/scripts/fgbio_consensus.sh" duplex "$UMI" "$WORK/in4/duplex.bam" | tee "$WORK/in4/duplex.txt"
eq "$(count "$WORK/in4/duplex.bam")" 4042 'duplex consensus output'
eq "$(samtools view -c -F 4 "$WORK/in4/duplex.bam")" 0 'duplex reads unmapped'
run_expected_failure scrna_no_cb bash "$SKILL/scripts/umi_tools_dedup.sh" scrna "$UMI" "$WORK/in4/no_cb.bam"
grep -q 'no CB:Z: tags' "$WORK/scrna_no_cb.err" || fail 'scRNA guard wording'

echo 'INPUT 5 — old alternative-marker regression'
mkdir -p "$WORK/in5"
micromamba run -n af-dup-extra bammarkduplicates2 I="$PLANTED" O="$WORK/in5/bio.bam" M="$WORK/in5/bio.metrics.txt" >"$WORK/in5/bio.out" 2>"$WORK/in5/bio.err"
eq "$(dups "$WORK/in5/bio.bam")" 100 'biobambam2 duplicates'
sambamba markdup -t 2 "$PLANTED" "$WORK/in5/sambamba.bam" >"$WORK/in5/sambamba.out" 2>"$WORK/in5/sambamba.err"
eq "$(dups "$WORK/in5/sambamba.bam")" 100 'sambamba duplicates'
samtools collate -O -u "$PLANTED" "$WORK/in5/collate" | samtools view -h - | samblaster 2>"$WORK/in5/samblaster.err" | samtools sort -o "$WORK/in5/samblaster.bam"
eq "$(dups "$WORK/in5/samblaster.bam")" 100 'samblaster duplicates'
grep -Eq 'Marked[[:space:]]+50 of[[:space:]]+250' "$WORK/in5/samblaster.err" || fail 'samblaster accounting'

echo 'INPUT 6 — NEW real RNA/assay boundary'
mkdir -p "$WORK/in6"
run_expected_failure declared_rnaseq env ASSAY=rnaseq bash "$SKILL/examples/markdup_pipeline.sh" "$RNA" "$WORK/in6/rna.bam"
grep -q 'wrong tool' "$WORK/declared_rnaseq.err" || fail 'declared RNA refusal'
[ ! -e "$WORK/in6/rna.bam" ] || fail 'declared RNA BAM left behind'
ASSAY=amplicon bash "$SKILL/examples/markdup_pipeline.sh" "$PLANTED" "$WORK/in6/amplicon_label.bam" >"$WORK/in6/amplicon_label.out" 2>"$WORK/in6/amplicon_label.err" || test $? -eq 2
grep -q 'wrong tool' "$WORK/in6/amplicon_label.err" || fail 'amplicon refusal'

echo 'INPUT 7 — NEW documented PacBio command on seeded synthetic HiFi input'
mkdir -p "$WORK/in7"
(cd "$WORK/in7" && python "$RUN/make_hifi.py") | tee "$WORK/in7/generate.txt"
(cd "$WORK/in7" && micromamba run -n af-dup-extra pbmarkdup -j 2 hifi.bam marked.bam)
eq "$(dups "$WORK/in7/marked.bam")" 12 'pbmarkdup planted duplicates'
(cd "$WORK/in7" && micromamba run -n af-dup-extra pbmarkdup --rmdup hifi.bam rm.bam)
eq "$(count "$WORK/in7/rm.bam")" 48 'pbmarkdup removal'

echo 'ALL_ASSERTIONS_PASSED'
