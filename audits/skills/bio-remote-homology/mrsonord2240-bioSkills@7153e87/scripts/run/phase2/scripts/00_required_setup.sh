#!/usr/bin/env bash
# Purpose: execute the Skill.md Required Setup verification block and validate its advertised banners.
set -euo pipefail

RUN=/mnt/openscience/audits/bio-remote-homology/run/phase2
OUT="$RUN/outputs/00_required_setup.txt"
{
  hmmsearch -h | head -3
  mmseqs version
  diamond --version
  hhblits -h | head -3
  foldseek 2>&1 | grep -i '^foldseek Version'
  for s in "$RUN"/skill-copy/*.sh; do bash -n "$s"; done
} >"$OUT"
grep -q 'HMMER 3.4' "$OUT"
grep -q '18.8cc5c' "$OUT"
grep -q 'diamond version 2.2.6' "$OUT"
grep -q 'HHblits 3.3.0' "$OUT"
grep -qi '^foldseek Version: 10.941cd33' "$OUT"
echo 'PASS: Required Setup banners and all shipped shell-script syntax checks succeeded.' >>"$OUT"
