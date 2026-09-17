from Bio import Entrez
import time
Entrez.email = 'bio-entrez-fetch-audit@openscience.local'
Entrez.tool = 'skill-auditor-bio-entrez-fetch'

h = Entrez.esearch(db='clinvar', term='BRCA1[gene] AND pathogenic[Clinical_significance]', retmax=3)
r = Entrez.read(h); h.close()
print('IdList:', r['IdList'])
time.sleep(0.34)

# Try EFetch on clinvar with rettype='vcv' (undocumented in SKILL.md's matrix)
uid = r['IdList'][0]
try:
    h = Entrez.efetch(db='clinvar', id=uid, rettype='vcv', retmode='xml')
    txt = h.read(); h.close()
    print('EFetch vcv/xml OK, bytes:', len(txt) if isinstance(txt, (str, bytes)) else 'n/a')
    print(str(txt)[:300])
except Exception as e:
    print('EFetch vcv/xml FAILED:', type(e).__name__, e)
time.sleep(0.34)

try:
    h = Entrez.esummary(db='clinvar', id=uid)
    d = Entrez.read(h); h.close()
    print('ESummary OK, type:', type(d))
    print(str(d)[:500])
except Exception as e:
    print('ESummary FAILED:', type(e).__name__, e)
