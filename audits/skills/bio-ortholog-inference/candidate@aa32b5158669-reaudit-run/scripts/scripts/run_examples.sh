#!/bin/bash
# Run the three shipped examples on the final bytes, paced; compara up to 3 attempts 60 s apart.
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
PY=F:/OpenScience/audit-envs/database-access/Scripts/python.exe
C=F:/OpenScience/wt/dbaccess-ortholog-inference/skills/bio-ortholog-inference/examples
O=F:/OpenScience/audits/bio-ortholog-inference/reaudit-run/scripts/evidence
$PY -u F:/OpenScience/audits/bio-ortholog-inference/reaudit-run/scripts/run_extra.py > $O/run_extra.txt 2>&1
for n in kegg_orthology cross_resource; do
  $PY -u $C/$n.py > $O/example_$n.txt 2>&1; echo "exit=$?" >> $O/example_$n.txt
  sleep 5
done
for a in 1 2 3; do
  $PY -u $C/compara_orthologs.py > $O/example_compara_orthologs_attempt$a.txt 2>&1; rc=$?
  echo "exit=$rc" >> $O/example_compara_orthologs_attempt$a.txt
  [ $rc -eq 0 ] && break
  sleep 60
done
echo done > $O/examples_done.flag
