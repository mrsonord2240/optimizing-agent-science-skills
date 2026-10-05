#!/bin/bash
# cn_correction.R route command in WSL science / crispr-ccr, on the QC-passing simulated A375 table (KY ids).
export HOME=/home/sci
SK=/mnt/openscience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline
D=/mnt/openscience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline/cn-correction-qcpass
W=/mnt/openscience/fix-evidence/recut-crispr-pipeline/reaudit-001/work/cn
rm -rf $W; mkdir -p $W; cp $D/a375.count.txt $W/; cd $W
time /home/sci/micromamba/envs/crispr-ccr/bin/Rscript $SK/scripts/cn_correction.R a375.count.txt screen
echo EXIT=$?
echo "### guard: non-integer input"
printf 'sgRNA\tGene\ta\tb\n' > bad.txt; printf 'x\tG\t1.5\t2\n' >> bad.txt
/home/sci/micromamba/envs/crispr-ccr/bin/Rscript $SK/scripts/cn_correction.R bad.txt bad
echo EXIT_GUARD=$?
