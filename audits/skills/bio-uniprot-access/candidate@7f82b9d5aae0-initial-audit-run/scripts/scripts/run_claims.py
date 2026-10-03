"""Doc-claim probes for bio-uniprot-access: inactive entries, query syntax, field names, endpoint table, paging."""
import os
import sys
import time

sys.dont_write_bytecode = True
CAND = r'F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access'
sys.path.insert(0, os.path.join(CAND, 'scripts'))
import requests
import uniprot_client as uc

B = uc.BASE
H = {'Accept': 'application/json'}


def get(path, **kw):
    try:
        r = requests.get(f'{B}{path}', headers=kw.pop('headers', H), timeout=90, **kw)
        return r.status_code, r.headers.get('X-Total-Results'), r.text[:110].replace('\n', ' ')
    except Exception as e:  # noqa
        return 'EXC', type(e).__name__, str(e)[:100]
    finally:
        time.sleep(0.3)


def step(name, fn):
    print(f'--- {name}')
    try:
        print(fn())
    except Exception as e:  # noqa
        print(f'EXC {type(e).__name__}: {str(e)[:250]}')


step('fetch_entry_json on an inactive (deleted) accession A0A008APR2', lambda: uc.fetch_entry_json('A0A008APR2'))

for q in ['gene:TP53', 'gene_exact:TP53', 'organism_id:9606 AND gene_exact:TP53', 'organism_name:"Homo sapiens" AND gene_exact:TP53',
          'length:[100 TO 500] AND organism_id:9606 AND reviewed:true AND gene_exact:TP53', 'go:0006915 AND organism_id:9606 AND reviewed:true',
          'keyword:KW-0067 AND organism_id:9606 AND reviewed:true AND xref:pdb', 'database:pdb AND gene_exact:TP53 AND organism_id:9606',
          'ec:2.7.1.1 AND reviewed:true', 'existence:1 AND organism_id:9606 AND reviewed:true AND gene_exact:TP53']:
    print('query', q, '->', get('/uniprotkb/search', params={'query': q, 'size': 1, 'fields': 'accession'})[:2])

FIELDS = ('accession,id,gene_names,gene_primary,protein_name,organism_name,organism_id,length,mass,sequence,cc_function,'
          'cc_subcellular_location,ft_domain,ft_binding,ft_active_site,go_p,go_c,go_f,xref_pdb,xref_alphafolddb,xref_ensembl,'
          'xref_refseq,keyword,ec,reviewed,cc_alternative_products')
print('documented fields table in one request ->', get('/uniprotkb/search', params={'query': 'accession:P04637', 'fields': FIELDS, 'format': 'tsv'}, headers={'Accept': 'text/plain'}))
bad = []
for f in FIELDS.split(','):
    r = requests.get(f'{B}/uniprotkb/search', params={'query': 'accession:P04637', 'fields': f, 'format': 'tsv'}, timeout=60)
    if r.status_code != 200:
        bad.append((f, r.status_code))
    time.sleep(0.2)
print('documented field names rejected by the service:', bad)

print('endpoint /uniprotkb/accessions:', get('/uniprotkb/accessions', params={'accessions': 'P04637,P38398,P51587', 'fields': 'accession', 'format': 'tsv'}))
print('endpoint /uniprotkb/P04637 (no suffix, JSON accept):', get('/uniprotkb/P04637'))
for suffix in ('json', 'fasta', 'tsv', 'xml', 'txt', 'gff'):
    print(f'single-entry suffix .{suffix}:', get(f'/uniprotkb/P04637.{suffix}')[0])
print('endpoint /uniref/search:', get('/uniref/search', params={'query': 'uniprot_id:P04637', 'size': 1, 'fields': 'id'}))
print('endpoint /proteomes/UP000005640:', get('/proteomes/UP000005640'))
print('endpoint /taxonomy/9606:', get('/taxonomy/9606'))
print('idmapping fields endpoint:', get('/configure/idmapping/fields')[:2])
print('result-fields endpoint:', get('/configure/uniprotkb/result-fields')[:2])

r = requests.get(f'{B}/uniprotkb/search', params={'query': 'organism_id:9606 AND reviewed:true AND keyword:KW-0418', 'size': 500, 'fields': 'accession', 'format': 'tsv'}, timeout=90)
link = r.headers.get('Link', '')
print('cursor paging: first page rows', len(r.text.strip().split('\n')) - 1, '; Link next present:', 'rel="next"' in link)
nxt = link.split('<')[1].split('>')[0] if 'rel="next"' in link else None
if nxt:
    r2 = requests.get(nxt, timeout=90)
    print('second page rows', len(r2.text.strip().split('\n')) - 1, '(total expected 625)')
