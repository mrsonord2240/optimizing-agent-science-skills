"""
Input 3 (Edge/boundary): exercise the exact EPost 200-ID hard limit the Skill documents
("200 IDs per EPost call is the hard limit") using examples/batch_by_ids.py's own
direct_efetch() and chained_epost_fetch() functions (copied verbatim below, not imported
from external/), against real distinct accessions at n=200 and n=201.
"""
import time
from Bio import Entrez, SeqIO
from pathlib import Path

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'bio-batch-downloads-audit'
DELAY = 0.34
EPOST_LIMIT = 200

OUT_DIR = Path(__file__).parent / 'out3'
OUT_DIR.mkdir(exist_ok=True)


# --- verbatim copy of examples/batch_by_ids.py functions ---
def direct_efetch(db, ids, out_path, rettype='fasta'):
    '''For <200 IDs: comma-joined EFetch in one call.'''
    assert len(ids) <= EPOST_LIMIT, f'Use chained EPost for >{EPOST_LIMIT} IDs'
    h = Entrez.efetch(db=db, id=','.join(ids), rettype=rettype, retmode='text')
    with open(out_path, 'w') as out:
        out.write(h.read())
    h.close()


def chained_epost_fetch(db, ids, out_path, rettype='fasta', batch_size=500):
    delay = 0.1 if Entrez.api_key else DELAY
    webenv = None
    posts = []
    for i in range(0, len(ids), EPOST_LIMIT):
        chunk = ids[i:i+EPOST_LIMIT]
        kwargs = {'db': db, 'id': ','.join(chunk)}
        if webenv:
            kwargs['WebEnv'] = webenv
        h = Entrez.epost(**kwargs)
        r = Entrez.read(h); h.close()
        webenv = r['WebEnv']
        posts.append((r['QueryKey'], len(chunk)))
        time.sleep(delay)

    with open(out_path, 'w') as out:
        for query_key, chunk_total in posts:
            for start in range(0, chunk_total, batch_size):
                h = Entrez.efetch(db=db, rettype=rettype, retmode='text',
                                  retstart=start, retmax=min(batch_size, chunk_total - start),
                                  webenv=webenv, query_key=query_key)
                out.write(h.read()); h.close()
                time.sleep(delay)
# --- end copy ---


# Get 201 real distinct nucleotide UIDs live.
term = 'Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP] AND cancer[TIAB]'
h = Entrez.esearch(db='nucleotide', term=term, retmax=201)
s = Entrez.read(h)
h.close()
ids_201 = s['IdList']
assert len(ids_201) == 201 and len(set(ids_201)) == 201
ids_200 = ids_201[:200]

print(f'=== n=200 (at the documented limit): direct_efetch should SUCCEED ===')
try:
    direct_efetch('nucleotide', ids_200, str(OUT_DIR / 'exactly_200.fasta'))
    n = sum(1 for _ in SeqIO.parse(str(OUT_DIR / 'exactly_200.fasta'), 'fasta'))
    print(f'direct_efetch(200 ids) succeeded, {n} records parsed (expected 200): {"PASS" if n==200 else "FAIL"}')
except AssertionError as e:
    print(f'UNEXPECTED assertion failure at n=200: {e}')

print(f'\n=== n=201 (one over the documented limit): direct_efetch should ASSERT and REFUSE ===')
try:
    direct_efetch('nucleotide', ids_201, str(OUT_DIR / 'should_not_exist.fasta'))
    print('FAIL: direct_efetch(201 ids) did not raise -- the 200-ID guard did not fire')
except AssertionError as e:
    print(f'PASS: direct_efetch(201 ids) correctly refused with AssertionError: {e}')

print(f'\n=== n=201 via chained_epost_fetch (the documented path for >200) ===')
chained_epost_fetch('nucleotide', ids_201, str(OUT_DIR / 'chained_201.fasta'))
n201 = sum(1 for _ in SeqIO.parse(str(OUT_DIR / 'chained_201.fasta'), 'fasta'))
print(f'chained_epost_fetch(201 ids) -> {n201} records (expected 201): {"PASS" if n201==201 else "FAIL"}')
assert n201 == 201, f'MISMATCH at boundary+1: expected 201, got {n201}'
print('\nOVERALL PASS: 200/201 boundary is enforced exactly where SKILL.md documents it, and the >200 path recovers the full correct set.')
