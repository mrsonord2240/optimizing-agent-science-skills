"""
Point-3 probe (dispatched by the coordinator): does any code path in the FIXED SKILL.md swallow
an NCBI-side backend outage (HTTP 200/400 with an <ERROR> element in the body) instead of raising
a clear exception?

Uses the two REAL error bodies this re-audit actually captured live from NCBI during today's
PubMed 2.0 search-backend outage (2026-09-17) -- not synthesized text -- fed directly into the
Skill's own parsing functions, bypassing the network so this doesn't depend on the outage
clearing.
"""
import sys
sys.path.insert(0, r'F:\OpenScience\audits\bio-entrez-fetch\run\skillmd_blocks')

REAL_ESEARCH_502_BODY = (
    b'<?xml version="1.0" encoding="UTF-8" ?>\n'
    b'<!DOCTYPE eSearchResult PUBLIC "-//NLM//DTD esearch 20060628//EN" '
    b'"https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20060628/esearch.dtd">\n'
    b'<eSearchResult>\n\t<ERROR>Search Backend failed: Pubmed 2.0 search API: '
    b'HTTP request returned 502 status.</ERROR>\n</eSearchResult>\n'
)

REAL_EFETCH_502_BODY = (
    '<?xml version="1.0" encoding="UTF-8" ?>\n<!DOCTYPE eEfetchResult PUBLIC "-//NLM//DTD efetch '
    '20131226//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20131226/efetch.dtd">\n'
    '<eFetchResult>\n\t<ERROR> Error: CEFetchPApplication::proxy_stream(): &#xa;&lt;html&gt;'
    '&lt;head&gt;&#xa;&lt;meta http-equiv=&quot;content-type&quot; content=&quot;text/html;'
    'charset=utf-8&quot;&gt;&#xa;&lt;title&gt;502 Server Error&lt;/title&gt;&#xa;&lt;/head&gt;'
    '&#xa;&lt;body text=#000000 bgcolor=#ffffff&gt;&#xa;&lt;h1&gt;Error: Server Error&lt;/h1&gt;'
    '&#xa;&lt;h2&gt;The server encountered a temporary error and could not complete your request.'
    '&lt;p&gt;Please try again in 30 seconds.&lt;/h2&gt;&#xa;&lt;h2&gt;&lt;/h2&gt;&#xa;&lt;/body&gt;'
    '&lt;/html&gt;</ERROR>\n</eFetchResult>\n'
)

print('=== 1. Entrez.read() route (used by pubmed_full(), lineage(), and the History-server '
      'fetch pattern) fed the real captured ESearch 502 body ===')
from Bio import Entrez
import io
try:
    parsed = Entrez.read(io.BytesIO(REAL_ESEARCH_502_BODY))
    print(f'SILENTLY SUCCEEDED (BAD): {parsed}')
except RuntimeError as e:
    print(f'RAISED RuntimeError (safe, self-explaining): {e}')
except Exception as e:
    print(f'RAISED {type(e).__name__} (safe): {e}')

print('\n=== 2. sra_runinfo()-style plain-text/CSV route fed the real captured EFetch 502 body ===')
print('    (SKILL.md\'s own sra_runinfo() code, verbatim parsing logic, no network)')


def sra_runinfo_parsing_logic(raw_text):
    # Exactly SKILL.md's sra_runinfo(), minus the network call -- `raw_text` stands in for
    # what h.read() would have returned.
    text = raw_text
    lines = text.strip().split('\n')
    header = lines[0].split(',')
    return [dict(zip(header, row.split(','))) for row in lines[1:]]


try:
    rows = sra_runinfo_parsing_logic(REAL_EFETCH_502_BODY)
    print(f'SILENTLY "SUCCEEDED": {len(rows)} row(s) produced from an error body')
    for r in rows:
        print(f'  {r}')
    print('  ^ This is the risk: no Python exception was raised. The header row becomes the '
          'first line of malformed XML, and every subsequent line becomes a "row" with mismatched '
          'field counts (dict(zip(...)) silently truncates to the shorter of header/row). An '
          'agent parsing this as a Run/Bases/Spots table would see plausible-looking dict output, '
          'not an alarm.')
except Exception as e:
    print(f'RAISED {type(e).__name__} (safe): {e}')

print('\n=== 3. fetch_genbank()-style SeqIO.read() route fed the real captured EFetch 502 body ===')
from Bio import SeqIO
from io import StringIO
try:
    rec = SeqIO.read(StringIO(REAL_EFETCH_502_BODY), 'genbank')
    print(f'SILENTLY SUCCEEDED (BAD): {rec}')
except Exception as e:
    print(f'RAISED {type(e).__name__} (safe, but no skill-level guidance names this case): {e}')

print('\n=== 4. The ONE place SKILL.md documents a body-sniff guard (Failure Modes: "EFetch '
      'returns HTML error page") -- is it applied in SKILL.md\'s own fetch_genbank() code '
      'pattern, or only in the separate examples/fetch_sequences.py file? ===')
skill_md = open(r'F:\OpenScience\wt\db-efetch\database-access\entrez-fetch\SKILL.md',
                 encoding='utf-8').read()
fetch_genbank_block = skill_md.split('### Single sequence by accession')[1].split('###')[0]
print('sniff_then_parse / LOCUS-check present in SKILL.md\'s own fetch_genbank():',
      'sniff' in fetch_genbank_block.lower() or 'LOCUS' in fetch_genbank_block and 'startswith' in fetch_genbank_block)
print('--- fetch_genbank() block as shipped in SKILL.md ---')
print(fetch_genbank_block.strip())
