source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; S=/mnt/openscience/as-qc-reaudit-scratch/star/run2
asenv as-core python $R/55_only_helper.py $R/skill/examples $S/pass2_ERR204916_Aligned.sortedByCoord.out.bam $S/pass2_ERR204916_SJ.out.tab $ASDATA/derived/X.fa
