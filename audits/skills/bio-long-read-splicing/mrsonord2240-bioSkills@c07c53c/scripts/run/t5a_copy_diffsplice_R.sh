#!/bin/bash
# Copy FLAIR's own diffSplice R script (the half of `flair diffSplice --test` that needs Rscript) out of the as-lr env so Windows R (r.sh) can run it.
AS=/f/OpenScience/audit-envs/alternative-splicing
$AS/wsl_run.sh 'cat /home/sci/micromamba/envs/as-lr/lib/python3.12/site-packages/flair/diffSplice_drimSeq.R' | tr -d '\r' > /f/OpenScience/audits/bio-long-read-splicing/run/out/diffSplice_drimSeq.R
head -5 /f/OpenScience/audits/bio-long-read-splicing/run/out/diffSplice_drimSeq.R
