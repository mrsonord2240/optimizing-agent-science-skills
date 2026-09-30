#!/bin/bash
RUN=/mnt/openscience/audits/bio-atac-seq-single-cell-atac/initial-audit-20260930
mkdir -p $RUN/out
for s in signac_asis signac_patched snap amulet tabix amulet_numpy_probe archr callpeaks wnn peakvi; do
  ( time bash $RUN/scripts/run_audit.sh $s ) > $RUN/out/$s.log 2>&1 &
done
wait
echo ALLDONE > $RUN/out/ALLDONE
