#!/usr/bin/env bash
# Purpose: rerun both shipped validators over every BAM archived from the 2026-09-20 re-audit.
# Inputs: the archived synthetic and fingerprint BAM fixtures; Usage: bash 01_regression_all_archived.sh
set -uo pipefail

ROOT=/mnt/openscience
SKILL="$ROOT/worktrees/bio-alignment-validation-finalpass/alignment-files/alignment-validation"
DATA="$ROOT/audits/_pre-fix-20260924/bio-alignment-validation/run/data"
OUT="$ROOT/audits/bio-alignment-validation/run/finalpass-20260924/out"
SUMMARY="$OUT/archived-validator-regression.tsv"

printf 'fixture\tvalidator\trc\tstatus\n' > "$SUMMARY"
bad=0
count=0
while IFS= read -r bam; do
    relative=${bam#"$DATA"/}
    safe=$(printf '%s' "$relative" | tr '/.' '__')
    for validator in python shell; do
        if [ "$validator" = python ]; then
            python "$SKILL/examples/validate_alignment.py" "$bam" > "$OUT/${safe}.py.out" 2> "$OUT/${safe}.py.err"
        else
            bash "$SKILL/examples/validate_alignment.sh" "$bam" > "$OUT/${safe}.sh.out" 2> "$OUT/${safe}.sh.err"
        fi
        rc=$?
        count=$((count + 1))
        case "$rc" in
            0|1|2) status=contract-ok ;;
            *) status=unexpected; bad=1 ;;
        esac
        if [ "$validator" = python ] && grep -q 'Traceback' "$OUT/${safe}.py.err"; then
            status=traceback
            bad=1
        fi
        printf '%s\t%s\t%s\t%s\n' "$relative" "$validator" "$rc" "$status" >> "$SUMMARY"
    done
done < <(find "$DATA" -type f -name '*.bam' -print | sort)

printf 'archived_bams=%s validator_runs=%s unexpected=%s\n' "$((count / 2))" "$count" "$bad" | tee "$OUT/archived-validator-regression.summary"
test "$bad" -eq 0
