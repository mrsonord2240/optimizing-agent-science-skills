source /mnt/openscience/audit-envs/bio-atac-seq-atac-qc/wsl_env.sh
S=/mnt/openscience/wt/atac-atac-qc/skills/bio-atac-seq-atac-qc/scripts
A=/mnt/openscience/audits/bio-atac-seq-atac-qc/audit-run; O=$A/out; W=$QCROOT/work; cd $O
echo "##### D-minus: BED6+gene-name column, true minus strand 1bp TSS"
python - <<'P'
import pyBigWig,subprocess,sys
O='/mnt/openscience/audits/bio-atac-seq-atac-qc/audit-run/out'
open(f'{O}/t.bed','w').write('chrT\t50050\t50051\tg1\t0\t-\tGENE\n')
# asymmetric planted profile: peak at 50050 exactly at TSS so strand doesn't matter for center; use asymmetric flank to detect reversal
P
echo "##### TSS timing: in-slice vs outside-slice (first 300 TSS each)"
T=$ATACDATA/annotation/gencode_v29_protein_coding_tss.chr1.bed
awk '$2>1000000 && $2<29000000' $T | head -300 > tss_in300.bed
awk '$2>40000000' $T | head -300 > tss_out300.bed
wc -l tss_in300.bed tss_out300.bed
( time python $S/encode_tss_enrichment.py $W/rep1.bw tss_in300.bed ) 2>&1 | grep -E "TSS_enrich|real"
( time timeout 120 python $S/encode_tss_enrichment.py $W/rep1.bw tss_out300.bed ) 2>&1 | grep -E "TSS_enrich|real"
echo "##### preseq verbose on unfiltered slice"
U=$ATACDATA/encode/GM12878_rep1_unfiltered.chr1_1-30000000.bam
preseq c_curve -v -B $U -o cc_v.tsv -s 1e6 2>&1 | tail -6
preseq c_curve -h 2>&1 | head -30
echo "##### R input formats"; ls $W/r 2>/dev/null | head
