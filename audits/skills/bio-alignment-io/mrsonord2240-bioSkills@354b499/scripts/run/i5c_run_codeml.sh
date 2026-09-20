#!/bin/bash
# run codeml M0 in each of the two dirs (written by i5c_paml_io.py); prints omega/lnL or the codeml error text
for tag in seq rel; do
  cd /mnt/openscience/audits/bio-alignment-io/run/data/codeml_$tag || exit 1
  rm -f mlc rst rub rlf 2lnf 4fold.nei lnf
  timeout 120 codeml codeml.ctl </dev/null > stdout.txt 2>&1
  echo "== $tag (codeml exit $?)"
  tail -2 stdout.txt
  grep -E 'omega \(dN/dS\)|^lnL' mlc 2>/dev/null
done
