#!/bin/bash
# INPUT 1 (Canonical): "Prepare my reference for GATK/Picard/bwa: index, dictionary, chrom sizes"
# Runs the shipped examples/prepare_reference.sh FROM A COPY and the documented commands, then in1_check.py asserts.
R=/mnt/openscience/audits/bio-reference-operations/run
W=$R/work/in1
rm -rf $W; mkdir -p $W; cd $W
cp $R/skill/examples/prepare_reference.sh .

echo "##### A. synthetic 3-contig reference, extension .fa"
mkdir A; cp $R/data/synthetic/synth.fa A/ref.fa
(cd A; bash ../prepare_reference.sh ref.fa; echo "exit=$?"; ls)

echo; echo "##### B. real chr22 slice, extension .fasta (nf-core / GATK bundle style name)"
mkdir B; cp $R/data/real/genome.fasta B/genome.fasta
(cd B; bash ../prepare_reference.sh genome.fasta; echo "exit=$?"; ls)

echo; echo "##### C. re-run on A (idempotency)"
(cd A; md5sum ref.dict ref.fa.fai ref.chrom.sizes > ../A_before.md5; bash ../prepare_reference.sh ref.fa >/dev/null; md5sum -c ../A_before.md5)

echo; echo "##### D. failure modes of the script"
(cd A; bash ../prepare_reference.sh; echo "no-arg exit=$?"; bash ../prepare_reference.sh nope.fa; echo "missing exit=$?")

echo; echo "##### E. bgzipped reference ref.fa.gz"
mkdir E; cp $R/data/synthetic/synth.fa E/ref.fa; (cd E; bgzip ref.fa; bash ../prepare_reference.sh ref.fa.gz; echo "exit=$?"; ls)

echo; echo "##### F. samtools dict -a/-s (SKILL line 85) and default dict text"
cd A
samtools dict -a GRCh38 -s "Homo sapiens" ref.fa -o with_meta.dict; cat with_meta.dict
echo "--- default"; cat ref.dict
cd ..

echo; echo "##### G. Picard 3.5.0 CreateSequenceDictionary on the same FASTA (independent producer)"
picard CreateSequenceDictionary -R A/ref.fa -O A/picard.dict 2>&1 | tail -2; cat A/picard.dict

echo; echo "##### H. GATK/Picard consumption of the dict: real BAM + genome.fasta with only genome.fasta.dict present (B)"
cp -r B Bh; cp $R/data/real/test.paired_end.sorted.bam Bh/h.bam
(cd Bh; gatk ValidateSamFile -I h.bam -R genome.fasta 2>&1 | grep -v -i -E 'jdk|INFO|^Using|Picked' | head -12)
echo "--- same after renaming dict the way GATK expects (genome.dict)"
(cd Bh; cp genome.fasta.dict genome.dict; gatk ValidateSamFile -I h.bam -R genome.fasta 2>&1 | grep -v -i -E 'jdk|INFO|^Using|Picked' | head -6)

echo; echo "##### I. usage-guide 'Validate Reference Setup' block (ug_17), verbatim, REF=A/ref.fa"
cd A
sed 's/chr1:1-100/chr1:1-100/' $R/snippets/ug_17_bash.txt > ../ug17.sh
bash ../ug17.sh
echo "--- same block on the .fasta case (B)"
cd ../B; sed 's/^REF=reference.fa/REF=genome.fasta/; s/chr1:1-100/chr22:1-100/' $R/snippets/ug_17_bash.txt > ../ug17b.sh; bash ../ug17b.sh
