#!/bin/bash
set -euo pipefail

source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
ROOT=/mnt/openscience/worktrees/bio-alignment-amplicon-clipping-final/alignment-files/alignment-amplicon-clipping
EX=$ROOT/examples/ampliconclip_workflow.sh
CHECK=$ROOT/examples/check_primer_residual.py
SC=$AFDATA/sarscov2
ART=$SC/sars-cov-2_v5.3.2.nanopore.bam
V5=$SC/v5.3.2.primer.bed
V3=$SC/v3.0.0.primer.bed
REF=$SC/MN908947.3.fasta
W=$(mktemp -d /tmp/amplicon-final-pass.XXXXXX)
trap 'rm -rf "$W"' EXIT

expect_success() {
    local name=$1 bed=$2
    bash "$EX" "$ART" "$bed" "$REF" "$W/$name.bam" >"$W/$name.log" 2>&1
    test -s "$W/$name.bam"
    test -s "$W/$name.bam.bai"
    grep -q '^Clipped BAM:' "$W/$name.log"
    echo "PASS success: $name"
}

expect_failure() {
    local name=$1 bed=$2 pattern=$3
    if bash "$EX" "$ART" "$bed" "$REF" "$W/$name.bam" >"$W/$name.log" 2>&1; then
        echo "unexpected success: $name" >&2
        return 1
    fi
    test ! -e "$W/$name.bam"
    test ! -e "$W/$name.bam.bai"
    grep -Eqi "$pattern" "$W/$name.log"
    echo "PASS failure: $name"
}

expect_success correct_v5 "$V5"

awk 'BEGIN{FS=OFS="\t"} {$2=$2+9; $3=$3+9; print}' "$V5" >"$W/shift9.bed"
expect_failure shifted9 "$W/shift9.bed" 'NOT CLIPPED share.*exceeds'
expect_failure wrong_v3 "$V3" 'NOT CLIPPED share.*exceeds'

{
    echo 'track name="ARTIC v5"'
    awk 'BEGIN{OFS=" "} {$1=$1; print}' "$V5"
} >"$W/header-spaces.bed"
expect_success header_spaces "$W/header-spaces.bed"

printf 'MN908947.3 29000 29010 off_target 0 +\n' >"$W/sparse.bed"
expect_failure sparse "$W/sparse.bed" 'clipped nothing|NOT CLIPPED share.*exceeds'

printf 'MN908947.3 0 20 bad 0\n' >"$W/five.bed"
set +e
python3 "$CHECK" "$ART" "$W/five.bed" >"$W/check-five.log" 2>&1
rc_five=$?
python3 "$CHECK" "$W/missing.bam" "$V5" >"$W/check-missing.log" 2>&1
rc_missing=$?
set -e
test "$rc_five" -eq 2
test "$rc_missing" -eq 2
grep -q '^bad input:' "$W/check-five.log"
grep -q '^bad input:' "$W/check-missing.log"
echo 'PASS checker invalid inputs'

touch "$W/existing.bam"
set +e
bash "$EX" "$ART" "$V5" "$REF" "$W/existing.bam" >"$W/existing.log" 2>&1
rc_existing=$?
set -e
test "$rc_existing" -ne 0
grep -q 'output already exists' "$W/existing.log"
echo 'PASS existing output guard'

echo 'FINAL PASS COMPLETE'
