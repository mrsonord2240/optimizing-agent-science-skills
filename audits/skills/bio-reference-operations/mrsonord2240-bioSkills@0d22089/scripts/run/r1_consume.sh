#!/bin/bash
# INPUT 1 part 2: do GATK 4.6.2.0 and Picard 3.5.0 actually LOAD the reference+dict that prepare_reference.sh wrote?
# Output judged by content: GATK must write a VCF with a #CHROM line and no "USER ERROR"; Picard must print "No errors found".
R=/mnt/openscience/audits/bio-reference-operations/run
W=$R/work/r1; cd $W
BAM=$R/data/real/test.paired_end.sorted.bam
run_one() { # dir ref
  local d="$1" ref="$2"
  cd "$W/$d"
  rm -f hc.vcf hc.vcf.idx
  gatk --java-options -Xmx2g HaplotypeCaller -R "$ref" -I $BAM -L chr22:1952-2300 -O hc.vcf > hc.log 2>&1
  local grc=$?
  local err=$(grep -c 'USER ERROR' hc.log)
  local hdr=$(grep -c '^#CHROM' hc.vcf 2>/dev/null)
  local msg=$(grep -m1 -A1 'USER ERROR' hc.log | tr '\n' ' ' | cut -c1-230)
  picard ValidateSamFile I=$BAM R="$ref" MODE=SUMMARY > pv.log 2>&1
  local prc=$?
  local pok=$(grep -c 'No errors found' pv.log)
  local pmsg=$(grep -m1 -i -E 'exception|error' pv.log | cut -c1-200)
  echo "$d/$ref | GATK rc=$grc USER_ERROR=$err vcf_has_#CHROM=$hdr | Picard rc=$prc no_errors=$pok | ${msg}${pmsg}"
}
run_one s1 genome.fasta
run_one s2 ref.fa
run_one s3 ref2.fna
run_one s4 refz.fa.gz
run_one s5 Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
run_one s6 hg38.p14.v2.fasta
run_one s7 genome.fna.gz
run_one s8 genome.fasta.gz
run_one s9 "my genome.fasta"
run_one s10.v2 noext
run_one s11 GENOME.FA
run_one s12 ref.fas
echo "##### NEGATIVE CONTROL: only the OLD name genome.fasta.dict present (pre-fix behaviour)"
mkdir -p $W/neg; cd $W/neg; cp $R/data/real/genome.fasta .; samtools faidx genome.fasta; samtools dict genome.fasta -o genome.fasta.dict
gatk --java-options -Xmx2g HaplotypeCaller -R genome.fasta -I $BAM -L chr22:1952-2300 -O hc.vcf > hc.log 2>&1; echo "GATK rc=$?"; grep -A1 'USER ERROR' hc.log | head -3
picard ValidateSamFile I=$BAM R=genome.fasta MODE=SUMMARY 2>&1 | grep -i -E 'No errors|Exception|dictionary|not exist' | head -3
