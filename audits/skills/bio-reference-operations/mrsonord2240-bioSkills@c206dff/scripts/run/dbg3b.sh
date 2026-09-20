cd /mnt/openscience/audits/bio-reference-operations/run/work/in3
picard ValidateSamFile I=s_num.bam R=s_num.fa MODE=SUMMARY IGNORE=MISSING_READ_GROUP 2>&1 | grep -v -E "WARNING|^\*|setlocale|^$" | tail -8
