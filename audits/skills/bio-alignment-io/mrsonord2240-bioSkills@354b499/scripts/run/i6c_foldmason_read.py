"""Input 6c: Foldmason result_aa.fa / result_3di.fa loaded with AlignIO + Align (SKILL 'Related Skills' claim)."""
import pathlib
from Bio import AlignIO, Align
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
d = pathlib.Path(__file__).parent/'data'/'fm'
aa = AlignIO.read(d/'result_aa.fa', 'fasta'); td = AlignIO.read(d/'result_3di.fa', 'fasta')
print('ids', [r.id for r in aa], 'aa', len(aa), aa.get_alignment_length(), '3di', len(td), td.get_alignment_length())
ok(len(aa) == 3 and aa.get_alignment_length() == td.get_alignment_length(), 'aa and 3Di alignments have same shape')
ok(all(set(str(r.seq)) <= set('ACDEFGHIKLMNPQRSTVWYX-') for r in aa), 'aa alphabet is amino acids')
ok(all(set(str(r.seq)) <= set('ACDEFGHIKLMNPQRSTVWYX-') for r in td), '3Di alphabet also 20-letter (as expected)')
a2 = Align.read(d/'result_aa.fa', 'fasta'); ok(a2.shape == (3, aa.get_alignment_length()), f'Align.read shape {a2.shape}')
# identity between 1MBN and 1A6M rows over co-aligned columns
r = [str(x.seq) for x in aa]; pairs = [(a, b) for a, b in zip(r[0], r[1]) if a != '-' and b != '-']
idn = sum(a == b for a, b in pairs) / len(pairs); print('1MBN vs 1A6M identity over aligned columns', round(idn, 3))
ok(idn > 0.95, 'near-identical structures give >95% column identity in the Foldmason aa MSA (sanity on content)')
