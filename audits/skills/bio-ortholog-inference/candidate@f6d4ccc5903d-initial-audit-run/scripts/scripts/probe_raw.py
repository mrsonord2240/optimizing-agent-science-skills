"""Raw live probes of the endpoints the Skill documents (timeouts on all calls). Read-only; saves JSON/text to probe_raw_output.txt."""
import sys, json, time, requests
sys.dont_write_bytecode = True
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out.append(s)
def get(url, **kw):
    try:
        r = requests.get(url, timeout=45, headers=kw.pop('headers', {}), **kw); return r
    except Exception as e:
        P('  EXC', type(e).__name__, str(e)[:160]); return None
J = {'Accept': 'application/json'}
# 1. Ensembl raw homology record: which confidence key exists?
r = get('https://rest.ensembl.org/homology/symbol/human/TP53', params={'type': 'orthologues', 'target_species': 'mouse'}, headers=J)
P('ENSEMBL homology status', r.status_code)
h = r.json()['data'][0]['homologies'][0]
P('homology keys:', sorted(h)); P('source keys:', sorted(h['source'])); P('target keys:', sorted(h['target']))
P('raw homology:', json.dumps(h))
time.sleep(0.5)
# 1b. confidence-bearing variant: ?compara=... / aligned=0 / format=condensed
r = get('https://rest.ensembl.org/homology/symbol/human/TP53', params={'type': 'orthologues', 'target_species': 'mouse', 'format': 'full'}, headers=J)
P('ENSEMBL format=full keys:', sorted(r.json()['data'][0]['homologies'][0]) if r is not None and r.ok else r)
time.sleep(0.5)
# 1c. nonexistent symbol
r = get('https://rest.ensembl.org/homology/symbol/human/NOT_A_GENE_XYZ', params={'type': 'orthologues'}, headers=J)
P('ENSEMBL bad symbol', r.status_code, r.text[:120])
time.sleep(0.5)
# 1d. type=orthologues vs paralogs; does this param actually drop paralogs?
r = get('https://rest.ensembl.org/homology/symbol/human/TP53', params={'type': 'orthologues', 'target_species': 'zebrafish'}, headers=J)
P('ENSEMBL zebrafish types', [x['type'] for x in r.json()['data'][0]['homologies']])
time.sleep(0.5)
# 2. OrthoDB v12
r = get('https://data.orthodb.org/v12/search', params={'query': 'TP53', 'species': 9606})
P('ORTHODB search', r.status_code, r.headers.get('content-type'), json.dumps(r.json())[:400])
sj = r.json(); g0 = sj['data'][0]
time.sleep(0.5)
for og in [g0, '4837993at2759']:
    r = get('https://data.orthodb.org/v12/orthologs', params={'id': og, 'species': 10090})
    P('ORTHODB orthologs', og, r.status_code, json.dumps(r.json())[:700] if r.ok else r.text[:200])
    time.sleep(0.5)
r = get('https://data.orthodb.org/v12/group', params={'id': '4837993at2759'})
P('ORTHODB group', r.status_code, r.text[:300])
time.sleep(0.5)
r = get('https://data.orthodb.org/v12/tab', params={'query': '4837993at2759'})
P('ORTHODB tab', r.status_code, r.text[:200])
time.sleep(0.5)
# does species filter in search matter?
r2 = get('https://data.orthodb.org/v12/search', params={'query': 'TP53', 'species': 10090})
P('ORTHODB search TP53 species=10090 count', len(r2.json().get('data', [])), 'vs 9606 count', len(sj['data']))
time.sleep(0.5)
# 3. OMA
for base in ['https://omabrowser.org/api', 'https://api.omabrowser.org/api']:
    for path in ['/version/', '/protein/P38398/', '/protein/P38398/orthologs/', '/genome/HUMAN/']:
        for i in range(2):
            r = get(base + path)
            if r is not None and r.status_code != 502: break
            time.sleep(3)
        P('OMA', base + path, None if r is None else (r.status_code, r.headers.get('content-type'), r.text[:150].replace('\n', ' ')))
        time.sleep(1)
# 4. KEGG: unknown gene / HTML
r = get('https://rest.kegg.jp/link/ko/hsa:99999999')
P('KEGG unknown gene', r.status_code, repr(r.text[:80]))
# 5. PANTHER documented base
r = get('https://pantherdb.org/services/oai/pantherdb/ortholog/matchortho', params={'geneInputList': 'P04637', 'organism': 9606, 'targetOrganism': 10090, 'orthologType': 'LDO'})
P('PANTHER', r.status_code, json.dumps(r.json())[:300])
r = get('http://pantherdb.org/services/oai/pantherdb/supportedgenomes', allow_redirects=False)
P('PANTHER http redirect', r.status_code, r.headers.get('location'))
# 6. eggNOG
for u in ['https://eggnog6.embl.de/api/', 'https://eggnogdb.org/api/']:
    r = get(u)
    P('EGGNOG', u, None if r is None else (r.status_code, r.url))
# 7. HomoloGene
r = get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi', params={'db': 'homologene', 'id': '460', 'retmode': 'text'})
P('HOMOLOGENE', r.status_code, r.text[:80])
open('probe_raw_output.txt', 'w', encoding='utf-8').write('\n'.join(out))
