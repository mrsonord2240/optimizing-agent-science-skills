#!/usr/bin/env python
"""
Input 1 (canonical): junction annotation known/novel on SYNTHETIC BAMs with planted class fractions.
Uses the Skill's own code paths: examples/splicing_qc.py::run_junction_annotation and the SKILL.md pandas snippet.
Run: asenv as-core python input1_junction_annotation.py
"""
import sys, os, json, subprocess, shutil
from collections import Counter
sys.dont_write_bytecode = True
RUN = '/mnt/openscience/audits/bio-splicing-qc/run'
D = f'{RUN}/data/synthetic'
W = f'{RUN}/work/in1'
shutil.rmtree(W, ignore_errors=True)
os.makedirs(W)
sys.path.insert(0, f'{RUN}/skill_copy/examples')
import splicing_qc as sq          # the Skill's shipped example (copied, not in external/)
import pandas as pd
import pysam

truth = json.load(open(f'{D}/truth.json'))

def skill_md_snippet(prefix):
    """verbatim logic of the SKILL.md 'Novel-vs-Known' python block"""
    junc = pd.read_csv(f'{prefix}.junction.xls', sep='\t')
    total = junc['read_count'].sum()
    by_class = junc.groupby('annotation')['read_count'].sum()
    known_frac = by_class.get('annotated', 0) / total
    novel_frac = (by_class.get('partial_novel', 0) + by_class.get('complete_novel', 0)) / total
    return junc, by_class, known_frac, novel_frac

def indep_count(bam, bed):
    """independent pysam count with the same semantics as RSeQC (known = donor in known set AND acceptor in known set)"""
    KD, KA, KJ = set(), set(), set()
    for l in open(bed):
        f = l.split()
        s = int(f[1]); sizes = [int(x) for x in f[10].strip(',').split(',')]; rel = [int(x) for x in f[11].strip(',').split(',')]
        ex = [(s + r, s + r + z) for r, z in zip(rel, sizes)]
        for (a, b), (c, d) in zip(ex[:-1], ex[1:]):
            KD.add(b); KA.add(c); KJ.add((b, c))
    cnt = Counter()
    with pysam.AlignmentFile(bam) as fh:
        for r in fh:
            if r.is_unmapped or r.is_secondary or r.mapping_quality < 30:
                continue
            pos = r.reference_start
            for op, ln in r.cigartuples:
                if op == 3:
                    cnt[(pos, pos + ln)] += 1
                if op in (0, 2, 3, 7, 8):
                    pos += ln
    cl = Counter(); cj = Counter(); strict = Counter()
    for (d, a), c in cnt.items():
        dk, ak = d in KD, a in KA
        k = 'annotated' if (dk and ak) else ('complete_novel' if (not dk and not ak) else 'partial_novel')
        cl[k] += c; cj[k] += 1
        strict['strict_annotated' if (d, a) in KJ else 'not_strict'] += c
    return cl, cj, strict

out = {}
for name in ['clean', 'novelrich']:
    bam = f'{D}/se_{name}.bam'
    prefix = f'{W}/{name}'
    print(f'=== {name}: Skill example run_junction_annotation() ===', flush=True)
    try:
        stats = sq.run_junction_annotation(bam, f'{D}/synth.bed12', prefix)
        print('run_junction_annotation returned DataFrame:', stats is not None, flush=True)
        ok_run = True
    except subprocess.CalledProcessError as e:
        print('SKILL EXAMPLE RAISED CalledProcessError', e, flush=True)
        ok_run = False
        # rerun with --skip-plot so we can still test the parse
        subprocess.run(['junction_annotation.py', '-i', bam, '-r', f'{D}/synth.bed12', '-o', prefix, '--skip-plot'], check=True)
    # SKILL.md snippet
    junc, by_class, kf, nf = skill_md_snippet(prefix)
    print('columns:', list(junc.columns))
    print('distinct annotation values (repr):', [repr(x) for x in junc['annotation'].unique()])
    print(f'SKILL.md snippet -> known: {kf:.1%}, novel: {nf:.1%}')
    # corrected parse (strip)
    junc['annotation'] = junc['annotation'].str.strip()
    by2 = junc.groupby('annotation')['read_count'].sum()
    tot = junc['read_count'].sum()
    kf2 = by2.get('annotated', 0) / tot
    nf2 = (by2.get('partial_novel', 0) + by2.get('complete_novel', 0)) / tot
    cl, cj, strict = indep_count(bam, f'{D}/synth.bed12')
    T = truth[name]
    res = dict(ran_ok=ok_run,
               skill_snippet_known=kf, skill_snippet_novel=nf,
               stripped_known=kf2, stripped_novel=nf2,
               indep_known_read_frac=cl['annotated'] / sum(cl.values()),
               truth_rseqc_known_read_frac=T['rseqc_known_read_frac'],
               truth_strict_annotated_read_frac=T['strict_annotated_read_frac'],
               truth_partial=T['partial_novel_read_frac'], truth_complete=T['complete_novel_read_frac'],
               rseqc_read_counts=by2.to_dict(), indep_read_counts=dict(cl),
               rseqc_junction_counts=junc.groupby('annotation').size().to_dict(), indep_junction_counts=dict(cj),
               truth_junction_counts={k: v['junctions'] for k, v in T['by_class'].items()},
               truth_known_junction_frac=T['rseqc_known_junction_frac'])
    out[name] = res
    print(json.dumps(res, indent=1, default=str))

json.dump(out, open(f'{RUN}/work/input1_result.json', 'w'), indent=1, default=str)
