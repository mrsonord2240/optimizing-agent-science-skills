# Pass 1: per sample; only SJ.out.tab is needed
STAR --runMode alignReads \
    --runThreadN 8 \
    --genomeDir /mnt/openscience/as-qc-reaudit-scratch/star/genome_index \
    --sjdbGTFfile /mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/reference/genes_chrX.gtf \
    --sjdbOverhang 149 \
    --readFilesIn /mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/fastq/ERR188383_chrX_1.fastq.gz /mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/fastq/ERR188383_chrX_2.fastq.gz \
    --readFilesCommand zcat \
    --outSAMtype None \
    --outFileNamePrefix pass1_${sample}_ \
    --outSJtype Standard \
    --outFilterMultimapNmax 20 \
    --alignSJoverhangMin 8 \
    --alignSJDBoverhangMin 3
