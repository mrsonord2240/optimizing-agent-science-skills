"""Input 5: retention per trimmer, classified with the Skill's rules (<20% removed light; >40% removed too aggressive;
retention < 0.7 warn)."""
import os
from Bio import AlignIO

L0 = AlignIO.read('input.fasta', 'fasta').get_alignment_length()
files = ['clip_kpic-smart-gap', 'clip_smart-gap', 'clip_kpic-gappy', 'clip_kpi-smart-gap', 'trimal_strictplus',
         'trimal_automated1', 'trimal_gappyout', 'trimal_strict', 'bmge112_h04', 'bmge112_h05', 'bmge200_e04']
print(f'untrimmed columns: {L0}')
print(f'{"method":<22}{"cols":>6}{"retained":>10}{"removed":>9}  rule verdict')
for f in files:
    if not os.path.exists(f + '.fasta') or os.path.getsize(f + '.fasta') == 0:
        print(f'{f:<22} no output'); continue
    L = AlignIO.read(f + '.fasta', 'fasta').get_alignment_length()
    r = L / L0
    v = 'light (<20% removed)' if r > 0.8 else ('>40% removed: TOO AGGRESSIVE per 20/40 rule' if r < 0.6 else '20-40% removed')
    if r < 0.7:
        v += '; retention<0.7 cap WARN'
    print(f'{f:<22}{L:>6}{r:>10.1%}{1-r:>9.1%}  {v}')
