'''Input 2 (Variant A): curated gene->pubmed RIF links for TP53 (Gene UID 7157),
a currently-linked case, contrasted against basic_linking.py's zero-hit PMID case.'''
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

TP53 = '7157'

h = Entrez.elink(dbfrom='gene', db='pubmed', id=TP53, linkname='gene_pubmed_rif')
r = Entrez.read(h); h.close()
rif_pmids = [l['Id'] for l in r[0]['LinkSetDb'][0]['Link']] if r[0]['LinkSetDb'] else []
print(f'gene_pubmed_rif for TP53 (7157): {len(rif_pmids)} curated PubMed citations')
print(f'First 5 PMIDs: {rif_pmids[:5]}')
time.sleep(DELAY)

h = Entrez.elink(dbfrom='gene', db='pubmed', id=TP53, linkname='gene_pubmed')
r = Entrez.read(h); h.close()
all_pmids = [l['Id'] for l in r[0]['LinkSetDb'][0]['Link']] if r[0]['LinkSetDb'] else []
print(f'gene_pubmed (all) for TP53 (7157): {len(all_pmids)} PubMed citations')
print(f'RIF is a subset of all: {set(rif_pmids).issubset(set(all_pmids))}')
