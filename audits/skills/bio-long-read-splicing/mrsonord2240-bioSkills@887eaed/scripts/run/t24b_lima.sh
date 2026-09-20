#!/bin/bash
# Why did the fixer's lima "not finish on the toy BAM"? Test: the same array with and without the ZMW (zm) tag; skera then lima --isoseq, 60-s timeout each.
R=/mnt/openscience/audits/bio-long-read-splicing/run; O=$R/out/kinnex3nozm; rm -rf $O; mkdir -p $O; cd $O; export PYTHONDONTWRITEBYTECODE=1
export PATH=/home/sci/micromamba/envs/as-pb/bin:$PATH
cp $R/out/kinnex3/primers.fasta $R/out/kinnex3/adapters7.fasta .
asenv as-lr python - <<'PY'
import pysam
src = pysam.AlignmentFile("../kinnex3/kinnex3.bam", check_sq=False); out = pysam.AlignmentFile("nozm.bam", "wb", template=src)
for r in src:
    tags = [t for t in r.get_tags() if t[0] != "zm"]; r.set_tags(tags); out.write(r)
out.close(); print("nozm.bam written; zm present:", any(r.has_tag("zm") for r in pysam.AlignmentFile("nozm.bam", check_sq=False)))
PY
skera split nozm.bam adapters7.fasta seg_nozm.bam > /dev/null 2>&1; echo "skera rc=$?; S-read names: $(samtools view seg_nozm.bam | cut -f1 | head -2 | tr '\n' ' ')"
timeout 60 lima seg_nozm.bam primers.fasta fl_nozm.bam --isoseq -j 2 > lima_nozm.log 2>&1; echo "lima WITHOUT zm: rc=$? (124 = killed by the 60-s timeout); records out: $(samtools view -c fl_nozm.IsoSeq_5p--IsoSeq_3p.bam 2>/dev/null)"
