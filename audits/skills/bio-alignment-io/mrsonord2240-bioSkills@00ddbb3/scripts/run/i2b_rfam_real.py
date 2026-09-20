"""INPUT 2b (Variant A, regression: Rfam real data + adversarial). REAL Rfam RF00005 (tRNA) seed Stockholm downloaded from rfam.org (public, CC0):
the SKILL's Stockholm annotation snippet, annotation-loss table, molecule_type NEXUS route (RNA), PHYLIP relaxed, and adversarial
mislabelled-format requests. Downstream: Infernal cmbuild on the original vs the AlignIO round-trip (run by i8_infernal.sh)."""
import io, os, re
from Bio import AlignIO, Align
from common import *
os.chdir(DATA)
RF = 'rfam_RF00005.sto'
txt = open(RF, encoding='utf-8').read()
gf = [l for l in txt.splitlines() if l.startswith('#=GF')]; print('source #=GF lines:', len(gf), '| #=GS:', sum(l.startswith('#=GS') for l in txt.splitlines()), '| #=GR:', sum(l.startswith('#=GR') for l in txt.splitlines()), '| #=GC:', [l.split()[1] for l in txt.splitlines() if l.startswith('#=GC')])
aln = AlignIO.read(RF, 'stockholm'); n, L = len(aln), aln.get_alignment_length(); print('AlignIO.read ->', n, 'x', L)
n_src = len([l for l in txt.splitlines() if l and not l.startswith('#') and l != '//'])
ok(n == n_src and n > 500, f'AlignIO.read Rfam RF00005: {n} sequences == {n_src} sequence lines in the file')
ok(all(len(str(r.seq)) == L for r in aln), 'all rows have the same length (rectangular)')
print('first ids', [r.id for r in aln[:3]], '| annotations', dict(aln[0].annotations))
ok(all(re.match(r'^[^/]+/\d+-\d+$', r.id) for r in aln), "Rfam ids follow the Pfam-style 'name/start-end' convention the SKILL describes")
r0 = aln[0]; ok(r0.annotations.get('start') == int(r0.id.split('/')[1].split('-')[0]) and r0.annotations.get('end') == int(r0.id.split('-')[-1]), "record.annotations start/end match the id suffix (SKILL: AlignIO already fills them; id keeps the suffix)")
print('--- SKILL annotation snippet, verbatim, on real Rfam')
code = block('Stockholm Format Annotations').replace("'pfam.sto'", repr(RF))
import contextlib
buf = io.StringIO()
ns = {'AlignIO': AlignIO}
with contextlib.redirect_stdout(buf): exec(code, ns)
out = buf.getvalue(); print(out[:300])
ss = ns['ss_cons']; ok(ss is not None and len(ss) == L, f"snippet's ss_cons length {None if ss is None else len(ss)} == alignment length {L}")
src_ss = ''.join(l.split(None, 2)[2].strip() for l in txt.splitlines() if l.startswith('#=GC SS_cons'))
ok(ss == src_ss, 'column_annotations["secondary_structure"] equals the source #=GC SS_cons string')
print('column_annotations keys:', list(aln.column_annotations))
print('records with per-residue SS (#=GR SS):', sum('secondary_structure' in r.letter_annotations for r in aln))
print('--- round-trip and annotation loss (SKILL table)')
b = io.StringIO(); AlignIO.write(aln, b, 'stockholm'); o = b.getvalue()
ok('#=GC SS_cons' in o, 'Stockholm->Stockholm keeps #=GC SS_cons (SKILL: preserved)')
ok(sum(l.startswith('#=GF') for l in o.splitlines()) < len(gf), f"#=GF lines: source {len(gf)} -> round trip {sum(l.startswith('#=GF') for l in o.splitlines())} (SKILL: GF header lines dropped by AlignIO)")
ok('#=GF AC' not in o and '#=GF ID' not in o, 'GF ID / AC absent after AlignIO round trip (SKILL: verified for Pfam; also true for Rfam)')
open('rfam_roundtrip.sto', 'w', encoding='utf-8').write(o)
b = io.StringIO(); AlignIO.write(aln, b, 'fasta'); ok('<' not in b.getvalue() and '(' not in b.getvalue().split('\n', 1)[1][:200], 'FASTA output carries no SS characters')
print('--- Bio.Align on real Rfam (SKILL: TypeError on real Pfam; plain files only)')
try: a = Align.read(RF, 'stockholm'); print('Align.read real Rfam works', a.shape)
except Exception as e: print('Align.read(real Rfam) ->', type(e).__name__, str(e)[:110])
print('--- NEXUS route with molecule_type=RNA (SKILL) and PHYLIP-relaxed')
AlignIO.convert(RF, 'stockholm', 'rfam.nex', 'nexus', molecule_type='RNA')
nx = AlignIO.read('rfam.nex', 'nexus'); ok((len(nx), nx.get_alignment_length()) == (n, L), f'stockholm->nexus (molecule_type="RNA") re-reads {len(nx)}x{nx.get_alignment_length()}')
print('NEXUS header:', [l for l in open('rfam.nex').read().splitlines() if 'datatype' in l.lower()])
try: AlignIO.convert(RF, 'stockholm', 'rfam_bad.nex', 'nexus'); ok(False, 'no molecule_type worked')
except ValueError as e: ok('molecule type' in str(e), 'without molecule_type: ValueError (SKILL)')
AlignIO.write(aln, 'rfam.phy', 'phylip-relaxed'); pr = AlignIO.read('rfam.phy', 'phylip-relaxed')
ok([r.id for r in pr] == [r.id for r in aln] and [str(r.seq).upper().replace('.', '-') for r in pr] == [str(r.seq).upper().replace('.', '-') for r in aln], 'phylip-relaxed round trip identical (ids with "/" and "-")')
try: AlignIO.write(aln, io.StringIO(), 'phylip'); print('strict phylip write of Rfam ids succeeded?!')
except ValueError as e: ok('Repeated name' in str(e), f'strict phylip write of the real Rfam ids raises (colliding 10-char prefixes): {str(e)[:70]}')
print('--- adversarial: user mislabels the format (SKILL Common Errors)')
def err(f):
    try: r = f(); return f'NO ERROR ({r})'
    except Exception as e: return f'{type(e).__name__}: {str(e)[:100]}'
print('stockholm file as clustal :', err(lambda: len(AlignIO.read(RF, 'clustal'))))
print('stockholm file as fasta   :', err(lambda: len(AlignIO.read(RF, 'fasta'))))
print('stockholm file as phylip  :', err(lambda: len(AlignIO.read(RF, 'phylip'))))
print('stockholm file as nexus   :', err(lambda: len(AlignIO.read(RF, 'nexus'))))
print('clustal file as stockholm :', err(lambda: len(AlignIO.read('pf.clustal', 'stockholm'))))
print('phylip-relaxed as fasta   :', err(lambda: len(AlignIO.read('rfam.phy', 'fasta'))))
bad = [err(lambda: len(AlignIO.read(RF, 'clustal'))), err(lambda: len(AlignIO.read(RF, 'phylip'))), err(lambda: len(AlignIO.read('pf.clustal', 'stockholm')))]
ok(all(not x.startswith('NO ERROR') for x in bad), 'mislabelled Stockholm-as-clustal, Stockholm-as-phylip and clustal-as-stockholm all fail loudly (no silent garbage)')
summary()
