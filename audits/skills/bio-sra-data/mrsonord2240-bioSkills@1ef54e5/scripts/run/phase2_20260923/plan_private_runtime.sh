#!/usr/bin/env bash
set -euo pipefail

/home/sci/.local/bin/micromamba create --dry-run -y -p /home/sci/sra-audit-20260923 \
  -c conda-forge -c bioconda sra-tools=3.4.1 pigz python=3.12 pip \
  > /mnt/openscience/audits/bio-sra-data/run/phase2_20260923/private_runtime_dry_run.out 2>&1
