#!/bin/bash
# Input 4 (Variant B): Skill's tool-selection table + consensus recommendation, on SYNTHETIC PE data with planted truth.
#  (a) hard-clip pipeline  (b) samtools consensus --config hiseq --ambig before/after clip
#  (c) iVar trim  (d) fgbio ClipBam (Skill lists it as a primer-trimming alternative)
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run
D=$R/data; W=$R/out/i4; rm -rf $W; mkdir -p $W; cd $W
BED=$D/synth_primers.bed; REF=$D/synth.fa; IN=$D/synth_pe.bam
echo "== (a) hard clip: seq lengths, H ops, SEQ truly lost"
samtools ampliconclip --strand --hard-clip -b $BED $IN -o hard.raw.bam 2>/dev/null
samtools sort -n hard.raw.bam | samtools fixmate -m - - | samtools sort -o hard.bam -
samtools calmd -b hard.bam $REF > hard.final.bam 2> hard.calmd.err; samtools index hard.final.bam
echo "calmd stderr bytes: $(wc -c < hard.calmd.err)"
echo "orig mean SEQ len: $(samtools view $IN | awk '{s+=length($10)}END{print s/NR}')  hard mean SEQ len: $(samtools view hard.final.bam | awk '{s+=length($10)}END{print s/NR}')  H-cigar reads: $(samtools view hard.final.bam | awk '$6~/H/' | wc -l)"
echo "== (b) samtools consensus --config hiseq --ambig over amp1:301-350 (1-based); pos310(0b)=idx10, pos335(0b)=idx35 in this 50bp window"
samtools ampliconclip --both-ends -b $BED $IN -o soft.raw.bam 2>/dev/null
samtools sort -n soft.raw.bam | samtools fixmate -m - - | samtools sort -o soft.bam -; samtools calmd -b soft.bam $REF > soft.final.bam 2>/dev/null; samtools index soft.final.bam
for t in unclipped soft; do
  b=$( [ $t = unclipped ] && echo $IN || echo soft.final.bam )
  samtools consensus --config hiseq --ambig -r amp1:301-350 -f fasta $b 2>$t.cons.err | grep -v '>' | tr -d '\n' > $t.cons.txt
  s=$(cat $t.cons.txt); echo "$t consensus: $s  base@310=${s:10:1} base@335=${s:35:1}  (len ${#s}) stderr: $(head -c 120 $t.cons.err)"
done
echo "ref  @310=$(samtools faidx $REF amp1:311-311 | tail -1) @335=$(samtools faidx $REF amp1:336-336 | tail -1); planted ALT @310=T @335=G"
echo "== (c) iVar trim on synthetic PE (sorted+indexed input), -q 0 -m 1"
ivar trim -i $IN -b $BED -p ivar -q 0 -m 1 2>&1 | grep -E 'Trimmed|quality|started|insert'
samtools sort -o ivar.sorted.bam ivar.bam; samtools index ivar.sorted.bam
echo "== (d) fgbio ClipBam has any primer/BED option?"
fgbio ClipBam --help 2>&1 | sed 's/\x1b\[[0-9;]*m//g' > clipbam_help.txt
echo "lines in ClipBam --help mentioning bed/primer/amplicon: $(grep -Eic 'bed|primer|amplicon' clipbam_help.txt) (of $(wc -l < clipbam_help.txt) lines)"
grep -E '^-|^--' clipbam_help.txt | grep -Ev 'async|version|compression|tmp-dir|log-level|validation|cram' | cut -c1-70
echo "   attempt: fixed 25-base 5' clip as the closest ClipBam equivalent"
samtools sort -n -u $IN | fgbio ClipBam -i /dev/stdin -o fgbio.bam -r $REF --read-one-five-prime 25 --read-two-five-prime 25 -c Soft 2>&1 | grep -vi 'INFO' | head -5
samtools sort -o fgbio.sorted.bam fgbio.bam; samtools index fgbio.sorted.bam
echo "records: ivar=$(samtools view -c ivar.sorted.bam) fgbio=$(samtools view -c fgbio.sorted.bam)"
