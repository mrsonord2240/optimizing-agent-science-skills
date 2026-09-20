#!/bin/bash
# Input 7 (part b): fgbio commands from SKILL.md 'UMI-Aware Deduplication' on the real UMI BAM (fgbio 4.1.1)
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W/in07
U=$D/test.paired_end.umi_unsorted.bam
strip() { sed 's/\x1b\[[0-9;]*m//g'; }
echo "### 7f. fgbio --help flags (ANSI stripped)"
for t in AnnotateBamWithUmis GroupReadsByUmi CallMolecularConsensusReads CallDuplexConsensusReads; do echo "-- $t"; fgbio $t --help 2>&1 | strip | grep -E '^(-i|-o|-f|-s|-e|-M|-t|-1|--input|--output|--fastq|--strategy|--edits|--min-reads|--raw-tag|--umi-tag|--assign-tag)' | cut -c1-110; done
echo "### 7g. GroupReadsByUmi straight on the raw unsorted UMI BAM, SKILL.md flags (--strategy=adjacency --edits=1)"
fgbio GroupReadsByUmi -i $U -o g_raw.bam --strategy=adjacency --edits=1 2>&1 | strip | tail -3; echo "  exit=${PIPESTATUS[0]}  records: $(samtools view -c g_raw.bam 2>&1 | tail -1)"
echo "### 7h. GroupReadsByUmi on samtools fixmate -m output (the Skill's own pipeline order)"
fgbio GroupReadsByUmi -i u.fmcs.bam -o g_fm.bam --strategy=adjacency --edits=1 2>&1 | strip | grep -iE 'error|exception|MQ|Grouped|Wrote' | head -3; echo "  exit=${PIPESTATUS[0]}"
echo "### 7i. with fgbio SetMateInformation first (input must be queryname-sorted: u.ns.bam from in07_umi.sh), then adjacency"
fgbio SetMateInformation -i u.ns.bam -o smi.bam 2>&1 | strip | tail -1
fgbio GroupReadsByUmi -i smi.bam -o g_adj.bam --strategy=adjacency --edits=1 2>&1 | strip | tail -2; echo "  records $(samtools view -c g_adj.bam); MI groups: $(samtools view g_adj.bam | grep -o 'MI:Z:[0-9/AB]*' | sort -u | wc -l); MI with /A|/B suffix: $(samtools view g_adj.bam | grep -c 'MI:Z:[0-9]*/[AB]')"
echo "### 7j. CallMolecularConsensusReads on adjacency groups (SKILL.md flags: --min-reads=1)"
fgbio CallMolecularConsensusReads -i g_adj.bam -o cons.bam --min-reads=1 2>&1 | strip | tail -3; echo "  exit=${PIPESTATUS[0]} consensus records: $(samtools view -c cons.bam)"
echo "### 7k. SKILL.md 'or for duplex': CallDuplexConsensusReads on the SAME adjacency-grouped BAM (SKILL.md flag form '--min-reads 1 1 0')"
fgbio CallDuplexConsensusReads -i g_adj.bam -o duplex_bad.bam --min-reads 1 1 0 2>&1 | strip | tail -4; echo "  exit=${PIPESTATUS[0]} duplex consensus records: $(samtools view -c duplex_bad.bam 2>&1 | tail -1)"
echo "### 7l. same but grouped with --strategy=paired (what duplex calling needs)"
fgbio GroupReadsByUmi -i smi.bam -o g_pair.bam --strategy=paired --edits=1 2>&1 | strip | tail -2; echo "  records $(samtools view -c g_pair.bam); MI with /A|/B suffix: $(samtools view g_pair.bam | grep -c 'MI:Z:[0-9]*/[AB]')"
fgbio CallDuplexConsensusReads -i g_pair.bam -o duplex_ok.bam --min-reads 1 1 0 2>&1 | strip | tail -3; echo "  exit=${PIPESTATUS[0]} duplex consensus records: $(samtools view -c duplex_ok.bam 2>&1 | tail -1)"
echo "### 7m. AnnotateBamWithUmis (-i -f -o) with a synthetic UMI fastq built from the RX tags"
samtools view smi.bam | awk '{for(i=12;i<=NF;i++) if($i ~ /^RX:Z:/){u=substr($i,6); gsub("-","",u); if(!($1 in seen)){seen[$1]=1; q=u; gsub(".","I",q); print "@"$1"\n"u"\n+\n"q}}}' > umi.fastq
echo "  umi.fastq reads: $(($(wc -l < umi.fastq)/4))"
samtools view -h -o /dev/stdout smi.bam | sed 's/\tRX:Z:[ACGT-]*//' | samtools view -b -o raw_noRX.bam -
fgbio AnnotateBamWithUmis -i raw_noRX.bam -f umi.fastq -o annotated.bam 2>&1 | strip | tail -2; echo "  exit=${PIPESTATUS[0]} annotated records with RX: $(samtools view annotated.bam | grep -c 'RX:Z')"
