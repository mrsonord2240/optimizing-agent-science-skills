#!/bin/bash
# Input 3 (Edge, regression): reference-set failure-mode diagnosis.
# Two concrete misconfigurations, checked against the Skill's now-rewritten
# Failure Modes table (SKILL.md "BAGEL2 returns no hits, crashes, or silently
# corrupts output on a bad reference set").
set -e
PY="F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe"

echo "=== Case A: species mismatch (mouse CEG file against human screen) ==="
"$PY" BAGEL.py bf -i foldchange.foldchange -o bayes_factor_speciesmismatch.txt \
    -e CEG_mouse.txt -n NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C -s 42 || \
    echo "Expected: hard crash (ValueError from scipy.stats.gaussian_kde), matches Skill's documented symptom."

echo "=== Case B: -e/-n arguments swapped ==="
"$PY" BAGEL.py bf -i foldchange.foldchange -o bayes_factor_swapped.txt \
    -e NEGv1.txt -n CEGv2.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C -s 42
echo "Exit code: $? (expect 0 -- silent corruption, not a crash)"
echo "Non-nan BF rows (expect 0):"
awk -F'\t' 'NR>1{gsub(/ /,"",$2); if($2!="nan") c++} END{print c+0}' bayes_factor_swapped.txt
