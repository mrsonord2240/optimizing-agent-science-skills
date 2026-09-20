#!/bin/bash
# Ground truth for Neff: HMMER hmmbuild eff_nseq on the real Pfam seed
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
cd /mnt/openscience/audits/bio-alignment-msa-parsing/run/data
hmmbuild --amino -n pf --informat stockholm pf.hmm /mnt/openscience/audit-envs/alignment/public-data/msa/PF00042_seed.sto < /dev/null > hmmbuild_out.txt 2>&1
grep -v '^#' hmmbuild_out.txt | head -5
