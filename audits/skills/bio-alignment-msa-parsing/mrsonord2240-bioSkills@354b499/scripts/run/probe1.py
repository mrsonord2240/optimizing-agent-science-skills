# Probe: what does AlignIO give for the real Pfam seed (gap chars, annotations)?
import warnings
from collections import Counter
from Bio import AlignIO
import Bio
print('biopython', Bio.__version__)
aln = AlignIO.read(r'F:\OpenScience\audit-envs\alignment\public-data\msa\PF00042_seed.sto', 'stockholm')
print(type(aln).__name__, len(aln), aln.get_alignment_length())
chars = Counter(''.join(str(r.seq) for r in aln))
print('non-letter chars:', {k: v for k, v in chars.items() if not k.isalpha()})
print('column_annotations keys:', list(aln.column_annotations.keys()))
r = aln[0]
print('record annotations keys:', list(r.annotations.keys()))
print('letter_annotations keys:', list(r.letter_annotations.keys()))
print("usage-guide key 'secondary_structure' in letter_annotations:", 'secondary_structure' in r.letter_annotations)
allk=set()
for rec in aln: allk|=set(rec.letter_annotations.keys())
print('all letter_annotation keys over records:', allk)
print("column_annotations.get('secondary_structure') ->", aln.column_annotations.get('secondary_structure'))
import Bio.Align.AlignInfo as AI
print('SummaryInfo attrs:', [a for a in dir(AI.SummaryInfo) if not a.startswith('_')])
import pyhmmer, pyhmmer.easel as e
print('pyhmmer', pyhmmer.__version__)
print('MSA attrs:', [a for a in dir(e.MSA) if 'weight' in a.lower()])
print('DigitalMSA attrs:', [a for a in dir(e.DigitalMSA) if 'weight' in a.lower()])
print('easel funcs w/ weight:', [a for a in dir(e) if 'weight' in a.lower()])
import pyhmmer.plan7 as p
print('Builder doc weight:', [l for l in (p.Builder.__init__.__doc__ or '').splitlines() if 'weight' in l.lower()][:6])
