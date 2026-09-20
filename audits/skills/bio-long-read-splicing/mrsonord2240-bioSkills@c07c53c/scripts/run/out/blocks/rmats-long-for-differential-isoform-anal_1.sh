conda install -c conda-forge -c bioconda rmats-long

# Preprocessing pipeline (ASM mode); per-script flag names verified vs Xinglab/rmats-long
rmats-long organize_gene_info_by_chr.py --gtf annotation.gtf --out-dir gene_info_by_chr/

# simplify_alignment_info processes one BAM at a time -> one TSV
for bam in *.bam; do
    rmats-long simplify_alignment_info.py --in-file "$bam" --out-tsv "alignment_info/${bam%.bam}.tsv"
done

# organize_alignment_info_by_gene_and_chr requires a samples-tsv (sample_id<TAB>tsv_path)
rmats-long organize_alignment_info_by_gene_and_chr.py \
    --gtf-dir gene_info_by_chr/ \
    --out-dir organized/ \
    --samples-tsv samples.tsv

rmats-long detect_splicing_events.py --align-dir organized/ --gtf-dir gene_info_by_chr/ --out-dir events/
rmats-long create_gtf_from_asm_definitions.py --event-dir events/ --out-gtf asm.gtf
rmats-long count_reads_for_asms.py --align-dir organized/ --event-dir events/ --gtf-dir gene_info_by_chr/ --out-dir asm_counts/

# Main differential analysis (ASM mode)
# --group-1 / --group-2 each take the PATH to a file whose single line is a
# comma-separated list of sample IDs (matching the BAM basenames in --align-dir).
echo 'ctrl1,ctrl2,ctrl3' > group1.txt
echo 'trt1,trt2,trt3' > group2.txt
rmats-long rmats_long.py \
    --group-1 group1.txt \
    --group-2 group2.txt \
    --event-dir events/ \
    --asm-counts-dir asm_counts/ \
    --align-dir organized/ \
    --gtf-dir gene_info_by_chr/ \
    --out-dir rmats_long_output/ \
    --adj-pvalue 0.05 \
    --delta-proportion 0.05 \
    --average-reads-per-group 10

# Alternative: abundance-based mode (when you already have ESPRESSO-style estimates)
rmats-long rmats_long.py \
    --abundance abundance.esp \
    --updated-gtf updated.gtf \
    --group-1 group1.txt \
    --group-2 group2.txt \
    --out-dir rmats_long_output/ \
    --no-splice-graph-plot
