#!/bin/bash
# One clean pass of every script of this audit, inside WSL `science` (env alignment-files), from a fresh data\ + work\.
# Launch:  F:/OpenScience/audit-envs/alignment-files/wsl_run.sh 'bash /mnt/openscience/audits/bio-pileup-generation/run/run_everything.sh'
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-pileup-generation/run
rm -rf work; mkdir -p work
for s in 00_make_data 01_make_new_data 02_make_fuzz \
         t01_regress_real_mpileup t02_regress_pysam_helpers t03_regress_edge_defaults t04_regress_bcftools t05_regress_library_real \
         t06_new_planted_and_fuzz t07_new_real_matrix \
         10_cigar_fuzz 11_baq_rf 12_find_variants_access 13_probe_seq_star_and_related 14_usage_guide_dedup \
         x_probe_stepper_baq x_probe_stepper_baq2 x_probe_stepper_baq3 x_probe_stepper_baq4 x_probe_stepper_baq5 x_probe_stepper_default; do
  python $s.py > log_$s.txt 2>&1
  echo "$s rc=$? : $(grep -a -c '^\[PASS\]' log_$s.txt) PASS, $(grep -a -c '^\[FAIL\]' log_$s.txt) FAIL"
done
bash x_wrongpipe.sh > log_x_wrongpipe.txt 2>&1; echo "x_wrongpipe rc=$?"
# versions for the record
{ samtools --version | head -1; bcftools --version | head -1; python -c "import pysam;print('pysam',pysam.__version__)"; } > log_versions.txt
rm -rf work
echo ALL DONE
