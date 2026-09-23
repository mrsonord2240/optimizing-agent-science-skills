#!/bin/bash
# Re-runs every step of the re-audit in order, from a Git Bash shell. Outputs land next to the scripts (in*_output.txt).
# Windows Python = F:/OpenScience/audit-envs/alignment/Scripts/python.exe (Biopython 1.88, pyhmmer 0.12.3); WSL steps call wsl_tools.sh.
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 MSYS2_ARG_CONV_EXCL='*'
PY=F:/OpenScience/audit-envs/alignment/Scripts/python.exe
# 0. real Ras seed (public EBI download, once): curl -sL -o data/PF00071_seed.sto.gz "https://www.ebi.ac.uk/interpro/api/entry/pfam/PF00071/?annotation=alignment:seed"
$PY mkdata.py
for s in mafft_globins hmmbuild_pf hmmalign_globins hmmalign_a2m mafft_hbb trim muscle_help muscle_ens8 muscle_ens73; do
  echo "##### $s"; wsl.exe -d science -- bash -lc "bash /mnt/openscience/audits/bio-alignment-msa-parsing/run/regression_phase1/wsl_tools.sh $s" 2>&1 | grep -av 'Failed to start the systemd'
done > wsl_tools_output.txt
$PY skillns.py > skillns_output.txt 2>&1
for n in in1_canonical in2_cleaning in3_edge in4_position_map in5_weights_neff_mi in6_scope_trimming in7_adversarial in8_real_new in9_weighting_coevolution; do
  $PY $n.py > ${n%%_*}_output.txt 2>&1; echo "$n: $(grep -c '^\[PASS\]' ${n%%_*}_output.txt) pass / $(grep -c '^\[FAIL\]' ${n%%_*}_output.txt) fail"
done
$PY examples_noargs.py > examples_noargs_output.txt 2>&1
$PY probes/probe_pb_easel2.py > probes/probe_pb_easel2_output.txt 2>&1
$PY probes/probe_sto_roundtrip.py > probes/probe_sto_roundtrip_output.txt 2>&1
$PY probes/probe_pb_easel.py > probes/probe_pb_easel_output.txt 2>&1      # first (wrong-variant) attempt at reproducing Easel pb: every variant off by 0.95-2.1
$PY probes/probe_scaling.py > probes/probe_scaling_output.txt 2>&1       # run time of the helpers vs alignment length
$PY build_report.py
$PY validate_report.py
