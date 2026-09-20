# Annotation junctions for minimap2 (BED12); --junc-bed makes it prefer annotated junctions and rescues annotated microexons (ONT needs --junc-bonus 16 for the short ones, see Microexons)
gffread gencode.v45.annotation.gtf --bed -o annotation.bed12

# PacBio HiFi (Iso-Seq) -> minimap2 splice:hq preset
minimap2 -ax splice:hq --secondary=no --junc-bed annotation.bed12 \
    -t 16 \
    reference.fa \
    isoseq.fastq.gz | \
    samtools sort -@ 8 -o isoseq_aligned.bam
samtools index isoseq_aligned.bam

# ONT direct cDNA (PCS-114, PCB-114): reads come in both orientations, so no -uf
minimap2 -ax splice -k14 --secondary=no --junc-bed annotation.bed12 --junc-bonus 16 \
    -t 16 \
    reference.fa \
    ont_cdna.fastq.gz | \
    samtools sort -@ 8 -o ont_cdna_aligned.bam
samtools index ont_cdna_aligned.bam

# ONT direct RNA (RNA004): every read is in transcript orientation, so -uf is correct
minimap2 -ax splice -uf -k14 --secondary=no --junc-bed annotation.bed12 --junc-bonus 16 \
    -t 16 \
    reference.fa \
    ont_rna.fastq.gz | \
    samtools sort -@ 8 -o ont_rna_aligned.bam
samtools index ont_rna_aligned.bam
