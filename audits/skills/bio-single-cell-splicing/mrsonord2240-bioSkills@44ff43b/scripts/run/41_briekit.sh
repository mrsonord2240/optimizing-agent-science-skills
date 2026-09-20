#!/bin/bash
# Can the example's prepare_splicing_events() (briekit-event -a GTF -o GFF3) work? Try to build briekit in the throwaway venv with numpy present.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
V=/tmp/scs_venv/bin
$V/pip install numpy scipy pandas 2>&1 | tail -1
$V/pip install setuptools wheel 2>&1 | tail -1
$V/pip install --no-build-isolation --no-deps briekit 2>&1 | tail -3
ls $V | grep -i brie
$V/briekit-event -h 2>&1 | head -30
