#!/bin/bash
# SYNTHETIC reference variants + BAMs with M5-bearing headers, for testing the SKILL's M5 diff snippet.
# Bases: real human chr22 slice reference + real reads (public-data/human).
set -e
PD=/mnt/openscience/audit-envs/alignment-files/public-data
RUN=/mnt/openscience/audits/bio-alignment-validation/run
R=$RUN/data/ref
mkdir -p $R
cp $PD/human/genome.fasta $R/ref_exact.fa
# soft-masked (lowercase) variant
python - <<'PY'
import re
R="/mnt/openscience/audits/bio-alignment-validation/run/data/ref"
seq=[l.rstrip("\n") for l in open(R+"/ref_exact.fa")]
hdr=seq[0]; body="".join(seq[1:])
def w(fn,h,b):
    with open(fn,"w") as f:
        f.write(h+"\n")
        for i in range(0,len(b),60): f.write(b[i:i+60]+"\n")
w(R+"/ref_softmask.fa",hdr,body[:10000].lower()+body[10000:])
w(R+"/ref_hardmask.fa",hdr,"N"*1000+body[1000:])            # hard-masked: first 1 kb -> N
w(R+"/ref_renamed.fa",">22",body)                            # chr22 -> 22 (Ensembl-style name)
w(R+"/ref_onebase.fa",hdr,body[:20000]+("A" if body[20000]!="A" else "C")+body[20001:])  # single SNV-level difference
# two-contig reference for name<->M5 association test
w(R+"/ref_two.fa",">chrA",body[:15000]); open(R+"/ref_two.fa","a").close()
with open(R+"/ref_two.fa","a") as f:
    f.write(">chrB\n")
    b=body[20000:38000]
    for i in range(0,len(b),60): f.write(b[i:i+60]+"\n")
PY
for f in ref_exact ref_softmask ref_hardmask ref_renamed ref_onebase ref_two; do samtools faidx $R/$f.fa; samtools dict $R/$f.fa -o $R/$f.dict; done
grep -h M5 $R/ref_exact.dict | cut -f1-4 | head -1
# BAM whose header carries M5 (as GATK/bwakit-style BAMs do): ctl_valid reads, @SQ replaced by dict of ref_exact
samtools view -H $RUN/data/ctl_valid.bam | grep -v '^@SQ' > $R/h_noSQ.txt
{ grep '^@HD' $R/h_noSQ.txt; grep '^@SQ' $R/ref_exact.dict | sed 's#\tUR:.*##'; grep -v '^@HD' $R/h_noSQ.txt; } > $R/h_m5.sam
samtools reheader $R/h_m5.sam $RUN/data/ctl_valid.bam > $R/bam_m5.bam
samtools view -H $R/bam_m5.bam | grep '^@SQ'
# two-contig BAM header with the two M5s SWAPPED between names (a real mis-assignment), empty of reads
python - <<'PY'
R="/mnt/openscience/audits/bio-alignment-validation/run/data/ref"
d=[l.rstrip("\n").split("\t") for l in open(R+"/ref_two.dict") if l.startswith("@SQ")]
def f(t,k): return [x for x in t if x.startswith(k)][0]
a,b=d
hdr="@HD\tVN:1.6\tSO:coordinate\n"
hdr+="\t".join(["@SQ",f(a,"SN"),f(a,"LN"),f(b,"M5")])+"\n"      # name chrA with chrB's M5
hdr+="\t".join(["@SQ",f(b,"SN"),f(b,"LN"),f(a,"M5")])+"\n"
open(R+"/h_swapped.sam","w").write(hdr)
PY
samtools view -b -o $R/bam_two_swapped.bam $R/h_swapped.sam
samtools view -H $R/bam_two_swapped.bam | grep '^@SQ'
echo done
