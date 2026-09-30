source /mnt/openscience/audits/bio-atac-seq-atac-peak-calling/reaudit-run/scripts/env.sh
# Genuinely failing library: rep2 = 6% read-name subsample of rep2 (low depth, nearly no reproducible peaks)
samtools view -b -s 7.06 $E2 -o $R/rep2_6pct.bam && samtools index $R/rep2_6pct.bam
samtools view -c $E2; samtools view -c $R/rep2_6pct.bam
