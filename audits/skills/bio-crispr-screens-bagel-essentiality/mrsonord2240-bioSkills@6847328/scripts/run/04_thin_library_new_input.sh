#!/bin/bash
# Input 6 (new, auditor-authored): synthetic thin-library stress test.
# Exercises the Skill's "Bootstrap CI is wide; BF estimates unstable" Failure
# Mode with a real run at 3 sgRNAs/gene (below the Skill's own 4-6/gene
# recommendation), using REAL CEGv2/NEGv1 gene symbols (see
# data/make_synthetic_thin_library.py) so the KDE has real training material
# and the only stressed variable is sgRNA count per gene.
set -e
PY="F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe"

"$PY" ../data/make_synthetic_thin_library.py   # writes HAP1_thin_library_synthetic.txt into cwd

"$PY" BAGEL.py fc -i HAP1_thin_library_synthetic.txt -o thin_fc -c T0 --min-reads 0

"$PY" BAGEL.py bf -i thin_fc.foldchange -o thin_bf_cv.txt \
    -e CEGv2.txt -n NEGv1.txt -c T18A,T18B,T18C -s 42

"$PY" BAGEL.py bf -i thin_fc.foldchange -o thin_bf_boot.txt \
    -e CEGv2.txt -n NEGv1.txt -c T18A,T18B,T18C -s 42 -b -NB 1000

echo "=== CI-spans-zero check on bootstrap output ==="
awk -F'\t' 'NR>1{if($3+0 > ($2<0?-$2:$2)) wide++; total++} END{print wide+0" / "total" genes have STD > |BF| (CI spans zero)"}' thin_bf_boot.txt
