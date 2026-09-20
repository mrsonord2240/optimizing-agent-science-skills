"""Re-audit independent check #1a (regression): confirm the UNFIXED 'Short peptide search'
pattern (PAM30, word_size=2, no gapcosts) still crashes against live NCBI, using a peptide the
original auditor and the fixer did NOT use (both used hemoglobin-beta fragments).

Peptide: human insulin B-chain, residues 1-15 (FVNQHLCGSHLVEAL) -- classic, stable sequence,
unrelated to HBB.
"""
import time
from Bio.Blast import NCBIWWW

PEPTIDE = 'FVNQHLCGSHLVEAL'

t0 = time.time()
print('Submitting UNFIXED short-peptide BLASTP (PAM30, no gapcosts) to NCBI...', flush=True)
try:
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
    )
    raw = handle.read()
    handle.close()
    print(f'UNEXPECTED SUCCESS after {time.time()-t0:.1f}s -- {len(raw)} bytes returned')
except Exception as e:
    print(f'FAILED as expected after {time.time()-t0:.1f}s: {type(e).__name__}: {e}')
