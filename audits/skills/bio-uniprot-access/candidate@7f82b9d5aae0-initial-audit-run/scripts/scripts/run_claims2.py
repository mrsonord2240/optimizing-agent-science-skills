"""Follow-ups: valid name for the rejected ft_ field, and the documented xref:pdb query alias."""
import sys, time
sys.dont_write_bytecode = True
import requests
B = 'https://rest.uniprot.org'
def total(q):
    r = requests.get(f'{B}/uniprotkb/search', params={'query': q, 'size': 1, 'fields': 'accession'}, timeout=60)
    time.sleep(0.3)
    return r.status_code, r.headers.get('X-Total-Results')
for f in ('ft_act_site', 'ft_active_site', 'ft_binding', 'ft_domain'):
    r = requests.get(f'{B}/uniprotkb/search', params={'query': 'accession:P04637', 'fields': f, 'format': 'tsv'}, timeout=60)
    print('field', f, '->', r.status_code, r.text.strip().split('\n')[0][:60] if r.ok else r.text[:80].replace('\n', ' '))
    time.sleep(0.3)
base = 'organism_id:9606 AND reviewed:true AND keyword:KW-0067'
print('KW-0067 base (no xref):', total(base))
print('base AND xref:pdb  (documented Combine example):', total(base + ' AND xref:pdb'))
print('base AND database:pdb:', total(base + ' AND database:pdb'))
print('base AND xref:pdb-*:', total(base + ' AND xref:pdb-*'))
print('base AND structure_3d:true:', total(base + ' AND structure_3d:true'))
print('gene_exact:TP53 AND xref:pdb:', total('gene_exact:TP53 AND organism_id:9606 AND xref:pdb'))
