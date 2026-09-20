"""Re-audit independent check #2b: confirm the FIXED megablast pattern
(program='blastn', megablast=True) succeeds against live NCBI, using human ACTB (distinct gene
from HBB, which both the original auditor and the fixer used for this exact check).
"""
import time
from io import StringIO
from Bio.Blast import NCBIWWW, NCBIXML

with open('reaudit_actb_query.fasta') as f:
    QUERY = f.read()

t0 = time.time()
print("Submitting qblast(program='blastn', megablast=True, ...) -- the FIXED form...", flush=True)
handle = NCBIWWW.qblast(
    program='blastn',
    megablast=True,
    database='refseq_select_rna',
    sequence=QUERY,
    expect=1e-10,
    hitlist_size=500,
    format_type='XML',
)
raw = handle.read()
handle.close()
with open('reaudit_megablast_fixed_raw.xml', 'w', encoding='utf-8') as f:
    f.write(raw)
print(f'Elapsed: {time.time()-t0:.1f}s, raw XML bytes: {len(raw)}')

record = NCBIXML.read(StringIO(raw))
print(f'Query length: {record.query_length}')
print(f'Total alignments: {len(record.alignments)}')
for aln in record.alignments[:10]:
    hsp = aln.hsps[0]
    ident = hsp.identities / hsp.align_length
    print(f'  {aln.accession:<14} id={ident:.3f}  E={hsp.expect:.2e}  {aln.title[:80]}')
