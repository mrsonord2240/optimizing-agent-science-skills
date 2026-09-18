'''Input 7 (new, not in pre-fix audit) -- independently verify the fix log's claim:
"Bio.Entrez.read() already raises RuntimeError on an <ERROR> body, so no fix was needed."
The dispatch specifically warns that a sibling Skill (bio-entrez-fetch) was caught silently
fabricating rows from exactly such a body, and that the difference was which parser was used.
Tests this against a realistic captured NCBI <ERROR> body (matching the shape SKILL.md's own
"Failure modes" table documents: WebEnv expiration, HTTP 200 with an <ERROR> body) fed through
Bio.Entrez.read(), which is what every pattern in this Skill (SKILL.md + all 3 examples/*.py)
uses to parse ESearch/EInfo/ESpell responses.
'''
import io
from Bio import Entrez

# Realistic bodies actually seen from NCBI E-utilities (matches SKILL.md's documented failure
# modes: "<ERROR>WebEnv not found</ERROR>" and the outage body from today's dispatch note,
# "<ERROR>Search Backend failed ... 502</ERROR>").
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
        print(f'  RuntimeError raised (expected, per fix log): {e}')
    except Exception as e:
        print(f'  Different exception type: {type(e).__name__}: {e}')
    print()

# Also confirm the shape of a REAL successful parse for contrast (so "no exception" above would
# be unambiguous, not a false negative from a parser that always throws).
h = Entrez.esearch(db='pubmed', term='CRISPR[Title]', retmax=0)
r = Entrez.read(h); h.close()
print(f'Control: real successful ESearch parses fine, Count={r["Count"]}, type={type(r).__name__}')
