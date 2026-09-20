#!/usr/bin/env python3
"""Input 4c: does samtools view -s 42.1 keep or drop all records of a template together (SKILL.md claim 1)?"""
import os, subprocess, sys, collections
import pysam
AFD = os.environ['AFDATA']; W = sys.argv[1]; os.makedirs(W, exist_ok=True)
src = f'{AFD}/1000g/HG00349.chr20_1400000-1500000.bam'
subprocess.run(f'samtools view -s 42.1 -b -o {W}/s42.bam {src}', shell=True, check=True)
full = collections.Counter(r.query_name for r in pysam.AlignmentFile(src))
sub = collections.Counter(r.query_name for r in pysam.AlignmentFile(f'{W}/s42.bam'))
bad = [q for q in sub if sub[q] != full[q]]
print('templates', len(full), 'kept', len(sub), f'({len(sub)/len(full):.3f})', 'templates with partial records kept:', len(bad))
assert not bad, bad[:3]
assert 0.08 <= len(sub) / len(full) <= 0.12
print('PASS samtools -s 42.1 pair/template-consistent, ~10%')
os.remove(f'{W}/s42.bam')
