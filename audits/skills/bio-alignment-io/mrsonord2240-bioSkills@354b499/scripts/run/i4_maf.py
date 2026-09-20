"""Input 4 (Variant B): UCSC MAF coordinate handling. SYNTHETIC genome (seeded random 200 nt) + hand-built MAF, verified against the genome."""
import random, io, pathlib
from Bio import AlignIO, Align
from Bio.Seq import Seq
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
here = pathlib.Path(__file__).parent
random.seed(7)
chr1 = ''.join(random.choice('ACGT') for _ in range(200))     # SYNTHETIC reference contig, srcSize=200
chr2 = ''.join(random.choice('ACGT') for _ in range(150))     # SYNTHETIC second species contig
# block 1: both on + strand. hg.chr1 +[20,40) ; mm.chr2 +[10,31) (one gap column in the reference row)
ref1 = chr1[20:40]; qry1 = chr2[10:31]      # 21 query bases vs 20 ref bases + 1 ref gap column
r1 = ref1[:8] + '-' + ref1[8:]; q1 = qry1
# block 2: mm on MINUS strand: text is revcomp of chr2 plus-strand [plus_start, plus_start+size); MAF start counts from the END
plus_start, size = 60, 24
qry2 = str(Seq(chr2[plus_start:plus_start+size]).reverse_complement()); maf_start = 150 - plus_start - size
ref2 = chr1[100:124]
lines = ['##maf version=1 scoring=synthetic', '',
 'a score=100', f's hg.chr1 20 {len(ref1)} + 200 {r1}', f's mm.chr2 10 {len(qry1)} + 150 {q1}', '',
 'a score=90', f's hg.chr1 100 {len(ref2)} + 200 {ref2}', f's mm.chr2 {maf_start} {size} - 150 {qry2}', '']
(here/'data'/'synthetic.maf').write_text('\n'.join(lines), encoding='utf-8')
(here/'data'/'synthetic_genome.txt').write_text(f'chr1\t{chr1}\nchr2\t{chr2}\n', encoding='utf-8')

print('--- AlignIO.parse(maf)')
blocks = list(AlignIO.parse(here/'data'/'synthetic.maf', 'maf'))
ok(len(blocks)==2, f'{len(blocks)} blocks parsed')
def maf_to_plus_strand_coords(row_anno):                 # VERBATIM from SKILL.md
    if row_anno['strand'] == '-':
        return row_anno['srcSize'] - row_anno['start'] - row_anno['size']
    return row_anno['start']
for bi, b in enumerate(blocks):
    for rec in b:
        an = rec.annotations; print(bi, rec.id, {k: an[k] for k in ('start','size','strand','srcSize')}, 'text', str(rec.seq)[:30])
ok(all({'start','size','strand','srcSize'} <= set(rec.annotations) for b in blocks for rec in b), 'annotation keys start,size,strand,srcSize exist (as SKILL states)')
ok(all(isinstance(rec.annotations['strand'], int) for b in blocks for rec in b), f"strand values are ints {[rec.annotations['strand'] for b in blocks for rec in b]} (SKILL says '+' or '-' and code compares == '-')")
for bi, b in enumerate(blocks):
    for rec in b:
        an = rec.annotations; contig = chr1 if rec.id.endswith('chr1') else chr2
        p = maf_to_plus_strand_coords(an); frag = contig[p:p+an['size']]
        if an['strand'] in ('-', -1):
            frag = str(Seq(frag).reverse_complement())
        got = str(rec.seq).replace('-', '')
        print(bi, rec.id, 'skill fn ->', p, 'genome fragment (revcomp if minus) == row text:', frag == got)
# Verbatim SKILL function on int strand -> compare to ground truth
truth = {('mm.chr2', 1): plus_start}
minus_rec = blocks[1][1]; res = maf_to_plus_strand_coords(minus_rec.annotations)
ok(res == plus_start, f'SKILL maf_to_plus_strand_coords on minus-strand row returned {res}; ground truth plus-strand start = {plus_start} (strand annotation = {minus_rec.annotations["strand"]!r})')
def fixed(an): return an['srcSize'] - an['start'] - an['size'] if an['strand'] in ('-', -1) else an['start']
ok(fixed(minus_rec.annotations) == plus_start, f'corrected function (strand in ("-",-1)) returns {fixed(minus_rec.annotations)}')

print('--- Bio.Align maf read/write (SKILL table says R/W)')
try:
    al = list(Align.parse(here/'data'/'synthetic.maf', 'maf')); print('Align.parse maf blocks', len(al), type(al[0]).__name__, al[0].coordinates.tolist() if hasattr(al[0],'coordinates') else '')
    ok(len(al)==2, 'Align.parse maf gives 2 Alignment objects')
    buf = io.StringIO(); Align.write(al, buf, 'maf'); ok('s hg.chr1' in buf.getvalue(), 'Align.write maf produced s-lines')
except Exception as e:
    ok(False, f'Bio.Align maf: {type(e).__name__}: {e}')
