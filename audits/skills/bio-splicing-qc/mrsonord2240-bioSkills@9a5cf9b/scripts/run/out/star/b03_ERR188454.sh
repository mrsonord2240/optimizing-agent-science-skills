# Cohort merge. SJ.out.tab columns: 1 chr, 2 start, 3 end, 4 strand (0 undefined, 1 +, 2 -),
# 5 motif (0 non-canonical), 6 annotated (0/1), 7 unique reads, 8 multi-mapped reads, 9 max overhang.
# Keep novel (6==0), canonical-motif junctions with >=3 unique reads; STAR wants only columns 1-4.
cat pass1_*_SJ.out.tab | awk '$6 == 0 && $5 > 0 && $7 >= 3' | cut -f1-4 | sort -u > cohort_novel_SJ.tab

# Pass 2: re-align with the augmented junction set
STAR --runMode alignReads \
    --runThreadN 8 \
    --genomeDir /mnt/openscience/as-qc-reaudit-scratch/star/genome_index \
    --sjdbGTFfile /mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/reference/genes_chrX.gtf \
    --sjdbFileChrStartEnd cohort_novel_SJ.tab \
    --sjdbOverhang 149 \
    --readFilesIn /mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/fastq/ERR188454_chrX_1.fastq.gz /mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/fastq/ERR188454_chrX_2.fastq.gz \
    --readFilesCommand zcat \
    --outSAMtype BAM SortedByCoordinate \
    --outSAMstrandField intronMotif \
    --outFileNamePrefix pass2_${sample}_ \
    --outSJtype Standard \
    --quantMode GeneCounts \
    --alignSJoverhangMin 8 \
    --alignSJDBoverhangMin 3

samtools index pass2_${sample}_Aligned.sortedByCoord.out.bam   # pysam fetch() needs the index
