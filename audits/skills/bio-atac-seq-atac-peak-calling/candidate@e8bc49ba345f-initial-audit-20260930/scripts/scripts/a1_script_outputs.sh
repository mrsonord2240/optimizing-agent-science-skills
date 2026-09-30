#!/bin/bash
# Independent checks of the Skill script's outputs (run by smoke_script.sh in tooling phase, identical bytes) + disjoint pseudorep comparison.
source /mnt/openscience/audit-envs/bio-atac-seq-atac-peak-calling/wsl_env.sh
O=$APC/run/script_default
S=/mnt/openscience/wt/atac-atac-peak-calling/skills/bio-atac-seq-atac-peak-calling/scripts/call_atac_peaks.sh
echo "== dirs"; ls $O/*/ | head -80
echo "== peak counts"; for f in rep1/rep1 rep2/rep2 pooled/pooled psr1_1/rep1_psr1 psr1_2/rep1_psr2; do echo $f $(wc -l < $O/${f}_peaks.narrowPeak); done
echo "== idr counts"; wc -l $O/idr/*.idr $O/idr/true_reps.no_blacklist.bed
echo "== pooled/psr2 referenced downstream?"; grep -n "pooled\|psr2_" $S
echo "== pseudorep read overlap (rep1 halves)"
samtools view $O/psr1_1/rep1.psr1.bam | cut -f1 | sort -u > $O/h1.names
samtools view $O/psr1_2/rep1.psr2.bam | cut -f1 | sort -u > $O/h2.names
tot=$(samtools view -c -F 4 /mnt/openscience/audit-envs/atac-seq/public-data/encode/GM12878_rep1_filtered.chr1_1-30000000.bam)
echo total_reads=$tot h1_names=$(wc -l < $O/h1.names) h2_names=$(wc -l < $O/h2.names) shared_names=$(comm -12 $O/h1.names $O/h2.names | wc -l)
echo "== head of idr output"; head -2 $O/idr/true_reps.idr | cut -f1-13
