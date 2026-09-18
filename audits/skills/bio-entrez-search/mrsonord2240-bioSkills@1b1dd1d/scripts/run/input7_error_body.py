'''Input 7 (Adversarial) -- regression, independently verify Bio.Entrez.read() raises rather than
silently fabricates on an <ERROR> body (the defect that hit the sibling Skill entrez-fetch).
'''
import io
from Bio import Entrez

error_bodies = [
    b'<?xml version="1.0" encoding="UTF-8" ?>\n'
    b'<!DOCTYPE eSearchResult PUBLIC "-//NLM//DTD esearch 20060628//EN" '
    b'"https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20060628/esearch.dtd">\n'
    b'<eSearchResult><ERROR>WebEnv not found</ERROR></eSearchResult>',

    b'<?xml version="1.0" encoding="UTF-8" ?>\n'
    b'<!DOCTYPE eSearchResult PUBLIC "-//NLM//DTD esearch 20060628//EN" '
    b'"https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20060628/esearch.dtd">\n'
    b'<eSearchResult><ERROR>Search Backend failed: Exception: 502 Proxy Error</ERROR></eSearchResult>',
]

for i, body in enumerate(error_bodies, 1):
    print(f'=== Body {i}: {body[-60:]} ===')
    handle = io.BytesIO(body)
    try:
        record = Entrez.read(handle)
        print(f'  NO EXCEPTION RAISED -- record = {record!r}')
        print('  DEFECT: parsed without error; check for silent fabrication')
    except RuntimeError as e:
        print(f'  RuntimeError raised (expected): {e}')
    except Exception as e:
        print(f'  Different exception type: {type(e).__name__}: {e}')
    print()

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
h = Entrez.esearch(db='pubmed', term='CRISPR[Title]', retmax=0)
r = Entrez.read(h); h.close()
print(f'Control: real successful ESearch parses fine, Count={r["Count"]}, type={type(r).__name__}')
