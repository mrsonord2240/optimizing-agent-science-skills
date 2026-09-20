#!/bin/bash
# Contamination commands from SKILL.md 'Contamination and Sample Swap': prefix naming and behaviour on the 1000G slice
PD=/mnt/openscience/audit-envs/alignment-files/public-data
RUN=/mnt/openscience/audits/bio-alignment-validation/run
W=$RUN/out/work; mkdir -p $W
B=$PD/1000g/HG00349.chr20_1400000-1500000.bam
F=$PD/1000g/chr20_padded_1500000.fa
echo "--- (a) literal SKILL prefix shape: /resources/1000g.b38.vcf.gz.SVD  (files that exist for that prefix: none in the released panel)"
ls $PD/resources | sed 's/^/    /'
verifybamid2 --SVDPrefix $PD/resources/1000g.b38.vcf.gz.SVD --Reference $F --BamFile $B --Output $W/vb_a > $W/vb_a.log 2>&1; echo "    rc=$?"; grep -iE 'fail|error|open|exit|Insufficient' $W/vb_a.log | head -3 | cut -c1-170
echo "--- (b) prefix that matches the released panel files (...vcf.gz.dat)"
verifybamid2 --SVDPrefix $PD/resources/1000g.phase3.10k.b38.vcf.gz.dat --Reference $F --BamFile $B --Output $W/vb_b > $W/vb_b.log 2>&1; echo "    rc=$?"; grep -iE 'fail|error|open|exit|Insufficient|FREEMIX' $W/vb_b.log | head -3 | cut -c1-170
ls $W/vb_b.* 2>/dev/null | head
echo "--- GC-bias output sanity (Picard summary on human slice)"
head -3 $W/gc_summary.txt 2>/dev/null | cut -c1-200
echo "--- contigs in the 1000G header that survive the SKILL aneuploidy filter (awk regex)"
samtools idxstats $B | awk '$2>0 && $1!~/^chr[XYM]|^GL|^KI|^chrUn|^chrEBV/ {n++; if($1!~/^chr([0-9]+)$/) o++} END{print "    survive="n" of which NOT plain chr1..chr22="o}'
samtools idxstats $B | awk '$2>0 && $1!~/^chr[XYM]|^GL|^KI|^chrUn|^chrEBV/ && $1!~/^chr([0-9]+)$/ {print "    e.g. "$1; k++; if(k>=4) exit}'
