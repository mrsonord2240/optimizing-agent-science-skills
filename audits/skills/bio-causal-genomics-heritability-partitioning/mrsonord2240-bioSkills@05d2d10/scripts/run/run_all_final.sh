#!/bin/bash
# Final consolidated regression + new-input run for the re-audit of
# bio-causal-genomics-heritability-partitioning, against a FRESH clone of
# CBIIT/ldsc (commit 1f09cf0c) installed exactly per SKILL.md's "Tool Install
# Notes", using the pre-existing micromamba env ldsc-py39 (WSL science seat).
set -uo pipefail

RUN=/mnt/openscience/audits/bio-causal-genomics-heritability-partitioning/run
LDSC=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools/ldsc-cbiit-reaudit-fresh
LDAK=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools/ldak-reaudit
OUT=$RUN/out
STAGE_UNSPLIT=$RUN/stage_unsplit
STAGE_CTS=$RUN/stage_cts
PY="micromamba run -n ldsc-py39 python"
mkdir -p "$OUT"

sec() { echo; echo "===== $1 ====="; }

# ---------------------------------------------------------------------------
# Regression Input 1a: munge_sumstats.py
# ---------------------------------------------------------------------------
sec "Input 1a: munge_sumstats.py"
$PY "$LDSC/munge_sumstats.py" \
  --sumstats "$LDSC/test/munge_test/sumstats" \
  --merge-alleles "$LDSC/test/munge_test/merge_alleles" \
  --N 6702 --signed-sumstats OR,1 \
  --out "$OUT/input1_munge" 2>&1 | tail -20

# ---------------------------------------------------------------------------
# Regression Input 1: --h2 total heritability (UNMODIFIED clone)
# ---------------------------------------------------------------------------
sec "Input 1: --h2 total heritability (UNMODIFIED clone, zero patches)"
$PY "$LDSC/ldsc.py" --h2 "$LDSC/test/simulate_test/sumstats/0" \
  --ref-ld "$STAGE_UNSPLIT/oneld_onefile" \
  --w-ld "$STAGE_UNSPLIT/w" \
  --out "$OUT/input1_h2" 2>&1 | tail -15
grep -E "Total Observed scale h2|Intercept|Ratio|Lambda|Mean Chi" "$OUT/input1_h2.log"

# ---------------------------------------------------------------------------
# Regression Input 2: partitioned h2 (UNMODIFIED clone)
# ---------------------------------------------------------------------------
sec "Input 2: partitioned h2 across 2 categories (UNMODIFIED clone)"
$PY "$LDSC/ldsc.py" --h2 "$LDSC/test/simulate_test/sumstats/0" \
  --ref-ld "$STAGE_UNSPLIT/twold_onefile" \
  --w-ld "$STAGE_UNSPLIT/w" \
  --print-coefficients \
  --out "$OUT/input2_partitioned" 2>&1 | tail -15
grep -E "Categories|Observed scale h2|Enrichment|Coefficients" "$OUT/input2_partitioned.log"

# ---------------------------------------------------------------------------
# Regression Input 3: cross-trait rg (UNMODIFIED clone, no numpy downgrade)
# ---------------------------------------------------------------------------
sec "Input 3: cross-trait rg (UNMODIFIED clone)"
$PY "$LDSC/ldsc.py" --rg "$LDSC/test/simulate_test/sumstats/0,$LDSC/test/simulate_test/sumstats/1" \
  --ref-ld "$STAGE_UNSPLIT/twold_onefile" \
  --w-ld "$STAGE_UNSPLIT/w" \
  --out "$OUT/input3_rg" 2>&1 | tail -15
grep -E "Genetic Correlation:|Z-score:|^P:|gcov_int" "$OUT/input3_rg.log"

# ---------------------------------------------------------------------------
# Regression Input 4: liability-scale h2 (UNMODIFIED clone)
# ---------------------------------------------------------------------------
sec "Input 4: liability-scale h2 (UNMODIFIED clone)"
$PY "$LDSC/ldsc.py" --h2 "$LDSC/test/simulate_test/sumstats/0" \
  --ref-ld "$STAGE_UNSPLIT/oneld_onefile" \
  --w-ld "$STAGE_UNSPLIT/w" \
  --samp-prev 0.08 --pop-prev 0.01 \
  --out "$OUT/input4_liability" 2>&1 | tail -15
grep -E "Total Liability scale h2|Intercept|Ratio" "$OUT/input4_liability.log"

# ---------------------------------------------------------------------------
# Regression Input 5: --h2-cts, before and after the documented one-line patch
# ---------------------------------------------------------------------------
sec "Input 5a: --h2-cts BEFORE the documented patch (expect the documented failure)"
( cd "$STAGE_CTS" && $PY "$LDSC/ldsc.py" --h2-cts "$LDSC/test/simulate_test/sumstats/0" \
  --ref-ld-chr "ldscore/oneld_onefile" \
  --ref-ld-chr-cts "test.ldcts" \
  --w-ld-chr "ldscore/w" \
  --out "$OUT/input5_cts_prepatch" ) 2>&1 | tail -20

echo
echo "Patch status in this clone (idempotent check):"
grep -n "iloc\[:,1:\]\|loc\[:,1:\]" "$LDSC/ldscore/sumstats.py"

sec "Input 5: --h2-cts AFTER the documented one-line patch"
( cd "$STAGE_CTS" && $PY "$LDSC/ldsc.py" --h2-cts "$LDSC/test/simulate_test/sumstats/0" \
  --ref-ld-chr "ldscore/oneld_onefile" \
  --ref-ld-chr-cts "test.ldcts" \
  --w-ld-chr "ldscore/w" \
  --out "$OUT/input5_cts_postpatch" ) 2>&1 | tail -20
echo "--- cell_type_results.txt ---"
cat "$OUT/input5_cts_postpatch.cell_type_results.txt"

# ---------------------------------------------------------------------------
# New Input 8: LDAK real execution (Tool Install Notes' LDAK section)
# ---------------------------------------------------------------------------
sec "New Input 8a: LDAK --calc-tagging (real execution against the clone's plink_test fixtures)"
( cd "$OUT" && "$LDAK/ldak6.3.linux" --calc-tagging test_tagging \
  --bfile "$LDSC/test/plink_test/plink" --power -.25 --window-kb 1000 ) 2>&1 | tail -20

sec "New Input 8b: LDAK --sum-hers (real execution, synthetic sumstats, auditor-authored)"
( cd "$OUT" && "$LDAK/ldak6.3.linux" --sum-hers test_sumher \
  --summary ldak_sumstats.txt --tagfile test_tagging.tagging --check-sums NO ) 2>&1 | tail -20
echo "--- test_sumher.hers ---"
cat "$OUT/test_sumher.hers"

# ---------------------------------------------------------------------------
# New Input 9: examples/smoke_test_ldsc.sh as a user would actually run it
# ---------------------------------------------------------------------------
sec "New Input 9a: smoke_test_ldsc.sh as CHECKED OUT on Windows (CRLF) via WSL bash"
LDSC_DIR="$LDSC" micromamba run -n ldsc-py39 bash "$RUN/smoke_test_ldsc_CRLF.sh"
echo "CRLF EXIT CODE: $?"

sec "New Input 9b: smoke_test_ldsc.sh from the git-COMMITTED bytes (LF)"
LDSC_DIR="$LDSC" micromamba run -n ldsc-py39 bash "$RUN/smoke_test_ldsc_LF.sh"
echo "LF EXIT CODE: $?"

echo
echo "ALL INPUTS COMPLETE"
