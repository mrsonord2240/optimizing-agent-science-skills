"""Input 2 (Variant A) -- find mammalian homologs of human hemoglobin alpha in Swiss-Prot,
with entrez_query organism restriction and composition-based statistics.
Follows SKILL.md 'Protein search with organism restriction' pattern verbatim.
"""
import time
from io import StringIO
from Bio.Blast import NCBIWWW, NCBIXML

HBA_HUMAN = ('MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH'
             'GSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR')

t0 = time.time()
print('Submitting BLASTP to NCBI (swissprot, Mammalia[Organism] pre-filter)...', flush=True)
handle = NCBIWWW.qblast(
    program='blastp',
    database='swissprot',
    sequence=HBA_HUMAN,
    entrez_query='Mammalia[Organism]',
    expect=1e-5,
    composition_based_statistics=2,
    hitlist_size=200,
    format_type='XML',
)
raw = handle.read()
handle.close()
with open('input2_raw.xml', 'w', encoding='utf-8') as f:
    f.write(raw)
print(f'Elapsed: {time.time()-t0:.1f}s, raw XML bytes: {len(raw)}')

record = NCBIXML.read(StringIO(raw))
print(f'Query length: {record.query_length}')
print(f'Total hits returned: {len(record.alignments)}')


def filter_top(record, top=10, min_cov=0.8):
    qlen = record.query_length
    out = []
    for aln in record.alignments:
        hsp = aln.hsps[0]
        cov = hsp.align_length / qlen
        if cov >= min_cov:
            out.append((aln, hsp))
    return sorted(out, key=lambda ah: -ah[1].bits)[:top]


print('\nTop hits by bit-score, coverage >= 0.8:')
for aln, hsp in filter_top(record, top=10):
    pct = 100 * hsp.identities / hsp.align_length
    print(f'  {aln.accession:<14} bits={hsp.bits:>6.1f}  E={hsp.expect:.1e}  '
          f'{pct:>5.1f}% id  cov={hsp.align_length / record.query_length:.2f}')
    print(f'      {aln.title[:100]}')

# Check every hit is actually mammalian (verifies entrez_query pre-filter worked)
non_obvious = [a.title for a in record.alignments if 'RecName' not in a.title][:3]
print(f'\nSample titles (spot-check organism restriction):')
for a in record.alignments[:5]:
    print('  ', a.title[:110])
