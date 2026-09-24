"""Input 4: junction_stats() vs planted truths. Usage (in as-core): python 41_in4_junctions.py <skill examples dir> <data dir>"""
import sys, json, subprocess
sys.path.insert(0, sys.argv[1]); import splicing_qc as sq
d = sys.argv[2]
# --- A. the auditor's original planted overhang library (truth.json 'overhang')
st = sq.junction_stats(f'{d}/synthetic/se_overhang.bam', min_overhang=8)
print('se_overhang.bam junctions:', len(st))
import pysam
print('   (12 reads per read type; expected overhangs: micro4 -> 4 and 4, micro10 -> 10 and 10, ov6 -> 6, ov50 -> 50)')
by_ov = {}
for k, v in sorted(st.items()):
    by_ov.setdefault(v['min_overhang'], []).append((k[1], k[2], v['reads'], v['reads_all']))
for ov, lst in sorted(by_ov.items()): print('   min_overhang', ov, '->', len(lst), 'junctions; (reads>=8, reads_all):', sorted(set((a[2], a[3]) for a in lst)))
# --- B. my edge BAM vs hand truth
truth = json.load(open(f'{d}/edge_truth.json')); ok = 0; bad = []
st8 = sq.junction_stats(f'{d}/edge.bam', min_overhang=8); st0 = sq.junction_stats(f'{d}/edge.bam', min_overhang=0)
print('edge.bam: helper found', len(st8), 'junctions; truth', len(truth))
for k, (r8, rall, mo) in truth.items():
    c, a, b = k.split(':')[0], *map(int, k.split(':')[1].split('-'))
    key = (c, a, b); got = st8.get(key)
    exp = {'reads': r8, 'reads_all': rall, 'min_overhang': mo}
    if got == exp: ok += 1
    else: bad.append((k, exp, got))
print('junctions equal to hand truth:', ok, 'of', len(truth)); [print('   MISMATCH', b) for b in bad]
print('extra junctions not in truth:', [k for k in st8 if f'{k[0]}:{k[1]}-{k[2]}' not in truth])
print('min_overhang=0: tiny junction reads', st0[('chrT', 12003, 12503)]['reads'], '(expected 7); min_overhang=30 on pA (mates 50/20 overhang):', sq.junction_stats(f'{d}/edge.bam', min_overhang=30)[('chrT', 8050, 8850)]['reads'], '(expected 5: mate 1 has 50)')
print('min_overhang=60 on pA:', sq.junction_stats(f'{d}/edge.bam', min_overhang=60)[('chrT', 8050, 8850)]['reads'], '(expected 0)')
print('summarize:', sq.summarize_junctions(st8))
