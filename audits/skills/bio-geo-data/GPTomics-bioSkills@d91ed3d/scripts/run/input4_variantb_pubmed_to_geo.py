"""
Input 4 (Variant B): "Find all GEO datasets cited in PMID 32228226 via
pubmed -> gds ELink (the Skill's own worked example, examples/geo_from_pubmed.py,
labeled as Blanco-Melo et al. 2020 Cell COVID-19 transcriptional response).
Summarize each with title, sample count, platform, and SuperSeries status."

Follows examples/geo_from_pubmed.py exactly as shipped, including its
hardcoded PMID and its claimed identity for that PMID, to test the worked
example as a user would actually run it.
"""
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34


def find_geo_for_pubmed(pmid):
    h = Entrez.elink(dbfrom='pubmed', db='gds', id=pmid)
    r = Entrez.read(h); h.close()
    if not r[0]['LinkSetDb']:
        return []
    gds_uids = [l['Id'] for l in r[0]['LinkSetDb'][0]['Link']]
    time.sleep(DELAY)
    h = Entrez.esummary(db='gds', id=','.join(gds_uids))
    return Entrez.read(h)


def article_info(pmid):
    h = Entrez.esummary(db='pubmed', id=pmid)
    r = Entrez.read(h)[0]; h.close()
    return r


PMID = '32228226'  # as shipped: claimed "Blanco-Melo et al. 2020 Cell (COVID-19 transcriptional response)"

print('=== Article (as shipped PMID) ===')
art = article_info(PMID)
print(f'  PMID:    {PMID}')
print(f'  Title:   {art.get("Title", "?")[:100]}')
print(f'  Journal: {art.get("Source", "?")}, {art.get("PubDate", "?")}')
time.sleep(DELAY)

print(f'\n=== GEO datasets cited in PMID {PMID} (as shipped) ===')
results = find_geo_for_pubmed(PMID)
print(f'n results: {len(results)}')
for ds in results:
    print(f'  {ds["Accession"]:12}  {ds["n_samples"]:>4} samples  GPL{ds["GPL"]:<8}')
    print(f'      {ds["title"][:90]}')

# Now the corrected PMID, to see whether the intended output actually exists.
CORRECT_PMID = '32416070'
print(f'\n=== Article (corrected PMID {CORRECT_PMID}) ===')
art2 = article_info(CORRECT_PMID)
print(f'  Title:   {art2.get("Title", "?")[:100]}')
print(f'  Journal: {art2.get("Source", "?")}, {art2.get("PubDate", "?")}')
time.sleep(DELAY)

print(f'\n=== GEO datasets cited in corrected PMID {CORRECT_PMID} ===')
results2 = find_geo_for_pubmed(CORRECT_PMID)
print(f'n results: {len(results2)}')
for ds in results2:
    print(f'  {ds["Accession"]:12}  {ds["n_samples"]:>4} samples  GPL{ds["GPL"]:<8}')
    print(f'      {ds["title"][:90]}')
