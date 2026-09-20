#!/bin/bash
# INPUT 4 (variant B, NEW measurement): SUPPA2 2.4 on SYNTHETIC sim2 (TPM built from the same molecules as the BAMs), n = 2..6 per group,
# following the SKILL.md loop (generateEvents -f ioe -e SE SS MX RI; psiPerEvent; diffSplice -m empirical -gc) and the classical variant.
# RE-MEASURES the Skill's "n>=4 in either mode" rule and its n=2..5 table on a different simulation (own seed, SE+A5SS+A3SS events).
# Truth: 28 strong + 8 moderate + 6 weak planted (A vs B); A vs C is the null comparison. TPM header = sample names only.
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
S=$R/data/sim2
W=$R/out/in4; rm -rf $W; mkdir -p $W; cd $W
$CORE python - <<PY
import pandas as pd
t = pd.read_csv("$S/tpm_all.tsv", sep="\t", index_col=0)
for n in range(2, 7):
    for g in "ABC":
        sub = ["%s%d" % (g, i) for i in range(1, n + 1)]
        with open("n%d_%s_tpm.tsv" % (n, g), "w") as o:
            o.write("\t".join(sub) + "\n")
            for tid, row in t[sub].iterrows(): o.write(tid + "\t" + "\t".join("%.3f" % v for v in row) + "\n")
print("TPM subsets written", t.shape)
PY
$SU suppa.py generateEvents -i $S/sim.gtf -o events -f ioe -e SE SS MX RI > gen.log 2>&1; echo "generateEvents rc=$?"
for ev in SE A5 A3 MX RI; do [ -f events_${ev}_strict.ioe ] && echo "events $ev: $(($(wc -l < events_${ev}_strict.ioe)-1))" || echo "events $ev: absent"; done
one() {
  local n=$1
  for ev in SE A5 A3; do
    for g in A B C; do micromamba run -n as-suppa suppa.py psiPerEvent -i events_${ev}_strict.ioe -e n${n}_${g}_tpm.tsv -o n${n}_${g}_${ev} > n${n}_${g}_${ev}.psilog 2>&1; done
    for g2 in B C; do
      for m in empirical classical; do
        micromamba run -n as-suppa suppa.py diffSplice -m $m -gc -i events_${ev}_strict.ioe -p n${n}_A_${ev}.psi n${n}_${g2}_${ev}.psi -e n${n}_A_tpm.tsv n${n}_${g2}_tpm.tsv -o d_n${n}_Av${g2}_${m}_${ev} > d_n${n}_Av${g2}_${m}_${ev}.log 2>&1
      done
    done
  done
}
for n in 2 3 4 5 6; do one $n; done      # serial: a first run with the five sizes in parallel lost two .dpsi files silently (rc 0, "Done!", no output file)
echo "dpsi files written: $(ls d_n*_*.dpsi | wc -l) of 60"; [ $(ls d_n*_*.dpsi | wc -l) -eq 60 ] || echo "ASSERT FAIL: missing dpsi files"
cat > eval_suppa2.py <<'PY'
import sys, numpy as np, pandas as pd
truth = pd.read_csv(sys.argv[1], sep='\t', keep_default_na=False).set_index('gene')
sign = np.sign(truth['delta_cond1_minus_cond0'])           # SUPPA2 dPSI = mean(cond2) - mean(cond1) = B - A
strong = set(truth.index[truth['class'] == 'DS_strong']); mod = set(truth.index[truth['class'] == 'DS_moderate']); weak = set(truth.index[truth['class'] == 'DS_weak'])
null = set(truth.index[truth['class'].str.startswith('null')]); se_ds = set(truth.index[(truth['etype'] == 'SE') & truth['class'].str.startswith('DS')])
print('planted: strong %d, moderate %d, weak %d, null genes %d' % (len(strong), len(mod), len(weak), len(null)))
for n in (2, 3, 4, 5, 6):
    for m in ('empirical', 'classical'):
        out = {}
        for cmp in ('AvB', 'AvC'):
            fr = []
            for ev in ('SE', 'A5', 'A3'):
                d = pd.read_csv(f'd_n{n}_{cmp}_{m}_{ev}.dpsi', sep='\t', index_col=0); d.columns = ['dpsi', 'p']; d.index = [i.split(';')[0] for i in d.index]; fr.append(d)
            d = pd.concat(fr); nn = int(d['p'].isna().sum()); d = d.dropna()
            called = set(d.index[(d['p'] < 0.05) & (d['dpsi'].abs() > 0.10)])
            out[cmp] = (called, float(d['p'].min()), len(d), nn, d)
        cb, minp, ne, nn, d = out['AvB']
        dirn = sum(np.sign(d.loc[g, 'dpsi']) == sign[g] for g in cb & se_ds)
        print(f'SUPPA2 {m:9s} n={n}: events {ne} (p NaN {nn}) | strong {len(cb & strong)}/{len(strong)} moderate {len(cb & mod)}/{len(mod)} weak {len(cb & weak)}/{len(weak)} | '
              f'false calls {len(cb & null)}/{len(cb)} | dir(SE) {dirn}/{len(cb & se_ds)} | min p {minp:.4f} | calls on NULL A-vs-C: {len(out["AvC"][0])}')
PY
$CORE python eval_suppa2.py $S/truth.tsv | tee eval_suppa2.txt
