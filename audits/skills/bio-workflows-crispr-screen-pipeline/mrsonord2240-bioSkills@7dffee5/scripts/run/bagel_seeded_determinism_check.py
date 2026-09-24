# Regression test for the fixed Skill Veto T3 (determinism) / Research Veto M3 finding:
# BAGEL2 bf run twice with the fixed SKILL.md's now-documented `-s 42` seed, on the
# same real HAP1 TKOv3 fold-change file (experiment.foldchange) used pre-fix.
# CLI invocations (run via PowerShell, native Windows PATH for RRA.exe/BAGEL.py deps):
#
# python BAGEL.py bf -i experiment.foldchange -o bayes_factor_seeded_run1.txt \
#   -e CEGv2.txt -n NEGv1.txt -c T18_A,T18_B,T18_C -s 42
# python BAGEL.py bf -i experiment.foldchange -o bayes_factor_seeded_run2.txt \
#   -e CEGv2.txt -n NEGv1.txt -c T18_A,T18_B,T18_C -s 42
import pandas as pd

a = pd.read_csv('bayes_factor_seeded_run1.txt', sep='\t')
b = pd.read_csv('bayes_factor_seeded_run2.txt', sep='\t')
m = a.merge(b, on='GENE', suffixes=('_1', '_2'))
print('mean abs diff:', (m['BF_1'] - m['BF_2']).abs().mean())
print('max abs diff:', (m['BF_1'] - m['BF_2']).abs().max())
h1 = (m['BF_1'] > 6)
h2 = (m['BF_2'] > 6)
print('BF>6 flips:', (h1 != h2).sum(), '/', len(m))
