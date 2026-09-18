'''Input 2 (Variant A) -- generalization check on the DbInfo[0] fix, regression.
Prompt: "List the searchable fields for the taxonomy and assembly databases, and tell me
when each was last updated."
Uses SKILL.md block 10 (list_fields), extracted programmatically from the shipped SKILL.md.
'''
from Bio import Entrez
import time

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

exec(open('skill_block_10.py', encoding='utf-8').read())
# defines list_fields(db) -> returns r['DbInfo'][0]['FieldList'] entries

for db in ['taxonomy', 'assembly']:
    fields = list_fields(db)
    print(f'=== {db} ===')
    print(f'Field count: {len(fields)}')
    print('First 5:', fields[:5])
    assert len(fields) > 0, f'expected nonempty field list for {db}'
    time.sleep(DELAY)

for db in ['structure', 'biosample']:
    h = Entrez.einfo(db=db)
    r = Entrez.read(h); h.close()
    shape = type(r['DbInfo']).__name__
    print(f'{db}: DbInfo type = {shape}, len = {len(r["DbInfo"])}')
    assert isinstance(r['DbInfo'], list), 'expected list-of-one shape'
    assert len(r['DbInfo']) == 1
    info = r['DbInfo'][0]
    print(f'  DbName={info["DbName"]}  Count={info["Count"]}  LastUpdate={info["LastUpdate"]}')
    time.sleep(DELAY)

print('ASSERT OK: DbInfo[0] fix generalizes across 4 additional databases')
