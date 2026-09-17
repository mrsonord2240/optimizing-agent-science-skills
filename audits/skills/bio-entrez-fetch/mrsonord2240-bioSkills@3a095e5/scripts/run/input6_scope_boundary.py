"""
Input 6 (Scope Boundary, regression of pre-fix P1 -- "no guidance for how a fetch-only Skill
receives its input IDs"):
"Search PubMed for CRISPR gene editing papers published in 2024, then fetch the MEDLINE records
for the top 5 hits so I can read title, authors, and MeSH terms."

The discovery half (ESearch) is not entrez-fetch's job. The fix added one sentence to SKILL.md's
intro: "This Skill assumes you already have UIDs or accessions to fetch. If you need to discover
them from a search term, use entrez-search first." -- this input checks both that the sentence
is actually present in the shipped file, AND that the documented rettype='medline' fetch pattern
(prose + XML-schema-brittleness section, not its own fenced block) still works.
"""
from Bio import Entrez, Medline
from io import StringIO
import time
import pathlib

Entrez.email = 'bio-entrez-fetch-reaudit@openscience.local'
Entrez.tool = 'skill-reauditor-bio-entrez-fetch'

SKILL_MD = pathlib.Path(r"F:\OpenScience\wt\db-efetch\database-access\entrez-fetch\SKILL.md")
text = SKILL_MD.read_text(encoding='utf-8')
scope_sentence_present = 'This Skill assumes you already have UIDs or accessions to fetch' in text
print(f'SCOPE_NOTE_PRESENT={scope_sentence_present}')

print('\n[out-of-scope setup via entrez-search]')
h = Entrez.esearch(db='pubmed', term='CRISPR gene editing[Title] AND 2024[PDAT]', retmax=5)
sr = Entrez.read(h); h.close()
pmids = sr['IdList']
print(f'PMIDs found: {pmids}')
time.sleep(0.34)

h = Entrez.efetch(db='pubmed', id=','.join(pmids), rettype='medline', retmode='text')
records = list(Medline.parse(StringIO(h.read()))); h.close()
print(f'\nRECORDS_RETURNED={len(records)}')
for r in records:
    print(f"  PMID {r.get('PMID', '?')}: {r.get('TI', '(no title)')[:80]}  MeSH={len(r.get('MH', []))}")
