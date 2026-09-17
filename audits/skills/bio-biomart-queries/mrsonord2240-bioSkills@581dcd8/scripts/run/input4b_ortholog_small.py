'''Input 4 retry, smaller query: same ortholog wide-table pattern but restricted to 4 named
genes (external_gene_name filter) instead of the whole chr17, to see whether a lighter query
avoids the live "Service unavailable" outage page hit by the full chr17 version.'''
from pybiomart import Server

server = Server(host='http://www.ensembl.org')
mart = server['ENSEMBL_MART_ENSEMBL']
ds = mart['hsapiens_gene_ensembl']

df = ds.query(
    attributes=[
        'ensembl_gene_id', 'external_gene_name',
        'mmusculus_homolog_ensembl_gene', 'mmusculus_homolog_orthology_type',
        'drerio_homolog_ensembl_gene', 'drerio_homolog_orthology_type',
    ],
    filters={'external_gene_name': ['TP53', 'BRCA1', 'EGFR', 'MYC']},
)
print(f'rows: {len(df)}')
print(df.head(20).to_string(index=False))
looks_like_html = df.astype(str).apply(lambda col: col.str.contains('<html', case=False, na=False)).any().any()
print(f'response looks like an HTML outage page: {looks_like_html}')
