"""
Input 2 (Variant A) - "List the searchable fields for the ClinVar database, and tell me
when it was last updated and how many records it has."

Follows SKILL.md "Discover fields for a database" pattern (EInfo) and the decision-table
row "What searchable fields does db Y have?" -> EInfo.

SKILL.md's own code pattern is:
    def list_fields(db):
        h = Entrez.einfo(db=db); r = Entrez.read(h); h.close()
        return [(f['Name'], f['FullName'], f['Description']) for f in r['DbInfo']['FieldList']]

and examples/database_info.py's db_info() returns r['DbInfo'] and the caller does
info["DbName"] directly. Both index DbInfo as a dict. This run reproduces that first (per
SKILL.md's own "Version Compatibility" instruction to introspect on ImportError/
AttributeError/TypeError), then applies the corrected access.
"""
from Bio import Entrez

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'skill-auditor-bio-entrez-search'


def list_fields_as_documented(db):
    h = Entrez.einfo(db=db)
    r = Entrez.read(h)
    h.close()
    return r['DbInfo']  # as SKILL.md / examples/database_info.py index it


print('=== Step 1: EInfo call exactly as SKILL.md documents it ===')
db_info_raw = list_fields_as_documented('clinvar')
print(f'type(r["DbInfo"]) = {type(db_info_raw)}')
try:
    _ = db_info_raw['DbName']
    print('Direct dict-style access succeeded (unexpected given TOOLS.md note #2)')
except TypeError as e:
    print(f'FAILED as documented in TOOLS.md note #2: {type(e).__name__}: {e}')

print('\n=== Step 2: corrected access -- DbInfo is a list-of-one on Biopython 1.88 ===')
info = db_info_raw[0]
print(f'DbName: {info["DbName"]}')
print(f'Description: {info["Description"]}')
print(f'Count: {info["Count"]}')
print(f'LastUpdate: {info["LastUpdate"]}')
print(f'Field count: {len(info["FieldList"])}')
for field in info['FieldList'][:10]:
    print(f'  {field["Name"]:<20} {field["FullName"]:<30} {field["Description"][:60]}')

assert info['DbName'].lower() == 'clinvar'
assert int(info['Count']) > 0
assert len(info['FieldList']) > 0
print('\nASSERT OK (after correcting the indexing bug): DbName matches, Count>0, FieldList non-empty')
