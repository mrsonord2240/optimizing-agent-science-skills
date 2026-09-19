import sys, time
sys.path.insert(0, ".")
from Bio import Entrez
Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'

queries = [
    ("BRCA1[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP]", "nucleotide"),
    ("INS[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP]", "nucleotide"),
    ("TP53[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP]", "nucleotide"),
]
for term, db in queries:
    h = Entrez.esearch(db=db, term=term, usehistory='y', retmax=0)
    s = Entrez.read(h); h.close()
    print(db, term, "->", s['Count'])
    time.sleep(0.34)
