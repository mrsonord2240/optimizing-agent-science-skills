source /mnt/openscience/audit-envs/bio-atac-seq-atac-qc/wsl_env.sh
A=/mnt/openscience/audits/bio-atac-seq-atac-qc/audit-run; O=$A/out; cd $O
F=$ATACDATA/encode/GM12878_rep1_filtered.chr1_1-30000000.bam; U=$ATACDATA/encode/GM12878_rep1_unfiltered.chr1_1-30000000.bam
for B in $F $U; do echo "### -P coord-sorted $(basename $B)"; preseq c_curve -B -P -v $B -o ccP.tsv -s 1e5 2>&1 | grep -v -E "^[0-9]+\s+[0-9]+$" | head -8; tail -3 ccP.tsv; done
echo "### filtered no -P"; preseq c_curve -B -v $F -o ccN.tsv -s 1e5 2>&1 | grep -E "TOTAL|DISTINCT READS"; tail -1 ccN.tsv
echo "### lc_extrap -P filtered"; preseq lc_extrap -B -P $F -o lcP.tsv -e 20000000 -s 2000000 2>&1 | tail -3; sed -n '1,3p;$p' lcP.tsv
