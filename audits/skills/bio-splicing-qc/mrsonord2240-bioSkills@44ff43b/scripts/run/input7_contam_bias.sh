#!/bin/bash
# Input 7 (adversarial/ambiguous): rRNA contamination (SKILL.md samtools recipe + fastq_screen), 3' bias (geneBody_coverage,
# Picard CollectRnaSeqMetrics) and the Picard/rMATS/featureCounts strand-convention comment block, on SYNTHETIC BAMs with planted truth.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
set -u
R=/mnt/openscience/audits/bio-splicing-qc/run
D=$R/data/synthetic
W=$R/work/in7
rm -rf $W; mkdir -p $W; cd $W

echo "== A. SKILL.md rRNA recipe on pe_rrna.bam (truth: 22% of mapped fragments are rRNA; 8% of pairs unmapped; half of rRNA fragments multimap x4)"
BAM=$D/pe_rrna.bam
samtools view -c $BAM | awk '{print "total:",$0}'
samtools view -c -L $D/synth.rrna.bed $BAM | awk '{print "rRNA:",$0}'
echo "flagstat:"; samtools flagstat $BAM | head -8
echo "primary mapped records (-F 0x904): $(samtools view -c -F 0x904 $BAM)"
echo "primary mapped rRNA records (-F 0x904 -L bed): $(samtools view -c -F 0x904 -L $D/synth.rrna.bed $BAM)"
echo "primary mapped read1 only (fragments) total: $(samtools view -c -F 0x904 -f 0x40 $BAM)  rRNA: $(samtools view -c -F 0x904 -f 0x40 -L $D/synth.rrna.bed $BAM)"

echo "== B. fastq_screen literal command from SKILL.md (default aligner bowtie2)"
asenv as-core python $R/mk_fq.py
cat > fastq_screen.conf <<EOF
DATABASE	rRNA	$W/rrna.fa
DATABASE	Genome	$W/genome.fa
EOF
gzip -kf sample_R1.fq
echo "-- literal: fastq_screen --conf fastq_screen.conf --threads 8 sample_R1.fq.gz"
fastq_screen --conf fastq_screen.conf --threads 8 sample_R1.fq.gz > fs_literal.log 2>&1; echo "rc=$?"; tr '\r' '\n' < fs_literal.log | tail -6
echo "-- with --aligner minimap2"
fastq_screen --conf fastq_screen.conf --aligner minimap2 --threads 4 sample_R1.fq.gz > fs_mm2.log 2>&1; echo "rc=$?"; tr '\r' '\n' < fs_mm2.log | tail -4
ls *_screen.txt 2>/dev/null && cat sample_R1_screen.txt

echo "== C. RSeQC geneBody_coverage uniform vs 3' biased"
for n in dutp bias3; do
  geneBody_coverage.py -i $D/pe_$n.bam -r $D/synth.bed12 -o gb_$n --skip-plot > gb_$n.log 2>&1; echo "$n rc=$?"
  cat gb_$n.geneBodyCoverage.txt | head -3 | cut -c1-260
done

echo "== D. Picard CollectRnaSeqMetrics (picard 3.5.0, env af-picard3)"
PIC="micromamba run -n af-picard3 picard"
for n in dutp bias3 rrna; do
  for SS in SECOND_READ_TRANSCRIPTION_STRAND FIRST_READ_TRANSCRIPTION_STRAND; do
    $PIC CollectRnaSeqMetrics I=$D/pe_$n.bam O=pic_${n}_$SS.txt REF_FLAT=$D/synth.refFlat.txt STRAND_SPECIFICITY=$SS \
         RIBOSOMAL_INTERVALS=$D/synth.rrna.interval_list VALIDATION_STRINGENCY=SILENT > pic_${n}_$SS.log 2>&1
    echo "$n $SS rc=$?"
  done
done
echo "== E. rMATS flag names (SKILL.md: --libType fr-firststrand / fr-secondstrand)"
rmats.py --help 2>&1 | grep -A3 -E "libType" | head -8
echo DONE
