#!/bin/bash
# Input 5: the shipped example script, unmodified, from a clean copy. TP53 VCF (regression of the pre-fix run) then the auditor GRCh38 panel + a REF-mismatch record.
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
rm -rf ex_run && mkdir ex_run && cp skill/examples/*.py ex_run/ && cp data/tp53_grch38.vcf data/panel_grch38_auditor.vcf ex_run/
FA=/mnt/openscience/as-spvp-scratch/g38/hg38_chr17_chrX.upper.fa
cd ex_run
echo "=== TP53 VCF (3 records incl. the pre-fix wrong-REF usage-guide record)"
micromamba run -n as-spliceai python spliceai_clingen_classify.py tp53_grch38.vcf $FA --build grch38 --out-prefix tp53 2>&1 | grep -av "cuda\|cpu_feature\|To enable\|absl\|^I0000\|^W0000\|pkg_resources\|^$"
cat tp53_classified.tsv
echo "=== auditor panel + wrong-REF record"
cp panel_grch38_auditor.vcf panel_mm.vcf
printf 'chrX\t101399747\tGLA_wrongREF\tA\tG\t.\t.\t.\n' >> panel_mm.vcf
micromamba run -n as-spliceai python spliceai_clingen_classify.py panel_mm.vcf $FA --build grch38 --out-prefix panel 2>&1 | grep -av "cuda\|cpu_feature\|To enable\|absl\|^I0000\|^W0000\|pkg_resources\|^$"
cat panel_classified.tsv | cut -f1-3,7-12
