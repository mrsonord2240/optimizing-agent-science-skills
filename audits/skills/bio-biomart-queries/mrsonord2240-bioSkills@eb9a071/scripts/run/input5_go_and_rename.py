# Input 5 (Stress, regression of pre-fix Input 5)
# Assembled from SKILL.md fenced blocks: setup_lite (server/mart/ds, see input2 comment) +
# block_2 (query_raw def) + block_6 (GO annotation pattern), with MARCH1 added to the gene
# list -- same HGNC-rename probe the pre-fix audit ran, to check the "Symbol-based filter
# misses HGNC renames" failure mode SKILL.md documents (MARCH1 -> MARCHF1 post-2020).
exec(open('setup_lite.txt', encoding='utf-8').read())
exec(open('block_2.txt', encoding='utf-8').read())

df = query_raw(ds,
    attributes=['ensembl_gene_id', 'external_gene_name',
                'go_id', 'name_1006', 'namespace_1003'],
    filters={'external_gene_name': ['TP53', 'BRCA1', 'MYC', 'EGFR', 'MARCH1']},
)
assert len(df) > 0, 'GO annotation query returned zero rows'
genes_found = set(df['Gene name'].unique())
print('OK:', len(df), 'GO rows; gene symbols present:', sorted(genes_found))
print('MARCH1 present (expected: NO, renamed to MARCHF1 post-2020):', 'MARCH1' in genes_found)
