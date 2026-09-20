"""Re-audit independent check #2a (regression): confirm program='megablast' (the literal string
from SKILL.md's Program table) still raises ValueError immediately against live NCBI, using a
gene (human ACTB) neither the original auditor nor the fixer used (both used HBB).
"""
import time
from Bio.Blast import NCBIWWW

with open('reaudit_actb_query.fasta') as f:
    QUERY = f.read()

t0 = time.time()
print("Submitting qblast(program='megablast', ...) -- the UNFIXED/documented-table form...", flush=True)
try:
    handle = NCBIWWW.qblast(
        program='megablast',
        database='refseq_select_rna',
        sequence=QUERY,
        hitlist_size=500,
        format_type='XML',
    )
    raw = handle.read()
    handle.close()
    print(f'UNEXPECTED SUCCESS after {time.time()-t0:.1f}s -- {len(raw)} bytes')
except Exception as e:
    print(f'FAILED as expected after {time.time()-t0:.1f}s: {type(e).__name__}: {e}')
