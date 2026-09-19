from Bio import Entrez
Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
# A term with Count well above 9999, queried WITHOUT usehistory='y' and WITHOUT retmax,
# to check SKILL.md's "Silent retmax cap" failure-mode claim (legacy esearch defaults cap at 9999).
h = Entrez.esearch(db='pubmed', term='cancer[TIAB]')
s = Entrez.read(h); h.close()
print('Count:', s['Count'], 'IdList len (default retmax, no usehistory):', len(s['IdList']))

h2 = Entrez.esearch(db='pubmed', term='cancer[TIAB]', retmax=100000)
s2 = Entrez.read(h2); h2.close()
print('Count:', s2['Count'], 'IdList len (retmax=100000 explicit, no usehistory):', len(s2['IdList']))
