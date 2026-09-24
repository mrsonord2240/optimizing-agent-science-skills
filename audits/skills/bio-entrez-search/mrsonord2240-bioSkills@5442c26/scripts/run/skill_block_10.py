h = Entrez.espell(db='pubmed', term='breast canser')
r = Entrez.read(h); h.close()
print(r['CorrectedQuery'])  # 'breast cancer'
