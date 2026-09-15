#!/bin/bash
# Input 3 (Edge): "Several of my BRCA1 hits say 'Conflicting classifications'. Break the conflict down by call and
# star rating, and keep only assertions with >=2 stars evaluated in the last 36 months." Live ClinVar (WSL, network),
# shipped examples/clinvar_query.py functions (cyvcf2 import requires WSL). Real public data, no individuals.
set -uo pipefail
export PATH=/tmp/vaca/env/bin:$PATH
URL=https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
bcftools view -r 17:43044295-43125483 -i 'INFO/CLNSIG~"Conflicting"' $URL 2>/dev/null | bcftools query -f '%ID\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\t%INFO/CLNSIGCONF\n' | head -6 > conflicts.tsv
cat conflicts.tsv
python run.py
