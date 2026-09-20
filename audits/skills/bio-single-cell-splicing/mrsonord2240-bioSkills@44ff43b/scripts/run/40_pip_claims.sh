#!/bin/bash
# Do the usage-guide install lines work? Throwaway venv in WSL /tmp (no shared env touched). Only checks resolve/build (no --deps of heavy TF stack for brie).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
rm -rf /tmp/scs_venv; asenv as-core python -m venv /tmp/scs_venv
V=/tmp/scs_venv/bin/pip
echo "=== pip install --no-deps brie (usage-guide 'pip install brie ...') ==="
$V install --no-deps brie 2>&1 | tail -8
echo "=== pip install --no-deps briekit (source of briekit-event used by example) ==="
$V install --no-deps briekit 2>&1 | tail -8
echo "=== pip download briekit sdist listing ==="
$V download briekit==0.2.2 --no-deps --no-binary :all: -d /tmp/scs_dl 2>&1 | tail -6
echo "=== salzman-lab/SpliZ pip-installable? ==="
ls /mnt/openscience/audit-envs/alternative-splicing/tools/src/SpliZ | grep -E "setup.py|pyproject" || echo "no setup.py / pyproject.toml in SpliZ repo"
echo "=== nextflow present? ==="; which nextflow || echo "nextflow not on PATH"
