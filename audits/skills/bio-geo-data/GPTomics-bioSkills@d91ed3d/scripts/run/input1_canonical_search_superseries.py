"""
Input 1 (Canonical): "Search GEO for human breast cancer RNA-seq series and flag
any that are SuperSeries before I download them."

Follows SKILL.md's documented code patterns:
  - "Search GEO for studies matching a query" (search_geo())
  - "The SuperSeries trap" detection (definitive SOFT-file check, the SKILL.md
    inline version -- NOT examples/search_geo.py's detect_super_series(), which
    TOOLS.md's tooling pass already found broken: GzipFile(mode='rt') raises
    ValueError. This input exercises the SKILL.md-documented function instead,
    to see whether the *skill's own primary documentation* holds up.)
"""
from Bio import Entrez
import gzip
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34


def search_geo(term, study_type='gse', organism=None, max_results=50):
    full_term = f'{term} AND {study_type}[Entry Type]'
    if organism:
        full_term += f' AND {organism}[Organism]'
    h = Entrez.esearch(db='gds', term=full_term, retmax=max_results)
    s = Entrez.read(h); h.close()
    if not s['IdList']:
        return []
    h = Entrez.esummary(db='gds', id=','.join(s['IdList']))
    summaries = Entrez.read(h); h.close()
    return summaries


def check_super_or_sub_series_from_bytes(soft_bytes):
    """Same logic as SKILL.md's check_super_or_sub_series(), but operating on
    already-downloaded bytes (saved to disk first, per the documented pattern
    of gzip.open(path, 'rt') -- not the in-memory BytesIO+GzipFile(mode='rt')
    approach that examples/search_geo.py uses and which is broken)."""
    tmp = 'tmp_family.soft.gz'
    with open(tmp, 'wb') as f:
        f.write(soft_bytes)
    super_of, sub_of = [], None
    with gzip.open(tmp, 'rt') as f:
        for line in f:
            if line.startswith('!Series_relation'):
                if 'SuperSeries of' in line:
                    super_of.append(line.split('SuperSeries of: ')[1].strip())
                elif 'SubSeries of' in line:
                    sub_of = line.split('SubSeries of: ')[1].strip()
            if line.startswith('^SAMPLE'):
                break
    return {'super_of': super_of, 'sub_of': sub_of}


print('=== search_geo("breast cancer", study_type=gse, organism=Homo sapiens, max_results=10) ===')
results = search_geo('breast cancer', organism='Homo sapiens', max_results=10)
print(f'n results: {len(results)}')
for r in results:
    acc = r.get('Accession', '?')
    n = r.get('n_samples', '?')
    gpl = r.get('GPL', '?')
    title = str(r.get('title', ''))[:70]
    summary = str(r.get('summary', ''))
    flagged = 'SuperSeries' in summary
    print(f'  {acc:12} {n:>4} samples  GPL{gpl:<8}  {"[flag:SuperSeries-in-summary]" if flagged else "":30} {title}')

# Pick the first flagged-or-not accession and run the DEFINITIVE SOFT check,
# exactly as SKILL.md instructs ("Definitive check: download SOFT and grep").
import urllib.request

target = results[0]['Accession'] if results else None
print(f'\n=== Definitive SuperSeries check via SOFT family file for {target} ===')
if target:
    prefix = target[:-3] + 'nnn'
    url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{prefix}/{target}/soft/{target}_family.soft.gz'
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            data = resp.read()
        info = check_super_or_sub_series_from_bytes(data)
        print(f'  {target}: {info}')
    except Exception as e:
        print(f'  ERROR fetching/parsing {target}: {type(e).__name__}: {e}')
