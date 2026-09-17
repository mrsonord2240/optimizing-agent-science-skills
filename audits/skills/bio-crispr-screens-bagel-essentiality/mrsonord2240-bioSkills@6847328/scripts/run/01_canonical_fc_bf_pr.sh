#!/bin/bash
# Input 1 (Canonical, regression) + Input 5 determinism check (regression).
# BAGEL.py = patched build 115 copy from TOOLS.md (numpy 2.x fixes), copied into
# this run/ dir. Reference data: real HAP1 TKOv3 screen (data/HAP1_TKOv3_reads.txt,
# 70,754 sgRNAs / 18,053 genes) + real CEGv2/NEGv1 reference sets.
set -e
PY="F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe"

# --- fold changes ---
"$PY" BAGEL.py fc -i HAP1_TKOv3_reads.txt -o foldchange -c HAP1_T0 --min-reads 30

# --- Bayes factors, seeded (-s 42), run twice: determinism regression check ---
"$PY" BAGEL.py bf -i foldchange.foldchange -o bayes_factor_seedA.txt \
    -e CEGv2.txt -n NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C -s 42
"$PY" BAGEL.py bf -i foldchange.foldchange -o bayes_factor_seedB.txt \
    -e CEGv2.txt -n NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C -s 42
diff bayes_factor_seedA.txt bayes_factor_seedB.txt && \
    echo "PASS: -s 42 reruns are byte-identical (determinism fix confirmed)"
cp bayes_factor_seedA.txt bayes_factor.txt

# --- Bayes factors, UNSEEDED, run twice: confirms the underlying non-determinism
#     the fix warns about still exists in BAGEL.py itself when -s is omitted ---
"$PY" BAGEL.py bf -i foldchange.foldchange -o bayes_factor_noseedC.txt \
    -e CEGv2.txt -n NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C
"$PY" BAGEL.py bf -i foldchange.foldchange -o bayes_factor_noseedD.txt \
    -e CEGv2.txt -n NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C
echo "Unseeded rerun diff line count (expect ~18053*2, i.e. every row differs):"
diff bayes_factor_noseedC.txt bayes_factor_noseedD.txt | wc -l

# --- precision-recall curve ---
"$PY" BAGEL.py pr -i bayes_factor.txt -o precision_recall.txt -e CEGv2.txt -n NEGv1.txt

# --- bootstrap mode (STD/NumObs columns), reduced -NB 100 for runtime ---
"$PY" BAGEL.py bf -i foldchange.foldchange -o bayes_factor_bootstrap.txt \
    -e CEGv2.txt -n NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C -s 42 -b -NB 100

# --- per-sgRNA BF contributions (-r), Input 5 regression ---
"$PY" BAGEL.py bf -i foldchange.foldchange -o bayes_factor_sgrna.txt \
    -e CEGv2.txt -n NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C -s 42 -r

# --- confirm the documented -s flag collision (--use-small-sample vs --seed) ---
"$PY" BAGEL.py bf --help
