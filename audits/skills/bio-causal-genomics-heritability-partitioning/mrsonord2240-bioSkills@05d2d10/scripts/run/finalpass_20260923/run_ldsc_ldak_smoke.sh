#!/usr/bin/env bash
# Fresh Phase 2 regression runner for bio-causal-genomics-heritability-partitioning.
# Inputs: network access to CBIIT/ldsc, the existing ldsc-py39 micromamba env, and LDAK 6.3.
# Usage: bash run_ldsc_ldak_smoke.sh
set -euo pipefail

RUN=/mnt/openscience/audits/bio-causal-genomics-heritability-partitioning/run/finalpass_20260923
OUT="$RUN/out"
LDSC="$RUN/ldsc-cbiit-clean"
LDAK=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools/ldak-reaudit/ldak6.3.linux
PY="micromamba run -n ldsc-py39 python"
mkdir -p "$OUT"

if [[ ! -d "$LDSC/.git" ]]; then
  git clone https://github.com/CBIIT/ldsc.git "$LDSC"
fi
git -C "$LDSC" checkout --detach 1f09cf0c5e61a38a281016fefcc1e0583cc78402
git -C "$LDSC" config core.autocrlf false
git -C "$LDSC" reset --hard 1f09cf0c5e61a38a281016fefcc1e0583cc78402
git -C "$LDSC" status --porcelain

STAGE="$RUN/stage"
rm -rf "$STAGE"
mkdir -p "$STAGE"
cp -r "$LDSC/test/simulate_test/ldscore" "$LDSC/test/simulate_test/sumstats" "$STAGE/"
cp "$STAGE/ldscore/w.l2.ldscore" "$STAGE/ldscore/w1.l2.ldscore"
cp "$STAGE/ldscore/w.l2.ldscore" "$STAGE/ldscore/w2.l2.ldscore"
gzip "$STAGE"/ldscore/*.l2.ldscore
printf 'CellTypeA\tldscore/twold_firstfile\nCellTypeB\tldscore/twold_secondfile\n' > "$STAGE/test.ldcts"

echo '=== Input 1: munge and total h2 ==='
$PY "$LDSC/munge_sumstats.py" --sumstats "$LDSC/test/munge_test/sumstats" --merge-alleles "$LDSC/test/munge_test/merge_alleles" --N 6702 --signed-sumstats OR,1 --out "$OUT/input1_munge"
$PY "$LDSC/ldsc.py" --h2 "$STAGE/sumstats/0" --ref-ld "$STAGE/ldscore/oneld_onefile1" --w-ld "$STAGE/ldscore/w1" --out "$OUT/input1_h2"
grep -E 'Total Observed scale h2|Intercept|Ratio|Mean Chi' "$OUT/input1_h2.log"

echo '=== Input 2: partitioned h2 ==='
$PY "$LDSC/ldsc.py" --h2 "$STAGE/sumstats/0" --ref-ld "$STAGE/ldscore/twold_onefile1" --w-ld "$STAGE/ldscore/w1" --print-coefficients --out "$OUT/input2_partitioned"
grep -E 'Total Observed scale h2|Categories|Enrichment' "$OUT/input2_partitioned.log"

echo '=== Input 3: cross-trait rg ==='
$PY "$LDSC/ldsc.py" --rg "$STAGE/sumstats/0,$STAGE/sumstats/1" --ref-ld "$STAGE/ldscore/twold_onefile1" --w-ld "$STAGE/ldscore/w1" --out "$OUT/input3_rg"
grep -E 'Genetic Correlation:|Z-score:|^P:|gcov_int' "$OUT/input3_rg.log"

echo '=== Input 4: liability-scale h2 bounds guard ==='
$PY "$LDSC/ldsc.py" --h2 "$STAGE/sumstats/0" --ref-ld "$STAGE/ldscore/oneld_onefile1" --w-ld "$STAGE/ldscore/w1" --samp-prev 0.08 --pop-prev 0.01 --out "$OUT/input4_liability"
grep -E 'Total Liability scale h2|Intercept|Ratio' "$OUT/input4_liability.log"

echo '=== Input 5: h2-cts fails unpatched, then passes patched ==='
set +e
( cd "$STAGE" && $PY "$LDSC/ldsc.py" --h2-cts sumstats/0 --ref-ld-chr ldscore/oneld_onefile --ref-ld-chr-cts test.ldcts --w-ld-chr ldscore/w --out "$OUT/input5_cts_unpatched" ) > "$OUT/input5_cts_unpatched.stdout" 2>&1
UNPATCHED_RC=$?
set -e
printf 'unpatched_exit=%s\n' "$UNPATCHED_RC" | tee "$OUT/input5_cts_unpatched.status"
grep -F 'cannot do slice indexing' "$OUT/input5_cts_unpatched.stdout"
sed -i 's/\.loc\[:,1:\]/.iloc[:,1:]/' "$LDSC/ldscore/sumstats.py"
( cd "$STAGE" && $PY "$LDSC/ldsc.py" --h2-cts sumstats/0 --ref-ld-chr ldscore/oneld_onefile --ref-ld-chr-cts test.ldcts --w-ld-chr ldscore/w --out "$OUT/input5_cts_patched" )
cat "$OUT/input5_cts_patched.cell_type_results.txt"

echo '=== Input 8: LDAK tagging and SumHer ==='
( cd "$OUT" && "$LDAK" --calc-tagging input8_tagging --bfile "$LDSC/test/plink_test/plink" --power -.25 --window-kb 1000 )
printf 'Predictor A1 A2 n Z\nrs_1 0 1 1000 0.3\nrs_2 2 1 1000 -0.2\nrs_3 0 2 1000 0.5\nrs_4 1 2 1000 6.0\nrs_5 1 2 1000 -0.4\nrs_6 2 1 1000 0.1\nrs_7 2 1 1000 0.2\n' > "$OUT/input8_sumstats.txt"
( cd "$OUT" && "$LDAK" --sum-hers input8_sumher --summary input8_sumstats.txt --tagfile input8_tagging.tagging --check-sums NO )
grep -E 'Her_All|Heritability' "$OUT/input8_sumher.hers"

echo '=== Input 9: current shipped smoke script ==='
cp /mnt/openscience/wt/causal-genomics-heritability-partitioning/causal-genomics/heritability-partitioning/examples/smoke_test_ldsc.sh "$RUN/input9_smoke_test_ldsc.sh"
LDSC_DIR="$LDSC" micromamba run -n ldsc-py39 bash "$RUN/input9_smoke_test_ldsc.sh" > "$OUT/input9_smoke.stdout" 2>&1
grep -E 'Total Observed scale h2|Genetic Correlation|All three LDSC entry points ran' "$OUT/input9_smoke.stdout"

echo 'FRESH_LDSC_LDAK_SMOKE_COMPLETE'
