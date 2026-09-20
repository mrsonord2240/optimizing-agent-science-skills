#!/bin/bash
# Input 7: (a) Skill's PSI-residual confounder snippet on the sim; (b) leafcutter confounders as extra groups-file columns
# (SKILL.md claim: 3rd, 4th... columns; verified in leafcutter_ds.R source); (c) perfectly confounded batch; (d) rMATS with n=1 vs n=1.
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
LC=$AS/tools/src/leafcutter
CORE="micromamba run -n as-core"; RL="micromamba run -n as-rleaf"
R=/mnt/openscience/audits/bio-differential-splicing/run
S=$R/data/sim
W=$R/out/in7; rm -rf $W; mkdir -p $W; cd $W
echo "=== (a) SKILL.md residual + Wilcoxon confounder route"
$CORE python $R/in7_confounders.py $S
echo "=== (b) leafcutter_ds.R with a batch column (imbalanced), reusing the in5 clustering (A,B 3v3)"
cp $R/out/in5/lc/lc_perind_numers.counts.gz .
printf 'A1\tA\tb1\nA2\tA\tb1\nA3\tA\tb2\nB1\tB\tb1\nB2\tB\tb2\nB3\tB\tb2\n' > groups_batch.txt
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 3 -o ds_batch lc_perind_numers.counts.gz groups_batch.txt > ds_batch.log 2>&1; echo "rc=$?"; tail -2 ds_batch.log | cut -c1-200
echo "tested: $(grep -c Success ds_batch_cluster_significance.txt); p.adjust<0.05: $(awk -F'\t' 'NR>1 && $6+0<0.05' ds_batch_cluster_significance.txt | wc -l) (no-covariate run in in5: 22 of 24 strong DS genes found + 1 weak)"
echo "=== (c) leafcutter with batch perfectly confounded with group (batch = group)"
printf 'A1\tA\tb1\nA2\tA\tb1\nA3\tA\tb1\nB1\tB\tb2\nB2\tB\tb2\nB3\tB\tb2\n' > groups_conf.txt
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 3 -o ds_conf lc_perind_numers.counts.gz groups_conf.txt > ds_conf.log 2>&1; echo "rc=$?"; tail -3 ds_conf.log | cut -c1-250
echo "tested: $(grep -c Success ds_conf_cluster_significance.txt 2>/dev/null); sig: $(awk -F'\t' 'NR>1 && $6+0<0.05' ds_conf_cluster_significance.txt 2>/dev/null | wc -l)"
echo "=== (d) rMATS-turbo n=1 vs n=1 (A1 vs C1 = NULL; A1 vs B1 = truth): does the Skill stop the agent? rMATS runs:"
for cmp in AvC AvB; do g2=${cmp: -1}
  mkdir -p r1_$cmp/tmp r1_$cmp/out; echo "$S/A1.bam" > r1_$cmp/b1.txt; echo "$S/${g2}1.bam" > r1_$cmp/b2.txt
  $CORE rmats.py --b1 r1_$cmp/b1.txt --b2 r1_$cmp/b2.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od r1_$cmp/out --tmp r1_$cmp/tmp --novelSS --cstat 0.05 > r1_$cmp.log 2>&1
  echo "rMATS 1v1 $cmp rc=$?"
done
$CORE python - <<PY
import numpy as np, pandas as pd
truth=pd.read_csv("$S/truth.tsv",sep="\t").set_index("gene")
for cmp in ("AvC","AvB"):
    d=pd.read_csv("$W/r1_%s/out/SE.MATS.JC.txt"%cmp,sep="\t"); d["gene"]=d["GeneID"].str.strip('"'); d=d.set_index("gene")
    sig=d[(d["FDR"]<0.05)&(d["IncLevelDifference"].abs()>0.10)]
    isnull=[truth.loc[g,"class"] in ("nochange","nochange_lowcov") for g in sig.index]
    if cmp=="AvC":   # nothing was planted in A vs C: every call is a false positive
        print("rMATS 1v1 AvC (NULL): events %d, called (FDR<.05 & |dPSI|>.10): %d = all false positives"%(len(d),len(sig)))
    else:
        print("rMATS 1v1 AvB: events %d, called: %d; planted-DS genes among them: %d; null genes among them (FP): %d"%(len(d),len(sig),len(sig)-sum(isnull),sum(isnull)))
PY
