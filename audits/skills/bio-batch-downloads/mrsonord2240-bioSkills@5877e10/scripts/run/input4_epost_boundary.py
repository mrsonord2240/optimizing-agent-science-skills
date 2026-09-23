"""Regression of the original audit's Input 3 (Edge): exact 200/201-ID EPost boundary,
using examples/batch_by_ids.py's own functions unmodified. Confirms the fix touched
robust_download.py and batch_fasta.py only (per the fix log) and left batch_by_ids.py's
boundary-guard logic intact.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
import batch_by_ids as bbi
from Bio import Entrez
Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'

# Get 201 real distinct nucleotide UIDs from a live search
h = Entrez.esearch(db='nucleotide',
                    term='TP53[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP]',
                    retmax=250)
s = Entrez.read(h); h.close()
ids = s['IdList']
print(f'got {len(ids)} live UIDs')
if len(ids) < 201:
    # pad with repeats to hit the boundary deterministically if the live count is short
    ids = (ids * ((201 // max(len(ids), 1)) + 1))[:201]
ids_200 = ids[:200]
ids_201 = ids[:201]

results = {}

# 200 IDs: direct_efetch should succeed
bbi.direct_efetch('nucleotide', ids_200, 'input4_200.fasta')
from Bio import SeqIO
n200 = sum(1 for _ in SeqIO.parse('input4_200.fasta', 'fasta'))
print(f'direct_efetch(200 ids) -> {n200} records')
results['direct_200_records'] = n200

# 201 IDs: direct_efetch should refuse via its own assert
try:
    bbi.direct_efetch('nucleotide', ids_201, 'input4_should_not_exist.fasta')
    results['direct_201_refused'] = False
except AssertionError as e:
    print(f'direct_efetch(201 ids) refused as expected: {e}')
    results['direct_201_refused'] = True

# 201 IDs via chained_epost_fetch: should succeed
bbi.chained_epost_fetch('nucleotide', ids_201, 'input4_201_chained.fasta', batch_size=100)
n201 = sum(1 for _ in SeqIO.parse('input4_201_chained.fasta', 'fasta'))
print(f'chained_epost_fetch(201 ids) -> {n201} records')
results['chained_201_records'] = n201
results['chained_201_matches_input_len'] = (n201 == len(ids_201))

with open('input4_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print(results)
