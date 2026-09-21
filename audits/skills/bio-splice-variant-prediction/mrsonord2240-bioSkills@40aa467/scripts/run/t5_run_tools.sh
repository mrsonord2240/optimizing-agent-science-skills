#!/bin/bash
# Input 5: remaining tool runs for the concordance test: SpliceAI GRCh38 (auditor panel), Pangolin GRCh37 chrX (panel, -m False)
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
G=/mnt/openscience/as-spvp-scratch/g38
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
micromamba run -n as-spliceai spliceai -I data/panel_grch38_auditor.vcf -O out/sai38_D50.vcf -R $G/hg38_chr17_chrX.upper.fa -A grch38 -D 50 -M 0 > out/sai38_D50.log 2>&1
echo "SpliceAI grch38 rc=$? tagged=$(grep -c 'SpliceAI=' out/sai38_D50.vcf)"
micromamba run -n as-pangolin pangolin data/panel_grch37.vcf $AS/public-data/derived/X.fa $AS/public-data/derived/chrX_GRCh37_ensembl.gffutils.db out/pang37_mF -d 50 -m False > out/pang37_mF.log 2>&1
echo "Pangolin grch37 rc=$? tagged=$(grep -c 'Pangolin=' out/pang37_mF.vcf)"
