awk 'BEGIN{OFS="\t"} {n=$10; split($11,sz,","); split($12,st,","); s=""; e="";
     for(i=1;i<=n;i++){s=s ($2+st[i]) ","; e=e ($2+st[i]+sz[i]) ","}
     print $4,$4,$1,$6,$2,$3,$7,$8,n,s,e}' genes.bed12 > refFlat.txt

picard CollectRnaSeqMetrics \
    I=sample.bam O=sample.rna_metrics.txt REF_FLAT=refFlat.txt \
    STRAND_SPECIFICITY=SECOND_READ_TRANSCRIPTION_STRAND \
    RIBOSOMAL_INTERVALS=rRNA_intervals.interval_list      # header-bearing interval_list, not BED

geneBody_coverage.py -i sample.bam -r genes.bed12 -o sample_geneBody --skip-plot
