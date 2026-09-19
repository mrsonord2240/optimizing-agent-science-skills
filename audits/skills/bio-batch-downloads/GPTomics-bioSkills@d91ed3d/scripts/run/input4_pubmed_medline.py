"""
Input 4 (Variant B): "Download every PubMed abstract for 'CRISPR AND 2024[PDAT]' in
MEDLINE format" -- a Quick-Start example verbatim from usage-guide.md.

Live Count on this query is 8,768 (2026-09-19), squarely in the Skill's own
5,000-100,000-from-a-query bracket -> 'ESearch with usehistory=y -> chunked EFetch'.
Uses SKILL.md's batch-size guidance for pubmed/medline (1000-2000/batch) and asserts the
downloaded MEDLINE record count and PMID set match the ESearch UID set exactly (no
truncation, no duplication) -- not just 'the call did not throw'.
"""
import time
from pathlib import Path
from Bio import Entrez, Medline

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'bio-batch-downloads-audit'
DELAY = 0.34
BATCH_SIZE = 1500  # within SKILL.md's documented pubmed/medline 1000-2000 range

OUT_DIR = Path(__file__).parent / 'out4'
OUT_DIR.mkdir(exist_ok=True)
OUT_PATH = OUT_DIR / 'crispr_2024.medline.txt'

TERM = 'CRISPR AND 2024[PDAT]'

h = Entrez.esearch(db='pubmed', term=TERM, usehistory='y', retmax=0)
s = Entrez.read(h)
h.close()
webenv, query_key, total = s['WebEnv'], s['QueryKey'], int(s['Count'])
print(f'ESearch (history server): Count={total}')

# Independently pull the full UID list (paginated, not via history) to have a ground-truth
# PMID set to compare against, per the audit brief's "assert on real content" requirement.
all_uids = []
for start in range(0, total, 9999):
    hh = Entrez.esearch(db='pubmed', term=TERM, retstart=start, retmax=9999)
    ss = Entrez.read(hh); hh.close()
    all_uids.extend(ss['IdList'])
    time.sleep(DELAY)
assert len(all_uids) == total, f'UID pagination mismatch: got {len(all_uids)}, expected {total}'
assert len(set(all_uids)) == total, 'Duplicate UIDs in paginated ESearch ground truth'
print(f'Ground-truth UID set: {len(all_uids)} distinct PMIDs')

t0 = time.time()
with open(OUT_PATH, 'w', encoding='utf-8') as out:
    for start in range(0, total, BATCH_SIZE):
        hh = Entrez.efetch(db='pubmed', rettype='medline', retmode='text',
                            retstart=start, retmax=BATCH_SIZE,
                            webenv=webenv, query_key=query_key)
        body = hh.read()
        hh.close()
        out.write(body)
        time.sleep(DELAY)
        print(f'  fetched {min(start + BATCH_SIZE, total)}/{total}')
elapsed = time.time() - t0
print(f'Download complete in {elapsed:.1f}s')

with open(OUT_PATH, encoding='utf-8') as fh:
    records = list(Medline.parse(fh))

print(f'MEDLINE records parsed: {len(records)}, expected: {total}')
assert len(records) == total, f'MISMATCH: expected {total} MEDLINE records, got {len(records)}'

fetched_pmids = {r.get('PMID') for r in records}
assert None not in fetched_pmids, 'Some MEDLINE records missing a PMID field'
assert fetched_pmids == set(all_uids), (
    f'PMID set mismatch: {len(fetched_pmids - set(all_uids))} extra, '
    f'{len(set(all_uids) - fetched_pmids)} missing')
print('PASS: MEDLINE-format history-server batch download recovered the exact PMID set, no truncation/duplication.')

# Sanity content check on a few real records.
sample = records[:3]
for r in sample:
    assert r.get('TI'), f'Record {r.get("PMID")} missing Title (TI) field'
print('Spot-checked 3 records: all have non-empty Title fields.')
