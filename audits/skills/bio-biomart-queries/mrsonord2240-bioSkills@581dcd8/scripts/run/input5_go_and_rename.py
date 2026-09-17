'''Input 5 (Stress/multi-part): "Get GO term annotations for TP53, BRCA1, MYC, EGFR, and also
MARCH1 (older gene symbol) -- flag if any symbol returns nothing." -- SKILL.md "GO term
annotation for a gene set" pattern, run verbatim (adds MARCH1 to test the Skill's own documented
"Symbol-based filter misses HGNC renames" failure mode).'''
from pybiomart import Server

server = Server(host='http://www.ensembl.org')
mart = server['ENSEMBL_MART_ENSEMBL']
ds = mart['hsapiens_gene_ensembl']

df = ds.query(
    attributes=['ensembl_gene_id', 'external_gene_name',
                'go_id', 'name_1006', 'namespace_1003'],
    filters={'external_gene_name': ['TP53', 'BRCA1', 'MYC', 'EGFR', 'MARCH1']},
)
print(f'rows: {len(df)}')
print(df.head(20).to_string(index=False))
