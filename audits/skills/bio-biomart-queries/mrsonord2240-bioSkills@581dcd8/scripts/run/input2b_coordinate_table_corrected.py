'''Input 2 continued: same request, with attribute name corrected from SKILL.md's "biotype"
to the real attribute "gene_biotype" (confirmed against live-cached attribute dump), to isolate
whether the rest of the documented pattern is otherwise sound.'''
from pybiomart import Server

server = Server(host='http://www.ensembl.org')
mart = server['ENSEMBL_MART_ENSEMBL']
ds = mart['hsapiens_gene_ensembl']

df = ds.query(
    attributes=['ensembl_gene_id', 'external_gene_name', 'chromosome_name',
                'start_position', 'end_position', 'strand', 'gene_biotype'],
    filters={'chromosome_name': '21', 'biotype': 'protein_coding'},
)
print(f'{len(df)} protein-coding genes on chr21')
print(df.head(10).to_string(index=False))
df.to_csv('input2_chr21_protein_coding.tsv', sep='\t', index=False)
