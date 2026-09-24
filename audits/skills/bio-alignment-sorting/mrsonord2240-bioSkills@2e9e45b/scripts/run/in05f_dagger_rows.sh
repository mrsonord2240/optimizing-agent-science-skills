#!/bin/bash
# INPUT 5f (stress, part 6): judge the fixer's dagger marking. The SKILL footnote says: "Tool not installed in the checking environment:
# the requirement is unverified here". Check (1) which dagger tools are really absent, and (2) run the ones that ARE present
# (fgbio CallMolecularConsensusReads, GATK Mutect2) so the row can be verified rather than merely hedged.
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in5f; rm -rf $W; mkdir -p $W; cd $W
H=$PD/human/test.paired_end.sorted.bam; G=$PD/human/genome.fasta
echo "### 5f.1 presence of every dagger tool in the alignment-files env (which)"
for t in featureCounts salmon rsem-calculate-expression rsem-sam-validator sniffles cuteSV manta configManta.py delly gatk fgbio; do
  p=$(which $t 2>/dev/null); echo "  $t: ${p:-ABSENT}"
done
echo "  gatk Mutect2 subcommand: $(gatk Mutect2 --help 2>&1 | head -3 | tr '\n' ' ' | cut -c1-120)"
echo "  fgbio CallMolecularConsensusReads: $(fgbio CallMolecularConsensusReads --help 2>&1 | grep -a -m1 -i 'call' | cut -c1-120)"
echo "### 5f.2 fgbio CallMolecularConsensusReads (row: 'grouped by MI tag (consumes GroupReadsByUmi output)')"
samtools sort -n -o umi_qn.bam $PD/human/test.paired_end.umi_unsorted.bam
fgbio SetMateInformation -i umi_qn.bam -o umi_smi.bam > smi.log 2>&1
fgbio GroupReadsByUmi -i umi_smi.bam -o grouped.bam --strategy=adjacency --edits=1 --raw-tag=RX > grp.log 2>&1
echo "  GroupReadsByUmi output: $(samtools view -c grouped.bam) records, MI groups $(samtools view grouped.bam | grep -ao 'MI:Z:[^[:space:]]*' | sort -u | wc -l), header: $(so grouped.bam)"
cmcr() { fgbio CallMolecularConsensusReads -i "$1" -o "$2" --min-reads 1 > "$2.log" 2>&1; rc=$?; echo "  $3: rc=$rc consensus records=$(samtools view -c "$2" 2>/dev/null) $(grep -a -E 'ERROR|Exception|not sorted|must be|Consensus reads emitted|Total Reads' "$2.log" | head -3 | tr '\n' '|' | cut -c1-260)"; }
cmcr grouped.bam cons_orig.bam "GroupReadsByUmi output as written (SO:$(so grouped.bam | grep -o 'SO:[a-z]*' | cut -d: -f2))"
samtools sort --template-coordinate -o grouped_tc.bam grouped.bam; cmcr grouped_tc.bam cons_tc.bam "template-coordinate sorted"
samtools sort -o grouped_cs.bam grouped.bam; cmcr grouped_cs.bam cons_cs.bam "coordinate sorted (MI groups scattered)"
samtools sort -t MI -o grouped_mi.bam grouped.bam; cmcr grouped_mi.bam cons_mi.bam "sort -t MI (grouped by MI tag)"
echo "  ungrouped input (no MI tag) -> ?"; cmcr umi_smi.bam cons_nomi.bam "no MI tag"
echo "### 5f.3 GATK Mutect2 (row: 'GATK HaplotypeCaller: coordinate and indexed (Mutect2 dagger)')"
samtools sort -n -o h_nat.bam $H
timeout 500 gatk --java-options -Xmx2g Mutect2 -R $G -I $H -O m2_cs.vcf > m2_cs.log 2>&1; echo "  coordinate-sorted+indexed: rc=$? vcf lines=$(grep -av '^#' m2_cs.vcf 2>/dev/null | wc -l) $(grep -a -E 'A USER ERROR' m2_cs.log | head -1 | cut -c1-200)"
timeout 500 gatk --java-options -Xmx2g Mutect2 -R $G -I h_nat.bam -O m2_ns.vcf > m2_ns.log 2>&1; echo "  name-sorted: rc=$? $(grep -a -E 'A USER ERROR' m2_ns.log | head -1 | cut -c1-200)"
mkdir -p noidx; cp $H noidx/h.bam
timeout 500 gatk --java-options -Xmx2g Mutect2 -R $G -I noidx/h.bam -O m2_ni.vcf > m2_ni.log 2>&1; echo "  coordinate-sorted, NOT indexed: rc=$? $(grep -a -E 'A USER ERROR' m2_ni.log | head -1 | cut -c1-200)"
summary
