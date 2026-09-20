#!/usr/bin/env python
"""Parse Input 7 outputs (run after input7_contam_bias.sh) and assert against planted truth. Run: asenv as-core python input7_parse.py"""
import os, re, json, glob
import numpy as np
W = '/mnt/openscience/audits/bio-splicing-qc/run/work/in7'
R = '/mnt/openscience/audits/bio-splicing-qc/run'
res = {}

def picard(path):
    rows = [l.rstrip('\n').split('\t') for l in open(path) if l.strip() and not l.startswith('#')]
    hdr = rows[0]; val = rows[1]
    return dict(zip(hdr, val))

def f(x):
    try: return float(x)
    except: return x

print('--- Picard CollectRnaSeqMetrics (pe_* synthetic; dUTP protocol => truth: SECOND_READ_TRANSCRIPTION_STRAND correct)')
for n in ['dutp', 'bias3', 'rrna']:
    for ss in ['SECOND_READ_TRANSCRIPTION_STRAND', 'FIRST_READ_TRANSCRIPTION_STRAND']:
        p = f'{W}/pic_{n}_{ss}.txt'
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            print(n, ss, 'NO OUTPUT; log tail:', open(p.replace('.txt', '.log')).read()[-300:].replace('\n', ' | ')); continue
        d = picard(p)
        keep = {k: f(d[k]) for k in ['PF_BASES', 'PCT_RIBOSOMAL_BASES', 'PCT_CODING_BASES', 'PCT_UTR_BASES', 'PCT_INTRONIC_BASES', 'PCT_INTERGENIC_BASES', 'PCT_MRNA_BASES',
                                     'PCT_CORRECT_STRAND_READS', 'PCT_INCORRECT_STRAND_READS', 'MEDIAN_CV_COVERAGE', 'MEDIAN_5PRIME_BIAS', 'MEDIAN_3PRIME_BIAS', 'MEDIAN_5PRIME_TO_3PRIME_BIAS'] if k in d}
        res[f'{n}_{ss}'] = keep
        print(n, ss.split('_')[0], {k: (round(v, 3) if isinstance(v, float) else v) for k, v in keep.items()})

print('--- geneBody_coverage uniform vs 3-prime biased')
for n in ['dutp', 'bias3']:
    txt = open(f'{W}/gb_{n}.geneBodyCoverage.txt').read().strip().split('\n')
    lab = txt[0].split('\t'); vals = np.array([float(v) for v in txt[1].split('\t')[1:]])
    lab = lab[1:] if lab[0] == 'Percentile' else lab
    lo, hi = vals[:20].mean(), vals[80:].mean()
    print(n, '5prime(first 20%%) mean %.1f  3prime(last 20%%) mean %.1f  ratio 5p/3p %.2f  (gene strand-aware; RSeQC flips minus-strand genes)' % (lo, hi, lo / hi))
    res[f'gb_{n}'] = dict(ratio_5p_3p=float(lo / hi), first20=float(lo), last20=float(hi))

print('--- samtools recipe (see stdout of input7_contam_bias.sh)')
json.dump(res, open(f'{R}/work/input7_result.json', 'w'), indent=1)
