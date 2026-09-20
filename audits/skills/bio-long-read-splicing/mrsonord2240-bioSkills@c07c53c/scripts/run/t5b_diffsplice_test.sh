#!/bin/bash
# `flair diffSplice --test` prerequisite step, run through the env's Windows R (r.sh): FLAIR's own diffSplice_drimSeq.R (copied out of the as-lr env)
# on the event tables written by the SKILL's FLAIR block. Rscript is absent in WSL as-lr, so `--test` fails there (see t5_real.log); this runs the R half by hand.
# usage: t5b_diffsplice_test.sh <workdir containing flair_diffsplice/>  (bash in Git Bash, not WSL)
W=$1
AS=/f/OpenScience/audit-envs/alternative-splicing
RS=/f/OpenScience/audits/bio-long-read-splicing/run/out/diffSplice_drimSeq.R
export PATH="$AS/Scripts:$PATH"; export PYTHON3="F:/OpenScience/audit-envs/alternative-splicing/Scripts/python.exe"
export R_LIBS="F:/OpenScience/audits/bio-long-read-splicing/run/out/rlib_extra"
for ev in es alt5 alt3 ir; do
  echo "##### $ev"
  $AS/r.sh $RS --threads 4 --outDir $W/flair_diffsplice --drim1 ${DRIM1:-6} --drim2 ${DRIM2:-3} --drim3 ${DRIM3:-15} --drim4 ${DRIM4:-5} --matrix $W/flair_diffsplice/diffsplice.$ev.events.quant.tsv --prefix $ev 2>&1 | tail -6
done
ls -la $W/flair_diffsplice
