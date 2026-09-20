#!/bin/bash
# Real-data follow-up: same FLAIR pipeline but from the alignment WITHOUT -uf (SKILL's ONT-unstranded recipe), to isolate the -uf effect.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/flair_test
O=$R/out/real_flair; cd $O
cp $P/genome.fa $P/genome.fa.fai .
LR="micromamba run -n as-lr"
$LR bedtools bamtobed -bed12 -i real_k14.bam > real_k14.bed; wc -l real_k14.bed
$LR flair correct -q real_k14.bed -f basic.annotation.gtf --junction_tab basic.shortread_junctions.tab -o rk -t 8 > rk.log 2>&1; echo "k14 correct rc=$? corrected=$(wc -l < rk_all_corrected.bed) inconsistent=$(wc -l < rk_all_inconsistent.bed)"
$LR flair collapse --query rk_all_corrected.bed --reads basic.reads.fa --genome genome.fa --gtf basic.annotation.gtf --output rkcoll --threads 8 --generate_map > rkcoll.log 2>&1; echo "collapse rc=$? isoforms=$(grep -c '>' rkcoll.isoforms.fa)"
$LR flair collapse --query rk_all_corrected.bed --reads basic.reads.fa --genome genome.fa --gtf basic.annotation.gtf --output rkcoll_hq --threads 8 --generate_map -p basic.promoter_regions.bed --gene_tss > rkcoll_hq.log 2>&1; echo "collapse+promoters rc=$? isoforms=$(grep -c '>' rkcoll_hq.isoforms.fa)"
echo "flair-native align: strand column split"; cut -f6 falign.bed | sort | uniq -c
echo "bamtobed(k14) strand split"; cut -f6 real_k14.bed | sort | uniq -c
echo "bamtobed(uf)  strand split"; cut -f6 real.bed | sort | uniq -c
echo "--- flair align help (what minimap2 args it uses)"; grep -n -i "minimap2\|-uf\|splice" $R/logs/flair_align_help.txt | head
rm -f genome.fa genome.fa.fai
