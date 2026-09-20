#!/bin/bash
# Is the example's transcript/exon-only awk step necessary? Feed the FULL IsoQuant GTF (gene/CDS/UTR/start_codon rows) to sqanti3_filter.py rules.
R=/mnt/openscience/audits/bio-long-read-splicing/run; cd $R/out/ex_hifi/out; rm -rf nofilter_dir
sqanti3_filter.py rules --sqanti_class sqanti3/sqanti3_classification.txt --filter_gtf isoquant/ctrl1/ctrl1.transcript_models.gtf -o nf -d nofilter_dir --skip_report > nofilter.log 2>&1; echo "rc=$?"
grep -a -E "Error|Assertion|raise" nofilter.log | tail -3 | cut -c1-200; ls nofilter_dir 2>/dev/null | tr '\n' ' '; echo; ls nofilter_dir/*filtered.gtf 2>/dev/null || echo "(no filtered GTF written)"
