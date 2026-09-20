"""Input 5b: multi-alignment I/O snippets (SKILL 'Multiple Alignments in One File', 'Read as List', 'Write Multiple', 'Write to Handle'), REAL Pfam (x3)."""
import pathlib, io
from Bio import AlignIO
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
here = pathlib.Path(__file__).parent; d = here/'data'
n = 0
for alignment in AlignIO.parse(d/'Pfam-mini.sto', 'stockholm'):           # SKILL snippet
    print(f'Alignment with {len(alignment)} sequences, length {alignment.get_alignment_length()}'); n += 1
ok(n == 3, f'AlignIO.parse stockholm yields {n} alignments')
alignments = list(AlignIO.parse(d/'Pfam-mini.sto', 'stockholm'))
ok(all((len(a), a.get_alignment_length()) == (73, 141) for a in alignments), 'each 73x141')
count = AlignIO.write(alignments, d/'output_multi.sto', 'stockholm'); print(f'Wrote {count} alignments')   # SKILL snippet
ok(count == 3 and len(list(AlignIO.parse(d/'output_multi.sto', 'stockholm'))) == 3, 'write multiple stockholm -> count 3, re-parse 3')
count = AlignIO.write(alignments, d/'output_multi.phy', 'phylip-relaxed')
back = list(AlignIO.parse(d/'output_multi.phy', 'phylip-relaxed'))
ok(count == 3 and len(back) == 3 and all(len(b) == 73 for b in back), f'multi-alignment phylip-relaxed round trip {count} written, {len(back)} parsed')
with open(d/'output_handle.aln', 'w') as handle:                      # SKILL "Write to Handle"
    AlignIO.write(alignments[0], handle, 'clustal')
a = AlignIO.read(d/'output_handle.aln', 'clustal'); ok(len(a) == 73 and a.get_alignment_length() == 141, 'clustal via handle round trip 73x141')
same = [str(x.seq).upper().replace('.', '-') for x in a] == [str(x.seq).upper().replace('.', '-') for x in alignments[0]]
ok(same, 'clustal round-trip residues identical to source')
print('--- Common Errors table claims')
def err(fn):
    try: fn(); return 'NO ERROR'
    except Exception as e: return f'{type(e).__name__}: {str(e)[:90]}'
(d/'empty.aln').write_text('')
print('empty file      :', err(lambda: AlignIO.read(d/'empty.aln', 'clustal')))
print('read() on multi :', err(lambda: AlignIO.read(d/'Pfam-mini.sto', 'stockholm')))
(d/'ragged.fa').write_text('>a\nACGTACGT\n>b\nACGT\n')                # SYNTHETIC unaligned records
print('ragged fasta    :', err(lambda: AlignIO.read(d/'ragged.fa', 'fasta')))
print('unknown format  :', err(lambda: AlignIO.read(d/'ragged.fa', 'a2m')))
print('nonexistent file:', err(lambda: AlignIO.read(d/'nope.aln', 'clustal')))
print('wrong format    :', err(lambda: AlignIO.read(d/'Pfam-mini.sto', 'clustal')))
print('fasta as phylip :', err(lambda: AlignIO.read(d/'pf.fasta', 'phylip')))
print('empty as fasta  :', err(lambda: AlignIO.read(d/'empty.aln', 'fasta')))
print('--- Bio.Align snippets (SKILL "Alternative: Bio.Align")')
from Bio import Align
al = Align.read(d/'pf.clustal', 'clustal'); print('Align.read clustal', type(al).__name__, len(al), al.shape)
ok(al.shape == (73, 141), 'Align.read clustal shape (73,141)')
Align.write(al, d/'align_out.fasta', 'fasta'); r = AlignIO.read(d/'align_out.fasta', 'fasta'); ok(len(r) == 73 and r.get_alignment_length() == 141, 'Align.write fasta -> re-read 73x141')
al2 = Align.read(d/'pf.fasta', 'fasta'); ok(al2.shape == (73, 141), 'Align.read fasta shape')
print('counts():', type(al2.counts()).__name__)
for fmt in ['phylip','nexus','stockholm','clustal']:
    try:
        buf = io.StringIO(); Align.write(al2, buf, fmt); print(f'Align.write {fmt}: {len(buf.getvalue())} chars')
    except Exception as e: print(f'Align.write {fmt}: {type(e).__name__}: {str(e)[:80]}')
