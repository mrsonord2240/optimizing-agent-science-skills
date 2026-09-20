#!/bin/bash
# FLAIR correct with orthogonal short-read junctions (flag that exists in 3.0.1: --junction_bed), on SYNTHETIC data.
# The short-read junction BED is built from the planted truth (score = 10 reads) as a stand-in for `regtools junctions extract`.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
D=$R/data/synth; O=$R/out/flair; cd $O
G=$D/chrS1.fa
LR="micromamba run -n as-lr"
S="ctrl1 ctrl2 ctrl3 trt1 trt2 trt3"
asenv as-core python - <<'EOF'
import re,collections
D="/mnt/openscience/audits/bio-long-read-splicing/run/data/synth"
tx=collections.defaultdict(list); st={}
for ln in open(D+"/read_tx.gtf"):
    f=ln.split("\t")
    if f[2]!="exon": continue
    t=re.search(r'transcript_id "([^"]+)"',f[8]).group(1); tx[t].append((int(f[3])-1,int(f[4]))); st[t]=f[6]
jn=set()
for t,ex in tx.items():
    ex.sort()
    for a,b in zip(ex[:-1],ex[1:]): jn.add((a[1],b[0],st[t]))
with open("sj_truth.bed","w") as o:
    for s,e,sd in sorted(jn): o.write("chrS1\t%d\t%d\tJUNC\t10\t%s\n"%(s,e,sd))
print(len(jn),"junctions written")
EOF
cat sj_truth.bed | head -3
for s in $S; do
  $LR flair correct -q $s.bed -f $D/ref.gtf --junction_bed sj_truth.bed -o corrSR_$s -t 4 > corrSR_$s.log 2>&1
  echo "$s correct(+junction_bed) rc=$? corrected=$(wc -l < corrSR_${s}_all_corrected.bed) inconsistent=$(wc -l < corrSR_${s}_all_inconsistent.bed)"
done
cat corrSR_*_all_corrected.bed > all_corrected_SR.bed
$LR flair collapse --query all_corrected_SR.bed --reads all_reads.fastq --genome $G --gtf $D/ref.gtf --output collapsedSR --threads 4 --generate_map > collapseSR.log 2>&1
echo "collapse rc=$?"; grep '>' collapsedSR.isoforms.fa
$LR flair quantify --reads_manifest reads_manifest.tsv --isoforms collapsedSR.isoforms.fa --output quantifiedSR --threads 4 > quantSR.log 2>&1
echo "quantify rc=$?"; cat quantifiedSR.counts.tsv
# annotation-free variant: junction-only correct (no GTF)
$LR flair correct -q ctrl1.bed --junction_bed sj_truth.bed -o corrJ_ctrl1 -t 4 > corrJ.log 2>&1; echo "correct without -f rc=$? corrected=$(wc -l < corrJ_ctrl1_all_corrected.bed)"
# correct with neither -f nor junctions (the SKILL says GTF or short reads; check the error)
$LR flair correct -q ctrl1.bed -o corrNone -t 4 > corrNone.log 2>&1; echo "correct with no evidence rc=$?"; tail -2 corrNone.log
