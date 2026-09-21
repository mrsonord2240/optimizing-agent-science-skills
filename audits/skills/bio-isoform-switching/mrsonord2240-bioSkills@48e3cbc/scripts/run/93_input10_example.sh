#!/bin/bash
# INPUT 10C: shipped example (from the copy) in real-data mode on the odd-ID 3 v 5 set (IDs "1-ctrl", "trt.1-b").
export PYTHONIOENCODING=utf-8
R=F:/OpenScience/audit-envs/alternative-splicing/r.sh
RUN=F:/OpenScience/audits/bio-isoform-switching/run; N=$RUN/data/odd_3v5
cd $RUN/work; rm -rf ex_odd; mkdir ex_odd
( time bash $R $RUN/skill/examples/isoform_switch_analysis.R $N/salmon_quant $N/annotation.gtf $N/transcripts.fa $N/sample_metadata.tsv ex_odd/out ) > ../93_input10_example.log 2>&1
grep -E "Significant|ORF origin|Consequence types|Plot|Error|stop|fewer|real" ../93_input10_example.log; ls -la ex_odd/out | head
