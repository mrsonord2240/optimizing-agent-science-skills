"""INPUT 3 (Edge, regression). PHYLIP pitfalls the fixed SKILL now states. SYNTHETIC names sharing 10-char prefixes + REAL Pfam ids + REAL HBB CDS ids.
Also Common Errors table rows (empty, multi, ragged, unknown format)."""
import io, re, os
from Bio import AlignIO, SeqIO
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from common import *
os.chdir(HERE/'data')
ids = ['Homo_sapiens_chr1','Homo_sapiens_chr2','Mus_musculus_chr1']; seqs = ['ACGTACGTAC','ACGTACGTAT','ACGAACGTAC']  # SYNTHETIC
aln = MultipleSeqAlignment([SeqRecord(Seq(s), id=i) for i, s in zip(ids, seqs)])
print('--- A. "Strict write of colliding 10-char prefixes raises ValueError: Repeated name Homo_sapie"')
for fmt in ['phylip', 'phylip-sequential']:
    try: AlignIO.write(aln, io.StringIO(), fmt); ok(False, f'{fmt} write of colliding names unexpectedly succeeded')
    except ValueError as e: ok("Repeated name 'Homo_sapie'" in str(e), f'{fmt} write raises: {str(e)[:70]}')
print('--- B. unique-but-long names are truncated silently (SKILL: "Names that stay unique are truncated without warning")')
a2 = MultipleSeqAlignment([SeqRecord(Seq(s), id=i) for i, s in zip(['Homo_sapiens','Mus_musculus','Bos_taurus_x'], seqs)])
buf = io.StringIO(); AlignIO.write(a2, buf, 'phylip'); back = AlignIO.read(io.StringIO(buf.getvalue()), 'phylip')
ok([r.id for r in back] == ['Homo_sapie','Mus_muscul','Bos_taurus'], f'strict truncation to 10 chars: {[r.id for r in back]}')
print('--- C. "The silent case is reading a foreign strict file whose names collide"')
foreign = ' 2 10\nHomo_sapieACGTACGTAC\nHomo_sapieACGTACGTAT\n'
b = AlignIO.read(io.StringIO(foreign), 'phylip'); ok(len({r.id for r in b}) == 1 and len(b) == 2, f'reader accepts 2 records with identical id {b[0].id!r} silently')
print('--- D. relaxed round trip, and writer rewrites ":" to "|" and drops "(" "," (SKILL claim)')
buf = io.StringIO(); AlignIO.write(aln, buf, 'phylip-relaxed'); back = AlignIO.read(io.StringIO(buf.getvalue()), 'phylip-relaxed')
ok([r.id for r in back] == ids and [str(r.seq) for r in back] == seqs, 'phylip-relaxed exact round trip of long names')
bad = MultipleSeqAlignment([SeqRecord(Seq('ACGT'), id=i) for i in ['a:1', 'b(2)', 'c,3']])
buf = io.StringIO(); AlignIO.write(bad, buf, 'phylip-relaxed'); rows = [l.split(' ')[0] for l in buf.getvalue().splitlines()[1:]]
print('written names:', rows)
ok(rows[0] == 'a|1', "':' written as '|'"); print('other writes: b(2) ->', rows[1], '| c,3 ->', rows[2])
try: AlignIO.write(MultipleSeqAlignment([SeqRecord(Seq('ACGT'), id='d 4')]), io.StringIO(), 'phylip-relaxed'); ok(False, 'space in id accepted')
except ValueError as e: print('id with a space ->', e)
ok(rows[1] == 'b2' and rows[2] == 'c3', 'SKILL says the writer "drops ( ,": b(2)->b2, c,3->c3')
print('--- E. SKILL sanitizer re.sub(r"[():,]","_",id) verbatim')
print([re.sub(r'[():,]', '_', i) for i in ['a:1', 'b(2)', 'c,3']])
print('--- F. NCBI-style ids and phylip-sequential (SKILL: shorten ids first, collide otherwise)')
recs = list(SeqIO.parse(PUB/'msa'/'hbb_cds_mammals.fasta', 'fasta'))[:6]
print('real ids:', [r.id for r in recs])
al = MultipleSeqAlignment([SeqRecord(Seq(str(r.seq)[:60]), id=r.id) for r in recs])
try: AlignIO.write(al, io.StringIO(), 'phylip-sequential'); ok(False, 'real NCBI ids wrote phylip-sequential without collision')
except ValueError as e: ok('Repeated name' in str(e), f'real NCBI ids collide in phylip-sequential as SKILL now warns: {str(e)[:60]}')
print('--- G. SKILL PHYLIP block verbatim, run on files written by Biopython')
AlignIO.write(aln, 'x_relaxed.phy', 'phylip-relaxed')
AlignIO.write(a2, 'x_strict.phy', 'phylip'); AlignIO.write(a2, 'x_seq.phy', 'phylip-sequential')
code = block('PHYLIP Format Pitfalls')
code = code.replace("'file.phy', 'phylip')", "'x_strict.phy', 'phylip')", 1).replace("AlignIO.read('file.phy', 'phylip-sequential')", "AlignIO.read('x_seq.phy', 'phylip-sequential')").replace("AlignIO.read('file.phy', 'phylip-relaxed')", "AlignIO.read('x_relaxed.phy', 'phylip-relaxed')")
ns = {'AlignIO': AlignIO}; exec(code, ns); ok(os.path.getsize('output.phy') > 0 and len(AlignIO.read('output.phy', 'phylip-relaxed')) == 3, 'verbatim PHYLIP block ran end to end; output.phy re-reads 3 records')
print('--- H. Common Errors table rows (Biopython 1.88) verbatim messages')
open('empty.aln', 'w').close(); open('ragged.fa', 'w').write('>a\nACGTACGT\n>b\nACGT\n')
AlignIO.write(AlignIO.read(str(PFAM), 'stockholm'), 'pf.sto_copy.sto', 'stockholm')
multi = ''.join(open(str(PFAM)).read() for _ in range(2)); open('multi.sto', 'w').write(multi)
def err(f):
    try: f(); return 'NO ERROR'
    except Exception as e: return f'{type(e).__name__}: {str(e)[:100]}'
rows = {
 'No records found in handle': err(lambda: AlignIO.read('empty.aln', 'clustal')),
 'More than one record found in handle': err(lambda: AlignIO.read('multi.sto', 'stockholm')),
 'Sequences must all be the same length': err(lambda: AlignIO.read('ragged.fa', 'fasta')),
 "Unknown format 'a2m'": err(lambda: AlignIO.read('ragged.fa', 'a2m')),
 'Need the molecule type to be defined': err(lambda: AlignIO.convert(str(PFAM), 'stockholm', 'z.nex', 'nexus')),
}
for k, v in rows.items(): ok(k in v, f'Common Errors [{k}] -> {v}')
ok(os.path.exists('z.nex') and os.path.getsize('z.nex') == 0, 'NEXUS write without molecule_type leaves 0-byte file (SKILL says "(leaving a 0-byte file)"): size ' + str(os.path.getsize('z.nex')))
summary()
