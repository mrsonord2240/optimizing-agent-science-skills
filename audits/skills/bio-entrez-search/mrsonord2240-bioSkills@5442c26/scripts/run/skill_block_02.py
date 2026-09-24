handle = Entrez.esearch(db='nucleotide', term='human BRCA1')
record = Entrez.read(handle)
handle.close()
print(record['QueryTranslation'])
# '("homo sapiens"[Organism] OR human[All Fields]) AND (BRCA1[Gene Name] OR BRCA1[All Fields])'
