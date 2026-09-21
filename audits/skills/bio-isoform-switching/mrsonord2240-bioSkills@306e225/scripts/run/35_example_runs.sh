#!/bin/bash
# Shipped example run from the COPY in run/skill/examples: (a) built-in demo, (b) real chrX 2 GBR v 2 YRI (metadata rows shuffled),
# (c) real chrX with mixed-population labels (GBR+YRI v GBR+YRI: should not be a strong signal).
export PYTHONIOENCODING=utf-8
R=F:/OpenScience/audit-envs/alternative-splicing/r.sh
RUN=F:/OpenScience/audits/bio-isoform-switching/run
PD=F:/OpenScience/audit-envs/alternative-splicing/public-data
EX=$RUN/skill/examples/isoform_switch_analysis.R
cd $RUN/work
echo "### (a) demo"; ( time bash $R $EX ) > ../35a_demo.log 2>&1
grep -E "DEMO|Significant|ORF origin|Consequence types|NMD-sensitive|Plot|Error|Warning" ../35a_demo.log | head -20
echo "### (b) real chrX"
mkdir -p ex_real/salmon
for s in ERR188383 ERR188428 ERR188454 ERR204916; do mkdir -p ex_real/salmon/$s; cp $PD/rnasplice/salmon/$s/quant.sf ex_real/salmon/$s/quant.sf; done
cp $PD/rnasplice/reference/genes_chrX.gtf ex_real/annotation.gtf; cp $PD/derived/chrX_tx.fa ex_real/transcripts.fa
printf 'sample_id\tcondition\nERR204916\tYRI\nERR188383\tGBR\nERR188454\tYRI\nERR188428\tGBR\n' > ex_real/meta.tsv
( time bash $R $EX ex_real/salmon ex_real/annotation.gtf ex_real/transcripts.fa ex_real/meta.tsv ex_real/out ) > ../35b_real.log 2>&1
grep -E "Significant|ORF origin|Consequence types|Plot|Error|Warning|stop|switching|Top" ../35b_real.log | head -20; ls -la ex_real/out | head
echo "### (c) real chrX mixed labels"
printf 'sample_id\tcondition\nERR188383\tA\nERR188454\tA\nERR188428\tB\nERR204916\tB\n' > ex_real/meta_mixed.tsv
( time bash $R $EX ex_real/salmon ex_real/annotation.gtf ex_real/transcripts.fa ex_real/meta_mixed.tsv ex_real/out_mixed ) > ../35c_mixed.log 2>&1
grep -E "Significant|No switches|Error|Warning|stop" ../35c_mixed.log | head
echo "### (d) bad metadata (missing sample)"
printf 'sample_id\tcondition\nERR188383\tGBR\nERR188454\tYRI\nERR188428\tGBR\n' > ex_real/meta_bad.tsv
bash $R $EX ex_real/salmon ex_real/annotation.gtf ex_real/transcripts.fa ex_real/meta_bad.tsv ex_real/out_bad > ../35d_badmeta.log 2>&1; grep -E "Error|only in" ../35d_badmeta.log
