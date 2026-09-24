#!/bin/bash
# INPUT 6c: produce REAL STARsolo SmartSeq SJ output (4 real chrX RNA-seq libraries treated as 4 'cells') to test the scQuint loader's real input format.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run; F=$ASDATA/rnasplice/fastq
W=$R/out/in6_scquint; rm -rf $W; mkdir -p $W; cd $W
IDX=/mnt/openscience/audit-envs/alternative-splicing/logs/smoke_irfinder/starref
: > manifest.tsv; for c in ERR188383 ERR188428 ERR188454 ERR204916; do printf "%s\t%s\t%s\n" $F/${c}_chrX_1.fastq.gz $F/${c}_chrX_2.fastq.gz $c >> manifest.tsv; done
cat manifest.tsv | cut -c1-200
asenv as-core STAR --genomeDir $IDX --runThreadN 8 --soloType SmartSeq --readFilesManifest manifest.tsv --readFilesCommand zcat --soloUMIdedup Exact --soloStrand Unstranded --soloFeatures Gene SJ --outSAMtype None --outFileNamePrefix ss_ 2>&1 | tail -5
find ss_Solo.out -type f | head -20; head -3 ss_Solo.out/SJ/raw/features.tsv 2>/dev/null; cat ss_Solo.out/SJ/raw/barcodes.tsv 2>/dev/null; head -4 ss_Solo.out/SJ/raw/matrix.mtx 2>/dev/null
