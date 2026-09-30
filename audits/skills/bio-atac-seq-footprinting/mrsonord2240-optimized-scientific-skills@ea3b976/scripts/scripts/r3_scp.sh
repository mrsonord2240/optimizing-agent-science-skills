#!/bin/bash
# Re-audit: scprinter_footprint.py unmodified in FRESH ra-footprint-scprinter env; fragments per usage-guide with FRESH ra-footprint samtools/bgzip/tabix.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PATH=/home/sci/.local/bin:$PATH PYTHONDONTWRITEBYTECODE=1
SKILL=/mnt/openscience/wt/atac-footprinting/skills/bio-atac-seq-footprinting
Q=bio-atac-seq-footprinting; E=/mnt/openscience/audit-envs/$Q; PD=/mnt/openscience/audit-envs/atac-seq/public-data
W=$E/reaudit-run/scp; rm -rf $W; mkdir -p $W; cd $W
L=/mnt/openscience/audits/$Q/reaudit-run/logs
BAM=$PD/encode/GM12878_rep1_filtered.chr1_1-30000000.bam
micromamba run -n ra-footprint samtools view -f 2 $BAM | awk 'BEGIN{OFS="\t"} $9>0 && $9<1000 {print $3,$4-1,$4-1+$9,"sample"}' | sort -k1,1 -k2,2n -k3,3n > frags.tsv
wc -l frags.tsv
micromamba run -n ra-footprint bgzip frags.tsv && micromamba run -n ra-footprint tabix -p bed frags.tsv.gz; echo "bgzip/tabix rc=$?"
zcat $PD/annotation/gencode.v29.chr1.gtf.gz > genes.gtf; zcat $PD/annotation/hg38-blacklist.v2.bed.gz > bl.bed
cp $E/fix-run/scp/regions.bed $E/fix-run/scp/regions_labels.tsv .
export SCPRINTER_DATA=$E/scprinter
( time micromamba run -n ra-footprint-scprinter python $SKILL/scripts/scprinter_footprint.py --fragments frags.tsv.gz --fasta $PD/reference/hg38.chr1.fa --gtf genes.gtf --blacklist bl.bed --regions regions.bed --outdir out --modes 2-100 --width 200 --device cuda:0 --jobs 2 ) > $L/r3_scprinter.log 2>&1; echo "rc=$?" >> $L/r3_scprinter.log
tail -6 $L/r3_scprinter.log
# failure guard: missing fragments file
micromamba run -n ra-footprint-scprinter python $SKILL/scripts/scprinter_footprint.py --fragments nope.tsv.gz --fasta $PD/reference/hg38.chr1.fa --gtf genes.gtf --blacklist bl.bed --regions regions.bed --outdir out_bad --bias out/bias.h5 --modes 10 > $L/r3_scp_missing.log 2>&1; echo "missing-fragments rc=$?"; tail -3 $L/r3_scp_missing.log | cut -c1-200
