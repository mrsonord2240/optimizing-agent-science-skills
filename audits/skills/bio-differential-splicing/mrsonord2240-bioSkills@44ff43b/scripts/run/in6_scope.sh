#!/bin/bash
# Input 6 (scope boundary): (a) MAJIQ V3 / VOILA availability (licence-gated, not installed); (b) single patient vs cohort hand-off tool leafcutterMD.R -h;
# (c) SKILL.md 'paired tumor-normal: rMATS --paired-stats' on the SYNTHETIC sim (A_i paired with B_i).
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
CORE="micromamba run -n as-core"
R=/mnt/openscience/audits/bio-differential-splicing/run; S=$R/data/sim
W=$R/out/in6; rm -rf $W; mkdir -p $W; cd $W
echo "=== (a) MAJIQ / VOILA"
for t in majiq voila; do which $t >/dev/null 2>&1 && echo "$t found" || echo "$t: NOT INSTALLED (licence-gated academic download; commands in SKILL.md cannot be executed)"; done
echo "=== (b) leafcutterMD.R -h (hand-off target for n=1 vs cohort)"
leafcutterMD.R -h 2>&1 | tr '\r' '\n' | head -25
echo "=== (c) rMATS --paired-stats, A1..A3 vs B1..B3 as pairs"
mkdir -p p/tmp p/out
$CORE rmats.py --b1 $S/b_A.txt --b2 $S/b_B.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od p/out --tmp p/tmp --novelSS --paired-stats > p.log 2>&1; echo "rc=$?"; tail -2 p.log | cut -c1-200
$CORE python - <<PY
import numpy as np, pandas as pd
t=pd.read_csv("$S/truth.tsv",sep="\t").set_index("gene")
d=pd.read_csv("$W/p/out/SE.MATS.JC.txt",sep="\t"); d["gene"]=d["GeneID"].str.strip('"'); d=d.set_index("gene")
sig=d[(d["FDR"]<0.05)&(d["IncLevelDifference"].abs()>0.10)]
print("paired-stats: events",len(d),"| FDR NaN:",int(d["FDR"].isna().sum()),"| called",len(sig),"| min FDR %.4f"%d["FDR"].min())
print("paired 3-pair min p possible (sign/Wilcoxon-type) -> planted strong DS detected:",sum(t.loc[g,"class"]=="DS_strong" for g in sig.index),"/24")
PY
