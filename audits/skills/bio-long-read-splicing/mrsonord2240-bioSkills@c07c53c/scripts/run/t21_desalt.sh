#!/bin/bash
# deSALT (SKILL table row "deSALT without annotation") on my planted microexon set (7/12/24 nt), no annotation. env as-sqanti.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/micro; O=$R/out/desalt; rm -rf $O; mkdir -p $O; cd $O; export PYTHONDONTWRITEBYTECODE=1
micromamba run -n as-sqanti deSALT index $D/chrU.fa idx > index.log 2>&1; echo "index rc=$?"
for P in hifi:ccs ontunstr:ont1d; do N=${P%%:*}; X=${P#*:}
  micromamba run -n as-sqanti deSALT aln -x $X -t 8 -o $N.sam idx $D/$N.fastq > aln_$N.log 2>&1; echo "$N aln rc=$? sam lines: $(grep -vc '^@' $N.sam 2>/dev/null)"
  samtools sort -o $N.bam $N.sam 2>/dev/null; samtools index $N.bam; asenv as-lr python $R/micro_table.py $N.bam $D/truth_chains.tsv "deSALT $N (no annotation)"; done
