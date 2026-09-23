"""Re-auditor NEW input 2: a fresh, realistic multi-step request the fixer/original auditor never
ran: search for a different disease domain (Alzheimer's, not breast cancer), then exercise the
platform-technology gdsType snippet (P2 fix) and SuperSeries check on a real result -- combining
three of the Skill's documented steps end to end on data no prior pass touched."""
from Bio import Entrez
import time

Entrez.email = 'reauditor-bio-geo-data@optimizing-agent-science-skills.local'
DELAY = 0.34


def search_geo(term, study_type='gse', organism=None, max_results=10):
    full_term = f'{term} AND {study_type}[Entry Type]'
    if organism:
        full_term += f' AND {organism}[Organism]'
    h = Entrez.esearch(db='gds', term=full_term, retmax=max_results)
    s = Entrez.read(h); h.close()
    if not s['IdList']:
        return []
    h = Entrez.esummary(db='gds', id=','.join(s['IdList']))
    return Entrez.read(h)


print("=== Search: Alzheimer's disease microarray, human ===")
results = search_geo("Alzheimer's disease microarray", organism='Homo sapiens', max_results=10)
for s in results:
    print(f'  {s["Accession"]:12} {s["n_samples"]:>4} samples  {s["GPL"]:<10}  {s["title"][:60]}')
time.sleep(DELAY)

assert results, "Expected at least one real GSE hit for this query"
top = results[0]
top_acc = top['Accession']
print(f'\n=== gdsType platform-technology snippet (SKILL.md P2 fix) on {top_acc} ===')
h = Entrez.esearch(db='gds', term=f'{top_acc}[Accession]', retmax=1)
s = Entrez.read(h); h.close(); time.sleep(DELAY)
h = Entrez.esummary(db='gds', id=s['IdList'][0])
gse_record = Entrez.read(h)[0]; h.close()
gds_type = gse_record.get('gdsType', '')
is_sequencing = 'high throughput sequencing' in gds_type
print(f'  gdsType: {gds_type!r}')
print(f'  is_sequencing: {is_sequencing}')
assert gds_type, "gdsType field should be present and non-empty on a real GDS/GSE record"

print(f'\n=== SuperSeries check (SKILL.md P1 fix area) on {top_acc} ===')
prefix = top_acc[:-3] + 'nnn'
url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{prefix}/{top_acc}/soft/{top_acc}_family.soft.gz'
import urllib.request, gzip, io
with urllib.request.urlopen(url, timeout=30) as resp:
    data = resp.read()
super_of, sub_of = [], None
try:
    with gzip.GzipFile(fileobj=io.BytesIO(data), mode='rb') as fb:
        f = io.TextIOWrapper(fb, encoding='utf-8', errors='replace')
        for line in f:
            if line.startswith('^SAMPLE'):
                break
            if line.startswith('!Series_relation'):
                if 'SuperSeries of' in line:
                    super_of.append(line.split('SuperSeries of: ')[1].strip())
                elif 'SubSeries of' in line:
                    sub_of = line.split('SubSeries of: ')[1].strip()
    print(f'  super_of={super_of}  sub_of={sub_of}')
except UnicodeDecodeError as e:
    print(f'  DECODE ERROR even with TextIOWrapper(utf-8): {e}')

print('\nDone: real gdsType + real SuperSeries status reported for a fresh accession never tested by the fixer or the original auditor.')
