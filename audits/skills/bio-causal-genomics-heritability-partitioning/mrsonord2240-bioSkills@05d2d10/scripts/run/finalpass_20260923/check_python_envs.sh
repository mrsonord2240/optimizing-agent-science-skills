#!/usr/bin/env bash
# Check which pre-existing isolated environment supplies the fixture-builder imports.
set -euo pipefail
for ENV_NAME in ldsc-py39 cg-hp-gcta bio; do
  echo "=== ${ENV_NAME} ==="
  micromamba run -n "${ENV_NAME}" python -c 'import sys; print(sys.version); import pandas; import pysnptools; print(pandas.__version__)' || true
done
