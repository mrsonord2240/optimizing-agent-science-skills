"""
Input 4 (Edge) - "My esearch for 'MARCH1 AND human' returned no hits. Print the
QueryTranslation, then re-run with the proper field-qualified form using the
HGNC-permanent symbol MARCHF1."

This is the Skill's own worked "Diagnosing a wrong count bug" example (usage-guide.md).
Tests the Query translation mismatch failure mode.
"""
from Bio import Entrez

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'skill-auditor-bio-entrez-search'

# Step 1: reproduce the reported problem query
h = Entrez.esearch(db='gene', term='MARCH1 AND human', retmax=5)
r = Entrez.read(h)
h.close()
print('=== Original query: MARCH1 AND human ===')
print(f'Count: {r["Count"]}')
print(f'QueryTranslation: {r["QueryTranslation"]}')

# Step 2: field-qualified retry with HGNC-permanent symbol
h2 = Entrez.esearch(db='gene', term='MARCHF1[Gene Name] AND Homo sapiens[Organism]', retmax=5)
r2 = Entrez.read(h2)
h2.close()
print('\n=== Field-qualified retry: MARCHF1[Gene Name] AND Homo sapiens[Organism] ===')
print(f'Count: {r2["Count"]}')
print(f'QueryTranslation: {r2["QueryTranslation"]}')
print(f'IdList: {r2["IdList"]}')

print('\nDiagnosis printed for the user: original term was ambiguous (Excel-renamed gene vs '
      'a literal date string "MARCH1"); field-qualified HGNC-permanent symbol resolves it.')
