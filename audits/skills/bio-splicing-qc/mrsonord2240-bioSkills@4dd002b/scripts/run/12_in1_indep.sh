source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run
cd $R/work/in1
for l in se_clean se_novelrich real; do echo "== $l"; asenv as-core python $R/11_in1_indep.py $l/sample.bam $l/genes.bed12 $l/sample_junc_annot.junction.xls; done
