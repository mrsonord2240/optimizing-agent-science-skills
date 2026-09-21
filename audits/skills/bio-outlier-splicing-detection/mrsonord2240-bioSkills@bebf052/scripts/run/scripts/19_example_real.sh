#!/bin/bash
# NEW input: the shipped example on 4 REAL chrX RNA-seq BAMs (nf-core rnasplice test data, 2 GBR + 2 YRI), FRASER 2.6.1
R=/mnt/openscience/audits/bio-outlier-splicing-detection/run/ex_real
cd $R; rm -rf fraser_workdir; export PYTHONDONTWRITEBYTECODE=1
micromamba run -n as-drop Rscript fraser2_rare_disease.R bams ERR188383.Aligned.out fraser_workdir > ../logs/19_example_real_2.6.1.log 2>&1
echo "rc=$?"; grep -v "^Sun\|^||\|^\\\|^//\|^ \|^$" ../logs/19_example_real_2.6.1.log | tail -n 15 | cut -c1-200; ls fraser_workdir
