"""Input 3 (Edge): PHYLIP pitfalls the SKILL warns about. SYNTHETIC alignment (names sharing 10-char prefixes) + real Pfam ids."""
import io, re
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
ids = ['Homo_sapiens_chr1','Homo_sapiens_chr2','Mus_musculus_chr1']
seqs = ['ACGTACGTAC','ACGTACGTAT','ACGAACGTAC']   # SYNTHETIC
aln = MultipleSeqAlignment([SeqRecord(Seq(s), id=i) for i, s in zip(ids, seqs)], )   # SKILL "Creating Alignments Programmatically"
ok(len(aln)==3 and aln.get_alignment_length()==10, 'MultipleSeqAlignment built programmatically (SKILL snippet)')

print('--- A. strict PHYLIP write with colliding 10-char prefixes (SKILL: "silently merge")')
buf = io.StringIO()
try:
    AlignIO.write(aln, buf, 'phylip'); out = buf.getvalue(); print(out)
    back = AlignIO.read(io.StringIO(out), 'phylip'); print('re-read ids:', [r.id for r in back])
    ok(len({r.id for r in back}) < 3, 'strict phylip silently produced duplicate/merged names')
except Exception as e:
    ok(False, f'strict phylip write raised (NOT silent): {type(e).__name__}: {e}')

print('--- B. strict PHYLIP write with distinct-but-truncating names (>10 chars, unique prefixes)')
aln2 = MultipleSeqAlignment([SeqRecord(Seq(s), id=i) for i, s in zip(['Homo_sapiens','Mus_musculus','Bos_taurus_x'], seqs)])
buf = io.StringIO(); AlignIO.write(aln2, buf, 'phylip'); print(buf.getvalue())
back = AlignIO.read(io.StringIO(buf.getvalue()), 'phylip'); print('re-read:', [r.id for r in back])
ok([r.id for r in back]==['Homo_sapie','Mus_muscul','Bos_taurus'], 'strict phylip truncated names to 10 chars (as SKILL says)')

print('--- C. relaxed keeps names; sequential vs interleaved layouts')
for fmt in ['phylip-relaxed','phylip-sequential']:
    try:
        buf = io.StringIO(); AlignIO.write(aln, buf, fmt); back = AlignIO.read(io.StringIO(buf.getvalue()), fmt)
        ok([r.id for r in back]==ids and [str(r.seq) for r in back]==seqs, f'{fmt} roundtrip exact: ids {[r.id for r in back]}')
    except Exception as e:
        ok(False, f'{fmt} write of long names raised: {type(e).__name__}: {e}  (phylip-sequential is 10-char strict; PAML route needs short unique names)')
print('--- C2. READING a foreign strict-PHYLIP file whose first 10 chars collide (the truly silent case)')
foreign = ' 2 10\nHomo_sapieACGTACGTAC\nHomo_sapieACGTACGTAT\n'
back = AlignIO.read(io.StringIO(foreign), 'phylip'); print('ids:', [r.id for r in back])
ok(len({r.id for r in back})==1, 'reader silently accepts two records with identical ids (no warning/error)')
# relaxed file read with the strict parser
rel = ' 2 10\nHomo_sapiens_chr1 ACGTACGTAC\nMus_musculus_chr1 ACGTACGTAC\n'
try:
    back = AlignIO.read(io.StringIO(rel), 'phylip'); print('strict parser on relaxed text ->', [r.id for r in back], [str(r.seq) for r in back])
except Exception as e: print('strict parser on relaxed text raises:', type(e).__name__, str(e)[:100])

print('--- D. SKILL: interleaved-vs-sequential mismatch "fail silently"')
# long alignment so phylip-relaxed writes interleaved blocks
long = MultipleSeqAlignment([SeqRecord(Seq(s*12), id=i) for i, s in zip(['a','b','c'], seqs)])
buf = io.StringIO(); AlignIO.write(long, buf, 'phylip-relaxed'); txt = buf.getvalue(); print(txt[:250])
try:
    back = AlignIO.read(io.StringIO(txt), 'phylip-sequential'); ok(False, f'sequential parser read interleaved text: {len(back)}x{back.get_alignment_length()} seqs {[len(r.seq) for r in back]}')
except Exception as e:
    ok(True, f'reading interleaved text with phylip-sequential raises loudly (not silent): {type(e).__name__}: {str(e)[:100]}')

print('--- E. SKILL sanitize snippet re.sub(r"[():,]","_",id) on names with colons')
bad = MultipleSeqAlignment([SeqRecord(Seq(s), id=i) for i, s in zip(['a:1','b(2)','c,3'], seqs)])
for r in bad: r.id = re.sub(r'[():,]', '_', r.id)
ok([r.id for r in bad]==['a_1','b_2_','c_3'], f'sanitised ids {[r.id for r in bad]}')
buf = io.StringIO(); AlignIO.write(bad, buf, 'phylip-relaxed'); back = AlignIO.read(io.StringIO(buf.getvalue()), 'phylip-relaxed'); ok([r.id for r in back]==['a_1','b_2_','c_3'], 'sanitised ids survive relaxed roundtrip')
# NB: SeqRecord.name/description still hold the old string; check what writers use
buf = io.StringIO(); bad2 = MultipleSeqAlignment([SeqRecord(Seq('ACGT'), id='x:y')]);
AlignIO.write(bad2, buf, 'phylip-relaxed'); print('unsanitised colon name written as:', buf.getvalue().splitlines()[1])

print('--- F. RAxML-NG "stop codons * in protein alignment" claim: does Biopython phylip write accept "*"?')
p = MultipleSeqAlignment([SeqRecord(Seq('MKV*AL'), id='p1'), SeqRecord(Seq('MKVLAL'), id='p2')])
buf = io.StringIO(); AlignIO.write(p, buf, 'phylip-relaxed'); print(buf.getvalue().strip().replace('\n',' | '))
p2 = MultipleSeqAlignment([SeqRecord(Seq(str(r.seq).replace('*','X')), id=r.id) for r in p]); ok('*' not in ''.join(str(r.seq) for r in p2), 'replace * with X per SKILL works')
