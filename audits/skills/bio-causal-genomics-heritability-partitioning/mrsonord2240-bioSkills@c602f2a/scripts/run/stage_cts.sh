#!/bin/bash
# Stage chromosome-split, gzipped LD score files for --h2-cts.
# ldscore() in ldscore/parse.py hardcodes the '.l2.ldscore.gz' suffix, so the
# clone's own unsplit test/simulate_test fixtures must be gzipped before use;
# every real reference bundle (eur_w_ld_chr, baselineLD_v2.2, etc.) already
# ships pre-gzipped, so this staging step is a toy-fixture-only necessity.
set -euo pipefail
RUN=/mnt/openscience/audits/bio-causal-genomics-heritability-partitioning/run
LDSC=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools/ldsc-cbiit-reaudit-fresh
STAGE=$RUN/stage_cts

rm -rf "$STAGE"
mkdir -p "$STAGE/ldscore"
for f in oneld_onefile1 oneld_onefile2 twold_firstfile1 twold_firstfile2 twold_secondfile1 twold_secondfile2; do
  cp "$LDSC/test/simulate_test/ldscore/$f.l2.ldscore" "$LDSC/test/simulate_test/ldscore/$f.l2.M_5_50" "$STAGE/ldscore/"
done
# No pre-split weight file ships in the clone; split the single w file into w1/w2.
cp "$LDSC/test/simulate_test/ldscore/w.l2.ldscore" "$STAGE/ldscore/w1.l2.ldscore"
cp "$LDSC/test/simulate_test/ldscore/w.l2.ldscore" "$STAGE/ldscore/w2.l2.ldscore"
gzip -f "$STAGE"/ldscore/*.l2.ldscore
printf 'CellTypeA\tldscore/twold_firstfile\nCellTypeB\tldscore/twold_secondfile\n' > "$STAGE/test.ldcts"
ls -la "$STAGE/ldscore"
