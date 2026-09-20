#!/bin/bash
# INPUT 5b (stress, part 2, REGRESSION + extension): verify the fixed SKILL's "Sort Order Required by Downstream Tool" table
# with the real tools. Rows executed: samtools index, fixmate (-n and -N), markdup, Picard (-n, -N), GATK MarkDuplicatesSpark,
# bcftools mpileup, GATK HaplotypeCaller, umi_tools dedup, fgbio GroupReadsByUmi, HTSeq (incl. the quoted 2820 / 5599).
# NOT installed (dagger rows): featureCounts, Salmon, RSEM, Sniffles, cuteSV, Manta, Delly, Mutect2(run not attempted), fgbio CallMolecularConsensusReads.
# NOTE all name-sort outputs use distinct names (case-insensitive fs: n.bam == N.bam).
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in5b; rm -rf $W; mkdir -p $W; cd $W
H=$PD/human/test.paired_end.sorted.bam; G=$PD/human/genome.fasta; PL=$PD/derived/planted_dups.bam
samtools sort -n -o ns_nat.bam $H; samtools sort -N -o ns_asc.bam $H
samtools sort -n -o pl_nat.bam $PL; samtools sort -N -o pl_asc.bam $PL

echo "### 5b.1 samtools index (row: coordinate, hard requirement)"
samtools index ns_nat.bam 2> idx1.err; echo "rc=$? msg: $(head -1 idx1.err)"
test -s ns_nat.bam.bai && echo "  [FAIL] index written for name-sorted BAM" || echo "  [PASS] index refused for name-sorted BAM"

echo "### 5b.2 samtools fixmate -m / markdup (rows)"
samtools markdup $PL md_nofix.bam 2> md_nofix.err; echo "  markdup on coordinate BAM WITHOUT fixmate -m: rc=$? msg: $(head -1 md_nofix.err)"
for o in nat asc; do
  samtools fixmate -m pl_$o.bam pl_fix_$o.bam && samtools sort -o pl_fix_cs_$o.bam pl_fix_$o.bam && samtools markdup pl_fix_cs_$o.bam md_$o.bam
  eq "fixmate row: -$o input -> markdup dup reads" "$(samtools view -c -f 1024 md_$o.bam)" "100"
done
samtools markdup pl_fix_nat.bam md_on_ns.bam 2> md_ns.err; echo "  markdup on NAME-sorted fixmate'd: rc=$? msg: $(head -1 md_ns.err)"

echo "### 5b.3 Picard MarkDuplicates / ValidateSamFile row: coordinate, or queryname in -N (ASCII); -n output rejected"
picard MarkDuplicates -I $PL -O pic_cs.bam -M pic_cs.txt --VALIDATION_STRINGENCY SILENT > pic_cs.log 2>&1; eq "Picard on coordinate: dup reads" "$(samtools view -c -f 1024 pic_cs.bam)" "100"
picard MarkDuplicates -I pl_nat.bam -O pic_nat.bam -M pic_nat.txt --VALIDATION_STRINGENCY SILENT > pic_nat.log 2>&1; rc=$?
echo "  Picard on -n: rc=$rc $(grep -a -m1 'Exception in thread' pic_nat.log | cut -c1-200)"
[ $rc -ne 0 ] && echo "  [PASS] -n rejected (rc=$rc)" || echo "  [FAIL] -n accepted"
picard MarkDuplicates -I pl_asc.bam -O pic_asc.bam -M pic_asc.txt --VALIDATION_STRINGENCY SILENT > pic_asc.log 2>&1; rc=$?
echo "  Picard on -N: rc=$rc dup reads $(samtools view -c -f 1024 pic_asc.bam 2>/dev/null)"; eq "Picard on -N: dup reads" "$(samtools view -c -f 1024 pic_asc.bam)" "100"
echo "-- Picard on the REAL human BAM name-sorted with -n (real names) vs -N"
picard MarkDuplicates -I ns_nat.bam -O hp_nat.bam -M hp_nat.txt --VALIDATION_STRINGENCY SILENT > hp_nat.log 2>&1; echo "  real -n: rc=$? $(grep -a -m1 -o 'Alignments added out of order' hp_nat.log)"
picard MarkDuplicates -I ns_asc.bam -O hp_asc.bam -M hp_asc.txt --VALIDATION_STRINGENCY SILENT > hp_asc.log 2>&1; echo "  real -N: rc=$? dup reads $(samtools view -c -f 1024 hp_asc.bam 2>/dev/null) (coordinate-input Picard: $(samtools view -c -f 1024 <(picard MarkDuplicates -I $H -O /dev/stdout -M hp_cs.txt --VALIDATION_STRINGENCY SILENT 2>/dev/null) 2>/dev/null))"

echo "### 5b.4 GATK MarkDuplicatesSpark (row: coordinate or queryname) local[2]"
for kind in "cs:$PL" "nat:pl_nat.bam" "asc:pl_asc.bam"; do
  k=${kind%%:*}; f=${kind#*:}
  timeout 400 gatk --java-options -Xmx2g MarkDuplicatesSpark -I $f -O gatk_$k.bam --spark-master local[2] > gatk_$k.log 2>&1; rc=$?
  echo "  input $k: rc=$rc dup reads flagged: $(samtools view -c -f 1024 gatk_$k.bam 2>/dev/null) $(grep -a -E 'A USER ERROR|Exception' gatk_$k.log | head -1 | cut -c1-160)"
done

echo "### 5b.5 bcftools mpileup (row: coordinate; name-sorted stops with 'The input is not sorted')"
bcftools mpileup -f $G $H 2> mp_cs.err | bcftools call -mv -Ov 2>/dev/null | grep -av '^#' > mp_cs.vcf; echo "  coordinate-sorted: variant records=$(wc -l < mp_cs.vcf)"
bcftools mpileup -f $G ns_nat.bam 2> mp_ns.err > mp_ns.vcf; rc=$?; echo "  name-sorted: rc=$rc msg: $(grep -a 'not sorted' mp_ns.err | head -1)"
grep -a -q 'The input is not sorted' mp_ns.err && echo "  [PASS] SKILL quote matches" || echo "  [FAIL] message differs"

echo "### 5b.6 GATK HaplotypeCaller (row: coordinate and indexed)"
timeout 400 gatk --java-options -Xmx2g HaplotypeCaller -R $G -I ns_nat.bam -O hc_ns.vcf > hc_ns.log 2>&1; echo "  name-sorted: rc=$?  $(grep -a -E 'A USER ERROR' hc_ns.log | head -1 | cut -c1-200)"
timeout 400 gatk --java-options -Xmx2g HaplotypeCaller -R $G -I $H -O hc_cs.vcf > hc_cs.log 2>&1; echo "  coordinate-sorted: rc=$?  vcf records=$(grep -av '^#' hc_cs.vcf 2>/dev/null | wc -l)"

echo "### 5b.7 umi_tools dedup (row: coordinate with index)"
samtools sort -o umi_cs.bam $PD/human/test.paired_end.umi_unsorted.bam
umi_tools dedup -I umi_cs.bam --paired --umi-tag=RX --extract-umi-method=tag -S ud_noidx.bam -L ud_noidx.log > /dev/null 2> ud_noidx.err; echo "  sorted but NOT indexed: rc=$? $(grep -a -E 'Error|error|index' ud_noidx.err | head -1 | cut -c1-160)"
samtools index umi_cs.bam
umi_tools dedup -I umi_cs.bam --paired --umi-tag=RX --extract-umi-method=tag -S ud.bam -L ud.log > /dev/null 2> ud.err; echo "  sorted + indexed: rc=$? records $(nrec umi_cs.bam) -> $(nrec ud.bam 2>/dev/null)  (TOOLS.md reference: 15788 -> 5689)"
eq "umi_tools dedup output records" "$(nrec ud.bam)" "5689"

echo "### 5b.8 fgbio GroupReadsByUmi (row: any order accepted; template-coordinate recommended; run fixmate -m / SetMateInformation first)"
fgbio GroupReadsByUmi --help 2>&1 | grep -a -i -E 'template-coordinate|any order|sort' | head -4
samtools sort -n -o umi_qn.bam $PD/human/test.paired_end.umi_unsorted.bam
fgbio SetMateInformation -i umi_qn.bam -o umi_smi.bam > smi.log 2>&1; echo "  SetMateInformation rc=$?"
grp() { fgbio GroupReadsByUmi -i "$1" -o "$2" --strategy=adjacency --edits=1 --raw-tag=RX > "$2.log" 2>&1; echo "  $3: rc=$? MI groups=$(samtools view "$2" 2>/dev/null | grep -ao 'MI:Z:[^[:space:]]*' | sort -u | wc -l) records=$(nrec "$2" 2>/dev/null) $(grep -a -E 'ERROR|Exception|must be' "$2.log" | head -1 | cut -c1-160)"; }
grp umi_smi.bam g_unsorted.bam "unsorted"
samtools sort -o umi_smi_cs.bam umi_smi.bam; grp umi_smi_cs.bam g_coord.bam "coordinate-sorted"
samtools sort --template-coordinate -o umi_smi_tc.bam umi_smi.bam; grp umi_smi_tc.bam g_tc.bam "template-coordinate-sorted"
samtools sort -n -o umi_smi_nat.bam umi_smi.bam; grp umi_smi_nat.bam g_nat.bam "name-sorted -n"
echo "-- SKILL: fgbio needs fixmate -m / SetMateInformation first: GroupReadsByUmi on samtools fixmate -m output:"
samtools fixmate -m umi_qn.bam umi_fm.bam; grp umi_fm.bam g_fm.bam "fixmate -m output (no MQ tag)"

echo "### 5b.9 HTSeq (row: '-r pos coordinate / -r name name-sorted; -r name on a coordinate-sorted file over-counts (5599 vs 2820 on the test BAM); -p is --samout-format')"
printf 'chr22\tsynth\texon\t1\t40001\t.\t+\t.\tgene_id "G1"; transcript_id "T1";\n' > one.gtf
htseq-count --help 2>&1 | grep -a -E '^\s+-p|--samout-format|--order' | head -4
run_hs() { # $1 label $2 -r $3 bam
  htseq-count -f bam -r $2 -s no -t exon $3 one.gtf > hs.txt 2> hs.err; echo "  $1: G1=$(grep -a '^G1' hs.txt | cut -f2) __no_feature=$(grep -a __no_feature hs.txt | cut -f2) __alignment_not_unique=$(grep -a __alignment_not_unique hs.txt | cut -f2) warn=$(grep -a -c -i 'warn' hs.err)"; }
echo "-- test BAM = human DNA PE BAM (2819 proper pairs):"
run_hs "coordinate -r pos" pos $H
run_hs "name(-n) -r name" name ns_nat.bam
run_hs "coordinate -r name (wrong)" name $H
echo "-- RNA PE BAM:"
R=$PD/human/test.rna.paired_end.sorted.bam; samtools sort -n -o rna_nat.bam $R
run_hs "coordinate -r pos" pos $R
run_hs "name(-n) -r name" name rna_nat.bam
run_hs "coordinate -r name (wrong)" name $R
echo "-- default -s yes on DNA BAM:"
htseq-count -f bam -r pos -t exon $H one.gtf 2>/dev/null | grep -a '^G1'
summary
