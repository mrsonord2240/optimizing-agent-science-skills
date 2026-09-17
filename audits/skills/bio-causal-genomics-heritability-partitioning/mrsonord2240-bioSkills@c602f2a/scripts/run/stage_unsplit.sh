#!/bin/bash
# Stage gzipped (unsplit) LD score files for --h2/--rg/liability-scale h2.
# Same gzip necessity as stage_cts.sh, but no chromosome split needed for
# these three flags (they accept a single-file --ref-ld/--w-ld prefix).
set -euo pipefail
ROOT=/mnt/openscience/audits/bio-causal-genomics-heritability-partitioning/run
LDSC=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools/ldsc-cbiit-reaudit-fresh
STAGE=$ROOT/stage_unsplit
mkdir -p "$STAGE"
cp "$LDSC/test/simulate_test/ldscore/oneld_onefile.l2.ldscore" "$LDSC/test/simulate_test/ldscore/oneld_onefile.l2.M_5_50" "$STAGE/"
cp "$LDSC/test/simulate_test/ldscore/twold_onefile.l2.ldscore" "$LDSC/test/simulate_test/ldscore/twold_onefile.l2.M_5_50" "$STAGE/"
cp "$LDSC/test/simulate_test/ldscore/w.l2.ldscore" "$STAGE/"
gzip -f "$STAGE"/*.l2.ldscore
ls -la "$STAGE"
