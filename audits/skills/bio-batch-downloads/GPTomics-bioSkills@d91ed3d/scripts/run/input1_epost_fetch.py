"""
Input 1 (Canonical): "I have a list of protein accessions in a file (>200 of them).
EPost them in chunks of 200 (since EPost's per-call limit is 200), then EFetch by
WebEnv/QueryKey in batches of 500."

Mirrors SKILL.md's "EPost large ID list, then EFetch" pattern / examples/batch_by_ids.py's
chained_epost_fetch(), run against a REAL distinct ID list (not the example's duplicated
6-accession list) to test the pattern at real scale with genuinely distinct records.
"""
import time
from pathlib import Path
from Bio import Entrez, SeqIO

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'bio-batch-downloads-audit'
DELAY = 0.34
EPOST_LIMIT = 200

OUT_DIR = Path(__file__).parent / 'out1'
OUT_DIR.mkdir(exist_ok=True)


def epost_and_fetch(db, ids, out_path, rettype='fasta', retmode='text', batch_size=500):
    """Exact pattern from SKILL.md's 'EPost large ID list, then EFetch' section."""
    delay = 0.1 if Entrez.api_key else DELAY
    webenv = None
    posted_keys = []
    for i in range(0, len(ids), EPOST_LIMIT):
        chunk = ids[i:i + EPOST_LIMIT]
        kwargs = {'db': db, 'id': ','.join(chunk)}
        if webenv:
            kwargs['WebEnv'] = webenv
        h = Entrez.epost(**kwargs)
        r = Entrez.read(h)
        h.close()
        webenv = r['WebEnv']
        posted_keys.append((r['QueryKey'], len(chunk)))
        print(f'  EPost chunk {i}-{i+len(chunk)}: QueryKey={r["QueryKey"]}')
        time.sleep(delay)

    with open(out_path, 'w') as out:
        for qk, n in posted_keys:
            for start in range(0, n, batch_size):
                h = Entrez.efetch(db=db, rettype=rettype, retmode=retmode,
                                   retstart=start, retmax=min(batch_size, n - start),
                                   webenv=webenv, query_key=qk)
                out.write(h.read())
                h.close()
                time.sleep(delay)
    return webenv, posted_keys


# Step 1: get a real, distinct ID list > 200 via a live ESearch (not duplicated IDs).
term = 'Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP] AND cancer[TIAB]'
h = Entrez.esearch(db='nucleotide', term=term, retmax=600)
s = Entrez.read(h)
h.close()
ids = s['IdList']
count = int(s['Count'])
print(f'ESearch: Count={count}, retrieved {len(ids)} UIDs (retmax=600), distinct={len(set(ids))}')
assert len(ids) == len(set(ids)), 'ESearch returned duplicate UIDs unexpectedly'
assert len(ids) > EPOST_LIMIT, 'Need >200 IDs to exercise the chunked-EPost path'

out_fasta = OUT_DIR / 'epost_fetch.fasta'
webenv, posted_keys = epost_and_fetch('nucleotide', ids, str(out_fasta))
posted_total = sum(n for _, n in posted_keys)
print(f'Posted total (sum of chunk sizes): {posted_total}, expected {len(ids)}')
assert posted_total == len(ids)

# Integrity check per SKILL.md's own verify_fasta_count pattern
observed = sum(1 for _ in SeqIO.parse(str(out_fasta), 'fasta'))
print(f'FASTA records observed: {observed}, expected (posted ID count): {len(ids)}')
assert observed == len(ids), f'MISMATCH: expected {len(ids)} records, got {observed}'
print('PASS: EPost-chunked + WebEnv/QueryKey EFetch produced exactly the expected record count, no loss/dup.')
