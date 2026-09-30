source /mnt/openscience/audit-envs/bio-atac-seq-atac-qc/wsl_env.sh
A=/mnt/openscience/audits/bio-atac-seq-atac-qc/audit-run; O=$A/out; W=$QCROOT/work; cd $O
U=$ATACDATA/encode/GM12878_rep1_unfiltered.chr1_1-30000000.bam; F=$ATACDATA/encode/GM12878_rep1_filtered.chr1_1-30000000.bam
preseq c_curve 2>&1 | head -30
echo "### -v head"; preseq c_curve -v -B $U -o cc_v.tsv -s 1e6 2>&1 | grep -v -E "^[0-9]+\s+[0-9]+$" | head -20
echo "### samtools counts"; samtools view -c $U; samtools view -c -F 3844 $U
echo "### -s 1e6 on FILTERED (1.05M reads)"; preseq c_curve -B $F -o ccf.tsv -s 1e6 2>&1 | tail -2; cat ccf.tsv
echo "### -s 1e5 on unfiltered tail"; tail -3 cc_1e5.tsv 2>/dev/null || tail -3 $W/cc_1e5.tsv
echo "### lc_extrap unfiltered vs distinct at obs (script says distinct 642251 over 1.82M reads)"
