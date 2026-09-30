#!/bin/bash
# A6: SKILL.md NFR filter (verbatim) + deepTools alignmentSieve --ATACshift, ENCODE GM12878 rep1 chr1:1-3Mb
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
R=$W/a6_nfr; rm -rf $R; mkdir -p $R; cd $R
IN=/mnt/openscience/audit-envs/atac-seq/public-data/encode/GM12878_rep1_filtered.chr1_1-30000000.bam
samtools view -b $IN chr1:1-3000000 > sample.bam; samtools index sample.bam
# --- verbatim from SKILL.md ---
samtools view -h sample.bam | \
    awk 'substr($0,1,1)=="@" || ($9 > 0 && $9 < 100) || ($9 < 0 && $9 > -100)' | \
    samtools view -b > sample.nfr.bam
samtools index sample.nfr.bam
# ------------------------------
echo "total reads: $(samtools view -c sample.bam)  NFR reads: $(samtools view -c sample.nfr.bam)"
echo "independent expectation (samtools -e): $(samtools view -c -e 'tlen>0 && tlen<100 || tlen<0 && tlen>-100' sample.bam)"
samtools view sample.nfr.bam | awk '{t=$9<0?-$9:$9; if(t>=100||t==0) bad++; if(t>mx)mx=t; n++} END{print "n="n" max|tlen|="mx" violations="bad+0}'
# alignmentSieve --ATACshift (named in SKILL.md tn5 section)
alignmentSieve --ATACshift -b sample.bam -o shifted.bam -p 4 > sieve.log 2>&1; echo "alignmentSieve rc=$?"
samtools sort -o shifted.sorted.bam shifted.bam; samtools index shifted.sorted.bam
python - <<'PY'
import pysam
a=pysam.AlignmentFile("sample.bam"); b=pysam.AlignmentFile("shifted.sorted.bam")
o={};
for r in a:
    if r.is_read1 or True: o[(r.query_name,r.is_read1)]=(r.reference_start,r.reference_end,r.is_reverse)
d={"fwd_start":[], "rev_end":[]}
for r in b:
    k=(r.query_name,r.is_read1)
    if k not in o: continue
    s,e,rev=o[k]
    if not rev: d["fwd_start"].append(r.reference_start-s)
    else: d["rev_end"].append(r.reference_end-e)
from collections import Counter
for k,v in d.items(): print(k, Counter(v).most_common(3), "n=",len(v))
PY
