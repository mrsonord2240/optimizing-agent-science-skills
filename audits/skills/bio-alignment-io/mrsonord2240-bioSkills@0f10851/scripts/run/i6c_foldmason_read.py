"""INPUT 6c: Foldmason result_aa.fa / result_3di.fa loaded with AlignIO / Bio.Align (SKILL Related Skills claim), REAL structures 1MBN/1A6M/1EMY."""
import os
from Bio import AlignIO, Align
from common import *
d = DATA/'fm'; os.chdir(d)
aa = AlignIO.read('result_aa.fa', 'fasta'); td = AlignIO.read('result_3di.fa', 'fasta')
print('ids', [r.id for r in aa], aa.get_alignment_length(), td.get_alignment_length())
ok(len(aa) == 3 and aa.get_alignment_length() == td.get_alignment_length(), 'aa and 3Di alignments load with AlignIO and have the same shape')
a2 = Align.read('result_aa.fa', 'fasta'); ok(a2.shape == (3, aa.get_alignment_length()), f'Align.read shape {a2.shape}')
r = [str(x.seq) for x in aa]; pairs = [(a, b) for a, b in zip(r[0], r[1]) if a != '-' and b != '-']
idn = sum(a == b for a, b in pairs) / len(pairs); ok(idn > 0.95, f'1MBN vs 1A6M column identity {idn:.3f} > 0.95 (same sperm-whale myoglobin, content sanity)')
import pathlib
h = pathlib.Path('result.html'); ok(h.exists() and h.read_text(errors='ignore', encoding='utf-8')[:400].lower().count('<') > 0, 'per-column LDDT report is HTML (SKILL says HTML, not BioPython-parseable)')
try: AlignIO.read('result.html', 'fasta'); ok(False, 'AlignIO parsed HTML?!')
except Exception as e: ok(True, f'AlignIO cannot parse the HTML report: {type(e).__name__}')
summary()
