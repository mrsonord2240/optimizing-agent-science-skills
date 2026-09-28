#!/bin/bash
set -u

source /mnt/openscience/audit-envs/bio-atac-seq-allele-specific-accessibility/wsl_env.sh

AUDIT=/mnt/openscience/audits/bio-atac-seq-allele-specific-accessibility/initial-opt10-20260928
RUN="$AUDIT/runs/rasqual-candidate"
EVIDENCE="$AUDIT/evidence/rasqual-candidate.txt"

rm -rf "$RUN"
mkdir -p "$RUN" "$(dirname "$EVIDENCE")"
: > "$EVIDENCE"

cd "$RASQUAL_SRC"

# Exact semantic shape documented by the candidate: one feature interval is
# supplied to -s/-e while -m claims 62 feature SNPs.
set +e
tabix data/chr11.gz 11:1816875-2824279 | \
  rasqual -y data/Y.bin -k data/K.bin -n 24 -j 1 -l 378 -m 62 \
    -s 2316875 -e 2324279 -f C11orf21 \
    > "$RUN/candidate-shape.tsv" 2> "$RUN/candidate-shape.stderr"
candidate_rc=$?
set -e
candidate_rows=$(awk 'NF {n++} END {print n+0}' "$RUN/candidate-shape.tsv")
printf 'candidate_documented_shape_rc=%s\n' "$candidate_rc" >> "$EVIDENCE"
printf 'candidate_documented_shape_rows=%s\n' "$candidate_rows" >> "$EVIDENCE"
printf 'candidate_documented_shape_stderr=%s\n' "$(tr '\n' ' ' < "$RUN/candidate-shape.stderr")" >> "$EVIDENCE"

# Public bundled positive control uses all 62 feature-SNP positions, as in the
# prepared primary smoke.
tabix data/chr11.gz 11:2315000-2340000 | \
  rasqual -y data/Y.bin -k data/K.bin -n 24 -j 1 -l 378 -m 62 \
    -s 2316875,2320655,2321750,2321914,2324112 \
    -e 2319151,2320937,2321843,2323290,2324279 \
    -t -f C11orf21 -z \
    > "$RUN/control.tsv" 2> "$RUN/control.stderr"
control_rows=$(awk 'NF {n++} END {print n+0}' "$RUN/control.tsv")
control_chi_square=$(awk 'NF {print $11; exit}' "$RUN/control.tsv")
printf 'public_control_rc=0\n' >> "$EVIDENCE"
printf 'public_control_rows=%s\n' "$control_rows" >> "$EVIDENCE"
printf 'public_control_chi_square=%s\n' "$control_chi_square" >> "$EVIDENCE"

cat "$EVIDENCE"
