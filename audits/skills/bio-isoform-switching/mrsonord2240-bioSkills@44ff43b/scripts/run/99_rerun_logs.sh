#!/bin/bash
# re-run the diagnostic scripts whose output was only shown interactively, saving logs (real GTF/FASTA staged first)
R=/f/OpenScience/audit-envs/alternative-splicing/r.sh
RUN=/f/OpenScience/audits/bio-isoform-switching/run
PD=/f/OpenScience/audit-envs/alternative-splicing/public-data
stage_real() { cp $PD/rnasplice/reference/genes_chrX.gtf $RUN/work/annotation.gtf; cp $PD/derived/chrX_tx.fa $RUN/work/transcripts.fa; }
for s in 21_samples_mask 31_dmfilter_defaults 40a_input4_prep 40a3_ptc_independent; do $R $RUN/$s.R 2>&1 | tr -d '\r' > $RUN/$s.log; done
for s in 35a2_debug_reduce 35a3_counts_scaling 35a4_scaling_deep 35a5_scaling_pvals 35a6_scaledtpm_hypothesis 36d_longest_orf_vs_biotype; do stage_real; $R $RUN/$s.R 2>&1 | tr -d '\r' > $RUN/$s.log; done
echo done
