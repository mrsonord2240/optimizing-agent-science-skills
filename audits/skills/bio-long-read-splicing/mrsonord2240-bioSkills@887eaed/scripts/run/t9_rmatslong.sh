#!/bin/bash
# rMATS-long block (SKILL text, extracted verbatim) on the 6 planted HiFi BAMs of out/hifi6 (ctrl1..3, trt1..3; the block's own group files name them),
# then three failure paths: (b) truncated BAM, (c) header-only BAM, (d) annotation whose contig names do not match the BAMs (chrQ vs Q).
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/plant; B=$R/out/blocks/rmats-long-for-differential-isoform-anal_1.sh; O=$R/out/rl; rm -rf $O; mkdir -p $O; cd $R
export PYTHONDONTWRITEBYTECODE=1
S="ctrl1 ctrl2 ctrl3 trt1 trt2 trt3"
mk() { rm -rf $O/$1; mkdir -p $O/$1; for s in $S; do cp $R/out/hifi6/$s.bam $R/out/hifi6/$s.bam.bai $O/$1/; done; cp $D/ref.gtf $O/$1/annotation.gtf; }
echo "##### (a) planted 3v3, block verbatim"; mk a; cd $O/a
bash $B > block.log 2>&1; echo "rc=$?"; tail -3 block.log | cut -c1-200
cat samples.tsv | head -3; ls alignment_info | tr '\n' ' '; echo; for t in differential_asms.tsv differential_isoforms.tsv; do echo "$t lines: $(wc -l < rmats_long_output/$t)"; done
cd $R; asenv as-lr python eval_rmatslong.py $O/a/rmats_long_output 2>&1 | tail -6
echo "##### (b) one truncated BAM"; mk b; cd $O/b; head -c 20000 ctrl2.bam > t.bam && mv t.bam ctrl2.bam; rm -f ctrl2.bam.bai
bash $B > block.log 2>&1; echo "rc=$?"; grep -a -i -E "error|empty|fail|truncat" block.log | head -4 | cut -c1-200; ls rmats_long_output 2>&1 | head -2
echo "##### (c) header-only BAM (no reads) for trt3"; mk c; cd $O/c; samtools view -H trt3.bam | samtools view -b -o t.bam -; mv t.bam trt3.bam; samtools index trt3.bam
bash $B > block.log 2>&1; echo "rc=$?"; grep -a -i -E "error|empty|fail" block.log | head -4 | cut -c1-200; ls rmats_long_output 2>&1 | head -2
echo "##### (d) annotation contig names do not match the BAM (chrQ vs Q)"; mk d; cd $O/d; sed 's/^chrQ/Q/' annotation.gtf > a2.gtf; mv a2.gtf annotation.gtf
bash $B > block.log 2>&1; echo "rc=$?"; grep -a -i -E "error|empty|fail|no rows" block.log | head -4 | cut -c1-200; for t in differential_asms.tsv differential_isoforms.tsv; do echo "$t lines: $(wc -l < rmats_long_output/$t 2>/dev/null)"; done
