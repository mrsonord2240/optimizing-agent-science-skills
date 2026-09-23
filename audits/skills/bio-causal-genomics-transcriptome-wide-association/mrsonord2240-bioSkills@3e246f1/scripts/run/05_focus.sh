#!/usr/bin/env bash
# Fresh FOCUS execution of the shipped DB builder and focus_finemap.sh.
set -euo pipefail
AUDIT='F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association'
SCRATCH='F:/OpenScience/audit-scratch/twas-final-pass-20260923'
PY='F:/OpenScience/runtime/envs/.p/python.exe'
VENV="$SCRATCH/focus-venv"
VPY="$VENV/Scripts/python.exe"
if ! "$VPY" -c 'import pyfocus, pandas' >/dev/null 2>&1; then
  "$PY" -m venv "$VENV"
  "$VPY" -m pip install --disable-pip-version-check pyfocus 'pandas<2.2' 'setuptools<81'
fi
PYFOCUS_DIR=$("$VPY" -c 'import pyfocus, os; print(os.path.dirname(pyfocus.__file__))')
sed -i '1i import warnings' "$PYFOCUS_DIR/data/exprref.py"
sed -i 's/np\.warnings\.catch_warnings/warnings.catch_warnings/;s/np\.warnings\.filterwarnings/warnings.filterwarnings/' "$PYFOCUS_DIR/data/ldref.py" "$PYFOCUS_DIR/data/exprref.py"
sed -i 's/\.pivot("model_id", "attr_name", "value")/.pivot(index="model_id", columns="attr_name", values="value")/' "$PYFOCUS_DIR/finemap.py"
sed -i 's/^\( *\)df = df\.append(null_dict, ignore_index=True)/\1df = pd.concat([df, pd.DataFrame([null_dict])], ignore_index=True)/' "$PYFOCUS_DIR/finemap.py"
"$VPY" "$AUDIT/run/05_focus_setup.py"
DATA="$AUDIT/data/focus_final"
"$VPY" "$AUDIT/run/skill-src/scripts/build_focus_db.py" "$DATA/panel.tsv" "$DATA/focus_gtex_v8_whole_blood.db" --ref-name finalpass_panel --tissue Whole_Blood
focus() { "$VPY" "$VENV/Scripts/focus" "$@"; }
export VPY VENV
export -f focus
cd "$DATA"
bash "$AUDIT/run/skill-src/examples/focus_finemap.sh"
test -s gwas_focus_whole_blood.focus.tsv
test -s gwas_focus_whole_blood.credible.tsv
cat gwas_focus_whole_blood.focus.tsv
cat gwas_focus_whole_blood.credible.tsv
