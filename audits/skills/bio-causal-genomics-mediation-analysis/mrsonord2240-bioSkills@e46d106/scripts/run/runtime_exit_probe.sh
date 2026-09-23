#!/bin/bash
# Diagnose whether post-computation exit 139 belongs to the Skill or the shared R runtime.
set -u
RSH=/f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh
for pkg in mediation TwoSampleMR HIMA MVMR; do
  "$RSH" -e "library($pkg); cat('$pkg loaded\\n')" >/dev/null 2>&1
  status=$?
  echo "${pkg}_minimal_exit=${status}"
done
exit 0
