#!/bin/bash
# Install cyvcf2 into a dedicated venv (system-site-packages, so numpy from the
# bio micromamba env is reused) so examples/check_normalization.py can be run
# without changing package versions in the shared bio env.
set -e
ENV=/mnt/openscience/audit-envs/bio-variant-normalization
mkdir -p "$ENV"
if [ -d "$ENV/install.lock" ]; then echo "LOCK EXISTS, abort"; exit 1; fi
mkdir "$ENV/install.lock"
trap 'rmdir "$ENV/install.lock"' EXIT
python3 -m venv --system-site-packages "$ENV/venv"
source "$ENV/venv/bin/activate"
pip install --quiet cyvcf2 2>&1 | tail -30
python3 -c "import cyvcf2; print('cyvcf2', cyvcf2.__version__)"
