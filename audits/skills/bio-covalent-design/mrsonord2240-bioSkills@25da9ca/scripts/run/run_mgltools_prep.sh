#!/usr/bin/env bash
set -euo pipefail

# Prepare a new receptor PDBQT with the documented WSL MGLTools route.
work_dir="/mnt/openscience/audits/bio-covalent-design/run/mgltools_output"
fixture="/mnt/openscience/audit-envs/cheminformatics-hit-triage-analyst/smoke/dock/3ptb.pdb"
mkdir -p "$work_dir"
rm -f "$work_dir/3ptb_prepared.pdbqt"
micromamba run -n mgltools pythonsh "$(micromamba run -n mgltools which prepare_receptor4.py)" \
  -r "$fixture" -o "$work_dir/3ptb_prepared.pdbqt" -A hydrogens
test -s "$work_dir/3ptb_prepared.pdbqt"
atoms=$(awk '/^(ATOM|HETATM)/ {n++} END {print n+0}' "$work_dir/3ptb_prepared.pdbqt")
charges=$(awk '/^(ATOM|HETATM)/ && substr($0,71,6) !~ /^ *0\.000$/ {n++} END {print n+0}' "$work_dir/3ptb_prepared.pdbqt")
test "$atoms" -gt 1000
test "$charges" -gt 1000
printf 'prepared_pdbqt=%s atoms=%s nonzero_gasteiger_charges=%s\n' "$work_dir/3ptb_prepared.pdbqt" "$atoms" "$charges"
