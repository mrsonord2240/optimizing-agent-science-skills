"""INPUT 2 (Variant A, regression). Stockholm: real Pfam PF00042 + SYNTHETIC RNA Stockholm (data/synthetic_rna.sto; GS/GR/GC lines).
Runs the SKILL's own code blocks VERBATIM (extracted from SKILL.md) and asserts on content."""
import io, re, os
from Bio import AlignIO, Align
from common import *
os.chdir(HERE/'data')
pf = str(PFAM)

print('--- A. real Pfam through AlignIO')
aln = AlignIO.read(pf, 'stockholm'); ok((len(aln), aln.get_alignment_length()) == (73, 141), 'AlignIO.read real Pfam stockholm 73x141')
r0 = aln[0]; print('id', r0.id, 'annotations', dict(r0.annotations))
ok(r0.annotations.get('start') == 31 and r0.annotations.get('end') == 141 and 'accession' in r0.annotations and '/' in r0.id,
   "SKILL Pfam-id paragraph: annotations start/end/accession already filled, id keeps '/31-141' suffix")
buf = io.StringIO(); AlignIO.write(aln, buf, 'stockholm'); out = buf.getvalue()
ok('#=GF AC' not in out and '#=GF ID' not in out and '#=GF DE' not in out, 'SKILL claim: AlignIO Stockholm->Stockholm drops #=GF ID/AC/DE (confirmed absent in output)')
print('GF-like lines in source:', sum(1 for l in open(pf) if l.startswith('#=GF')), '| GF lines in round trip:', sum(1 for l in out.splitlines() if l.startswith('#=GF')))

print('--- B. SKILL claims about Bio.Align + Stockholm on real Pfam (Common Errors rows)')
try: Align.read(pf, 'stockholm'); ok(False, 'Align.read(real Pfam) unexpectedly worked')
except TypeError as e: ok('per-letter annotation' in str(e), f'Align.read real Pfam -> TypeError as Common Errors row says: {str(e)[:90]}')
except Exception as e: ok(False, f'Align.read different error {type(e).__name__}: {e}')
try: sum(1 for _ in Align.parse(pf, 'stockholm')); ok(False, 'Align.parse unexpectedly worked')
except TypeError as e: ok('per-letter annotation' in str(e), 'Align.parse real Pfam -> same TypeError')
fa = Align.read(str(DATA/'pf.fasta'), 'fasta') if (DATA/'pf.fasta').exists() else None
AlignIO.write(aln, DATA/'pf.fasta', 'fasta'); fa = Align.read(str(DATA/'pf.fasta'), 'fasta')
try: Align.write(fa, io.StringIO(), 'stockholm'); ok(False, 'Align.write stockholm of a FASTA-read Alignment unexpectedly worked')
except AttributeError as e: ok('column_annotations' in str(e), f'Align.write(stockholm) on FASTA-read Alignment -> AttributeError column_annotations (Common Errors row): {str(e)[:80]}')

print('--- C. SKILL Stockholm annotation snippet (verbatim), on the synthetic RNA file')
code = block('Stockholm Format Annotations').replace("'pfam.sto'", "'synthetic_rna.sto'")
import contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    ns = {'AlignIO': AlignIO}; exec(code, ns)
txt = buf.getvalue(); print(txt)
ok('SS: <<<<___.>>>>.....' in txt, 'snippet prints per-record secondary structure from #=GR SS')
ok(ns['ss_cons'] == '<<<<___.>>>>.....', f"snippet's ss_cons = {ns['ss_cons']!r} == file's #=GC SS_cons")
rna = AlignIO.read('synthetic_rna.sto', 'stockholm')
ok(rna.column_annotations.get('reference_annotation') == 'xxxxxxxx.xxxxxxxx', 'GC RF appears as column_annotations["reference_annotation"] (not stated in SKILL, a naming note)')
buf = io.StringIO(); AlignIO.write(rna, buf, 'stockholm'); o = buf.getvalue()
ok('#=GC SS_cons' in o and '#=GR seqA/1-16 SS' in o, 'Stockholm->Stockholm keeps GC + GR lines (SKILL: "preserves GS/GR/GC")')
ok('#=GS' in o, '#=GS lines preserved on round trip? -> ' + str('#=GS' in o))
buf = io.StringIO(); AlignIO.write(rna, buf, 'fasta'); ok('<' not in buf.getvalue(), 'Stockholm->FASTA discards SS annotations (SKILL says so)')
print('--- D. Bio.Align Stockholm on the synthetic RNA file (SKILL: "plain files only")')
try:
    a = Align.read('synthetic_rna.sto', 'stockholm'); print('Align.read synthetic RNA sto ->', a.shape)
except Exception as e: print('Align.read synthetic RNA sto ->', type(e).__name__, str(e)[:100])
print('--- E. SKILL NEXUS molecule-type block (Stockholm input, verbatim), then re-read')
code = block('NEXUS Output Needs').replace("'input.sto'", "'synthetic_rna.sto'").replace("'output.nex'", "'rna_out.nex'").replace("'DNA'", "'RNA'")
code = code.split('\n\n')[0]
exec(code, {'AlignIO': AlignIO})
n = AlignIO.read('rna_out.nex', 'nexus'); ok((len(n), n.get_alignment_length()) == (2, 17), f'stockholm->nexus with molecule_type="RNA" re-reads {len(n)}x{n.get_alignment_length()}')
ok('datatype=rna' in open('rna_out.nex').read().lower(), 'NEXUS says datatype=rna')
try: AlignIO.convert('synthetic_rna.sto', 'stockholm', 'noarg.nex', 'nexus'); ok(False, 'no molecule_type unexpectedly worked')
except ValueError as e: ok('molecule type' in str(e), 'without molecule_type -> ValueError (as the SKILL says)')
print('--- F. Skill says: Stockholm->PHYLIP/FASTA discards; check a real Pfam GS-lines survival claim')
print('real Pfam #=GS lines in source:', sum(1 for l in open(pf) if l.startswith('#=GS')), '| in AlignIO round trip:', sum(1 for l in out.splitlines() if l.startswith('#=GS')))
summary()
