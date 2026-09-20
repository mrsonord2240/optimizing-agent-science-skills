#!/bin/bash
# counts after lima / isoseq refine / isoseq cluster2 on my Kinnex toy (zm tag present); PATH has as-pb first
R=/mnt/openscience/audits/bio-long-read-splicing/run; cd $R/out/kinnex3; export PATH=/home/sci/micromamba/envs/as-pb/bin:$PATH PYTHONDONTWRITEBYTECODE=1
cat fl.lima.summary | head -12
for f in segmented.bam fl.IsoSeq_5p--IsoSeq_3p.bam flnc.bam; do echo "$f records: $(samtools view -c $f)"; done
timeout 100 isoseq cluster2 flnc.bam transcripts.bam -j 4 > cl2.log 2>&1; echo "cluster2 rc=$? ; $(ls transcripts* 2>/dev/null | tr '\n' ' ')"; tail -3 cl2.log | cut -c1-200
[ -f transcripts.bam ] && echo "transcripts.bam records: $(samtools view -c transcripts.bam)"
