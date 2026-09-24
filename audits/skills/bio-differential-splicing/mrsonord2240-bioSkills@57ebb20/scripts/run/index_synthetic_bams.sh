#!/usr/bin/env bash
# Index final-pass synthetic BAM inputs for regtools and Shiba.
set -euo pipefail
ROOT=/mnt/openscience/audits/bio-differential-splicing/run/data
SAMTOOLS=/home/sci/.local/bin/micromamba
for folder in sim sim2 sim2b sim2p; do
  [ -d "$ROOT/$folder" ] || continue
  for bam in "$ROOT/$folder"/*.bam; do
    [ -e "$bam" ] || continue
    "$SAMTOOLS" run -n as-core samtools index "$bam"
  done
done
echo "indexed synthetic BAMs"
