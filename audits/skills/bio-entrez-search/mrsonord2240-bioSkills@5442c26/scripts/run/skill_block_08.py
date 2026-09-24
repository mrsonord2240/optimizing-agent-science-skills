h = Entrez.esearch(db='pubmed', term='covid vaccine efficacy 2024', retmax=0)
r = Entrez.read(h); h.close()
print(r['QueryTranslation'])
# '("covid 19 vaccines"[MeSH Terms] OR ("covid 19"[All Fields] AND ...
# Now use this rewritten string explicitly to guarantee reproducibility.
