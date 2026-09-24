# Input 5: SKILL.md B02 (pass 1) and B03 (merge + pass 2 + samtools index) run per sample on the 4 real chrX GEUVADIS-derived samples (2x75).
# ONLY edits (sed): genome_index, gencode.v45.basic.gtf, sample_R1/R2.fq.gz -> the real paths. Flags untouched (incl. --sjdbOverhang 149, --runThreadN 8).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; P=$ASDATA/rnasplice
S=/mnt/openscience/as-qc-reaudit-scratch/star; cd $S; mkdir -p run2 && cd run2
samples="ERR188383 ERR188428 ERR188454 ERR204916"
ed() { sed -e "s#genome_index#$S/genome_index#" -e "s#gencode.v45.basic.gtf#$P/reference/genes_chrX.gtf#" -e "s#sample_R1.fq.gz sample_R2.fq.gz#$P/fastq/${sample}_chrX_1.fastq.gz $P/fastq/${sample}_chrX_2.fastq.gz#" "$1"; }
for sample in $samples; do ed $R/blocks/B02.sh > b02_$sample.sh; export sample; asenv as-core bash b02_$sample.sh > p1_$sample.stdout 2>&1; echo "pass1 $sample rc=$?"; done
echo "--- pass-1 SJ.out.tab files"; wc -l pass1_*_SJ.out.tab
for sample in $samples; do ed $R/blocks/B03.sh > b03_$sample.sh; export sample; asenv as-core bash b03_$sample.sh > p2_$sample.stdout 2>&1; echo "pass2 $sample rc=$?"; done
echo "--- merged file"; wc -l cohort_novel_SJ.tab; head -3 cohort_novel_SJ.tab | cat -A | head -3
echo "--- pass 1 vs pass 2 unique-read mapping %"; for s in $samples; do echo "$s p1 $(grep 'Uniquely mapped reads %' pass1_${s}_Log.final.out | cut -f2)  p2 $(grep 'Uniquely mapped reads %' pass2_${s}_Log.final.out | cut -f2)"; done
ls -la pass2_*Aligned.sortedByCoord.out.bam* | awk '{print $5, $9}'
