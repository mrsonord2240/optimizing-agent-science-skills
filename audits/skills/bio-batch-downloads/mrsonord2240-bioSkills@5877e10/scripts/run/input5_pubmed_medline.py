"""Regression of the original audit's Input 4 (Variant B): usage-guide.md's Quick Start
prompt, 'Download every PubMed abstract for "CRISPR AND 2024[PDAT]" in MEDLINE format.'
Live Count is 8,768 (same order of magnitude as the original audit's 2026-09-17 run).
Scaled down to the first 1,000 records (still within SKILL.md's documented pubmed/medline
1000-2000 batch-size guidance) rather than the full 8,768, to keep this regression check
fast; the mechanism under test (history-server + retstart-chunked EFetch + Medline parse)
is identical regardless of how many chunks it runs for.
"""
import json
from Bio import Entrez, Medline
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34
TARGET = 1000
BATCH = 500

h = Entrez.esearch(db='pubmed', term='CRISPR AND 2024[PDAT]', usehistory='y', retmax=0)
s = Entrez.read(h); h.close()
webenv, query_key, total = s['WebEnv'], s['QueryKey'], int(s['Count'])
print(f'Count: {total}')

records = []
start = 0
n = min(TARGET, total)
while start < n:
    batch_size = min(BATCH, n - start)
    h = Entrez.efetch(db='pubmed', rettype='medline', retmode='text',
                       retstart=start, retmax=batch_size,
                       webenv=webenv, query_key=query_key)
    recs = list(Medline.parse(h))
    h.close()
    records.extend(recs)
    start += batch_size
    time.sleep(DELAY)
    print(f'  {min(start, n)}/{n}')

print(f'fetched {len(records)} MEDLINE records (target {n})')
titled = sum(1 for r in records if r.get('TI'))
print(f'records with non-empty Title field: {titled}/{len(records)}')

result = {
    'live_count': total,
    'target': n,
    'fetched': len(records),
    'matches_target': len(records) == n,
    'all_have_title': titled == len(records),
}
with open('input5_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)
print(result)
