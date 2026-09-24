# 1. Count splicing events per cell. sample_list.tsv: BAM path <tab> cell id; BAMs sorted AND indexed
#    (droplet data: -s possorted.bam -b barcodes.tsv.gz instead of -S; tags default to --cellTAG CB --UMItag UR)
brie-count \
    -a splicing_events.gff3 \
    -S sample_list.tsv \
    -o brie_counts/ \
    -p 16

# 2. Fit BRIE2 with LRT against the cell covariates (cell_metadata.tsv: cell id + numeric feature columns)
