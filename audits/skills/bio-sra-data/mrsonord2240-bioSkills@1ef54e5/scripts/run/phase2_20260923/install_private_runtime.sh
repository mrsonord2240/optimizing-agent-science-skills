#!/usr/bin/env bash
set -euo pipefail

/home/sci/.local/bin/micromamba create -y -p /home/sci/sra-audit-20260923 \
  -c conda-forge -c bioconda sra-tools=3.4.1 pigz python=3.12 pip \
  > /mnt/openscience/audits/bio-sra-data/run/phase2_20260923/private_runtime_install.out 2>&1
/home/sci/.local/bin/micromamba install -y -p /home/sci/sra-audit-20260923 -c bioconda entrez-direct \
  > /mnt/openscience/audits/bio-sra-data/run/phase2_20260923/private_edirect_install.out 2>&1
/home/sci/sra-audit-20260923/bin/python -m pip install --disable-pip-version-check pysradb==2.5.1 biopython==1.88 \
  > /mnt/openscience/audits/bio-sra-data/run/phase2_20260923/private_pysradb_install.out 2>&1
