"""Re-auditor NEW input 1: verify SKILL.md's own corrected SuperSeries worked example
(GSE346738) actually demonstrates a real, live SuperSeries -- not just reading the fix log's claim.
Uses SKILL.md's inline check_super_or_sub_series(), copied verbatim from the fixed SKILL.md."""
from Bio import Entrez
import gzip
import time

Entrez.email = 'reauditor-bio-geo-data@optimizing-agent-science-skills.local'
DELAY = 0.34


def check_super_or_sub_series(gse):
    prefix = gse[:-3] + 'nnn'
    url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{prefix}/{gse}/soft/{gse}_family.soft.gz'
    import urllib.request
    urllib.request.urlretrieve(url, f'{gse}.soft.gz')
    super_of = []
    sub_of = None
    with gzip.open(f'{gse}.soft.gz', 'rt') as f:
        for line in f:
            if line.startswith('!Series_relation'):
                if 'SuperSeries of' in line:
                    super_of.append(line.split('SuperSeries of: ')[1].strip())
                elif 'SubSeries of' in line:
                    sub_of = line.split('SubSeries of: ')[1].strip()
            if line.startswith('^SAMPLE'):
                break
    return {'super_of': super_of, 'sub_of': sub_of}


print('=== SKILL.md worked example: check_super_or_sub_series(GSE346738) ===')
result = check_super_or_sub_series('GSE346738')
print(result)
assert result['super_of'], "Expected a populated super_of list -- SKILL.md's own docstring claim"
assert set(result['super_of']) == {'GSE283260', 'GSE346737'}, f"Unexpected super_of: {result['super_of']}"
print('PASS: GSE346738 is a live SuperSeries of', result['super_of'])
time.sleep(DELAY)

# Cross-check via ESummary too, independent of the FTP/SOFT mechanism
print('\n=== Cross-check via ESummary(db=gds) on GSE346738 and its two claimed subseries ===')
for gse in ['GSE346738', 'GSE283260', 'GSE346737']:
    h = Entrez.esearch(db='gds', term=f'{gse}[Accession]')
    s = Entrez.read(h); h.close()
    time.sleep(DELAY)
    if not s['IdList']:
        print(f'  {gse}: NOT FOUND in gds')
        continue
    h = Entrez.esummary(db='gds', id=s['IdList'][0])
    rec = Entrez.read(h)[0]; h.close()
    print(f'  {gse}: n_samples={rec.get("n_samples")}, title={str(rec.get("title"))[:70]}')
    time.sleep(DELAY)
