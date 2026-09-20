#!/bin/bash
# Input 5 (Adversarial/ambiguous): the traps a real user hits. Illumina SARS-CoV-2 BAM is on MT192765.1 but the ARTIC BED is MN908947.3;
# wrong reference for calmd; name-sorted input; Skill's BED example verbatim (with '#' comment line).
# Every case runs the SHIPPED example script from a copy and reads what it prints and what it writes.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; D=$R/data; W=$R/out/i5; rm -rf $W; mkdir -p $W; cd $W
cp -r $R/skill $W/skillcopy
SC=$AFDATA/sarscov2; EX=$W/skillcopy/examples/ampliconclip_workflow.sh
ILL=$SC/test.paired_end.sorted.bam
echo "== F1: Illumina PE BAM (contig MT192765.1) + ARTIC BED (MN908947.3) + matching-FASTA for the BAM, via shipped example"
samtools view -H $ILL | grep '^@SQ'
bash $EX $ILL $SC/v5.3.2.primer.bed $SC/genome.fasta $W/f1.bam > f1.out 2>&1; echo "example exit code: $?"; tail -4 f1.out | cut -c1-160
echo "records out: $(samtools view -c $W/f1.bam)  reads with any S: $(samtools view $W/f1.bam | awk '$6~/S/' | wc -l) (input reads with S: $(samtools view $ILL | awk '$6~/S/' | wc -l))"
echo "-- raw ampliconclip stats for same pair (what the Skill never shows):"
samtools ampliconclip --both-ends -b $SC/v5.3.2.primer.bed $ILL -o /dev/null 2>&1 | grep -E 'TOTAL CLIPPED|NOT CLIPPED|WRITTEN'

echo "== F2: right BAM+BED but WRONG reference FASTA for calmd (genome.fasta = MT192765.1) via shipped example"
bash $EX $SC/sars-cov-2_v5.3.2.nanopore.bam $SC/v5.3.2.primer.bed $SC/genome.fasta $W/f2.bam > f2.out 2>&1; echo "example exit code: $?"; tail -5 f2.out | cut -c1-200
ls -la $W/f2.bam $W/f2.bam.bai 2>&1 | cut -c1-120
echo "-- what calmd itself says (stderr, which the example discards with 2>/dev/null):"
samtools ampliconclip --both-ends -b $SC/v5.3.2.primer.bed $SC/sars-cov-2_v5.3.2.nanopore.bam -o t.bam 2>/dev/null
samtools calmd -b t.bam $SC/genome.fasta 2>&1 >/dev/null | head -3 | cut -c1-200

echo "== F3: name-sorted (queryname) input to ampliconclip (Skill prerequisite says coordinate-sorted)"
samtools sort -n -o $W/nsort.bam $SC/sars-cov-2_v5.3.2.nanopore.bam
samtools ampliconclip --strand -b $SC/v5.3.2.primer.bed $W/nsort.bam -o $W/f3.bam 2>&1 | grep -E 'TOTAL CLIPPED|NOT CLIPPED|WRITTEN|rror'
echo "exit ${PIPESTATUS[0]}; clipped reads count in output with S at start: $(samtools view $W/f3.bam | awk '$6~/^[0-9]+S/' | wc -l)"

echo "== F4: Skill's BED example verbatim (5 cols, '#' comment line, chr1) - does the comment line parse? (contig chr1 absent from BAM)"
printf '# tab-separated, 0-based half-open like all BED\nchr1\t100\t125\tprimer_1_F\t+\nchr1\t500\t525\tprimer_1_R\t-\n' > skill_bed_example.bed
samtools ampliconclip -b skill_bed_example.bed $ILL -o /dev/null 2>&1 | head -4 | cut -c1-160
echo "-- same file but with --strand"
samtools ampliconclip --strand -b skill_bed_example.bed $ILL -o /dev/null 2>&1 | head -4 | cut -c1-160

echo "== F5: skill's Quick Reference 'samtools ampliconclip ... -o clipped.bam' then straight to index/variant calling (no re-sort)"
samtools ampliconclip --strand -b $SC/v5.3.2.primer.bed $SC/sars-cov-2_v5.3.2.nanopore.bam -o $W/f5.bam 2>/dev/null
samtools index $W/f5.bam 2>&1 | head -2 | cut -c1-160; echo "index exit ${PIPESTATUS[0]}; header: $(samtools view -H $W/f5.bam | head -1)"
