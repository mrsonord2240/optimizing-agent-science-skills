#!/bin/bash
# INPUT 1 (part 2): consequence of the ".fasta -> genome.fasta.dict" naming, on a GATK tool that really needs the dict;
# and the usage-guide validate block with REF substituted properly.
R=/mnt/openscience/audits/bio-reference-operations/run
cd $R/work/in1
python $R/in1_check.py
echo
echo "##### GATK HaplotypeCaller with only genome.fasta.dict (what prepare_reference.sh produced for a .fasta)"
mkdir -p B2; cp B/genome.fasta B/genome.fasta.fai B/genome.fasta.dict B2/; cp $R/data/real/test.paired_end.sorted.bam B2/h.bam
(cd B2; rm -f genome.dict; ls; cp $R/data/real/test.paired_end.sorted.bam.bai h.bam.bai
 gatk HaplotypeCaller -R genome.fasta -I h.bam -L chr22:1952-2100 -O out.vcf 2>&1 | grep -i -E 'error|dict|exception|Done|Tool returned' | head -6; echo "vcf exists: $(ls out.vcf 2>&1)")
echo "##### same, after genome.dict exists"
(cd B2; cp genome.fasta.dict genome.dict
 gatk HaplotypeCaller -R genome.fasta -I h.bam -L chr22:1952-2100 -O out2.vcf 2>&1 | grep -i -E 'error|dict|exception|Tool returned' | head -6; ls out2.vcf; grep -vc '^#' out2.vcf)
echo
echo "##### ug_17 block, REF substituted for the .fa case"
cd A; sed 's/^REF=reference.fa/REF=ref.fa/; s/chr1:1-100/chr1:1-100/' $R/snippets/ug_17_bash.txt > ../ug17.sh; bash ../ug17.sh
