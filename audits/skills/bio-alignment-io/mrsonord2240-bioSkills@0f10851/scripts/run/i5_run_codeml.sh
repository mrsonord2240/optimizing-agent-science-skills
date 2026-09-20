#!/bin/bash
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
for tag in seq rel; do
  cd /mnt/openscience/audits/bio-alignment-io/run/data/tools/codeml_$tag || exit 1
  rm -f mlc rst rub rlf 2lnf 4fold.nei lnf
  timeout 120 codeml codeml.ctl </dev/null > stdout.txt 2>&1
  echo "== $tag (codeml exit $?)"; tail -2 stdout.txt
  grep -E 'omega \(dN/dS\)|^lnL' mlc 2>/dev/null
done
