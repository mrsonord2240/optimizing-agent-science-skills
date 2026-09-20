"""Input 2 (Variant A): Stockholm handling. Real Pfam PF00042 seed + SYNTHETIC RNA stockholm with GS/GR/GC lines (data/synthetic_rna.sto)."""
import re, io, pathlib, warnings
from Bio import AlignIO, Align
here = pathlib.Path(__file__).parent
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
pf = pathlib.Path(r'F:\OpenScience\audit-envs\alignment\public-data\msa\PF00042_seed.sto')

print('--- A. real Pfam via AlignIO (SKILL "Reading Alignments" / "Stockholm")')
aln = AlignIO.read(pf, 'stockholm'); ok((len(aln), aln.get_alignment_length())==(73,141), f'AlignIO.read stockholm -> {len(aln)}x{aln.get_alignment_length()}')
print('first id:', aln[0].id, '| record.annotations keys:', sorted(aln[0].annotations)[:6], '| column_annotations:', dict(aln.column_annotations).keys() if aln.column_annotations else {})
print('alignment.annotations keys:', sorted(aln.annotations)[:8])

print('--- B. SKILL "Alternative: Bio.Align" Stockholm on the same real file')
try:
    a2 = Align.read(pf, 'stockholm'); ok(False, f'Align.read unexpectedly worked {len(a2)}')
except Exception as e:
    ok(False, f'Align.read(real Pfam, stockholm) FAILED: {type(e).__name__}: {str(e)[:110]}')
try:
    n = sum(1 for _ in Align.parse(pf, 'stockholm')); ok(False, f'Align.parse worked {n}')
except Exception as e:
    ok(False, f'Align.parse(real Pfam, stockholm) FAILED: {type(e).__name__}: {str(e)[:110]}')

print('--- C. SKILL Stockholm annotation snippet on SYNTHETIC RNA stockholm')
rna = AlignIO.read(here/'data'/'synthetic_rna.sto', 'stockholm')
print('records', [r.id for r in rna], 'len', rna.get_alignment_length())
for r in rna:
    print(r.id, 'annotations:', dict(r.annotations), '| letter_annotations keys:', list(r.letter_annotations))
print('column_annotations keys:', list(rna.column_annotations))
snippet_letter = [('secondary_structure' in r.letter_annotations) for r in rna]
ok(any(snippet_letter), "SKILL key 'secondary_structure' present in letter_annotations (per-record) -> " + str(snippet_letter))
ss_cons = rna.column_annotations.get('secondary_structure')
ok(ss_cons is not None, f"SKILL `alignment.column_annotations.get('secondary_structure')` -> {ss_cons!r}")
ok(ss_cons=='<<<<___.>>>>.....' and rna.column_annotations.get('reference_annotation')=='xxxxxxxx.xxxxxxxx', "SS_cons value and RF ('reference_annotation') match the file")
ok(all(r.letter_annotations['secondary_structure']=='<<<<___.>>>>.....' for r in rna), 'per-record GR SS values match the file')

print('--- D. round trip stockholm->stockholm keeps GC/GR? and ->fasta drops them')
buf = io.StringIO(); AlignIO.write(rna, buf, 'stockholm'); out = buf.getvalue()
ok('#=GC SS_cons' in out and '#=GR seqA/1-16 SS' in out, 'stockholm round trip keeps GC SS_cons + GR SS lines')
print(out)
buf = io.StringIO(); AlignIO.write(rna, buf, 'fasta'); ok('<' not in buf.getvalue(), 'fasta output carries no SS characters (annotations discarded, as SKILL says)')

print('--- E. Stockholm -> NEXUS with molecule_type (SKILL "With Alphabet Specification")')
AlignIO.convert(here/'data'/'synthetic_rna.sto', 'stockholm', here/'data'/'synth_out.nex', 'nexus', molecule_type='RNA')
n = AlignIO.read(here/'data'/'synth_out.nex', 'nexus'); ok(len(n)==2 and n.get_alignment_length()==17, f'nexus reread {len(n)}x{n.get_alignment_length()}')
try:
    AlignIO.convert(pf, 'stockholm', here/'data'/'pfam_noarg.nex', 'nexus')
    ok(True, 'stockholm->nexus without molecule_type on real Pfam works')
except Exception as e:
    ok(False, f'stockholm->nexus real Pfam without molecule_type: {type(e).__name__}: {e}')
try:
    AlignIO.convert(pf, 'stockholm', here/'data'/'pfam_prot.nex', 'nexus', molecule_type='protein'); n=AlignIO.read(here/'data'/'pfam_prot.nex','nexus'); ok(len(n)==73, f'protein nexus w/ molecule_type=protein reread {len(n)}x{n.get_alignment_length()}')
except Exception as e:
    ok(False, f'protein nexus: {type(e).__name__}: {e}')

print('--- F. Pfam name/start-end convention: SKILL says parse suffix before IQ-TREE/RAxML')
r0 = aln[0]; ok(re.match(r'^[^/]+/\d+-\d+$', r0.id) is not None, f'real Pfam id follows name/start-end: {r0.id}')
ok('start' in r0.annotations and r0.annotations['start']==31 and r0.annotations['end']==141, f"SKILL says Biopython does not split name/start-end; it DOES fill annotations start/end = {r0.annotations['start']}/{r0.annotations['end']} (id keeps suffix: {r0.id})")
print('--- G. phylip-relaxed write of the real Pfam ids (contain "/" and "-")')
buf = io.StringIO(); AlignIO.write(aln, buf, 'phylip-relaxed'); first = buf.getvalue().splitlines()[:2]; print(first[0], '|', first[1][:60])
back = AlignIO.read(io.StringIO(buf.getvalue()), 'phylip-relaxed'); ok([r.id for r in back]==[r.id for r in aln], 'phylip-relaxed re-read preserves all 73 long ids')

print('--- H. real Pfam GF header lines survive AlignIO round trip?')
buf = io.StringIO(); AlignIO.write(aln, buf, 'stockholm'); o = buf.getvalue()
ok('#=GF AC' not in o and '#=GF ID' not in o, 'real Pfam #=GF ID/AC/DE header metadata are NOT round-tripped by AlignIO (dropped silently); GC seq_cons kept: ' + str('#=GC seq_cons' in o))
