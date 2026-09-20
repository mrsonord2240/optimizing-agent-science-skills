#!/bin/bash
# exploration of samtools consensus behaviour on the planted-truth BAM (feeds in4.py expectations)
R=/mnt/openscience/audits/bio-reference-operations/run
mkdir -p $R/work/in4x; cd $R/work/in4x
cp $R/data/synthetic/synth_chr.bam* $R/data/synthetic/synth.fa .
lens() { awk '/^>/{if(n)print n,l; n=$0; l=0; next}{l+=length($0)}END{print n,l}' $1; }
echo "== default"; samtools consensus synth_chr.bam -o d.fa; lens d.fa
echo "== -a"; samtools consensus -a synth_chr.bam -o a.fa; lens a.fa
echo "== -aa"; samtools consensus -aa synth_chr.bam -o aa.fa; lens aa.fa
echo "== -A"; samtools consensus -A synth_chr.bam -o A.fa; lens A.fa
echo "== -T ref"; samtools consensus -T synth.fa synth_chr.bam -o T.fa; lens T.fa; cmp d.fa T.fa && echo "T identical to default"
echo "== -a -T ref"; samtools consensus -a -T synth.fa synth_chr.bam -o aT.fa; lens aT.fa; cmp a.fa aT.fa && echo "aT identical to -a"
echo "== -r chr1:1-1000"; samtools consensus -r chr1:1-1000 synth_chr.bam -o r.fa; lens r.fa; head -1 r.fa
echo "== configs"; for c in hiseq hifi r10.4_sup r10.4_dup ultima bogus; do samtools consensus --config $c synth_chr.bam -o cfg_$c.fa 2>&1 | head -2; echo "$c rc=$? $(md5sum < cfg_$c.fa 2>/dev/null | cut -c1-8)"; done
echo "== --help rc"; samtools consensus --help >/dev/null 2>&1; echo "help rc=$?"
echo "== -d 5"; samtools consensus -d 5 synth_chr.bam -o d5.fa; lens d5.fa
echo "== fastq"; samtools consensus -f fastq synth_chr.bam -o q.fq; head -2 q.fq | cut -c1-60; awk 'NR%4==2{print length($0)} NR%4==0{print length($0)}' q.fq | head -4
echo "== pileup fmt"; samtools consensus -f pileup -r chr1:198-202 synth_chr.bam | head -6
