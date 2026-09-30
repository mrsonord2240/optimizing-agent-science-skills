source /mnt/openscience/audit-envs/bio-atac-seq-atac-qc/wsl_env.sh
A=/mnt/openscience/audits/bio-atac-seq-atac-qc/audit-run; O=$A/out; cd $O
F=$ATACDATA/encode/GM12878_rep1_filtered.chr1_1-30000000.bam
samtools sort -n -@4 -o fil.nsort.bam $F
echo "### -P filtered nsort default seg_len"; preseq c_curve -B -P -v fil.nsort.bam -o ccP.tsv -s 1e5 2>&1 | grep -v -E "^[0-9]+\s+[0-9]+$" | tail -8; head -4 ccP.tsv
echo "### -P -l 20000"; preseq c_curve -B -P -l 20000 fil.nsort.bam -o ccP2.tsv -s 1e5 2>&1 | tail -3; head -4 ccP2.tsv
echo "### lc_extrap -P"; preseq lc_extrap -B -P -l 20000 fil.nsort.bam -o lcP.tsv -e 20000000 -s 2000000 2>&1 | tail -3; head -4 lcP.tsv; tail -2 lcP.tsv
