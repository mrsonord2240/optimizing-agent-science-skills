#!/bin/bash
# INPUT 5b (stress, part 2): verify the SKILL's "Sort Order Required by Downstream Tool" table with the real tools.
# Rows executed: samtools index, fixmate, markdup, bcftools mpileup, GATK HaplotypeCaller, GATK MarkDuplicatesSpark,
#   Picard MarkDuplicates (context), umi_tools dedup, fgbio GroupReadsByUmi, HTSeq.  Not installed/not executed:
#   featureCounts, Salmon, RSEM, Sniffles, cuteSV, Manta, Delly, fgbio CallMolecularConsensusReads (help text only).
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in5b; rm -rf $W; mkdir -p $W; cd $W
H=$PD/human/test.paired_end.sorted.bam; G=$PD/human/genome.fasta; PL=$PD/derived/planted_dups.bam
samtools sort -n -o ns.bam $H
samtools sort -n -o pl_ns.bam $PL

echo "### 5b.1 samtools index (row: coordinate, hard requirement)"
samtools index ns.bam 2> idx1.err; echo "rc=$? msg: $(head -2 idx1.err | tr '\n' '|')"
test -s ns.bam.bai && echo "  [FAIL] index written for name-sorted BAM" || echo "  [PASS] index refused/not written for name-sorted BAM"

echo "### 5b.2 samtools fixmate -m / markdup (rows: name-or-collate ; coordinate after fixmate)"
samtools view -H $PL | head -0
samtools markdup $PL md_nofix.bam 2> md_nofix.err; echo "  markdup on coordinate BAM WITHOUT fixmate -m: rc=$? msg: $(head -2 md_nofix.err | tr '\n' '|')"
samtools fixmate -m pl_ns.bam pl_fix.bam; samtools markdup pl_fix.bam md_ns.bam 2> md_ns.err; echo "  markdup on NAME-sorted (fixmate'd) BAM: rc=$? msg: $(head -2 md_ns.err | tr '\n' '|')"
samtools sort -o pl_fix_cs.bam pl_fix.bam; samtools markdup pl_fix_cs.bam md_cs.bam; eq "markdup on coordinate-sorted fixmate'd: dup reads" "$(samtools view -c -f 1024 md_cs.bam)" "100"

echo "### 5b.3 Picard MarkDuplicates on name-sorted input (context for MarkDuplicatesSpark row)"
picard MarkDuplicates -I pl_ns.bam -O pic_ns.bam -M pic_ns.txt --VALIDATION_STRINGENCY SILENT > pic_ns.log 2>&1; echo "rc=$?"
grep -a -m1 'Exception in thread' pic_ns.log | cut -c1-230
[ -s pic_ns.bam ] && echo "  (partial pic_ns.bam exists: $(samtools view -c -f 1024 pic_ns.bam 2>/dev/null) dup flags)"
samtools sort -N -o pl_N.bam $PL
picard MarkDuplicates -I pl_N.bam -O pic_N.bam -M pic_N.txt --VALIDATION_STRINGENCY SILENT > pic_N.log 2>&1; echo "  Picard on samtools sort -N (ASCII) input: rc=$? dup reads flagged: $(samtools view -c -f 1024 pic_N.bam 2>/dev/null) (100 expected)"
[ "$(samtools view -c -f 1024 pic_N.bam 2>/dev/null)" = "100" ] && echo "  [PASS] Picard MarkDuplicates works on -N (ASCII) name-sorted BAM but CRASHES on -n (natural) output => the SKILL 'sort -n = lexicographic' row is wrong for Picard-type consumers"
echo "-- GATK MarkDuplicatesSpark (row: coordinate or queryname) local[2] on planted BAM, coordinate input:"
timeout 400 gatk --java-options -Xmx2g MarkDuplicatesSpark -I $PL -O gatk_cs.bam --spark-master local[2] > gatk_cs.log 2>&1; echo "  rc=$?"; grep -a -E 'ERROR|Exception|Duplicate|duplicat' gatk_cs.log | head -4
test -s gatk_cs.bam && echo "  dup reads flagged: $(samtools view -c -f 1024 gatk_cs.bam) (100 expected)"
echo "-- ... queryname input (samtools sort -n):"
timeout 400 gatk --java-options -Xmx2g MarkDuplicatesSpark -I pl_ns.bam -O gatk_ns.bam --spark-master local[2] > gatk_ns.log 2>&1; echo "  rc=$?"; grep -a -E 'ERROR|Exception|A USER ERROR' gatk_ns.log | head -3
test -s gatk_ns.bam && echo "  dup reads flagged: $(samtools view -c -f 1024 gatk_ns.bam) (100 expected)"

echo "### 5b.4 bcftools mpileup (row: coordinate) on coordinate vs name-sorted real BAM"
bcftools mpileup -f $G $H 2> mp_cs.err | bcftools call -mv -Ov 2>/dev/null | grep -av '^#' > mp_cs.vcf; echo "  coordinate-sorted: variant records=$(wc -l < mp_cs.vcf)  stderr=$(head -1 mp_cs.err | cut -c1-90)"
bcftools mpileup -f $G ns.bam 2> mp_ns.err > mp_ns.vcf; echo "  name-sorted: rc=$? msg: $(grep -a -v '^\[mpileup\] 1 samples' mp_ns.err | head -2 | tr '\n' '|' | cut -c1-200)"
grep -av '^#' mp_ns.vcf | wc -l | { read n; echo "  name-sorted mpileup VCF data lines: $n (coordinate-sorted gives $(bcftools mpileup -f $G $H 2>/dev/null | grep -av '^#' | wc -l))"; }

echo "### 5b.5 GATK HaplotypeCaller (row: coordinate) name-sorted vs coordinate-sorted"
timeout 400 gatk --java-options -Xmx2g HaplotypeCaller -R $G -I ns.bam -O hc_ns.vcf > hc_ns.log 2>&1; echo "  name-sorted: rc=$?  $(grep -a -E 'A USER ERROR|ERROR' hc_ns.log | head -2 | tr '\n' '|' | cut -c1-260)"
timeout 400 gatk --java-options -Xmx2g HaplotypeCaller -R $G -I $H -O hc_cs.vcf > hc_cs.log 2>&1; echo "  coordinate-sorted: rc=$?  vcf records=$(grep -av '^#' hc_cs.vcf 2>/dev/null | wc -l)"

echo "### 5b.6 umi_tools dedup (row: coordinate with index)"
samtools sort -o umi_cs.bam $PD/human/test.paired_end.umi_unsorted.bam
umi_tools dedup -I umi_cs.bam --paired --umi-tag=RX --extract-umi-method=tag -S ud_noidx.bam -L ud_noidx.log > /dev/null 2> ud_noidx.err; echo "  sorted but NOT indexed: rc=$? $(grep -a -E 'Error|error|index' ud_noidx.err | head -2 | tr '\n' '|' | cut -c1-200)"
samtools index umi_cs.bam
umi_tools dedup -I umi_cs.bam --paired --umi-tag=RX --extract-umi-method=tag -S ud.bam -L ud.log > /dev/null 2> ud.err; echo "  sorted + indexed: rc=$? records $(nrec umi_cs.bam) -> $(nrec ud.bam 2>/dev/null)  (TOOLS.md reference: 15788 -> 5689)"
samtools sort -n -o umi_ns.bam $PD/human/test.paired_end.umi_unsorted.bam
umi_tools dedup -I umi_ns.bam --paired --umi-tag=RX --extract-umi-method=tag -S ud_ns.bam > /dev/null 2> ud_ns.err; echo "  name-sorted (unindexable): rc=$? $(grep -a -E 'Error|error|index' ud_ns.err | head -2 | tr '\n' '|' | cut -c1-200)"

echo "### 5b.7 fgbio GroupReadsByUmi (row: 'any order accepted; template-coordinate recommended')"
fgbio GroupReadsByUmi --help 2>&1 | grep -a -i -E 'sort|template|order|queryname' | head -8 > fg_help.txt; cat fg_help.txt
samtools sort -n -o umi_qn.bam $PD/human/test.paired_end.umi_unsorted.bam
fgbio SetMateInformation -i umi_qn.bam -o umi_smi.bam > smi.log 2>&1; echo "  SetMateInformation rc=$?"
grp() { fgbio GroupReadsByUmi -i "$1" -o "$2" --strategy=adjacency --edits=1 --raw-tag=RX > "$2.log" 2>&1; echo "  $3: rc=$? MI groups=$(samtools view "$2" 2>/dev/null | grep -ao 'MI:Z:[^[:space:]]*' | sort -u | wc -l) records=$(nrec "$2" 2>/dev/null) $(grep -a -E 'ERROR|Exception|must be' "$2.log" | head -1 | cut -c1-160)"; }
grp umi_smi.bam g_unsorted.bam "unsorted (original order)"
samtools sort -o umi_smi_cs.bam umi_smi.bam; grp umi_smi_cs.bam g_coord.bam "coordinate-sorted"
samtools sort --template-coordinate -o umi_smi_tc.bam umi_smi.bam; grp umi_smi_tc.bam g_tc.bam "template-coordinate-sorted"
samtools sort -n -o umi_smi_n.bam umi_smi.bam; grp umi_smi_n.bam g_n.bam "name-sorted (samtools -n natural)"
echo "-- CallMolecularConsensusReads help (sort statement):"; fgbio CallMolecularConsensusReads --help 2>&1 | grep -a -i -E 'sort|group|MI tag' | head -4

echo "### 5b.8 HTSeq (row: featureCounts/HTSeq 'coordinate or name (-p for paired)')  real RNA PE BAM + synthetic 1-gene GTF"
printf 'chr22\tsynth\texon\t1\t40001\t.\t+\t.\tgene_id "G1"; transcript_id "T1";\n' > one.gtf
R=$PD/human/test.rna.paired_end.sorted.bam
samtools sort -n -o rna_ns.bam $R
htseq-count -f bam -r pos -s no -t exon $R one.gtf > hs_pos.txt 2> hs_pos.err; echo "  coordinate-sorted, -r pos: $(head -1 hs_pos.txt) | $(sed -n 2p hs_pos.txt | tr '\t' ' ')  (see stderr: $(grep -a -c -i warn hs_pos.err) warn lines)"
htseq-count -f bam -r name -s no -t exon rna_ns.bam one.gtf > hs_name_ns.txt 2> hs_name_ns.err; echo "  name-sorted, -r name: $(head -1 hs_name_ns.txt) $(grep -a -c -i warn hs_name_ns.err) warn"
htseq-count -f bam -r name -s no -t exon $R one.gtf > hs_name_cs.txt 2> hs_name_cs.err; echo "  coordinate-sorted, -r name (WRONG combination): $(head -1 hs_name_cs.txt) | warn lines: $(grep -a -c -i warn hs_name_cs.err) | $(grep -a -i -m1 -E 'warn|mate' hs_name_cs.err | cut -c1-150)"
echo "  counts: pos=$(head -1 hs_pos.txt | cut -f2) name/ns=$(head -1 hs_name_ns.txt | cut -f2) name/cs=$(head -1 hs_name_cs.txt | cut -f2)"
summary
