#!/bin/bash
# Input 4 (Variant B) + Skill Veto T3 determinism check.
# Exact commands run against the synthetic combo_counts.txt / combo_design.txt
# produced by gen_mageck_mle_data.py, following the SKILL.md
# "Run Combinatorial Screen Analysis (MAGeCK MLE with Interaction Indicator)"
# section verbatim (same --count-table / --design-matrix / --output-prefix
# invocation pattern).

PY="F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe"
MAGECK="F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/mageck"

cd "F:/OpenScience/audits/bio-crispr-screens-combinatorial-screens/data" || exit 1

# First run
"$PY" "$MAGECK" mle \
    --count-table combo_counts.txt \
    --design-matrix combo_design.txt \
    --output-prefix combo_mle

# Second run on IDENTICAL inputs, no seed option exists in `mageck mle --help`
# -- used to check Skill Veto T3 (Result Determinism) on the interaction|fdr
# column that the Skill's MAGeCK MLE section relies on for interaction
# significance.
"$PY" "$MAGECK" mle \
    --count-table combo_counts.txt \
    --design-matrix combo_design.txt \
    --output-prefix combo_mle_run2

# Compare beta point-estimates (found identical) vs interaction|fdr
# (found different for 39/40 genes) between the two runs.
"$PY" -c "
import pandas as pd
a = pd.read_csv('combo_mle.gene_summary.txt', sep='\t').set_index('Gene')
b = pd.read_csv('combo_mle_run2.gene_summary.txt', sep='\t').set_index('Gene')
print('beta cols identical:', (a[['geneA|beta','geneB|beta','interaction|beta']].round(6) == b[['geneA|beta','geneB|beta','interaction|beta']].round(6)).all().all())
print('interaction|fdr identical:', (a['interaction|fdr'] == b['interaction|fdr']).all())
diff = a['interaction|fdr'] != b['interaction|fdr']
print('genes with differing interaction|fdr:', diff.sum(), '/', len(a))
"
