import requests
B = 'https://rest.uniprot.org/uniprotkb/search'
for q in ('proteome:UP000005640', 'proteome:UP000005640 AND reviewed:true', 'proteome:UP000005640 AND reviewed:false',
          'proteome:UP000005640 AND organism_id:9606 AND reviewed:true'):
    r = requests.get(B, params={'query': q, 'size': 1, 'fields': 'accession'}, timeout=60)
    print(q, '->', r.headers['X-Total-Results'])
p = requests.get('https://rest.uniprot.org/proteomes/UP000005640.json', timeout=60).json()
print({k: p.get(k) for k in ('id', 'proteomeType', 'proteinCount', 'geneCount', 'taxonomy')} if isinstance(p, dict) else p)
