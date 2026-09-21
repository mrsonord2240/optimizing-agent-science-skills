#!/bin/bash
# NEW synthetic sets for inputs 9 and 10 (generator 05_gen_het.R). Everything is synthetic.
R=F:/OpenScience/audit-envs/alternative-splicing/r.sh; cd F:/OpenScience/audits/bio-isoform-switching/run
bash $R 05_gen_het.R data/het_null 9101 6 6 0 0.2 srr
bash $R 05_gen_het.R data/het_3v3 9102 3 3 1 0.2 srr
bash $R 05_gen_het.R data/het_6v6 9103 6 6 1 0.2 srr
bash $R 05_gen_het.R data/odd_3v5 9104 3 5 1 0.0 odd
