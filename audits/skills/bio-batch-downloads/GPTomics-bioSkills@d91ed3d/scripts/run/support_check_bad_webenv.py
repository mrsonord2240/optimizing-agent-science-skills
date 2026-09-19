from Bio import Entrez
Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
try:
    h = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text',
                       retstart=0, retmax=10, webenv='BOGUS_WEBENV_STRING',
                       query_key='99')
    body = h.read()
    h.close()
    print('Got body, first 500 chars:')
    print(body[:500] if isinstance(body, str) else body[:500])
except Exception as e:
    print(f'Exception type: {type(e).__name__}: {e}')
