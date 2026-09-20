isoquant \
    --reference reference.fa \
    --genedb gencode.v45.annotation.gtf \
    --fastq sample1.fastq.gz sample2.fastq.gz \
    --data_type pacbio_ccs \
    --output isoquant_output \
    --threads 16 \
    --model_construction_strategy default_pacbio
