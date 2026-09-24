source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; S=/mnt/openscience/as-qc-reaudit-scratch/star/run2
mkdir -p $R/work/n1
asenv as-core python $R/81_n1_cohort.py $R/skill/examples $S $R/work/in1/real/genes.bed12 $R/data/synthetic $R/work/n1
echo "--- independent class check on the 4 real pass-2 BAMs (RSeQC xls written by the helper run vs pysam)"
for s in ERR188383 ERR188428 ERR188454 ERR204916; do asenv as-core python $R/11_in1_indep.py $S/pass2_${s}_Aligned.sortedByCoord.out.bam $R/work/in1/real/genes.bed12 $R/work/n1/$s.junction.xls | tail -1; done
