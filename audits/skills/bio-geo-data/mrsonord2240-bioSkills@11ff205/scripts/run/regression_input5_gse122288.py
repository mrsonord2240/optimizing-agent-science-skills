"""
Input 5 (Stress / multi-part): "Detect whether GSE122288 is a SuperSeries
(the Skill's own worked example accession); if so, list its SubSeries and
recommend processing them independently. Then, for GSE122288 as a whole,
walk through the processed-vs-raw decision matrix: is this Affymetrix
(-> CEL + RMA) or RNA-seq (-> SRA + re-quantify)? Don't trust the submitter's
series-matrix values for downstream stats."

Exercises: SKILL.md's own "esummary(db='gds', id='200122288')" example call,
the definitive SOFT-based SuperSeries check on the Skill's own worked example
accession, and the platform-lookup step a real "which technology" decision
needs (GPL -> technology type via Entrez esummary(db='gpl', ...)).
"""
from Bio import Entrez
import gzip
import urllib.request
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

print('=== SKILL.md worked example: Entrez.esummary(db="gds", id="200122288") ===')
h = Entrez.esummary(db='gds', id='200122288')
r = Entrez.read(h)[0]; h.close()
print(f'  Accession: {r.get("Accession")}')
print(f'  Title: {str(r.get("title",""))[:90]}')
print(f'  n_samples: {r.get("n_samples")}')
print(f'  GPL: {r.get("GPL")}')
print(f'  summary field (first 300 chars): {str(r.get("summary",""))[:300]!r}')
time.sleep(DELAY)


def check_super_or_sub_series(gse):
    prefix = gse[:-3] + 'nnn'
    url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{prefix}/{gse}/soft/{gse}_family.soft.gz'
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


print('\n=== Definitive SOFT-based check on GSE122288 (SKILL.md worked example) ===')
info = check_super_or_sub_series('GSE122288')
print(f'  {info}')

if info['super_of']:
    print(f'\n  -> SuperSeries confirmed; wraps: {info["super_of"]}')
    print('  Recommendation: process each SubSeries independently to avoid mixed-platform batch.')
    for sub in info['super_of'][:2]:
        time.sleep(DELAY)
        try:
            sub_info = check_super_or_sub_series(sub)
            print(f'    {sub}: {sub_info}')
        except Exception as e:
            print(f'    {sub}: ERROR {type(e).__name__}: {e}')
elif info['sub_of']:
    print(f'\n  -> This accession is itself a SubSeries of {info["sub_of"]}.')
else:
    print('\n  -> Standalone Series (not a SuperSeries, not a SubSeries).')
    print('  SKILL.md\'s own inline docstring example claims this accession returns')
    print('  {\'super_of\': [\'GSExxxxx\', \'GSEyyyyy\'], \'sub_of\': None} -- checking against live data above.')

# Platform lookup step for the processed-vs-raw decision (Affymetrix vs RNA-seq)
gpl = str(r.get('GPL', ''))
if gpl:
    time.sleep(DELAY)
    print(f'\n=== Platform lookup for GPL{gpl} (Affymetrix vs RNA-seq decision) ===')
    hg = Entrez.esearch(db='gds', term=f'GPL{gpl}[Accession]')
    sg = Entrez.read(hg); hg.close()
    # Direct platform technology is better read from the platform record itself
    hp = Entrez.esummary(db='gds', id='100' + gpl if gpl.isdigit() else gpl)
    try:
        rp = Entrez.read(hp)[0]; hp.close()
        print(f'  Platform technology text: {str(rp.get("summary",""))[:200]}')
    except Exception as e:
        print(f'  Platform esummary lookup did not resolve cleanly: {type(e).__name__}: {e}')
