#!/bin/bash
# Second spaced round: vep_annotation then compara_homology, up to 3 tries each, 90 s apart.
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
PY=F:/OpenScience/audit-envs/database-access/Scripts/python.exe
C=F:/OpenScience/wt/dbaccess-ensembl-rest/skills/bio-ensembl-rest/examples
O=F:/OpenScience/audits/bio-ensembl-rest/reaudit-run/evidence
for n in vep_annotation compara_homology; do
  for a in 3 4 5; do
    sleep 90
    $PY -u $C/$n.py > $O/example_${n}_attempt$a.txt 2>&1; rc=$?
    echo "exit=$rc" >> $O/example_${n}_attempt$a.txt
    [ $rc -eq 0 ] && break
  done
done
echo done > $O/examples_done2.flag
