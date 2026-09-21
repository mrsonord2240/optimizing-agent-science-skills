# Pass 1: per sample; only SJ.out.tab is needed
STAR --runMode alignReads \
    --runThreadN 8 \
    --genomeDir genome_index \
    --sjdbGTFfile gencode.v45.basic.gtf \
    --sjdbOverhang 149 \
    --readFilesIn sample_R1.fq.gz sample_R2.fq.gz \
    --readFilesCommand zcat \
    --outSAMtype None \
    --outFileNamePrefix pass1_${sample}_ \
    --outSJtype Standard \
    --outFilterMultimapNmax 20 \
    --alignSJoverhangMin 8 \
    --alignSJDBoverhangMin 3
