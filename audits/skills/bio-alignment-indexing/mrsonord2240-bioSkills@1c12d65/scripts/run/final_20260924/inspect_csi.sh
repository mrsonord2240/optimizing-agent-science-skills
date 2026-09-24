#!/usr/bin/env bash
set -euo pipefail
d=/mnt/openscience/audits/bio-alignment-indexing/run/final_20260924/work/inspect
rm -rf "$d"
mkdir -p "$d"
cp /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam "$d/sample.bam"
samtools index -c -m 12 "$d/sample.bam"
od -Ax -tx1 -N32 "$d/sample.bam.csi"
od -An -j4 -N4 -tu4 "$d/sample.bam.csi"
od -An -j8 -N4 -tu4 "$d/sample.bam.csi"
