'''Input 8 (NEW -- not in the prior re-audit) -- verify the second fix pass's CURATED_DBS
disclosure claims independently, and run the documented widen-to-all-databases snippet across
the FULL live database list (not the fixer's spot-check of 2 of 38).

Prompt: "The Skill says CURATED_DBS only covers 10 of NCBI's 38 databases. Confirm that's still
true today, that all 10 curated names are real live databases, and that the one-line snippet it
gives for widening to all databases actually works across every database EInfo lists -- not just
a couple."

Claims under test (SKILL.md "Cross-database counts" section, fix commit 1b1dd1d):
  1. "EInfo currently lists 38 [databases]"
  2. CURATED_DBS (10 names) are all valid, real, live database names
  3. widen snippet: cross_db_counts(term, dbs=Entrez.read(Entrez.einfo())['DbList'])
     actually executes across the FULL db list without error and returns real counts
'''
import time
from Bio import Entrez

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34
CURATED_DBS = ['pubmed', 'pmc', 'nucleotide', 'protein', 'gene', 'sra', 'gds', 'bioproject', 'biosample', 'clinvar']


def cross_db_counts(term, dbs):
    counts = {}
    errors = {}
    for db in dbs:
        try:
            h = Entrez.esearch(db=db, term=term, retmax=0)
            r = Entrez.read(h); h.close()
            counts[db] = int(r['Count'])
        except Exception as e:
            errors[db] = f'{type(e).__name__}: {e}'
        time.sleep(DELAY)
    return counts, errors


print('=== Step 1: live EInfo full database list ===')
h = Entrez.einfo()
r = Entrez.read(h); h.close()
all_dbs = r['DbList']
print(f'Live EInfo database count: {len(all_dbs)}')
assert len(all_dbs) == 38, f'SKILL.md claims 38; live EInfo returned {len(all_dbs)}'
time.sleep(DELAY)

print('\n=== Step 2: are all 10 CURATED_DBS names real, live database names? ===')
not_curated_valid = [db for db in CURATED_DBS if db not in all_dbs]
print(f'CURATED_DBS entries NOT found in live EInfo list: {not_curated_valid}')
assert not not_curated_valid, f'CURATED_DBS contains invalid db names: {not_curated_valid}'
print(f'All {len(CURATED_DBS)} CURATED_DBS names confirmed valid live databases.')
print(f'CURATED_DBS covers {len(CURATED_DBS)}/{len(all_dbs)} = {100*len(CURATED_DBS)/len(all_dbs):.1f}% of live databases')
assert len(CURATED_DBS) == 10 and len(all_dbs) - len(CURATED_DBS) >= 20, \
    'SKILL.md disclosure text (10 of 38) should still roughly hold'

print('\n=== Step 3: run the documented widen-to-all-databases snippet across ALL 38 (not 2) ===')
term = 'BRCA1'
t0 = time.time()
counts, errors = cross_db_counts(term, dbs=all_dbs)
elapsed = time.time() - t0
print(f'Widen snippet ran against {len(all_dbs)} databases in {elapsed:.1f}s')
print(f'Succeeded on {len(counts)}/{len(all_dbs)} databases; {len(errors)} raised an exception')
if errors:
    print('Databases that raised an exception:')
    for db, msg in errors.items():
        print(f'  {db}: {msg}')

nonzero = {db: c for db, c in counts.items() if c > 0}
print(f'\nNonzero-count databases ({len(nonzero)}): showing top 10 by count')
for db in sorted(nonzero, key=nonzero.get, reverse=True)[:10]:
    print(f'  {db:<20} {nonzero[db]:>12,}')

# The widen snippet is only genuinely "working" if it succeeds on (nearly) every database, not
# just the two the fixer spot-checked (pubmed, protein).
assert len(errors) == 0, f'widen snippet raised on {len(errors)} of {len(all_dbs)} databases: {errors}'
assert len(nonzero) >= 5, 'expected a real gene symbol to hit more than a handful of databases'
print('\nASSERT OK: widen-to-all-databases snippet ran clean across the FULL 38-database list, zero errors')
