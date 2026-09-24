#!/bin/bash
# Run in WSL (cyvcf2 has no Windows wheel): /tmp/vaca/env python 3.12, cyvcf2 0.34.0
set -uo pipefail
cd "$(dirname "$0")"
P=/tmp/vaca/env/bin/python
$P -c "import cyvcf2; print('cyvcf2', cyvcf2.__version__)"
$P py_filter.py; echo "py_filter exit=$?"
grep -v '^#' filtered.vcf | cut -f1,2 > py_kept.tsv
$P ../../data/score_truth.py py_kept.tsv "cyvcf2 block kept:"
echo "QD<2 artifacts kept by the Python block (it has no QD term): $(grep -v '^#' filtered.vcf | grep -cE 'QD=(0\.|1\.)')"
