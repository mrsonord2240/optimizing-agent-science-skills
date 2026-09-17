'''Input 2 (Variant A): "Pull all protein-coding genes on chromosome 21 with coordinates
and biotype in one BioMart query." -- SKILL.md "Pull gene coordinate table for a chromosome"
pattern, run verbatim except chromosome 17 -> 21 (smaller chromosome, faster live query).'''
from pybiomart import Server

server = Server(host='http://www.ensembl.org')
mart = server['ENSEMBL_MART_ENSEMBL']
ds = mart['hsapiens_gene_ensembl']

df = ds.query(
    attributes=['ensembl_gene_id', 'external_gene_name', 'chromosome_name',
                'start_position', 'end_position', 'strand', 'biotype'],
    filters={'chromosome_name': '21', 'biotype': 'protein_coding'},
)
print(f'{len(df)} protein-coding genes on chr21')
print(df.head(10).to_string(index=False))
df.to_csv('input2_chr21_protein_coding.tsv', sep='\t', index=False)
