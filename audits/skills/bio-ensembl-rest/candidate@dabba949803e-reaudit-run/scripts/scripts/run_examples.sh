#!/bin/bash
# Run the three shipped examples on the final bytes; one spaced attempt each, compara up to 3 attempts.
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
PY=F:/OpenScience/audit-envs/database-access/Scripts/python.exe
C=F:/OpenScience/wt/dbaccess-ensembl-rest/skills/bio-ensembl-rest/examples
O=F:/OpenScience/audits/bio-ensembl-rest/reaudit-run/evidence
for n in lookup_and_overlap vep_annotation; do
  $PY -u $C/$n.py > $O/example_$n.txt 2>&1; echo "exit=$?" >> $O/example_$n.txt
  sleep 3
done
for a in 1 2 3; do
  $PY -u $C/compara_homology.py > $O/example_compara_homology_attempt$a.txt 2>&1; rc=$?
  echo "exit=$rc" >> $O/example_compara_homology_attempt$a.txt
  [ $rc -eq 0 ] && break
  sleep 60
done
echo done > $O/examples_done.flag
