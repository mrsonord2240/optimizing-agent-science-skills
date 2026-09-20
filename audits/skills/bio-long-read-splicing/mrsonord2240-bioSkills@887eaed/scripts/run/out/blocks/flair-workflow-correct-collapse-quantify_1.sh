# BAM -> BED12 (or `flair align`), one file per sample
bedtools bamtobed -bed12 -i aligned.bam > aligned.bed

# correct takes no genome; needs --gtf and/or short-read junctions (STAR SJ.out.tab via --junction_tab, or BED via --junction_bed)
flair correct \
    --query aligned.bed \
    --gtf gencode.v45.annotation.gtf \
    --junction_tab SJ.out.tab \
    --output flair_corrected \
    --threads 16

# collapse all samples together: cat the corrected BEDs, pass every reads file
flair collapse \
    --query flair_corrected_all_corrected.bed \
    --reads sample.fastq.gz \
    --genome reference.fa \
    --gtf gencode.v45.annotation.gtf \
    --output flair_collapsed \
    --threads 16

# reads_manifest.tsv: no header, tab-separated: sample_id  condition  batch  /path/reads.fastq.gz
flair quantify \
    --reads_manifest reads_manifest.tsv \
    --isoforms flair_collapsed.isoforms.fa \
    --output flair_quantified \
    --threads 16

flair diffSplice \
    --isoforms flair_collapsed.isoforms.bed \
    --counts_matrix flair_quantified.counts.tsv \
    --out_dir flair_diffsplice \
    --test \
    --threads 16
