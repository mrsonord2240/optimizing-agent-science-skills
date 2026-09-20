#!/bin/bash
# Run the SKILL DTU block (sourced verbatim by t9_dtu.R) in the FLAIR run directory of the planted HiFi 3v3 design; Windows R via r.sh.
AS=/f/OpenScience/audit-envs/alternative-splicing; R=F:/OpenScience/audits/bio-long-read-splicing/run
$AS/r.sh $R/t9_dtu.R $R/out/hifi6 $R/data/plant/truth_dtu.tsv 2>&1 | tail -12
# same block on the REAL 6-sample LRGASP FLAIR quantify output (out/real; truth args are irrelevant there)
$AS/r.sh $R/t9_dtu.R $R/out/real $R/data/plant/truth_dtu.tsv 2>&1 | tail -8
