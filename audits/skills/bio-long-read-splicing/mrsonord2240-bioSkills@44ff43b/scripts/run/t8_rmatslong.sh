#!/bin/bash
# Input 6/7 (part 1): SKILL.md "rMATS-long" ASM-mode workflow, every command with the SKILL's flags, on SYNTHETIC 3 v 3 BAMs (planted GA.1:GA.2 = 70:30 vs 20:80).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
D=$R/data/synth
O=$R/out/rmatslong; rm -rf $O; mkdir -p $O; cd $O
for s in ctrl1 ctrl2 ctrl3 trt1 trt2 trt3; do cp $R/out/flair/$s.bam $R/out/flair/$s.bam.bai .; done
cp $D/ref.gtf annotation.gtf
RL="rmats-long"
set -x
$RL organize_gene_info_by_chr.py --gtf annotation.gtf --out-dir gene_info_by_chr/ > s1.log 2>&1; echo "s1 rc=$?"
mkdir -p alignment_info
for bam in *.bam; do
    $RL simplify_alignment_info.py --in-file "$bam" --out-tsv "alignment_info/${bam%.bam}.tsv" > s2_${bam%.bam}.log 2>&1; echo "s2 ${bam} rc=$?"
done
: > samples.tsv
for s in ctrl1 ctrl2 ctrl3 trt1 trt2 trt3; do printf "%s\t%s\n" $s alignment_info/$s.tsv >> samples.tsv; done
$RL organize_alignment_info_by_gene_and_chr.py --gtf-dir gene_info_by_chr/ --out-dir organized/ --samples-tsv samples.tsv > s3.log 2>&1; echo "s3 rc=$?"
$RL detect_splicing_events.py --align-dir organized/ --gtf-dir gene_info_by_chr/ --out-dir events/ > s4.log 2>&1; echo "s4 rc=$?"
$RL create_gtf_from_asm_definitions.py --event-dir events/ --out-gtf asm.gtf > s5.log 2>&1; echo "s5 rc=$?"
$RL count_reads_for_asms.py --align-dir organized/ --event-dir events/ --gtf-dir gene_info_by_chr/ --out-dir asm_counts/ > s6.log 2>&1; echo "s6 rc=$?"
echo 'ctrl1,ctrl2,ctrl3' > group1.txt
echo 'trt1,trt2,trt3' > group2.txt
$RL rmats_long.py --group-1 group1.txt --group-2 group2.txt --event-dir events/ --asm-counts-dir asm_counts/ --align-dir organized/ --gtf-dir gene_info_by_chr/ --out-dir rmats_long_output/ --adj-pvalue 0.05 --delta-proportion 0.05 --average-reads-per-group 10 > s7.log 2>&1; echo "s7 rc=$?"
set +x
tail -5 s7.log | cut -c1-250
echo "--- outputs"; find rmats_long_output -maxdepth 2 -type f | head -30
echo "--- asm counts"; ls asm_counts | head; head -5 asm_counts/* 2>/dev/null | head -20
