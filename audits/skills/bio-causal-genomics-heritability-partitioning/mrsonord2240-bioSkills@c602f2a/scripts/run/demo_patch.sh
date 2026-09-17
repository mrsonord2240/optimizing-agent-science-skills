#!/bin/bash
set -uo pipefail
LDSC=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools/ldsc-cbiit-reaudit-fresh
STAGE_CTS=/mnt/openscience/audits/bio-causal-genomics-heritability-partitioning/run/stage_cts
OUT=/mnt/openscience/audits/bio-causal-genomics-heritability-partitioning/run/out
PY="micromamba run -n ldsc-py39 python"

echo "Current state of the target line:"
grep -n "iloc\[:,1:\]\|loc\[:,1:\]" "$LDSC/ldscore/sumstats.py"

echo
echo "===== Reverting to the UNPATCHED (upstream) line to demonstrate the real, documented failure ====="
sed -i 's/\.iloc\[:,1:\]/.loc[:,1:]/' "$LDSC/ldscore/sumstats.py"
grep -n "iloc\[:,1:\]\|loc\[:,1:\]" "$LDSC/ldscore/sumstats.py"

echo
echo "===== Input 5a: --h2-cts on the UNPATCHED clone (genuine failure, not stale evidence) ====="
( cd "$STAGE_CTS" && $PY "$LDSC/ldsc.py" --h2-cts "$LDSC/test/simulate_test/sumstats/0" \
  --ref-ld-chr "ldscore/oneld_onefile" \
  --ref-ld-chr-cts "test.ldcts" \
  --w-ld-chr "ldscore/w" \
  --out "$OUT/input5_cts_prepatch_genuine" ) 2>&1 | tail -25
echo "EXIT CODE: $?"

echo
echo "===== Re-applying the documented one-line patch ====="
sed -i 's/\.loc\[:,1:\]/.iloc[:,1:]/' "$LDSC/ldscore/sumstats.py"
grep -n "iloc\[:,1:\]\|loc\[:,1:\]" "$LDSC/ldscore/sumstats.py"

echo
echo "===== Input 5: --h2-cts on the RE-PATCHED clone (confirms the patch is what fixes it) ====="
( cd "$STAGE_CTS" && $PY "$LDSC/ldsc.py" --h2-cts "$LDSC/test/simulate_test/sumstats/0" \
  --ref-ld-chr "ldscore/oneld_onefile" \
  --ref-ld-chr-cts "test.ldcts" \
  --w-ld-chr "ldscore/w" \
  --out "$OUT/input5_cts_postpatch_confirmed" ) 2>&1 | tail -15
cat "$OUT/input5_cts_postpatch_confirmed.cell_type_results.txt"
