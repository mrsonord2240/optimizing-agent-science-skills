#!/usr/bin/env bash
# Purpose: build fresh edge fixtures and verify validator contracts, including an unreadable CRAM.
# Inputs: public human BAM/CRAM plus generated SAM; Usage: bash 02_fresh_edge_cases.sh
set -uo pipefail

ROOT=/mnt/openscience
SKILL="$ROOT/worktrees/bio-alignment-validation-finalpass/alignment-files/alignment-validation"
PUBLIC="$ROOT/audit-envs/alignment-files/public-data/human"
WORK="$ROOT/audits/bio-alignment-validation/run/finalpass-20260924/data"
OUT="$ROOT/audits/bio-alignment-validation/run/finalpass-20260924/out"
BASE="$PUBLIC/test.paired_end.sorted.bam"

samtools view -h "$BASE" | awk '/^@/ { print; next } { if (n < 50) print; n++ }' > "$WORK/tiny_valid.sam"
samtools view -b -o "$WORK/tiny_valid.bam" "$WORK/tiny_valid.sam"
cat > "$WORK/no_sq_unmapped.sam" <<'EOF'
@HD	VN:1.6	SO:unknown
fresh	4	*	0	0	*	*	0	0	A	I
EOF
samtools view -b -o "$WORK/no_sq_unmapped.bam" "$WORK/no_sq_unmapped.sam"

run_case() {
    local label=$1 bam=$2 expected=$3
    python "$SKILL/examples/validate_alignment.py" "$bam" > "$OUT/${label}.py.out" 2> "$OUT/${label}.py.err"; py_rc=$?
    bash "$SKILL/examples/validate_alignment.sh" "$bam" > "$OUT/${label}.sh.out" 2> "$OUT/${label}.sh.err"; sh_rc=$?
    printf '%s py=%s sh=%s expected=%s\n' "$label" "$py_rc" "$sh_rc" "$expected" | tee -a "$OUT/fresh-edge-cases.summary"
    test "$py_rc" -eq "$expected"
    test "$sh_rc" -eq "$expected"
}

: > "$OUT/fresh-edge-cases.summary"
run_case tiny_valid "$WORK/tiny_valid.bam" 0
grep -q 'Too few primary reads to grade pairing or strand balance (n<100)' "$OUT/tiny_valid.py.out"
grep -q 'Too few primary reads to grade pairing or strand balance (n<100)' "$OUT/tiny_valid.sh.out"
run_case no_sq_unmapped "$WORK/no_sq_unmapped.bam" 2
grep -q 'no @SQ header' "$OUT/no_sq_unmapped.py.err"
grep -q 'fails samtools quickcheck' "$OUT/no_sq_unmapped.sh.err"

export REF_PATH=/nonexistent_ref_dir
run_case unreadable_cram "$PUBLIC/test.paired_end.sorted.cram" 2
grep -q 'cannot be decoded completely' "$OUT/unreadable_cram.sh.err"
unset REF_PATH
