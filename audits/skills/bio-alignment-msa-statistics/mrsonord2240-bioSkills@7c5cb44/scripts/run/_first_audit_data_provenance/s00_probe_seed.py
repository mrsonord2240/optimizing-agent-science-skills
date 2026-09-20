"""Probe the real Pfam PF00042 seed: gap alphabet, case, then write alignment.fasta variants.
Synthetic? NO - real data. Output is asserted."""
import sys
from collections import Counter
from Bio import AlignIO

aln = AlignIO.read('data/PF00042_seed.sto', 'stockholm')
chars = Counter()
for r in aln:
    chars.update(str(r.seq))
print('n_seq', len(aln), 'n_col', aln.get_alignment_length())
print('char alphabet:', ''.join(sorted(chars)))
print('gap chars: "-"=%d  "."=%d' % (chars['-'], chars['.']))
print('lowercase count:', sum(v for k, v in chars.items() if k.islower()))
# rows using '-' vs '.'
rows_dash = sum('-' in str(r.seq) for r in aln)
rows_dot = sum('.' in str(r.seq) for r in aln)
print('rows with "-":', rows_dash, ' rows with ".":', rows_dot)

# variant A: as-is FASTA (keeps '.' gaps)  -> what a user gets from AlignIO.convert
AlignIO.write(aln, 'data/seed_raw.fasta', 'fasta')
# variant B: '.' -> '-' (correct normalisation)
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
norm = MultipleSeqAlignment([SeqRecord(Seq(str(r.seq).replace('.', '-')), id=r.id.replace('/', '_'), description='') for r in aln])
AlignIO.write(norm, 'data/seed_norm.fasta', 'fasta')
chk = AlignIO.read('data/seed_norm.fasta', 'fasta')
assert chk.get_alignment_length() == 141 and len(chk) == 73
assert '.' not in ''.join(str(r.seq) for r in chk)
print('wrote data/seed_raw.fasta and data/seed_norm.fasta; asserted 73x141 and no "." in norm')
