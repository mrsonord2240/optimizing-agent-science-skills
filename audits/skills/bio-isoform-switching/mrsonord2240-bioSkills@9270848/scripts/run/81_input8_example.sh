#!/bin/bash
# INPUT 8D: shipped example (from the copy) in real-data mode on the NEW unbalanced 4v7 set with a batch covariate column in the metadata.
export PYTHONIOENCODING=utf-8
R=F:/OpenScience/audit-envs/alternative-splicing/r.sh
RUN=F:/OpenScience/audits/bio-isoform-switching/run
N=$RUN/data/new1
cd $RUN/work; rm -rf ex_new; mkdir ex_new
( time bash $R $RUN/skill/examples/isoform_switch_analysis.R $N/salmon_quant $N/annotation.gtf $N/transcripts.fa $N/sample_metadata.tsv ex_new/out ) > ../81_input8_example.log 2>&1
grep -E "Significant|ORF origin|Consequence types|Plot|Error|stop|fewer|real" ../81_input8_example.log
ls -la ex_new/out | head
