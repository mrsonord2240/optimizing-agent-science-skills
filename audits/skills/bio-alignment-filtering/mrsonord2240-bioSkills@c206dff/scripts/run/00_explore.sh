#!/bin/bash
# Explore flag / MAPQ composition of the real BAMs used as inputs.
AFD=$AFDATA
for b in human/test.paired_end.sorted.bam human/test.rna.paired_end.sorted.bam 1000g/HG00349.chr20_1400000-1500000.bam derived/planted_dups.bam sarscov2/sars-cov-2_v5.3.2.nanopore.bam; do
  echo "=== $b"
  samtools view $AFD/$b | awk '{f[$2]++; q[$5]++} END{for(k in f) printf "flag %s: %d\n",k,f[k]; for(k in q) printf "mapq %s: %d\n",k,q[k]}' | sort -k1,1 -k2,2n | head -60
  samtools view -H $AFD/$b | grep -E '^@(HD|RG)' | head -3
done
echo "== NM tag presence (human)"
samtools view $AFD/human/test.paired_end.sorted.bam | awk '{n=0; for(i=12;i<=NF;i++) if($i ~ /^NM:/) n=1; c[n]++} END{for(k in c) print "hasNM="k, c[k]}'
echo "== tags in human"
samtools view $AFD/human/test.paired_end.sorted.bam | head -2 | cut -f 12-
samtools --version | head -1
python -c "import pysam; print('pysam', pysam.__version__)"
which bc || echo "NO bc"
