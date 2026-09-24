#!/bin/bash
# INPUT 5b (extras on the NEW sim2 data, after in5 has run):
#  (1) Shiba on the sim2 GTF WITHOUT decoys (SE, A5SS, A3SS only): Skill says "The GTF must contain every event type with reads (Shiba 0.8.2 raised a KeyError on a GTF with SE events only)"
#  (2) SKILL.md filter block (block 1) and Result Prioritization block (block 8) VERBATIM on the n=4 rMATS A-vs-B table
#  (3) which planted strong events does the Skill's coverage filter (min_inc + min_skip >= 10, minima over ALL replicates) drop as n grows?
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
S=$R/data/sim2
W=$R/out/in5b; rm -rf $W; mkdir -p $W; cd $W
echo "=== (1) Shiba n=2 on sim.gtf (no decoy event types)"
mkdir -p shiba_nodecoy; cd shiba_nodecoy
{ printf 'sample\tbam\tgroup\ttechnology\n'; for i in 1 2; do printf 'A%s\t%s/A%s.bam\tRef\tshort\n' $i $S $i; printf 'B%s\t%s/B%s.bam\tAlt\tshort\n' $i $S $i; done; } > exp.tsv
cat > config.yaml <<CFG
workdir: $W/shiba_nodecoy/out
gtf: $S/sim.gtf
experiment_table: $W/shiba_nodecoy/exp.tsv
unannotated: False
minimum_anchor_length: 6
minimum_intron_length: 50
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
$SH shiba.py -p 4 --mame config.yaml > shiba.log 2>&1; echo "rc=$?"; grep -a 'KeyError\|Error' shiba.log | head -3 | cut -c1-200; ls out/results/splicing 2>/dev/null | tr '\n' ' '; echo
cd ..
echo "=== (2) SKILL.md blocks 1 and 8 verbatim on sim2 n=4 A-vs-B rMATS output"
mkdir -p blk; cd blk
mkdir -p rmats_output; cp $R/out/in5/n4/rmats_AvB/out/*.txt rmats_output/
$CORE python $R/extract_blocks.py get 1 blk1.py; $CORE python $R/extract_blocks.py get 8 blk8.py
cat blk1.py blk8.py > run_blocks.py
echo "print('significant rows:', len(significant), '| top events:'); print(top_events[['GeneID','IncLevelDifference','FDR','exon_length','nmd_likely','score']].head(8).to_string())" >> run_blocks.py
$CORE python run_blocks.py 2>&1 | cut -c1-200
cd ..
echo "=== (3) coverage-filter loss by n (rMATS A-vs-B, SE + A5SS + A3SS): strong DS events with FDR<.05 & |dPSI|>.10 that fail min_inc+min_skip>=10"
$CORE python - <<'PY'
import pandas as pd, numpy as np
R = '/mnt/openscience/audits/bio-differential-splicing/run'
truth = pd.read_csv(f'{R}/data/sim2/truth.tsv', sep='\t', keep_default_na=False).set_index('gene')
strong = set(truth.index[truth['class'] == 'DS_strong'])
mr = lambda s: s.astype(str).str.split(',').apply(lambda x: min(int(v) for v in x))
for n in (2, 3, 4, 6):
    fr = [pd.read_csv(f'{R}/out/in5/n{n}/rmats_AvB/out/{ev}.MATS.JC.txt', sep='\t') for ev in ('SE', 'A5SS', 'A3SS')]
    d = pd.concat(fr, ignore_index=True); d['gene'] = d['GeneID'].str.strip('"')
    d['mi'] = mr(d['IJC_SAMPLE_1']).combine(mr(d['IJC_SAMPLE_2']), min); d['ms'] = mr(d['SJC_SAMPLE_1']).combine(mr(d['SJC_SAMPLE_2']), min)
    std = (d['FDR'] < 0.05) & (d['IncLevelDifference'].abs() > 0.10)
    tot = []
    for i, r in d.iterrows():
        a = [int(x) + int(y) for x, y in zip(str(r.IJC_SAMPLE_1).split(','), str(r.SJC_SAMPLE_1).split(','))] + [int(x) + int(y) for x, y in zip(str(r.IJC_SAMPLE_2).split(','), str(r.SJC_SAMPLE_2).split(','))]
        tot.append(min(a))
    d['rep_total_min'] = tot
    skill = std & ((d['mi'] + d['ms']) >= 10)
    alt = std & (d['rep_total_min'] >= 10)
    g_std, g_skill, g_alt = set(d.loc[std, 'gene']) & strong, set(d.loc[skill, 'gene']) & strong, set(d.loc[alt, 'gene']) & strong
    nullcalls = lambda m: len(set(d.loc[m, 'gene']) - set(truth.index[truth['class'].isin(['DS_strong', 'DS_moderate', 'DS_weak'])]))
    print(f'n={n}: strong found FDR+dPSI {len(g_std)}/28 | + Skill filter (sum of minima >= 10) {len(g_skill)}/28 | + per-replicate total >= 10 {len(g_alt)}/28 | false calls: {nullcalls(std)} / {nullcalls(skill)} / {nullcalls(alt)}')
    if n == 6:
        lost = d[std & ~skill & d['gene'].isin(strong)][['gene', 'IncLevel1', 'IncLevel2', 'mi', 'ms', 'rep_total_min']]
        print('n=6 strong events dropped by the Skill filter (min_inc, min_skip = minima over all 12 replicates):'); print(lost.head(10).to_string())
PY
