#!/bin/bash
# Input 5: WebLogo (pip, Windows venv) with the SKILL pdf command; Ghostscript is not installed on Windows
DV=/f/OpenScience/audit-envs/data-visualization
mkdir -p out/wlwin; cd out/wlwin
awk '{print ">s"NR; print $0}' ../../data/dna_n200.txt > n200.fa
export PYTHONUTF8=1
$DV/Scripts/weblogo.exe --version 2>&1 | tail -1
for f in pdf png svg eps logodata; do
  $DV/Scripts/weblogo.exe --format $f --sequence-type dna --color-scheme classic --units bits --composition equiprobable --fineprint '' --size large < n200.fa > logo.$f 2> err.$f; echo "$f exit=$? bytes=$(stat -c %s logo.$f) :: $(tail -1 err.$f | cut -c1-160)"
done
which gs gswin64c 2>&1 | head -2
