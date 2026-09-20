import json
with open('result.json') as f:
    report = json.load(f)
lddt_per_column = report['scores']          # NOT 'per_column_lddt' (that key does not exist; .get returns None)
assert len(lddt_per_column) == len(report['entries'][0]['aa'])   # one value per MSA column

print("SNIPPET OK", len(lddt_per_column))
