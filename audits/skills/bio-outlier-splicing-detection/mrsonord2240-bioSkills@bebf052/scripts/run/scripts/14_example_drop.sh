#!/bin/bash
# shipped example (skill/examples/fraser2_rare_disease.R) from a clean copy, FRASER 2.6.1 (as-drop); default args except bam_dir
R=/mnt/openscience/audits/bio-outlier-splicing-detection/run/ex_drop
cd $R; rm -rf fraser_workdir; export PYTHONDONTWRITEBYTECODE=1
micromamba run -n as-drop Rscript fraser2_rare_disease.R bams PATIENT_001 fraser_workdir > ../logs/14_example_2.6.1.log 2>&1
echo "rc=$?"; tail -n 6 ../logs/14_example_2.6.1.log | cut -c1-200; ls fraser_workdir; head -5 fraser_workdir/PATIENT_001_outliers.tsv | cut -c1-200
