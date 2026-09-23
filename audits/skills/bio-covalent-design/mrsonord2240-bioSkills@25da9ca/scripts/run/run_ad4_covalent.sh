#!/usr/bin/env bash
set -euo pipefail

# Rerun the official AutoDock4 covalent flexible-side-chain tutorial in an audit-owned copy.
source_dir="/mnt/openscience/audit-envs/cheminformatics-hit-triage-analyst/tools/ad4-covalent-tutorial"
work_dir="/mnt/openscience/audits/bio-covalent-design/run/ad4_covalent_output"
ad4="/mnt/openscience/audit-envs/cheminformatics-hit-triage-analyst/tools/autodock4/autodock4.exe"
ag4="/mnt/openscience/audit-envs/cheminformatics-hit-triage-analyst/tools/autodock4/autogrid4.exe"
rm -rf "$work_dir"
mkdir -p "$work_dir"
cp -a "$source_dir/." "$work_dir/"
cd "$work_dir/adCovalentDockResidue/3upo_test/output"
"$ag4" -p 3upo_priotein.gpf -l audit_3upo.glg
"$ad4" -p ligcovalent_3upo_protein.dpf -l audit_ligcovalent_3upo_protein.dlg
test -s audit_3upo.glg
test -s audit_ligcovalent_3upo_protein.dlg
maps=$(find . -maxdepth 1 -name '3upo_priotein.*.map' | wc -l)
best=$(grep -m1 'Estimated Free Energy of Binding' audit_ligcovalent_3upo_protein.dlg | awk '{print $8}')
test "$maps" -eq 8
test -n "$best"
python - "$best" <<'PY'
import sys
score = float(sys.argv[1])
assert -11.5 < score < -10.0, score
print(f"grid_maps=8 best_binding_kcal_per_mol={score:.2f}")
PY
