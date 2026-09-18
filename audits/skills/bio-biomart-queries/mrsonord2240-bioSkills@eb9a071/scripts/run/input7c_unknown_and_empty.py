"""Isolated retry of Input 7b's steps 3-4 (unknown ID mixed with real, and an empty-list
filter) on their own -- the first combined run hit these back-to-back with a 414 from the
long-ID-list step immediately before, so it's unclear whether the "non-TSV response" result
was genuine or a knock-on effect of hitting the server right after a rejected oversized
request. Isolating them with a fresh Dataset object and no preceding request should tell.
"""
exec(open('setup_lite.txt', encoding='utf-8').read())
exec(open('block_2.txt', encoding='utf-8').read())

print('=== Unknown/fake Ensembl ID mixed with a real one ===')
mixed_ids = ['ENSG00000141510', 'ENSG99999999999']  # TP53 (real) + fabricated (fake)
try:
    mixed_df = query_raw(ds, attributes=['ensembl_gene_id', 'external_gene_name'],
                          filters={'ensembl_gene_id': mixed_ids})
    found_ids = set(mixed_df['Gene stable ID'])
    print(f'OK: {len(mixed_df)} rows; columns={list(mixed_df.columns)}')
    print(mixed_df.to_string(index=False))
    print('real ID found:', 'ENSG00000141510' in found_ids)
    print('fake ID silently dropped (not errored):', 'ENSG99999999999' not in found_ids)
except Exception as e:
    print(f'FAILED: {type(e).__name__}: {e}')

print('\n=== Empty list as a filter value ===')
try:
    empty_df = query_raw(ds, attributes=['ensembl_gene_id', 'external_gene_name'],
                          filters={'ensembl_gene_id': []})
    print(f'OK (no exception): empty-list filter returned {len(empty_df)} rows, columns={list(empty_df.columns)}')
except Exception as e:
    print(f'FAILED/raised: {type(e).__name__}: {e}')
