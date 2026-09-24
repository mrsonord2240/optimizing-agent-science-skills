# isoforms.gtf: transcript and exon rows only (FLAIR isoforms.gtf as is; from IsoQuant:
#   awk -F'\t' '$3=="transcript" || $3=="exon"' <prefix>.transcript_models.gtf > isoforms.gtf)
# -o is a file prefix, -d the output directory. --CAGE_peak and --polyA_motif_list are optional: drop them without files
sqanti3_qc.py \
    --isoforms isoforms.gtf \
    --refGTF gencode.v45.annotation.gtf \
    --refFasta reference.fa \
    -o sqanti3 -d sqanti3_qc \
    --aligner_choice minimap2 \
    --CAGE_peak hg38.cage_peak_phase1and2combined_coord.bed \
    --polyA_motif_list human.polyA.list.txt \
    --cpus 8
# classification: sqanti3_qc/sqanti3_classification.txt

sqanti3_filter.py rules \
    --sqanti_class sqanti3_qc/sqanti3_classification.txt \
    --filter_gtf isoforms.gtf \
    -o sqanti3_filtered -d sqanti3_filtered \
    --skip_report
# filtered GTF: sqanti3_filtered/sqanti3_filtered.filtered.gtf; per-isoform filter_result: *_RulesFilter_classification.txt
