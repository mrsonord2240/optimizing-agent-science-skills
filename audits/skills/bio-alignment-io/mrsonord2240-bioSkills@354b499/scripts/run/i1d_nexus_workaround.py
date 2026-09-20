"""Input 1d: does the SKILL's own 'molecule_type' route fix Clustal->NEXUS (the crash in convert_formats.py)? REAL Pfam clustal + shipped DNA sample."""
import pathlib
from Bio import AlignIO
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
here = pathlib.Path(__file__).parent; d = here/'data'
AlignIO.convert(here/'skill'/'examples'/'sample_alignment.aln', 'clustal', d/'sample.nex', 'nexus', molecule_type='DNA')
a = AlignIO.read(d/'sample.nex', 'nexus')
ok(len(a) == 4 and a.get_alignment_length() == 21 and str(a[0].seq) == 'ATGGCTAGCTAG-ACGTACGT', f'convert(..., molecule_type="DNA") clustal->nexus re-read {len(a)}x{a.get_alignment_length()}, row1 {a[0].seq}')
aln = AlignIO.read(d/'pf.clustal', 'clustal')
for r in aln: r.annotations['molecule_type'] = 'protein'
AlignIO.write(aln, d/'pf_manual.nex', 'nexus'); b = AlignIO.read(d/'pf_manual.nex', 'nexus')
ok((len(b), b.get_alignment_length()) == (73, 141), 'read-modify-write with record.annotations["molecule_type"]="protein" works: 73x141 (not documented in SKILL manual-conversion snippet)')
