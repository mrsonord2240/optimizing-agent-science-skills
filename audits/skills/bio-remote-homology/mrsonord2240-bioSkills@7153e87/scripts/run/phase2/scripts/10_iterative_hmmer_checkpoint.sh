#!/usr/bin/env bash
# Purpose: regression-test the fixed --chkhmm prefix and dynamic highest-round checkpoint selection in Skill.md.
set -euo pipefail

RUN=/mnt/openscience/audits/bio-remote-homology/run/phase2
WORK="$RUN/work/iterative_hmmer_checkpoint"
OUT="$RUN/outputs/10_iterative_hmmer_checkpoint.txt"
QUERY="$RUN/skill-copy/data/P17612.fasta"
TARGET=/mnt/openscience/audit-envs/database-access/public-data/local-blast/swissprot_sample.fasta
rm -rf "$WORK"
mkdir -p "$WORK"
(
  cd "$WORK"
  jackhmmer -N 3 --chkhmm iter --tblout hits.tbl "$QUERY" "$TARGET"
  hmmsearch "$(ls iter-*.hmm | sort -V | tail -1)" "$TARGET" > hits.txt
) >"$OUT" 2>&1
test -f "$WORK/iter-2.hmm"
grep -q 'Q197B6' "$WORK/hits.txt"
printf 'checkpoint_files=\n' >>"$OUT"
ls "$WORK"/iter-*.hmm >>"$OUT"
echo 'PASS: HMMER wrote iter-2.hmm and the documented glob selected it for an HMMER hit on Q197B6.' >>"$OUT"
