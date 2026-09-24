#!/usr/bin/env bash
# Purpose: prove CrosscheckFingerprints does not collapse same-RG/PU samples when grouped by file.
# Inputs: archived synthetic 60-site fingerprint fixtures; Usage: bash 03_crosscheck_by_file.sh
set -uo pipefail

ROOT=/mnt/openscience
DATA="$ROOT/audits/_pre-fix-20260924/bio-alignment-validation/run/data/fp"
OUT="$ROOT/audits/bio-alignment-validation/run/finalpass-20260924/out/crosscheck-by-file.metrics"
picard CrosscheckFingerprints \
    I="$DATA/A_sameSM_as_B.bam" I="$DATA/B.bam" \
    HAPLOTYPE_MAP="$DATA/hap.txt" CROSSCHECK_BY=FILE \
    LOD_THRESHOLD=-5 EXPECT_ALL_GROUPS_TO_MATCH=true OUTPUT="$OUT" \
    > "${OUT}.stdout" 2> "${OUT}.stderr"
rc=$?
printf 'crosscheck_by_file_rc=%s\n' "$rc" | tee "${OUT}.summary"
test "$rc" -eq 1
grep -Eq 'UNEXPECTED_MISMATCH|LOD_SCORE' "$OUT"
