"""
Input 5 (Stress) -- known-paralog-pair recovery check, analogous to the
"VALIDATION" section at the end of the Skill's own examples/gi_scoring.py
(which checks recovery of MAPK1/MAPK3, AKT1/AKT2, PIK3CA/PIK3CB,
HSP90AA1/HSP90AB1 against the called synthetic-lethal set).

Run against gi_scores_genome.tsv (Input 1's 200-pair output). The reference
list intentionally includes 3 pairs that WERE planted as synthetic-lethal and
2 pairs that were NOT, to confirm the recovery check discriminates correctly
rather than trivially matching everything.
"""
import pandas as pd

df = pd.read_csv('gi_scores_genome.tsv', sep='\t')

known_pairs = [
    ('G0001', 'G0002'),  # planted SL
    ('G0005', 'G0006'),  # planted SL
    ('G0009', 'G0010'),  # planted SL
    ('G0100', 'G0101'),  # NOT planted as interacting (negative control)
    ('G0150', 'G0151'),  # NOT planted as interacting (negative control)
]

sl_set = set(zip(
    df[df.gi_class == 'synthetic_lethal'].gene_A,
    df[df.gi_class == 'synthetic_lethal'].gene_B,
))

recovered = [p for p in known_pairs if p in sl_set]
print(f'Known pairs recovered as synthetic-lethal: {len(recovered)}/{len(known_pairs)} -> {recovered}')
