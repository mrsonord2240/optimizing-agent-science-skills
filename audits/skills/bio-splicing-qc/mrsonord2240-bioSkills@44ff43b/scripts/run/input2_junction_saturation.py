#!/usr/bin/env python
"""
Input 2 (variant A): junction saturation vs planted depth (SYNTHETIC deep / mid / shallow) + real chrX + edge cases.
Uses examples/splicing_qc.py::run_junction_saturation and the SKILL.md "plateau detection rule" (<2% rise from 80% to 100%).
Run: asenv as-core python input2_junction_saturation.py
"""
import sys, os, re, json, shutil, subprocess
import numpy as np
sys.dont_write_bytecode = True
RUN = '/mnt/openscience/audits/bio-splicing-qc/run'
D = f'{RUN}/data/synthetic'
AS = '/mnt/openscience/audit-envs/alternative-splicing/public-data'
W = f'{RUN}/work/in2'
shutil.rmtree(W, ignore_errors=True)
os.makedirs(W)
sys.path.insert(0, f'{RUN}/skill_copy/examples')
import splicing_qc as sq
import pysam
truth = json.load(open(f'{D}/truth.json'))

def parse_r(prefix):
    txt = open(f'{prefix}.junctionSaturation_plot.r').read()
    v = {}
    for k in 'xyzw':
        m = re.search(rf'^{k}=c\(([^)]*)\)', txt, re.M)
        v[k] = [int(float(t)) for t in m.group(1).split(',')]
    return v

def plateau_rule(vals, x):
    """SKILL.md: 'if from 80% to 100% of reads the junction count rises by <2%, consider it plateaued'"""
    i80 = x.index(80)
    if vals[i80] == 0:
        return None, 'undefined (0 junctions at 80%)'
    g = (vals[-1] - vals[i80]) / vals[i80]
    return g, 'PLATEAU' if g < 0.02 else 'STILL RISING'

def expected_known(counts, fr):
    return sum(1 - (1 - fr) ** c for c in counts)

res = {}
for nm in ['sat_deep', 'sat_mid', 'sat_shallow']:
    bam = f'{D}/se_{nm}.bam'
    pre = f'{W}/{nm}'
    sq.run_junction_saturation(bam, f'{D}/synth.bed12', pre)
    v = parse_r(pre)
    T = truth[nm]
    a_counts = [j['reads'] for j in T['junction_list'] if j['cls'] == 'A']
    exp = [expected_known(a_counts, x / 100) for x in v['x']]
    g_known, verdict_known = plateau_rule(v['y'], v['x'])
    g_all, verdict_all = plateau_rule(v['z'], v['x'])
    # analytic expected growth 80->100
    e_g = (exp[-1] - exp[v['x'].index(80)]) / exp[v['x'].index(80)]
    res[nm] = dict(x=v['x'], known=v['y'], all=v['z'], novel=v['w'], expected_known=[round(e, 1) for e in exp],
                   max_abs_dev_vs_expected=max(abs(a - b) for a, b in zip(v['y'], exp)),
                   known_growth_80_100=g_known, known_verdict=verdict_known, all_growth=g_all, all_verdict=verdict_all,
                   novel_growth=plateau_rule(v['w'], v['x'])[0], expected_known_growth=e_g,
                   lambda_A=T['lambda_A'], true_distinct_known=len(a_counts))
    print(nm, json.dumps({k: res[nm][k] for k in ['known_growth_80_100', 'known_verdict', 'all_growth', 'all_verdict', 'novel_growth', 'expected_known_growth', 'max_abs_dev_vs_expected', 'true_distinct_known']}, default=str), flush=True)
    print('  known curve:', v['y'])
    print('  expected   :', [round(e) for e in exp])

# independent count of distinct junctions at 100% (pysam)
def distinct(bam, mapq=30):
    s = set()
    with pysam.AlignmentFile(bam) as fh:
        for r in fh:
            if r.is_unmapped or r.is_secondary or r.mapping_quality < mapq:
                continue
            p = r.reference_start
            for op, ln in r.cigartuples:
                if op == 3:
                    s.add((p, p + ln))
                if op in (0, 2, 3, 7, 8):
                    p += ln
    return s
for nm in ['sat_deep', 'sat_mid', 'sat_shallow']:
    d = distinct(f'{D}/se_{nm}.bam')
    print(nm, 'pysam distinct junctions:', len(d), 'RSeQC all@100%:', res[nm]['all'][-1], 'known@100:', res[nm]['known'][-1])
    res[nm]['pysam_distinct_all'] = len(d)

# ---- edge: chromosome-name mismatch (BED contig 'S' vs BAM 'chrS')
pre = f'{W}/mismatch'
r = subprocess.run(['junction_saturation.py', '-i', f'{D}/se_sat_deep.bam', '-r', f'{D}/synth_nochr.bed12', '-o', pre], capture_output=True, text=True)
print('MISMATCH rc', r.returncode, 'stderr tail:', r.stderr[-400:].replace('\n', ' | '))
try:
    v = parse_r(pre)
    print('mismatch curves: known', v['y'][:3], '.. all', v['z'][:3], '.. ; plateau verdict (known):', plateau_rule(v['y'], v['x']))
    res['mismatch'] = dict(rc=r.returncode, known=v['y'], all=v['z'], verdict=plateau_rule(v['y'], v['x']))
except Exception as e:
    print('mismatch parse failed:', repr(e))
    res['mismatch'] = dict(rc=r.returncode, error=repr(e), stderr=r.stderr[-600:])

# ---- real chrX (XS BAM) with the gffread BED12
bed = f'{AS}/derived/chrX.bed12'
bam = f'{AS}/derived/xs_bams/ERR188383.xs.bam'
os.makedirs(f'{W}/real', exist_ok=True)
sq.run_junction_saturation(bam, bed, f'{W}/real/ERR188383')
v = parse_r(f'{W}/real/ERR188383')
res['real_chrX_ERR188383'] = dict(known=v['y'], all=v['z'], novel=v['w'], known_verdict=plateau_rule(v['y'], v['x']), all_verdict=plateau_rule(v['z'], v['x']), novel_verdict=plateau_rule(v['w'], v['x']))
print('REAL chrX known', v['y'], plateau_rule(v['y'], v['x']))
print('REAL chrX all  ', v['z'], plateau_rule(v['z'], v['x']))
print('REAL chrX novel', v['w'], plateau_rule(v['w'], v['x']))

# -s step flag (Skill: 'use -s flag to set custom step intervals')
pre = f'{W}/step1'
subprocess.run(['junction_saturation.py', '-i', f'{D}/se_sat_mid.bam', '-r', f'{D}/synth.bed12', '-o', pre, '-s', '1', '--skip-plot'], check=True, capture_output=True)
v = parse_r(pre)
print('-s 1 yields', len(v['x']), 'sampling points; first/last x', v['x'][0], v['x'][-1])
res['step1_points'] = len(v['x'])

json.dump(res, open(f'{RUN}/work/input2_result.json', 'w'), indent=1, default=str)
