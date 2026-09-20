# -t single = paired-end reads (use -t single for single-end); --readLength = the read length
micromamba run -n as-core rmats.py \
    --b1 condition1_bams.txt \
    --b2 condition2_bams.txt \
    --gtf annotation.gtf \
    -t single \
    --readLength 50 \
    --variable-read-length \
    --libType fr-unstranded \
    --nthread 8 \
    --od rmats_output \
    --tmp rmats_tmp \
    --novelSS \
    --cstat 0.05
