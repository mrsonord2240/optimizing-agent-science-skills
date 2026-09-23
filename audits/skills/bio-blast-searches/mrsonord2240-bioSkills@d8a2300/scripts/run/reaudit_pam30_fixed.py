"""Re-audit independent check #1b: confirm the FIXED 'Short peptide search' pattern
(PAM30, word_size=2, gapcosts='9 1') succeeds against live NCBI, using a peptide neither the
original auditor nor the fixer used.

Peptide: human insulin B-chain, residues 1-15 (FVNQHLCGSHLVEAL).
"""
import time
from io import StringIO
from Bio.Blast import NCBIWWW, NCBIXML

PEPTIDE = 'FVNQHLCGSHLVEAL'

t0 = time.time()
print('Submitting FIXED short-peptide BLASTP (PAM30, gapcosts=9 1) to NCBI...', flush=True)
handle = NCBIWWW.qblast(
    program='blastp',
    database='swissprot',
    sequence=PEPTIDE,
    matrix_name='PAM30',
    word_size=2,
    gapcosts='9 1',
    expect=1000,
    composition_based_statistics=3,
    hitlist_size=100,
    format_type='XML',
)
raw = handle.read()
handle.close()
with open('reaudit_pam30_fixed_raw.xml', 'w', encoding='utf-8') as f:
    f.write(raw)
print(f'Elapsed: {time.time()-t0:.1f}s, raw XML bytes: {len(raw)}')

record = NCBIXML.read(StringIO(raw))
print(f'Query length: {record.query_length}')
print(f'Total hits returned: {len(record.alignments)}')
for aln in record.alignments[:8]:
    hsp = aln.hsps[0]
    print(f'  {aln.accession:<14} bits={hsp.bits:>6.1f}  E={hsp.expect:.2e}  '
          f'ident={hsp.identities}/{hsp.align_length}')
    print(f'      {aln.title[:100]}')
