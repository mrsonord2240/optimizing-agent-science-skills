#!/bin/bash
# INPUT 5r (REGRESSION of the first audit's inputs 4/5): SYNTHETIC sim (first audit's generator, byte-identical data, 3 replicates, SE only, 24 strong + 6 weak planted, A vs C null),
# run with the FIXED Skill's instructions: rMATS (-t single --readLength 50 --novelSS --cstat 0.05), leafcutter (-i 3 -g 3 -c 10 -k True), SUPPA2 3v3 loop empirical and classical,
# and 2v2 for rMATS/leafcutter. First audit numbers (pre-fix Skill, same data): rMATS 3v3 24/24 strong 0 FP; leafcutter 22/24 strong; SUPPA2 empirical 23/24.
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
S=$R/data/sim
W=$R/out/in5r; rm -rf $W; mkdir -p $W; cd $W
for cmp in AvB AvC; do
  g2=${cmp: -1}
  mkdir -p rmats_$cmp/tmp rmats_$cmp/out
  $CORE rmats.py --b1 $S/b_A.txt --b2 $S/b_$g2.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od rmats_$cmp/out --tmp rmats_$cmp/tmp --novelSS --cstat 0.05 > rmats_$cmp.log 2>&1
  echo "rMATS 3v3 $cmp rc=$? SE rows $(($(wc -l < rmats_$cmp/out/SE.MATS.JC.txt)-1))"
done
mkdir -p lc; cd lc
for s in A1 A2 A3 B1 B2 B3 C1 C2 C3; do PATH=$R/bin:$PATH regtools junctions extract -a 8 -m 50 -s XS $S/$s.bam -o $s.junc > /dev/null 2>&1; done
ls *.junc > juncfiles.txt
PATH=$R/bin:$PATH python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o lc -m 50 -l 500000 -k True > cl.log 2>&1; echo "cluster rc=$? introns $(zcat lc_perind_numers.counts.gz | tail -n +2 | wc -l)"
for cmp in AvB AvC; do
  g2=${cmp: -1}
  printf 'A1\tA\nA2\tA\nA3\tA\n%s1\t%s\n%s2\t%s\n%s3\t%s\n' $g2 $g2 $g2 $g2 $g2 $g2 > groups_$cmp.txt
  $RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 3 -g 3 -c 10 -o ds_$cmp lc_perind_numers.counts.gz groups_$cmp.txt > ds_$cmp.log 2>&1
  echo "leafcutter 3v3 $cmp rc=$? tested $(ntested ds_${cmp}_cluster_significance.txt)"
done
cd ..
echo "=== SUPPA2 3v3 (SKILL.md loop; sim.gtf is SE-only, so only SE events exist)"
mkdir -p suppa; cd suppa
$CORE python - <<PY
import pandas as pd
t = pd.read_csv("$S/tpm_all.tsv", sep="\t", index_col=0)
for g in "ABC":
    sub = [g + str(i) for i in (1, 2, 3)]
    with open(g + "_tpm.tsv", "w") as o:
        o.write("\t".join(sub) + "\n")
        for tid, row in t[sub].iterrows(): o.write(tid + "\t" + "\t".join("%.3f" % v for v in row) + "\n")
PY
$SU suppa.py generateEvents -i $S/sim.gtf -o events -f ioe -e SE SS MX RI > gen.log 2>&1
for cmp in AvB AvC; do g2=${cmp: -1}
  $SU suppa.py psiPerEvent -i events_SE_strict.ioe -e A_tpm.tsv -o A_SE > /dev/null 2>&1; $SU suppa.py psiPerEvent -i events_SE_strict.ioe -e ${g2}_tpm.tsv -o ${g2}_SE > /dev/null 2>&1
  for m in empirical classical; do
    $SU suppa.py diffSplice -m $m -gc -i events_SE_strict.ioe -p A_SE.psi ${g2}_SE.psi -e A_tpm.tsv ${g2}_tpm.tsv -o diff_${cmp}_${m}_SE > d_${cmp}_$m.log 2>&1
  done
done
$CORE python - <<'PY'
import sys, numpy as np, pandas as pd
R = '/mnt/openscience/audits/bio-differential-splicing/run'
truth = pd.read_csv(f'{R}/data/sim/truth.tsv', sep='\t', keep_default_na=False).set_index('gene')
sign = np.sign(truth['delta_B_minus_A']); strong = set(truth.index[truth['class'] == 'DS_strong']); weak = set(truth.index[truth['class'] == 'DS_weak']); null = set(truth.index[truth['class'].isin(['nochange', 'nochange_lowcov'])])
for cmp in ('AvB', 'AvC'):
    for m in ('empirical', 'classical'):
        d = pd.read_csv(f'diff_{cmp}_{m}_SE.dpsi', sep='\t', index_col=0); d.columns = ['dpsi', 'p']; d.index = [i.split(';')[0] for i in d.index]; d = d.dropna()
        c = set(d.index[(d['p'] < 0.05) & (d['dpsi'].abs() > 0.10)])
        extra = f"strong {len(c & strong)}/24 weak {len(c & weak)}/6 false {len(c & null)} dir {sum(np.sign(d.loc[g,'dpsi']) == sign[g] for g in c & (strong | weak))}/{len(c & (strong | weak))} min p {d['p'].min():.3f}" if cmp == 'AvB' else f'calls on null {len(c)}'
        print(f'SUPPA2 {m:9s} {cmp} 3v3: {extra}')
PY
cd ..
echo "=== score rMATS and leafcutter 3v3 (first audit's eval_sim.py)"
$CORE python $R/eval_sim.py $S/truth.tsv $W 2>&1 | cut -c1-300
echo "=== rMATS + leafcutter 2v2 (A1,A2 vs B1,B2 / C1,C2)"
mkdir -p $W/two; cd $W/two
for cmp in AvB AvC; do g2=${cmp: -1}; mkdir -p rmats_$cmp/tmp rmats_$cmp/out
  echo "$S/A1.bam,$S/A2.bam" > b1_$cmp.txt; echo "$S/${g2}1.bam,$S/${g2}2.bam" > b2_$cmp.txt
  $CORE rmats.py --b1 b1_$cmp.txt --b2 b2_$cmp.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od rmats_$cmp/out --tmp rmats_$cmp/tmp --novelSS --cstat 0.05 > rmats_$cmp.log 2>&1
done
mkdir -p lc; cp $W/lc/lc_perind_numers.counts.gz lc/; cd lc
for cmp in AvB AvC; do g2=${cmp: -1}; printf 'A1\tA\nA2\tA\n%s1\t%s\n%s2\t%s\n' $g2 $g2 $g2 $g2 > groups_$cmp.txt
  $RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 2 -g 2 -c 10 -o ds_$cmp lc_perind_numers.counts.gz groups_$cmp.txt > ds_$cmp.log 2>&1; done
cd ..
$CORE python $R/eval_sim.py $S/truth.tsv $W/two 2>&1 | cut -c1-300
