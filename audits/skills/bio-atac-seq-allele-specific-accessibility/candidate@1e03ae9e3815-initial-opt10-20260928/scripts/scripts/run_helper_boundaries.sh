#!/bin/bash
set -u

source /mnt/openscience/audit-envs/bio-atac-seq-allele-specific-accessibility/wsl_env.sh

AUDIT=/mnt/openscience/audits/bio-atac-seq-allele-specific-accessibility/initial-opt10-20260928
RUN="$AUDIT/runs/helper-boundaries"
EVIDENCE="$AUDIT/evidence/helper-boundaries.txt"
HELPER="$ASA_CANDIDATE/scripts/aggregate_peak_ase.py"
PY=/home/sci/micromamba/envs/atac-core/bin/python

rm -rf "$RUN"
mkdir -p "$RUN" "$(dirname "$EVIDENCE")"
: > "$EVIDENCE"

run_case() {
  local name=$1
  local counts=$2
  local peaks=$3
  local out="$RUN/$name.tsv"
  set +e
  "$PY" "$HELPER" --ase-counts "$counts" --peaks "$peaks" --output "$out" \
    > "$RUN/$name.stdout" 2> "$RUN/$name.stderr"
  local rc=$?
  set -e
  local rows=0
  if test -f "$out"; then
    rows=$(awk 'NR>1 {n++} END {print n+0}' "$out")
  fi
  printf '%s\trc=%s\toutput=%s\trows=%s\n' \
    "$name" "$rc" "$(test -f "$out" && echo yes || echo no)" "$rows" >> "$EVIDENCE"
  if test -f "$out"; then
    "$PY" - "$name" "$out" >> "$EVIDENCE" <<'PY'
import sys
import pandas as pd

name, path = sys.argv[1:]
df = pd.read_csv(path, sep="\t")
print(f"{name}\tcolumns={','.join(df.columns)}")
if len(df):
    row = df.iloc[0]
    print(
        f"{name}\tpeak={row.iloc[0]}\tref_frac={row['ref_frac']:.6f}"
        f"\tsnp_count={int(row['snp_count'])}\tadj_p={row['adj_p']:.8g}"
    )
PY
  fi
  if test -s "$RUN/$name.stderr"; then
    printf '%s\tstderr_tail=%s\n' "$name" \
      "$(tail -2 "$RUN/$name.stderr" | tr '\n' ' ')" >> "$EVIDENCE"
  fi
}

run_case same_reference_direction "$AUDIT/inputs/counts_same_reference.tsv" "$AUDIT/inputs/peaks.bed"
run_case opposite_reference_direction "$AUDIT/inputs/counts_opposite_reference.tsv" "$AUDIT/inputs/peaks.bed"
run_case no_peak_overlap "$AUDIT/inputs/counts_same_reference.tsv" "$AUDIT/inputs/no_overlap.bed"
run_case all_below_depth "$AUDIT/inputs/counts_below_depth.tsv" "$AUDIT/inputs/peaks.bed"
run_case bed4_named "$AUDIT/inputs/counts_same_reference.tsv" "$AUDIT/inputs/peaks_named.bed"

cat "$EVIDENCE"
