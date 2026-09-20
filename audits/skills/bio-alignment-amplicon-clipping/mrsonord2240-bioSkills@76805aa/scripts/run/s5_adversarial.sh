#!/bin/bash
# Input 5 (Adversarial, regression of the pre-fix traps + false-positive probes of the new hard-fail checks).
# Every case runs the SHIPPED example script from a COPY and reads its exit code AND what it wrote.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; D=$R/data; W=$R/out/i5; rm -rf $W; mkdir -p $W; cd $W
cp -r $R/skill $W/skillcopy; EX=$W/skillcopy/examples/ampliconclip_workflow.sh
SC=$AFDATA/sarscov2; ILL=$SC/test.paired_end.sorted.bam; ART=$SC/sars-cov-2_v5.3.2.nanopore.bam; BED=$SC/v5.3.2.primer.bed
run() { name=$1; shift; "$@" > $name.out 2>&1; rc=$?; echo "   example rc=$rc; last lines: $(grep -av 'bam_sort_core' $name.out | tail -2 | cut -c1-190 | tr '\n' '|')"; echo "   output BAM exists: $(ls $W/$name.bam 2>/dev/null | wc -l)"; }

echo "== F1 (regression): Illumina PE BAM (MT192765.1) + ARTIC BED (MN908947.3) + genome.fasta (MT192765.1)"
run f1 bash $EX $ILL $BED $SC/genome.fasta $W/f1.bam
echo "== F2 (regression): right BAM+BED, WRONG reference FASTA (MT192765.1) for a MN908947.3 BAM"
run f2 bash $EX $ART $BED $SC/genome.fasta $W/f2.bam
echo "== F2b: wrong FASTA with the FASTA-contig pre-check bypassed (edited copy of the example) -> does the MD assertion catch it?"
cp -r $W/skillcopy $W/skillcopy_nochk
python - <<'PY'
p = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/out/i5/skillcopy_nochk/examples/ampliconclip_workflow.sh"
s = open(p, encoding="utf-8").read()
import re
s2 = re.sub(r'\[ -z "\$\(comm -23[^\n]*\n', '', s)
print("pre-check removed:", s != s2)
open(p, "w", encoding="utf-8", newline="\n").write(s2)
PY
run f2b bash $W/skillcopy_nochk/examples/ampliconclip_workflow.sh $ART $BED $SC/genome.fasta $W/f2b.bam
echo "== F3: name-sorted input to the example (Skill prerequisite: coordinate-sorted)"
samtools sort -n -o nsort.bam $ART
run f3 bash $EX nsort.bam $BED $SC/MN908947.3.fasta $W/f3.bam
echo "   (if rc=0: records $(samtools view -c $W/f3.bam 2>/dev/null))"
echo "== F4: reference FASTA without .fai"
cp $SC/MN908947.3.fasta nofai.fa
run f4 bash $EX $ART $BED nofai.fa $W/f4.bam
echo "== F5: missing arguments / nonexistent BAM"
bash $EX > f5a.out 2>&1; echo "   no args rc=$?: $(head -1 f5a.out | cut -c1-120)"
bash $EX nonexist.bam $BED $SC/MN908947.3.fasta $W/f5.bam > f5b.out 2>&1; echo "   missing BAM rc=$?: $(grep -a -m2 -i 'fail\|error\|no such' f5b.out | cut -c1-140 | tr '\n' '|')"

echo "=== FALSE-POSITIVE PROBES: legitimate inputs the new hard-fail checks might reject"
echo "-- P1: multi-contig BAM (ARTIC reads on MN908947.3 plus an extra header contig 'decoy' with no reads), BED covers one contig, FASTA holds both"
samtools view -h $ART | awk 'BEGIN{OFS="\t"} /^@SQ/ && !d {print; print "@SQ\tSN:decoy\tLN:1000"; d=1; next} {print}' | samtools view -b -o multi.bam -
samtools index multi.bam
cat $SC/MN908947.3.fasta > multi.fa; printf '>decoy\nACGTACGTAC\n' >> multi.fa; samtools faidx multi.fa
run p1 bash $EX multi.bam $BED multi.fa $W/p1.bam
echo "-- P2: FASTA lacks an unrelated BAM contig (BAM has decoy, FASTA does not; BED does not use decoy) -> reference has only the amplicon contig"
run p2 bash $EX multi.bam $BED $SC/MN908947.3.fasta $W/p2.bam
echo "-- P3: BED with extra contigs the BAM does not have (v3+v5 BED on contig MN908947.3 plus 'chrX' primers)"
{ cat $BED; printf 'chrX\t100\t130\tx_LEFT_1\t1\t+\tACGT\n'; } > bed_extra.bed
run p3 bash $EX $ART bed_extra.bed $SC/MN908947.3.fasta $W/p3.bam
echo "-- P4: legitimate sparse sample: BED matches the contig but the only reads fall between primers (SYNTHETIC: strand_cases.bam read c2, 140-200, primer-free)"
samtools view -h $D/strand_cases.bam | awk '/^@/ || $1=="c2_fwd_control_no_primer"' | samtools view -b -o nooverlap.bam -; samtools index nooverlap.bam
echo "   records: $(samtools view -c nooverlap.bam)"
run p4 bash $EX nooverlap.bam $D/synth_primers.bed $D/synth.fa $W/p4.bam
echo "-- P5: real Illumina PE reads (nf-core, MT192765.1, shotgun-like starts) with the ARTIC BED renamed to MT192765.1 (coordinates ~ same genome), default modes"
sed 's/^MN908947.3/MT192765.1/' $BED > bed_mt.bed
run p5 bash $EX $ILL bed_mt.bed $SC/genome.fasta $W/p5.bam
echo "   P5 same, CLIP_OPTS=--both-ends (no --strand)"
CLIP_OPTS=--both-ends run p5b bash $EX $ILL bed_mt.bed $SC/genome.fasta $W/p5b.bam
echo "=== Skill step 0 (contig comm) on F1 pair: expect EMPTY output"
comm -12 <(samtools view -H $ILL | awk -F'\t' '$1=="@SQ"{sub("SN:","",$2); print $2}' | sort) <(awk '!/^#/{print $1}' $BED | sort -u) | wc -l
