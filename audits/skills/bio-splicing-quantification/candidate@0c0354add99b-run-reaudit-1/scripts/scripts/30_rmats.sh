#!/bin/bash
# reaudit: fresh rMATS runs with the Skill's stated flags (real chrX 2v2 + planted). Outputs to ../out only.
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
D=$AS/public-data; R=$D/rnasplice; P=$D/planted
RUN=/mnt/openscience/audits/bio-splicing-quantification/run-reaudit-1
O=$RUN/out; mkdir -p $O; cd $O
micromamba run -n as-core rmats.py --version 2>&1 | tail -1
mkdir -p rmats_real/out rmats_real/tmp
echo "$R/bam/ERR188383.Aligned.out.bam,$R/bam/ERR188428.Aligned.out.bam" > rmats_real/b1.txt
echo "$R/bam/ERR188454.Aligned.out.bam,$R/bam/ERR204916.Aligned.out.bam" > rmats_real/b2.txt
micromamba run -n as-core rmats.py --b1 rmats_real/b1.txt --b2 rmats_real/b2.txt --gtf $R/reference/genes_chrX.gtf -t paired --readLength 75 \
  --variable-read-length --libType fr-firststrand --nthread 8 --od rmats_real/out --tmp rmats_real/tmp --novelSS --statoff > rmats_real/rmats.log 2>&1
echo "rmats real rc=$?"; wc -l rmats_real/out/*.MATS.J*.txt
mkdir -p rmats_planted/out rmats_planted/tmp
micromamba run -n as-core rmats.py --b1 $P/b1.txt --b2 $P/b2.txt --gtf $P/planted.gtf -t single --readLength 50 --nthread 2 --od rmats_planted/out --tmp rmats_planted/tmp --libType fr-unstranded --statoff > rmats_planted/rmats.log 2>&1
echo "rmats planted rc=$?"; wc -l rmats_planted/out/*.MATS.J*.txt
