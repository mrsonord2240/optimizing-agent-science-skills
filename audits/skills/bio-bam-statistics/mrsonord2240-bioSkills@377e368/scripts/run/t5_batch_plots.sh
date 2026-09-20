#!/bin/bash
# INPUT 5 (Stress; regression of pre-fix input 5): block-006 batch loop on 15 BAMs (real, synthetic, edge incl. empty/uBAM/QC-fail), then plot-bamstats (block 012), MultiQC (block 013), stats -r GC-depth (table row)
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work
D=/mnt/openscience/audit-envs/alignment-files/public-data
rm -rf batch; mkdir batch; cd batch
cp $D/human/test.paired_end.sorted.bam human_pe.bam; cp $D/human/test.paired_end.sorted.bam.bai human_pe.bam.bai;  cp $D/human/test.rna.paired_end.sorted.bam human_rna.bam
cp $D/derived/planted_dups.bam planted_dups.bam;      cp $D/1000g/HG00349.chr20_1400000-1500000.bam g1000.bam
cp $D/sarscov2/sars-cov-2_v5.3.2.nanopore.bam artic_nanopore.bam; cp $D/sarscov2/test.single_end.sorted.bam sc2_se.bam
cp $R/data/synth.bam synthetic_flags.bam; cp $R/data/empty.bam empty.bam; cp $R/data/rf.bam rf.bam
for n in unmapped_only ubam_no_sq supp_sec_heavy qcfail_heavy all_qcfail mixed_pairs; do cp $R/data/edge/$n.bam edge_$n.bam; done
ls *.bam | wc -l
echo "=== block 006 verbatim"; bash $R/blocks/006_bash.sh; column -t summary.tsv
echo "=== rows vs hand counts (truth.py)"; python $R/t5_batch_check.py summary.tsv
echo "=== plot-bamstats (block 012) on human BAM"; samtools stats human_pe.bam > stats.txt; plot-bamstats -p plots/ stats.txt 2>&1 | tail -2; ls plots/*.png | wc -l; ls plots | head -3
echo "=== multiqc (block 013 verbatim, directory holding stats/flagstat/idxstats text)"
mkdir -p mq && cd mq && cp ../stats.txt human.stats && samtools flagstat ../human_pe.bam > human.flagstat && samtools idxstats ../human_pe.bam > human.idxstats
bash $R/blocks/013_bash.sh 2>&1 | grep -E 'Found|samtools|Report|ERROR' | head -8
ls multiqc_out; python - <<'PY'
import re
h=open('multiqc_out/multiqc_report.html',encoding='utf-8').read()
print('report bytes', len(h), '| mentions: ', {k: len(re.findall(k,h,re.I)) for k in ['Samtools','Flagstat','Idxstats','human']})
PY
grep -c . multiqc_out/multiqc_data/multiqc_samtools_stats.txt multiqc_out/multiqc_data/multiqc_samtools_flagstat.txt; grep -m3 -i 'reads_mapped\|total_passed\|mapped_passed' multiqc_out/multiqc_data/multiqc_samtools_flagstat.txt | cut -c1-200; cd ..
echo "=== stats -r ref (table row: '-r ref.fa for GC-depth') GCD lines without / with -r"
samtools stats human_pe.bam | grep -c '^GCD'; samtools stats -r $D/human/genome.fasta human_pe.bam | grep -c '^GCD'
samtools stats -r $D/human/genome.fasta human_pe.bam | grep '^GCD' | head -2
samtools stats --GC-depth 1000 -r $D/human/genome.fasta human_pe.bam | grep -c '^GCD'
echo "=== samtools stats CRAM: skill says 'CRAM needs --reference ref.fa'"
samtools stats --reference $D/human/genome.fasta $D/human/test.paired_end.sorted.cram | grep '^SN' | sed -n '1,8p' | cut -f2-3
samtools stats $D/human/test.paired_end.sorted.cram 2>&1 | head -3
echo "=== GC-depth on the 1000G slice (100 kb): with vs without -r (padded fasta)"
G=$D/1000g/HG00349.chr20_1400000-1500000.bam
samtools stats --GC-depth 20000 $G | grep '^GCD' | head -3
samtools stats --GC-depth 20000 -r $D/1000g/chr20_padded_1500000.fa $G | grep '^GCD' | head -3
