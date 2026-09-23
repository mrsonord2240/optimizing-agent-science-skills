#!/usr/bin/env bash
# Purpose: regression-test the shipped Pfam script's explicit zero-domain result handling with a reduced local Pfam fixture.
set -euo pipefail

RUN=/mnt/openscience/audits/bio-remote-homology/run/phase2
WORK="$RUN/work/pfam_no_hit"
OUT="$RUN/outputs/09_pfam_no_hit.txt"
rm -rf "$WORK"
mkdir -p "$WORK/db"
cp "$RUN/skill-copy/data/PF00069.hmm" "$WORK/db/Pfam-A.hmm"
hmmpress "$WORK/db/Pfam-A.hmm" >"$WORK/hmmpress.txt"
(
  cd "$WORK"
  bash "$RUN/skill-copy/pfam_annotation.sh" "$RUN/data/no_hit.fa" "$WORK/db"
) >"$OUT"
grep -q 'No Pfam-A domains found above the gathering threshold.' "$OUT"
echo 'PASS: zero-hit query exits successfully with the documented explicit message.' >>"$OUT"
