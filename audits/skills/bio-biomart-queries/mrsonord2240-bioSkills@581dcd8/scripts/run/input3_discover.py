'''Input 3 (Edge): "Before I trust the field names, list the real attributes and filters
available on the human gene dataset so I don't hallucinate field names." -- SKILL.md
"Discover attributes / filters programmatically" pattern, run verbatim, plus an explicit
check of whether 'ensembl_gene_id' (used as a filter in two of the Skill's three code
patterns) is actually enumerated by ds.filters.'''
from pybiomart import Server

server = Server(host='http://www.ensembl.org')
mart = server['ENSEMBL_MART_ENSEMBL']
ds = mart['hsapiens_gene_ensembl']

attrs = ds.attributes
ortho_attrs = [a for a in attrs if 'homolog' in a]
print(f'{len(ortho_attrs)} ortholog attributes; first 5: {ortho_attrs[:5]}')

filts = ds.filters
chrom_filts = [f for f in filts if 'chrom' in f]
print(f'{len(chrom_filts)} chromosome-related filters: {chrom_filts}')

print(f'\nTotal filters enumerated by ds.filters: {len(filts)}')
print(f"Is 'ensembl_gene_id' in ds.filters? {'ensembl_gene_id' in filts}")
print(f"Is 'biotype' in ds.attributes (as an ATTRIBUTE, not filter)? {'biotype' in attrs}")
print(f"Is 'gene_biotype' in ds.attributes? {'gene_biotype' in attrs}")
