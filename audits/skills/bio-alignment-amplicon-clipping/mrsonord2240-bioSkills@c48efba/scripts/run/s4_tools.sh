#!/bin/bash
# Input 4 (Variant B): hard-clip archive, tool alternatives, consensus, Quick Reference lines, related-skill pointers, removed claims.
# SYNTHETIC PE data (planted truth) plus real ARTIC for the pointer/BAQ claim.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run
D=$R/data; W=$R/out/i4; rm -rf $W; mkdir -p $W; cd $W
BED=$D/synth_primers.bed; REF=$D/synth.fa; IN=$D/synth_pe.bam
echo "== (a) Quick Reference hard-clip line: samtools ampliconclip --both-ends --strand --hard-clip -b primers.bed in.bam -o clipped.bam"
samtools ampliconclip --both-ends --strand --hard-clip -b $BED $IN -o clipped.bam 2>&1 | grep -E 'TOTAL CLIPPED|WRITTEN' | tr '\n' ' '; echo
echo "== Quick Reference repair line, fed from a pipe: cat clipped.bam | samtools sort -n - | samtools fixmate -m - - | samtools sort -o out.bam -"
cat clipped.bam | samtools sort -n - | samtools fixmate -m - - | samtools sort -o out.bam - ; echo "rc=${PIPESTATUS[*]}"
samtools calmd -b out.bam $REF > hard.final.bam 2> hard.calmd.err; samtools index hard.final.bam
echo "calmd stderr bytes: $(wc -c < hard.calmd.err)"
echo "orig mean SEQ len: $(samtools view $IN | awk '{s+=length($10)}END{print s/NR}')  hard mean SEQ len: $(samtools view hard.final.bam | awk '{s+=length($10)}END{print s/NR}')  H-cigar reads: $(samtools view hard.final.bam | awk '$6~/H/' | wc -l)"
echo "== (b) soft-clip, reversibility, then samtools consensus --config hiseq --ambig (SKILL ARTIC note)"
samtools ampliconclip --both-ends --strand -b $BED $IN -o soft.raw.bam 2>/dev/null
samtools sort -n soft.raw.bam | samtools fixmate -m - - | samtools sort -o soft.bam -; samtools calmd -b soft.bam $REF > soft.final.bam 2>/dev/null; samtools index soft.final.bam
samtools view $IN | awk '{print $1"\t"$2"\t"$10}' | sort > o.seq; samtools view soft.final.bam | awk '{print $1"\t"$2"\t"$10}' | sort > s.seq
echo "soft: reads with byte-identical SEQ vs original: $(comm -12 o.seq s.seq | wc -l) of $(wc -l < o.seq); with S in CIGAR: $(samtools view soft.final.bam | awk '$6~/S/' | wc -l)"
for t in unclipped soft; do
  b=$( [ $t = unclipped ] && echo $IN || echo soft.final.bam )
  samtools consensus --config hiseq --ambig -r amp1:301-350 -f fasta $b 2>$t.cons.err | grep -v '>' | tr -d '\n' > $t.cons.txt
  s=$(cat $t.cons.txt); echo "$t consensus: $s  base@310=${s:10:1} base@335=${s:35:1} (len ${#s}) stderr: $(head -c 100 $t.cons.err)"
done
echo "ref @310=$(samtools faidx $REF amp1:311-311 | tail -1) @335=$(samtools faidx $REF amp1:336-336 | tail -1); planted ALT @310=T @335=G"
echo "== (c) iVar block on synthetic PE (verbatim flags: -q 0 -m 1; needs sorted+indexed input)"
ivar trim -i $IN -b $BED -p ivar -q 0 -m 1 2>&1 | grep -aE 'Trimmed|Found'
samtools sort -o ivar.sorted.bam ivar.bam; samtools index ivar.sorted.bam
echo "== (d) fgbio ClipBam: SKILL says it 'clips a fixed number of bases or overlapping mate ends and takes no primer file'"
fgbio ClipBam --help 2>&1 | sed 's/\x1b\[[0-9;]*m//g' > clipbam_help.txt
echo "lines mentioning bed/primer/amplicon in ClipBam --help: $(grep -Eic 'bed|primer|amplicon' clipbam_help.txt) of $(wc -l < clipbam_help.txt)"
grep -E '^ *-[a-zA-Z]|^ *--' clipbam_help.txt | grep -Ev 'async|version|compression|tmp-dir|log-level|validation|cram' | cut -c1-90 | head -14
samtools sort -n -u $IN | fgbio ClipBam -i /dev/stdin -o fgbio.bam -r $REF --read-one-five-prime 25 --read-two-five-prime 25 -c Soft 2>&1 | grep -vi 'INFO' | head -3
samtools sort -o fgbio.sorted.bam fgbio.bam; samtools index fgbio.sorted.bam
echo "== planted-truth scoring"
python $R/s4_check.py
echo "== (e) removal check: what still mentions ClipBam / BAMClipper / BAQ / MD-dependence in the fixed Skill"
grep -n -i 'clipbam\|bamclipper' $R/skill/SKILL.md $R/skill/usage-guide.md | cut -c1-200
grep -n -i 'baq' $R/skill/SKILL.md $R/skill/usage-guide.md $R/skill/examples/* | cut -c1-220
echo "== (f) pointers: samtools vs bcftools mpileup flags (SKILL Related Skills)"
echo "samtools mpileup -aa -A -d 600000 -B:"; samtools mpileup -aa -A -d 600000 -B -f $REF -r amp1:300-305 $IN 2>&1 | head -2 | cut -c1-80
echo "bcftools mpileup -aa (should fail):"; bcftools mpileup -aa -A -d 600000 -B -f $REF -r amp1:300-305 $IN 2>&1 | head -2 | cut -c1-120
echo "bcftools mpileup --max-depth 600000 -a FORMAT/AD,FORMAT/DP -B:"; bcftools mpileup --max-depth 600000 -a FORMAT/AD,FORMAT/DP -B -f $REF -r amp1:300-305 $IN 2>&1 | grep -v '^##' | head -3 | cut -c1-120
echo "== (g) BAQ claim on real ARTIC: bcftools mpileup output with vs without MD, with vs without -B"
SC=$AFDATA/sarscov2; A=$R/out/i1
samtools view -h $A/clipped_final.bam | sed -E 's/\tMD:Z:[^\t]*//' | samtools view -b -o noMD.bam -; samtools index noMD.bam
echo "records with MD: $(samtools view $A/clipped_final.bam | grep -c 'MD:Z:'); noMD.bam: $(samtools view noMD.bam | grep -c 'MD:Z:')"
for b in $A/clipped_final.bam noMD.bam; do for flag in "" "-B"; do
  n=$(bcftools mpileup $flag -f $SC/MN908947.3.fasta $b 2>/dev/null | grep -v '^#' | md5sum | cut -c1-10); k=$(bcftools mpileup $flag -f $SC/MN908947.3.fasta $b 2>/dev/null | grep -vc '^#')
  echo "$(basename $b) flag='$flag' body md5=$n records=$k"
done; done
