source /mnt/openscience/audit-envs/bio-atac-seq-atac-qc/wsl_env.sh
S=/mnt/openscience/wt/atac-atac-qc/skills/bio-atac-seq-atac-qc/scripts
A=/mnt/openscience/audits/bio-atac-seq-atac-qc/audit-run; O=$A/out; cd $O
echo "##### TSS planted"; python $A/scripts/t_tss.py $S/encode_tss_enrichment.py $O
echo "##### LC planted"; python $A/scripts/t_lc.py $S/library_complexity.py $O
echo "##### AGG"; bash $A/scripts/t_agg.sh $S $O
