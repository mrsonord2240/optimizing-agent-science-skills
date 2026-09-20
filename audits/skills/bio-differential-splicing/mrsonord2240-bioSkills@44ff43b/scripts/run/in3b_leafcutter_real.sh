#!/bin/bash
# Input 3b: leafcutter on the REAL chrX 2v2 (XS-tagged BAMs). Redo of the in3 leafcutter section with -m 10 (the Skill's -m 50 leaves 0 clusters on ~100k reads/sample).
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
D=$AS/public-data/rnasplice; XB=$AS/public-data/derived/xs_bams
LC=$AS/tools/src/leafcutter
CORE="micromamba run -n as-core"; RL="micromamba run -n as-rleaf"
R=/mnt/openscience/audits/bio-differential-splicing/run
GTF=$D/reference/genes_chrX.gtf
S1=ERR188383; S2=ERR188428; S3=ERR188454; S4=ERR204916
W=$R/out/in3b; rm -rf $W; mkdir -p $W; cd $W
for s in $S1 $S2 $S3 $S4; do $CORE regtools junctions extract -a 8 -m 50 -s XS $XB/$s.xs.bam -o $s.junc > /dev/null 2>&1; echo "$s junctions: $(grep -vc '^track' $s.junc) strand col: $(awk '!/^track/{print $6}' $s.junc | sort | uniq -c | tr '\n' ' ')"; done
ls *.junc > juncfiles.txt
for m in 50 10; do
  $CORE python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o lc$m -m $m -l 500000 > cl$m.log 2>&1
  echo "cluster -m $m rc=$? intron rows: $(zcat lc${m}_perind_numers.counts.gz | tail -n +2 | wc -l)"
done
$CORE python - <<PY
import re
ex=set()
for l in open("$GTF"):
    f=l.rstrip("\n").split("\t")
    if len(f)>8 and f[2]=="exon":
        m=re.search(r'gene_name "([^"]+)"',f[8]); ex.add((f[0],int(f[3]),int(f[4]),f[6],m.group(1)))
with open("exons.txt","w") as o:
    o.write("chr\tstart\tend\tstrand\tgene_name\n")
    for e in sorted(ex): o.write("\t".join(map(str,e))+"\n")
print("exon file rows",len(ex))
PY
printf "$S1\tGBR\n$S2\tGBR\n$S3\tYRI\n$S4\tYRI\n" > groups_real.txt
printf "$S1\tP1\n$S3\tP1\n$S2\tP2\n$S4\tP2\n" > groups_perm.txt
echo "--- default flags on 2v2:"
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -e exons.txt -o ds_default lc10_perind_numers.counts.gz groups_real.txt > ds_default.log 2>&1; echo "rc=$?"; tail -1 ds_default.log | cut -c1-160
for cmp in real perm; do
  $RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 2 -g 2 -c 5 -e exons.txt -o ds_$cmp lc10_perind_numers.counts.gz groups_$cmp.txt > ds_$cmp.log 2>&1
  echo "leafcutter $cmp rc=$? tested $(grep -c Success ds_${cmp}_cluster_significance.txt) ; p.adjust<0.05: $(awk -F'\t' 'NR>1 && $6+0<0.05' ds_${cmp}_cluster_significance.txt | wc -l)"
  head -1 ds_${cmp}_cluster_significance.txt
done
