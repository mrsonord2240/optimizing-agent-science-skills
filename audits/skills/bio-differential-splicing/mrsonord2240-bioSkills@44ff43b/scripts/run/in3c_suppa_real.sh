#!/bin/bash
# Input 3c: SUPPA2 (as-suppa, 2.4) on Salmon TPM of the REAL chrX 2v2, following SKILL.md's loop exactly:
#   generateEvents -f ioe -e SE SS MX RI ; psiPerEvent ; diffSplice -m empirical -gc   and   -m classical.
# TPM files: header = sample names only (SUPPA2 requirement; not stated in SKILL.md).
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
D=$AS/public-data/rnasplice
CORE="micromamba run -n as-core"; SU="micromamba run -n as-suppa"
R=/mnt/openscience/audits/bio-differential-splicing/run
GTF=$D/reference/genes_chrX.gtf
W=$R/out/in3c; rm -rf $W; mkdir -p $W; cd $W
$CORE python - <<PY
import pandas as pd
cols={}
for s in ("ERR188383","ERR188428","ERR188454","ERR204916"):
    cols[s]=pd.read_csv("$D/salmon/%s/quant.sf"%s,sep="\t",index_col=0)["TPM"]
t=pd.DataFrame(cols)
def w(name, sub):
    with open(name,"w") as o:
        o.write("\t".join(sub)+"\n")
        for tid,row in t[sub].iterrows(): o.write(tid+"\t"+"\t".join("%.4f"%v for v in row)+"\n")
w("gbr_tpm.tsv",["ERR188383","ERR188428"]); w("yri_tpm.tsv",["ERR188454","ERR204916"])
w("p1_tpm.tsv",["ERR188383","ERR188454"]); w("p2_tpm.tsv",["ERR188428","ERR204916"])
print("TPM table",t.shape)
PY
$SU suppa.py generateEvents -i $GTF -o events -f ioe -e SE SS MX RI > gen.log 2>&1; echo "generateEvents rc=$?"; ls events*ioe | tr '\n' ' '; echo
for ev in SE A5 A3 MX RI; do echo "events $ev: $(($(wc -l < events_${ev}_strict.ioe)-1))"; done
for ev in SE A5 A3 MX RI; do
  for pair in "gbr yri real" "p1 p2 perm"; do set -- $pair
    $SU suppa.py psiPerEvent -i events_${ev}_strict.ioe -e ${1}_tpm.tsv -o ${1}_${ev} > psi_${1}_${ev}.log 2>&1
    $SU suppa.py psiPerEvent -i events_${ev}_strict.ioe -e ${2}_tpm.tsv -o ${2}_${ev} > psi_${2}_${ev}.log 2>&1
    for m in empirical classical; do
      $SU suppa.py diffSplice -m $m -gc -i events_${ev}_strict.ioe -p ${1}_${ev}.psi ${2}_${ev}.psi -e ${1}_tpm.tsv ${2}_tpm.tsv -o diff_${3}_${m}_${ev} > diff_${3}_${m}_${ev}.log 2>&1
      rc=$?; f=diff_${3}_${m}_${ev}.dpsi
      if [ -f $f ]; then n=$(($(wc -l < $f)-1)); sig=$(awk -F'\t' 'NR>1 && $3+0<0.05 && ($2+0>0.1 || $2+0<-0.1)' $f | wc -l); else n=NA; sig=NA; fi
      echo "$ev $3 $m rc=$rc tested=$n sig(p<0.05,|dPSI|>.1)=$sig"
    done
  done
done
echo "--- header of one dpsi file:"; head -3 diff_real_classical_SE.dpsi
echo "--- min p-value in classical real SE:"; awk -F'\t' 'NR>1 && $3!="nan"{print $3}' diff_real_classical_SE.dpsi | sort -g | head -3
