"""
Input 6 (Scope Boundary): "Search PubMed for CRISPR gene editing papers published in 2024, then
fetch the MEDLINE records for the top 5 hits so I can read title, authors, and MeSH terms."

This request's first half (finding PMIDs via ESearch) is entrez-search's job, not
entrez-fetch's -- entrez-fetch's SKILL.md and usage-guide.md never mention ESearch at all,
its whole premise is "you already have IDs." A correctly-scoped agent should note that the
discovery step belongs to a different Skill, do the minimum ESearch needed to get PMIDs (or ask
the user to supply them), and use entrez-fetch's own documented MEDLINE pattern
(Bio.Medline.parse against rettype='medline') for the actual fetch step it is responsible for.
"""
from Bio import Entrez, Medline
from io import StringIO
import time

Entrez.email = 'bio-entrez-fetch-audit@openscience.local'
Entrez.tool = 'skill-auditor-bio-entrez-fetch'

# --- out-of-scope step (belongs to entrez-search, done minimally here to get PMIDs) ---
h = Entrez.esearch(db='pubmed', term='CRISPR[Title] AND 2024[PDAT]', retmax=5, sort='relevance')
search_result = Entrez.read(h)
h.close()
pmids = search_result['IdList']
print(f'[out-of-scope setup via entrez-search] PMIDs found: {pmids}')
time.sleep(0.34)

# --- in-scope step: entrez-fetch's own documented MEDLINE pattern ---
h = Entrez.efetch(db='pubmed', id=','.join(pmids), rettype='medline', retmode='text')
records = list(Medline.parse(StringIO(h.read())))
h.close()

for r in records:
    print(f'PMID {r.get("PMID", "?")}')
    print(f'  {r.get("TI", "(no title)")[:100]}')
    print(f'  First author: {r.get("FAU", ["(no authors)"])[0] if r.get("FAU") else "(no authors)"}')
    print(f'  MeSH terms: {len(r.get("MH", []))}')
