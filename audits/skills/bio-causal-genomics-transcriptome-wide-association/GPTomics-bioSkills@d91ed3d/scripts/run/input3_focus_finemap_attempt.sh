#!/bin/bash
# Input 3 (FOCUS edge case, gene-dense locus): attempted focus finemap after a fresh
# `pip install pyfocus` (matching usage-guide.md's own install instruction, no pandas pin).
# Result: crashes with TypeError: read_csv() got an unexpected keyword argument
# 'delim_whitespace' -- pyfocus 0.802's own pyfocus/data/gwas.py, exprref.py, ldref.py, and
# models/convert.py all call pd.read_csv(..., delim_whitespace=True), a kwarg pandas>=2.2
# deprecated and pandas 3.0 (installed here, since pyfocus's setup.py pins only
# "pandas>=0.23.0" with no upper bound) removed outright. Reproduced directly:
cd "F:/OpenScience/audit-envs/mendelian-randomization-analyst"
D3="F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association/data/focus_edge"
mkdir -p "$D3"
# Minimal GWAS file in the format focus finemap expects (whitespace-delimited).
cat > "$D3/gwas.sumstats" << 'GWAS'
SNP CHR BP A1 A2 Z P
rs637471 1 98683576 T C 6.5 8.03e-11
GWAS
./twas-venv/Scripts/python.exe twas-venv/Scripts/focus finemap \
  "$D3/gwas.sumstats" "F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/src/plink2R/data" \
  "F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association/data/spredixcan/synthetic_model.db" \
  --chr 1 --p-threshold 5e-8 --out "$D3/focus_out"
