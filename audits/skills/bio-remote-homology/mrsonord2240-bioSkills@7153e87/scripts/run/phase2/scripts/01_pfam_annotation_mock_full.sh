#!/usr/bin/env bash
# Purpose: run the shipped full Pfam script against the bundled real Pkinase model as a reduced-db substitute.
# The full Pfam-A download remains intentionally blocked because it is about 1.7 GB compressed.
set -euo pipefail

RUN=/mnt/openscience/audits/bio-remote-homology/run/phase2
WORK="$RUN/work/pfam_hit"
OUT="$RUN/outputs/01_pfam_annotation_mock_full.txt"
rm -rf "$WORK"
mkdir -p "$WORK/db"
cp "$RUN/skill-copy/data/PF00069.hmm" "$WORK/db/Pfam-A.hmm"
hmmpress "$WORK/db/Pfam-A.hmm" >"$WORK/hmmpress.txt"
(
  cd "$WORK"
  bash "$RUN/skill-copy/pfam_annotation.sh" "$RUN/skill-copy/data/P17612.fasta" "$WORK/db"
) >"$OUT"
grep -q 'Pkinase' "$OUT"
awk -F '\t' '$2 == "Pkinase" && $4 < 1e-70 && $5 > 200 {ok=1} END {exit !ok}' "$OUT"
echo 'PASS: shipped full script reports Pkinase with a low full-sequence E-value and high full score.' >>"$OUT"
