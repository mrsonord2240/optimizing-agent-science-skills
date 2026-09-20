#!/bin/bash
# Input 3 (edge): REAL chrX 2v2 (GBR ERR188383,ERR188428 vs YRI ERR188454,ERR204916; 2x75 nt paired-end, unstranded, Ensembl GRCh37).
# n=2 vs n=2 is the design the Skill routes to Shiba / leafcutter and tells you to keep SUPPA2 away from.
# Also a PERMUTED comparison (one GBR + one YRI per side) as a mixed-population null-ish control.
# Truth is unknown for real data: we assert internal consistency, cross-tool concordance and no-crash behaviour.
# NOTE (as run 2026-09-20): the leafcutter section produced 0 clusters with the Skill's -m 50 on this small chrX subset, and the SUPPA2
# section failed because the auditor's TPM header carried a 'Name' label (SUPPA2 wants a header with only the sample names).
# Both were redone in in3b_leafcutter_real.sh and in3c_suppa_real.sh; the rMATS and Shiba sections here are the ones used.
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
D=$AS/public-data/rnasplice; XB=$AS/public-data/derived/xs_bams
LC=$AS/tools/src/leafcutter
CORE="micromamba run -n as-core"; RL="micromamba run -n as-rleaf"; SU="micromamba run -n as-suppa"; SH="micromamba run -n as-shiba"
R=/mnt/openscience/audits/bio-differential-splicing/run
W=$R/out/in3; rm -rf $W; mkdir -p $W; cd $W
GTF=$D/reference/genes_chrX.gtf
S1=ERR188383; S2=ERR188428; S3=ERR188454; S4=ERR204916
# comparisons: real = GBR(S1,S2) vs YRI(S3,S4); perm = (S1,S3) vs (S2,S4)
declare -A G1=( [real]="$S1 $S2" [perm]="$S1 $S3" ); declare -A G2=( [real]="$S3 $S4" [perm]="$S2 $S4" )
for cmp in real perm; do
  mkdir -p rmats_$cmp/tmp rmats_$cmp/out
  l1=""; for s in ${G1[$cmp]}; do l1="$l1,$D/bam/$s.Aligned.out.bam"; done; echo "${l1#,}" > rmats_$cmp/b1.txt
  l2=""; for s in ${G2[$cmp]}; do l2="$l2,$D/bam/$s.Aligned.out.bam"; done; echo "${l2#,}" > rmats_$cmp/b2.txt
  echo "=== rMATS $cmp, unstranded 75nt (SKILL flags minus wrong libType), --novelSS --cstat 0.05"
  $CORE rmats.py --b1 rmats_$cmp/b1.txt --b2 rmats_$cmp/b2.txt --gtf $GTF -t paired --readLength 75 --variable-read-length --libType fr-unstranded --nthread 8 --od rmats_$cmp/out --tmp rmats_$cmp/tmp --novelSS --cstat 0.05 > rmats_$cmp.log 2>&1
  echo "rc=$?"; for e in SE A3SS A5SS MXE RI; do echo "$e rows $(($(wc -l < rmats_$cmp/out/$e.MATS.JC.txt)-1))"; done
done
echo "=== rMATS real with the SKILL.md libType fr-firststrand (data are unstranded: infer_experiment ~0.46/0.45)"
mkdir -p rmats_fs/tmp rmats_fs/out
$CORE rmats.py --b1 rmats_real/b1.txt --b2 rmats_real/b2.txt --gtf $GTF -t paired --readLength 75 --variable-read-length --libType fr-firststrand --nthread 8 --od rmats_fs/out --tmp rmats_fs/tmp --novelSS --cstat 0.05 > rmats_fs.log 2>&1
echo "rc=$?"; echo "SE rows $(($(wc -l < rmats_fs/out/SE.MATS.JC.txt)-1))"
echo "total IJC+SJC summed over SE events, unstranded vs firststrand:"
for x in real fs; do awk -F'\t' 'NR>1{n=split($13,a,",");for(i=1;i<=n;i++)s+=a[i]; n=split($14,b,",");for(i=1;i<=n;i++)s+=b[i]; n=split($15,c,",");for(i=1;i<=n;i++)s+=c[i]; n=split($16,d,",");for(i=1;i<=n;i++)s+=d[i]} END{print FILENAME, s}' rmats_$x/out/SE.MATS.JC.txt; done

echo "=== leafcutter (XS-tagged copies of the BAMs; upstream STAR BAMs have no XS tag) -i 2 -g 2 -c 5"
mkdir -p lc; cd lc
for s in $S1 $S2 $S3 $S4; do $CORE regtools junctions extract -a 8 -m 50 -s XS $XB/$s.xs.bam -o $s.junc > /dev/null 2>&1; done
ls *.junc > juncfiles.txt
$CORE python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o lc -m 50 -l 500000 > cl.log 2>&1; echo "cluster rc=$?; intron rows $(zcat lc_perind_numers.counts.gz | tail -n +2 | wc -l)"
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
echo "--- leafcutter_ds.R with DEFAULT flags on 2v2 (SKILL says leafcutter needs n>=2):"
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -e exons.txt -o ds_default lc_perind_numers.counts.gz groups_real.txt > ds_default.log 2>&1; echo "rc=$?"; tail -2 ds_default.log | cut -c1-250
for cmp in real perm; do
  $RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 2 -g 2 -c 5 -e exons.txt -o ds_$cmp lc_perind_numers.counts.gz groups_$cmp.txt > ds_$cmp.log 2>&1
  echo "leafcutter $cmp rc=$? tested $(grep -c Success ds_${cmp}_cluster_significance.txt) sig p.adjust<0.05: $(awk -F'\t' 'NR>1 && $6+0<0.05' ds_${cmp}_cluster_significance.txt | wc -l)"
done
cd ..
echo "=== Shiba real + perm (strand: XS needs XS-tagged BAMs)"
for cmp in real perm; do
  mkdir -p shiba_$cmp; ( cd shiba_$cmp
  { printf 'sample\tbam\tgroup\ttechnology\n'
    for s in ${G1[$cmp]}; do printf '%s\t%s/%s.xs.bam\tRef\tshort\n' $s $XB $s; done
    for s in ${G2[$cmp]}; do printf '%s\t%s/%s.xs.bam\tAlt\tshort\n' $s $XB $s; done; } > exp.tsv
  cat > config.yaml <<CFG
workdir: $W/shiba_$cmp/out
gtf: $GTF
experiment_table: $W/shiba_$cmp/exp.tsv
unannotated: False
minimum_anchor_length: 6
minimum_intron_length: 70
maximum_intron_length: 500000
strand: XS
only_psi: False
only_psi_group: False
fdr: 0.05
delta_psi: 0.1
reference_group: Ref
alternative_group: Alt
minimum_reads: 10
individual_psi: True
ttest: False
excel: False
CFG
  $SH shiba.py -p 8 --mame config.yaml > shiba.log 2>&1; echo "shiba $cmp rc=$?"; tail -2 shiba.log | cut -c1-200 )
done
echo "=== SUPPA2 from Salmon TPM (same reads), events from the chrX GTF"
mkdir -p suppa; cd suppa
$CORE python - <<PY
import pandas as pd
S={"ERR188383":None,"ERR188428":None,"ERR188454":None,"ERR204916":None}
cols={}
for s in S:
    q=pd.read_csv("$D/salmon/%s/quant.sf"%s,sep="\t",index_col=0)
    cols[s]=q["TPM"]
t=pd.DataFrame(cols)
t.to_csv("tpm_all.tsv",sep="\t",float_format="%.4f")
t[["ERR188383","ERR188428"]].to_csv("gbr_tpm.tsv",sep="\t",float_format="%.4f")
t[["ERR188454","ERR204916"]].to_csv("yri_tpm.tsv",sep="\t",float_format="%.4f")
t[["ERR188383","ERR188454"]].to_csv("p1_tpm.tsv",sep="\t",float_format="%.4f")
t[["ERR188428","ERR204916"]].to_csv("p2_tpm.tsv",sep="\t",float_format="%.4f")
print("TPM table",t.shape)
PY
$SU suppa.py generateEvents -i $GTF -o events -f ioe -e SE SS MX RI > gen.log 2>&1; echo "generateEvents rc=$?"; ls events* | tr '\n' ' '; echo
for ev in SE A5 A3 MX RI; do
  for pair in "gbr yri real" "p1 p2 perm"; do set -- $pair
    $SU suppa.py psiPerEvent -i events_${ev}_strict.ioe -e ${1}_tpm.tsv -o ${1}_${ev} > psi_${1}_${ev}.log 2>&1
    $SU suppa.py psiPerEvent -i events_${ev}_strict.ioe -e ${2}_tpm.tsv -o ${2}_${ev} > psi_${2}_${ev}.log 2>&1
    for m in empirical classical; do
      $SU suppa.py diffSplice -m $m -gc -i events_${ev}_strict.ioe -p ${1}_${ev}.psi ${2}_${ev}.psi -e ${1}_tpm.tsv ${2}_tpm.tsv -o diff_${3}_${m}_${ev} > diff_${3}_${m}_${ev}.log 2>&1
      echo "$ev $3 $m rc=$? rows=$(($(wc -l < diff_${3}_${m}_${ev}.dpsi 2>/dev/null || echo 1)-1)) $(tail -1 diff_${3}_${m}_${ev}.log | cut -c1-120)"
    done
  done
done
