#!/bin/bash
# Root-cause check: does sqanti3_filter.py accept IsoQuant's transcript_models.gtf once the 'gene' rows are removed?
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
cd /mnt/openscience/audits/bio-long-read-splicing/run/out/example/longread_output_sample
G=isoquant/sample/sample.transcript_models.gtf
cut -f3 $G | grep -v '^#' | sort | uniq -c
awk -F'\t' '$0 ~ /^#/ || $3 != "gene"' $G > tm_nogene.gtf
micromamba run -n as-sqanti sqanti3_filter.py rules --sqanti_class sqanti3/sqanti3_classification.txt --filter_gtf tm_nogene.gtf --output f_nogene --dir f_nogene_dir --skip_report > f_nogene.log 2>&1; echo "filter (no gene rows) rc=$?"
ls -la f_nogene_dir/*.gtf
