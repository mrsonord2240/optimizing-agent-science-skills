"""Input 3 (Edge) -- BLAST a very short (12 aa) proteomics peptide.
Follows SKILL.md 'Short peptide search' pattern verbatim (PAM30, word_size=2, expect=1000, CBS=3).
"""
import time
from io import StringIO
from Bio.Blast import NCBIWWW, NCBIXML

# 12-aa fragment of human hemoglobin beta chain (VHLTPEEKSAVT, residues 1-12 of HBB)
PEPTIDE = 'VHLTPEEKSAVT'

t0 = time.time()
print('Submitting short-peptide BLASTP to NCBI (swissprot, PAM30/word=2/CBS=3)...', flush=True)
handle = NCBIWWW.qblast(
    program='blastp',
    database='swissprot',
    sequence=PEPTIDE,
    matrix_name='PAM30',
    word_size=2,
    expect=1000,
    composition_based_statistics=3,
    hitlist_size=100,
    format_type='XML',
    gapcosts='9 1',  # SKILL.md's own word-size/matrix table (line ~118) says PAM30 needs gap
                     # open,extend = 9,1 -- but the "Short peptide search" code pattern in the
                     # same SKILL.md omits gapcosts entirely, defaulting to BLOSUM62's 11,1,
                     # which NCBI rejects outright for PAM30. Added here to prove the fix.
)
raw = handle.read()
handle.close()
with open('input3_raw.xml', 'w', encoding='utf-8') as f:
    f.write(raw)
print(f'Elapsed: {time.time()-t0:.1f}s, raw XML bytes: {len(raw)}')

record = NCBIXML.read(StringIO(raw))
print(f'Query length: {record.query_length}')
print(f'Total hits returned: {len(record.alignments)}')
for aln in record.alignments[:10]:
    hsp = aln.hsps[0]
    print(f'  {aln.accession:<14} bits={hsp.bits:>6.1f}  E={hsp.expect:.2e}  '
          f'ident={hsp.identities}/{hsp.align_length}')
    print(f'      {aln.title[:100]}')
