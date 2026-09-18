# Input 3 (Edge, regression of pre-fix Input 3)
# Assembled from SKILL.md fenced blocks: block_1 (discovery) + block_8 (discover
# attributes/filters programmatically). Also re-checks the root cause the pre-fix
# audit found: is 'ensembl_gene_id' absent from ds.filters (the client-side gap
# SKILL.md now documents), and is 'gene_biotype' present / 'biotype' absent as an
# *attribute* (the P1 fix)?
exec(open('block_1.txt', encoding='utf-8').read())
exec(open('block_8.txt', encoding='utf-8').read())

print()
print('ensembl_gene_id in ds.filters:', 'ensembl_gene_id' in ds.filters)
print('external_gene_name in ds.filters:', 'external_gene_name' in ds.filters)
print('gene_biotype in ds.attributes:', 'gene_biotype' in ds.attributes)
print('biotype in ds.attributes:', 'biotype' in ds.attributes)
print('biotype in ds.filters:', 'biotype' in ds.filters)

assert 'ensembl_gene_id' not in ds.filters, 'client-side gap SKILL.md documents no longer reproduces -- check if pybiomart version changed'
assert 'gene_biotype' in ds.attributes, 'gene_biotype attribute missing'
assert 'biotype' not in ds.attributes, 'biotype unexpectedly present as an attribute'
assert 'biotype' in ds.filters, 'biotype filter missing'
print('\nOK: SKILL.md Version Compatibility claims confirmed live against current pybiomart/Ensembl state.')
