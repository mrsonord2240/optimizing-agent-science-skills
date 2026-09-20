#!/usr/bin/env bash
# Re-audit (2026-09-19) independent verification of the pyfocus pandas/np.warnings fix
# (Input 3) and the Windows MA-FOCUS drive-letter caveat fix (Input 6).
#
# Built a FRESH isolated venv (not the fixer's scratchpad venv, which no longer exists,
# and not the shared twas-venv, confirmed still unpatched at pandas 3.0.5):
#   python -m venv venv
#   venv/Scripts/python.exe -m pip install pyfocus "pandas<2.2" "setuptools<81"
#   -> pandas 2.1.4, numpy 1.26.4, setuptools 80.10.2 (matches SKILL.md's documented pin)
set -x

VENV=venv
FOCUS="$VENV/Scripts/python.exe $VENV/Scripts/focus"

# --- Reproduce crash 1 (delim_whitespace) on a bare install: done separately, matches
#     the original audit's own reproduction; not repeated here since already on record.

# --- Reproduce crash 2 (np.warnings) UNPATCHED, real end-to-end call ---
cd data/focus
$FOCUS finemap gwas.sumstats ld/EUR.1 custom_focus_direct.db \
  --tissue Whole_Blood --p-threshold 5e-8 --locations 38:EUR --out finemap_unpatched
# Result: "[ERROR] module 'numpy' has no attribute 'warnings'" -- reproduced

# --- Apply the documented patch (exactly as in SKILL.md Tool Install Notes) ---
# PYFOCUS_DIR=$(venv/Scripts/python.exe -c "import pyfocus, os; print(os.path.dirname(pyfocus.__file__))")
# sed -i "1i import warnings" "$PYFOCUS_DIR/data/exprref.py"
# sed -i "s/np\.warnings\.catch_warnings/warnings.catch_warnings/;s/np\.warnings\.filterwarnings/warnings.filterwarnings/" \
#     "$PYFOCUS_DIR/data/ldref.py" "$PYFOCUS_DIR/data/exprref.py"

# --- Build a REAL pyfocus-schema FOCUS weight DB (closing the gap the fix log flagged
#     as unexercised) via pyfocus.models.db directly, bypassing `focus import ... fusion`'s
#     undocumented mygene+rpy2 dependency (confirmed blocked: rpy2 needs R built as a
#     shared library, unavailable here) -- see reaudit_input3_build_focus_db.py ---
python reaudit_input3_build_focus_db.py

# --- Run focus finemap against the real DB (patched pyfocus) ---
$FOCUS finemap gwas.sumstats ld/EUR.1 custom_focus_direct.db \
  --tissue Whole_Blood --p-threshold 5e-8 --locations 38:EUR --out finemap_out3
# Result: NEW crash, not previously documented:
#   "[ERROR] DataFrame.pivot() takes 1 positional argument but 4 were given"
#   (pyfocus/finemap.py:1012, positional pivot() args removed by pandas>=2.0)
# After patching that line to use keyword args:
#   "[ERROR] 'DataFrame' object has no attribute 'append'"
#   (pyfocus/finemap.py:188, df.append() removed by pandas>=2.0)
# After patching BOTH (pd.concat replacement), focus finemap completes and produces real,
# ground-truth-correct PIP output: pips_pop1=1.0 for the true gene, ~3.4e-08 for NULL.MODEL.

# --- Input 6: MA-FOCUS Windows drive-letter caveat ---
# Absolute path repro (mis-detects population count from drive-letter colon):
$FOCUS finemap "$DATA_ABS/gwas.sumstats" "$DATA_ABS/ld/EUR.1" custom_focus_direct.db \
  --tissue Whole_Blood --p-threshold 5e-8 --locations 38:EUR --out finemap_abspath_test
# Result: "The number of LD refernece panel is different from the number of GWAS data."
#   (absolute Windows path's drive-letter colon collides with pyfocus's ':'-based
#   multi-ancestry split) -- reproduced independently.

# Real 3-population MA-FOCUS run using the now-documented relative-path workaround:
$FOCUS finemap \
  "gwas.sumstats:gwas.sumstats:gwas.sumstats" \
  "ld/EUR.1:ld/EUR.1:ld/EUR.1" \
  "custom_focus_direct.db:custom_focus_direct.db:custom_focus_direct.db" \
  --tissue Whole_Blood --p-threshold 5e-8 --locations "38:EUR-EAS-AFR" --out ma_focus_test
# Result: "Detecting 3 populations for fine-mapping" (correct); completes and produces
# real pips_pop1/pips_pop2/pips_pop3/pips_me columns, confirming both the Windows
# workaround and the fixer's pips_me/pips_popN column-naming claim end-to-end.
