"""Input 7 (Adversarial/ambiguous) -- user gives a bare sequence with no parameters and says
'just BLAST it, give me the top hit'. Tests whether the Skill's own defaults (as an agent would
apply them per SKILL.md guidance: refseq_select-family db for reproducibility, sensible expect)
produce a sane, defensible result without being told the specifics.
"""
import time
from io import StringIO
from Bio.Blast import NCBIWWW, NCBIXML

# Bare sequence, no FASTA defline, no organism/program stated by the "user"
RAW_SEQ = 'ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAG'

t0 = time.time()
print('Applying SKILL.md defaults for an unspecified request: blastn, refseq_select_rna '
      '(reproducible default per SKILL.md Database decision table), expect=1e-10, hitlist_size=500.')
handle = NCBIWWW.qblast(
    program='blastn',
    database='refseq_select_rna',
    sequence=RAW_SEQ,  # no '>' defline -- tests the "Empty FASTA defline submitted" failure mode
    expect=1e-10,
    hitlist_size=500,
    format_type='XML',
)
raw = handle.read()
handle.close()
print(f'Elapsed: {time.time()-t0:.1f}s, raw XML bytes: {len(raw)}')

record = NCBIXML.read(StringIO(raw))
print(f'record.query = {record.query!r}')
print(f'Total alignments: {len(record.alignments)}')
top = sorted(record.alignments, key=lambda a: a.hsps[0].expect)[0]
hsp = top.hsps[0]
print(f'Top hit: {top.accession}  E={hsp.expect:.1e}  bits={hsp.bits:.1f}  {top.title[:90]}')
if record.query is None or record.query == '':
    print('CONFIRMED: SKILL.md Failure Modes "Empty FASTA defline submitted" -- record.query '
          'is empty/None when a bare sequence (no ">id" line) is submitted, exactly as documented.')
else:
    print(f'NOTE: record.query came back as {record.query!r}, not empty -- defline handling '
          'may differ from the documented failure mode on this Biopython/NCBI version.')
