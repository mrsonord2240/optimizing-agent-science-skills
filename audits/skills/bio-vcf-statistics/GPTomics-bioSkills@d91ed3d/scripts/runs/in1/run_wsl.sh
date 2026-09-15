#!/bin/bash
# WSL part of input 1: shipped examples/vcf_stats.py (cyvcf2 0.34.0) and plot-vcfstats (bcftools 1.21 + matplotlib).
set -uo pipefail
cd "$(dirname "$0")"
export PATH=/tmp/vaca/env/bin:$PATH
python -c "import cyvcf2, matplotlib; print('cyvcf2', cyvcf2.__version__, 'matplotlib', matplotlib.__version__)"
echo "== examples/vcf_stats.py cohort.vcf.gz =="; python vcf_stats.upstream_copy.py cohort.vcf.gz; echo "exit=$?"
echo "== examples/vcf_stats.py with no argument =="; python vcf_stats.upstream_copy.py; echo "exit=$?"
echo "== plot-vcfstats -p qc_plots/ stats.txt =="
rm -rf qc_plots; plot-vcfstats -p qc_plots/ stats.txt > plot.log 2>&1; echo "exit=$?"; tail -4 plot.log
ls qc_plots 2>/dev/null | head -20
