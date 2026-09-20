#!/bin/bash
# Misc regression checks (pre-fix inputs 1/3/4): REF_CACHE block, dict -a/-s, dict UR text, minimap2 compare block, determinism, hostile file names.
R=/mnt/openscience/audits/bio-reference-operations/run
W=$R/work/r9; rm -rf $W; mkdir -p $W; cd $W
cp $R/data/real/genome.fasta $R/data/real/test.paired_end.sorted.cram .
echo "##### 1. SKILL 'Pre-populate CRAM REF_CACHE' block (snippet skill_28) verbatim with HOME=$W/home, then decode with no -T"
mkdir -p home; sed 's/reference.fa/genome.fasta/' $R/snippets/skill_28_bash.txt > cache.sh
HOME=$W/home bash cache.sh > cache.out 2>&1; echo "rc=$?"; head -3 cache.out | cut -c1-200
echo "cache files:"; find home/ref_cache -type f | head -3
echo "decoded records via REF_PATH (expect >=5 lines printed by head, block prints 10):"; wc -l < cache.out
n=$(HOME=$W/home REF_PATH="$W/home/ref_cache/%2s/%2s/%s" samtools view test.paired_end.sorted.cram | wc -l); echo "full decode via cache, no -T: $n records (expect 5644)"
echo "and WITHOUT the cache and without -T (must fail loudly, not silently):"
REF_PATH=/nonexistent REF_CACHE=/nonexistent samtools view test.paired_end.sorted.cram 2>&1 | head -2 | cut -c1-200
echo "##### 2. samtools dict -a/-s and default text"
samtools dict -a GRCh38 -s "Homo sapiens" genome.fasta -o meta.dict; cat meta.dict | cut -c1-200
samtools dict genome.fasta | head -2 | cut -c1-200
cp genome.fasta rel.fa; samtools dict rel.fa | sed -n 2p | cut -c1-200
echo "##### 3. SKILL 'Compare Consensus to Reference': consensus -> minimap2 -a"
samtools consensus $R/data/real/test.paired_end.sorted.bam -o consensus.fa; grep -c '>' consensus.fa
minimap2 -a genome.fasta consensus.fa > comparison.sam 2>/dev/null; echo "minimap2 rc=$?"; samtools view -c comparison.sam; samtools view comparison.sam | cut -f1-6 | head -2
echo "##### 4. determinism: samtools consensus x3 md5"
for i in 1 2 3; do samtools consensus --ambig -d 3 $R/data/real/test.paired_end.sorted.bam | md5sum; done
echo "##### 5. hostile file name through prepare_reference.sh"
mkdir -p 'h;x $(echo pwned)'; cp genome.fasta "h;x \$(echo pwned)/we\"ird'name.v2.fasta"
cp $R/skill/examples/prepare_reference.sh .
(cd "h;x \$(echo pwned)" && bash ../prepare_reference.sh "we\"ird'name.v2.fasta" > ../hostile.out 2>&1; echo "rc=$?"; ls)
grep -c pwned ../hostile.out 2>/dev/null; cat hostile.out | tail -4
echo "##### 6. samtools dict overwrite of an existing dict (SKILL script idempotent)"
cp genome.fasta idem.fa; bash prepare_reference.sh idem.fa > /dev/null 2>&1; md5sum idem.dict idem.fa.fai idem.chrom.sizes > before.md5; bash prepare_reference.sh idem.fa > /dev/null 2>&1; md5sum -c before.md5
echo "##### 7. plain-gzip (not bgzip) FASTA, e.g. straight from Ensembl/NCBI: prepare_reference.sh accepts .gz per its usage line"
mkdir -p gz; cp genome.fasta gz/plain.fa; (cd gz; gzip plain.fa; bash ../prepare_reference.sh plain.fa.gz; echo "rc=$?"; ls)
echo "SKILL mentions bgzip? -> $(grep -c -i bgzip $R/skill/SKILL.md) hits in SKILL.md, $(grep -c -i bgzip $R/skill/usage-guide.md) in usage-guide.md"
