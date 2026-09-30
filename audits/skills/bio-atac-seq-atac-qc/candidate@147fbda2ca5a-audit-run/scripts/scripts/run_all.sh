source /mnt/openscience/audit-envs/bio-atac-seq-atac-qc/wsl_env.sh
S=/mnt/openscience/wt/atac-atac-qc/skills/bio-atac-seq-atac-qc/scripts
A=/mnt/openscience/audits/bio-atac-seq-atac-qc/audit-run; O=$A/out; D=$ATACDATA/encode
cd $O
echo "### frag_nrf unfiltered"; python $A/scripts/frag_nrf.py $D/GM12878_rep1_unfiltered.chr1_1-30000000.bam | tee frag_unf.json
echo "### frag_nrf filtered"; python $A/scripts/frag_nrf.py $D/GM12878_rep1_filtered.chr1_1-30000000.bam | tee frag_fil.json
echo "### skill script (previous run)"; cat $QCROOT/work/lc_unf.json $QCROOT/work/lc_fil.json | tr -d '\n '; echo
