"""Input 1 (Canonical) -- identify an unknown DNA sequence with BLASTN against a reproducible db.
Follows SKILL.md 'Standard remote BLASTN with reproducible parameters' pattern verbatim.
"""
import sys
import time
from Bio.Blast import NCBIWWW, NCBIXML

QUERY = '''>HBB_partial
ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAG'''

t0 = time.time()
print('Submitting BLASTN to NCBI (refseq_select_rna)...', flush=True)
try:
    handle = NCBIWWW.qblast(
        program='blastn',
        database='refseq_select_rna',
        sequence=QUERY,
        expect=1e-10,
        word_size=11,
        hitlist_size=500,
        format_type='XML',
    )
    raw = handle.read()
    handle.close()
    with open('input1_raw.xml', 'w', encoding='utf-8') as f:
        f.write(raw)
    print(f'Elapsed: {time.time()-t0:.1f}s, raw XML bytes: {len(raw)}')

    from io import StringIO
    record = NCBIXML.read(StringIO(raw))
    print(f'Query: {record.query[:60]}')
    print(f'Query length: {record.query_length}')
    print(f'Database: {record.database}')
    print(f'Total alignments returned: {len(record.alignments)}')

    def top_n_by_bitscore(record, n=10, min_identity=0.7, min_coverage=0.5):
        qlen = record.query_length
        hits = []
        for aln in record.alignments:
            hsp = aln.hsps[0]
            ident = hsp.identities / hsp.align_length
            cov = hsp.align_length / qlen
            if ident >= min_identity and cov >= min_coverage:
                hits.append({
                    'accession': aln.accession,
                    'title': aln.title,
                    'evalue': hsp.expect,
                    'bits': hsp.bits,
                    'identity': ident,
                    'coverage': cov,
                })
        return sorted(hits, key=lambda h: -h['bits'])[:n]

    hits = top_n_by_bitscore(record)
    print(f'\nFiltered hits (identity>=0.7, coverage>=0.5): {len(hits)}')
    for i, hit in enumerate(hits, 1):
        print(f'  {i:>2}. {hit["accession"]:<14}  bits={hit["bits"]:>6.1f}  E={hit["evalue"]:.1e}  '
              f'id={hit["identity"]:.2f}  cov={hit["coverage"]:.2f}')
        print(f'      {hit["title"][:90]}')
except Exception as e:
    print(f'ERROR: {type(e).__name__}: {e}', file=sys.stderr)
    raise
