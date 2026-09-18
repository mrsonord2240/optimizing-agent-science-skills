# Curated RefSeq mRNA only, human, between 500 and 5000 nt
term = 'Homo sapiens[ORGN] AND srcdb_refseq[PROP] AND biomol_mrna[PROP] AND 500:5000[SLEN]'

# Reviewed SwissProt human kinases
term = 'Homo sapiens[ORGN] AND swissprot[Filter] AND kinase[Protein Name]'

# PubMed: human studies in last 30 days, full-text in PMC
term = 'CRISPR[Title] AND humans[MeSH Terms] AND last 30 days[EDAT] AND pubmed pmc[sb]'
