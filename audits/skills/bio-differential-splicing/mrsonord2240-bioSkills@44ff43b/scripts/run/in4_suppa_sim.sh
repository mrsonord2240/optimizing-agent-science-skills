#!/bin/bash
# Input 4 (Variant B): SUPPA2 2.4 on the SYNTHETIC 120-gene sim (TPM from the same molecules as the BAMs), 3v3, following the
# SKILL.md loop verbatim: generateEvents -f ioe -e SE SS MX RI ; psiPerEvent ; diffSplice -m empirical -gc / -m classical.
# Truth: 24 strong + 6 weak planted dPSI genes (A vs B), none in A vs C.
export PYTHONDONTWRITEBYTECODE=1
R=/mnt/openscience/audits/bio-differential-splicing/run
S=$R/data/sim
CORE="micromamba run -n as-core"; SU="micromamba run -n as-suppa"
W=$R/out/in4; rm -rf $W; mkdir -p $W; cd $W
$CORE python - <<PY
import pandas as pd
t=pd.read_csv("$S/tpm_all.tsv",sep="\t",index_col=0)
def w(name, sub):
    with open(name,"w") as o:
        o.write("\t".join(sub)+"\n")
        for tid,row in t[sub].iterrows(): o.write(tid+"\t"+"\t".join("%.3f"%v for v in row)+"\n")
w("A_tpm.tsv",["A1","A2","A3"]); w("B_tpm.tsv",["B1","B2","B3"]); w("C_tpm.tsv",["C1","C2","C3"])
PY
$SU suppa.py generateEvents -i $S/sim.gtf -o events -f ioe -e SE SS MX RI > gen.log 2>&1; echo "generateEvents rc=$?"; tail -2 gen.log | cut -c1-200
for ev in SE A5 A3 MX RI; do [ -f events_${ev}_strict.ioe ] && echo "events $ev: $(($(wc -l < events_${ev}_strict.ioe)-1))" || echo "events $ev: file absent"; done
for cmp in AvB AvC; do
  g2=${cmp: -1}
  for ev in SE; do   # only SE exists in the simulated annotation
    $SU suppa.py psiPerEvent -i events_${ev}_strict.ioe -e A_tpm.tsv -o A_${ev} > psiA.log 2>&1
    $SU suppa.py psiPerEvent -i events_${ev}_strict.ioe -e ${g2}_tpm.tsv -o ${g2}_${ev} > psi$g2.log 2>&1
    for m in empirical classical; do
      $SU suppa.py diffSplice -m $m -gc -i events_${ev}_strict.ioe -p A_${ev}.psi ${g2}_${ev}.psi -e A_tpm.tsv ${g2}_tpm.tsv -o diff_${cmp}_${m}_${ev} > diff_${cmp}_${m}.log 2>&1
      echo "$cmp $m rc=$? files: $(ls diff_${cmp}_${m}_${ev}.* 2>/dev/null | tr '\n' ' ')"
    done
  done
done
cat > eval_suppa.py <<'PY'
import sys, numpy as np, pandas as pd
truth = pd.read_csv(sys.argv[1], sep='\t').set_index('gene')
exp_sign = np.sign(truth['delta_B_minus_A'])   # SUPPA2 dPSI = mean(cond2) - mean(cond1) = B - A (verified in lib/diff_tools.py calculate_delta_psi and on G000)
strong = set(truth.index[truth['class'] == 'DS_strong']); weak = set(truth.index[truth['class'] == 'DS_weak'])
null = set(truth.index[truth['class'].isin(['nochange', 'nochange_lowcov'])])
for cmp in ('AvB', 'AvC'):
    for m in ('empirical', 'classical'):
        d = pd.read_csv(f'diff_{cmp}_{m}_SE.dpsi', sep='\t', index_col=0)
        d.columns = ['dpsi', 'p']
        d.index = [i.split(';')[0] for i in d.index]
        n_nan = int(d['p'].isna().sum()); dd = d.dropna()
        called = set(dd.index[(dd['p'] < 0.05) & (dd['dpsi'].abs() > 0.10)])
        r = dict(events=len(d), p_nan=n_nan, min_p=float(dd['p'].min()), n_called=len(called))
        if cmp == 'AvB':
            r.update(strong=f'{len(called & strong)}/{len(strong)}', weak=f'{len(called & weak)}/{len(weak)}', FP_null=len(called & null),
                     dir_ok=f"{sum(np.sign(dd.loc[g,'dpsi']) == exp_sign[g] for g in called & (strong | weak))}/{len(called & (strong | weak))}")
        else:
            r['FP_null'] = len(called)
        print(f'SUPPA2 {m:9s} {cmp}:', r)
PY
$CORE python eval_suppa.py $S/truth.tsv
