"""Probe of the new min_occupancy NaN default: the usage-guide prompt "Which columns are most conserved?" is answered by ranking
column_conservation() values. Python's sort/max with NaN keys is order-dependent and silent. Does an agent following SKILL.md
get a wrong top-10 on the real Pfam seed (23 NaN columns) and the real kinase seed (157 NaN columns)?  Compare against
(a) NaN-aware ranking, (b) the pre-fix behaviour (NaN -> occupied-column raw score with no occupancy rule).
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b11_nan_ranking_probe.py"""
import os, sys, math
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import battery as B, msa_utils, conservation_profile as CP
for tag, path, fmt in [('Pfam globin seed', os.path.join(HERE, 'data', 'seed_dot.fasta'), 'fasta'), ('Pfam kinase seed', os.path.join(HERE, 'data', 'new', 'PF00069.sto'), 'stockholm')]:
    aln = msa_utils.load_alignment(path, fmt); L = aln.get_alignment_length()
    cons = [CP.column_conservation(aln, i) for i in range(L)]
    nn = sum(math.isnan(x) for x in cons)
    naive_sorted = sorted(range(L), key=lambda i: -cons[i])[:10]                       # what a naive agent writes
    naive_max = max(range(L), key=lambda i: cons[i])
    clean = [(i, c) for i, c in enumerate(cons) if not math.isnan(c)]
    proper = [i for i, c in sorted(clean, key=lambda t: -t[1])][:10]
    proper_vals = sorted([c for _, c in clean], reverse=True)[:10]
    naive_vals = [cons[i] for i in naive_sorted]
    raw0 = [CP.column_conservation(aln, i, min_occupancy=0.0) for i in range(L)]
    prefix = sorted(range(L), key=lambda i: -(0.0 if math.isnan(raw0[i]) else raw0[i]))[:10]
    print(f'{tag}: {nn} NaN columns of {L}')
    print('   naive sorted(key=-cons)[:10]  :', naive_sorted, [None if math.isnan(x) else round(x, 2) for x in naive_vals])
    print('   NaN-aware top-10               :', proper, [round(x, 2) for x in proper_vals])
    print('   naive == NaN-aware top-10      :', set(naive_sorted) == set(proper), '| NaN columns inside naive top-10:', sum(math.isnan(cons[i]) for i in naive_sorted))
    print('   naive max() column value       :', cons[naive_max], '(NaN means max returned a NaN column)')
    print('   pre-fix style (no occupancy rule) top-10: columns with <50% residues (now NaN):', sum(1 for i in prefix if math.isnan(cons[i])))
