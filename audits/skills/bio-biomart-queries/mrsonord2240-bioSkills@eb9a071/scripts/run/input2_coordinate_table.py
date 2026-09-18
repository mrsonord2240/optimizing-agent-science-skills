# Input 2 (Variant A, regression of pre-fix Input 2)
# Assembled from SKILL.md fenced blocks: setup_lite (server/mart/ds construction lines,
# taken verbatim from the start of block_3 -- avoids re-fetching the full attribute/filter
# discovery dump on every run, which burns rate-limit budget for no reason on this input)
# + block_2 (query_raw def) + block_4 (coordinate-table pattern, chr17, attribute
# 'gene_biotype' -- pre-fix used the wrong name 'biotype' here and crashed).
exec(open('setup_lite.txt', encoding='utf-8').read())
exec(open('block_2.txt', encoding='utf-8').read())
exec(open('block_4.txt', encoding='utf-8').read())

assert len(df) > 0, 'coordinate table returned zero rows'
assert 'Gene type' in df.columns or 'gene_biotype' in df.columns, f'unexpected columns: {list(df.columns)}'
print('OK: chr17 coordinate table has', len(df), 'rows; columns:', list(df.columns))
print(df.head(5).to_string(index=False))
