# PYTHONIOENCODING=utf-8
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'

try:
    h = Entrez.esearch(db='pubmed', term='CRISPR[Title]', retmax=0)
    r = Entrez.read(h); h.close()
    print('OK: Count =', r['Count'])
except Exception as e:
    print('ERROR type:', type(e).__name__)
    print('ERROR msg:', e)
