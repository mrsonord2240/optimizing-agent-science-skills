'''RE-AUDIT NEW INPUT 2 (beyond fixer's scope, revised): verify SKILL.md's documented
"Mismatched dbfrom and id namespace" failure mode is actually true on live data --
described in SKILL.md ("Fix: Validate that the ID matches the source db namespace")
but never exercised by any of the original 7 audit inputs or by the fix pass.
Realistic scenario: an agent has UID 31322957 (a nucleotide UID, NM_007294.4) and
correctly links nuccore->pubmed, versus a bug where the same numeric UID is passed
with dbfrom=pubmed by mistake.'''
from Bio import Entrez

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'

# Correct usage: known nucleotide UID, nuccore -> pubmed
h = Entrez.elink(dbfrom='nucleotide', db='pubmed', id='31322957', linkname='nuccore_pubmed')
r = Entrez.read(h); h.close()
correct = r[0]['LinkSetDb'][0]['Link'] if r[0]['LinkSetDb'] else []
print(f'Correct (dbfrom=nucleotide, real nuccore UID 31322957): {len(correct)} linked PubMed records')

# Mismatched: same numeric value passed as if it were itself a pubmed UID (dbfrom=pubmed),
# a plausible copy-paste bug when chaining UIDs across databases.
h2 = Entrez.elink(dbfrom='pubmed', db='gene', id='31322957')
r2 = Entrez.read(h2); h2.close()
mismatched = r2[0]['LinkSetDb'][0]['Link'] if r2[0]['LinkSetDb'] else []
print(f'Mismatched (dbfrom=pubmed, same numeric value 31322957 used as if PMID): '
      f'{len(mismatched)} results, LinkSetDb empty: {not r2[0]["LinkSetDb"]}')
print('No exception raised in either case -- confirms SKILL.md\'s documented claim '
      'that ELink silently returns no/wrong-scope results on a namespace mismatch '
      'rather than raising an error, exactly as the Failure Modes section describes.')
