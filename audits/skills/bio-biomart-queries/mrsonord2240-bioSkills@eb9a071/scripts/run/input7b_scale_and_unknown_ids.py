"""Input 7b (Adversarial, live) -- inputs a real user would realistically send that the
pre-fix and fixer's own verification never tried:
  1. A LONG ID list (500+ real Ensembl gene IDs) through query_raw() -- SKILL.md's own
     "Goal" text for Bulk ID mapping says "Convert 5,000 Ensembl Gene IDs"; query_raw()
     sends the whole built XML through ds.get(), which is pybiomart's ServerBase.get() --
     a plain HTTP GET with the XML in a query string parameter, not a POST body. Does
     that actually work at a scale approaching the Skill's own advertised use case, or
     does it hit a URL-length wall?
  2. One UNKNOWN/fake Ensembl ID mixed into a real filter list -- does the query silently
     drop it (correct) or error out?
  3. An EMPTY list value for a filter -- realistic if an agent forgets to check a list is
     non-empty before building the query.
"""
exec(open('setup_lite.txt', encoding='utf-8').read())
exec(open('block_2.txt', encoding='utf-8').read())

# --- 1. Long ID list: get ~600 real chr1 protein-coding gene IDs first, then bulk-map them ---
print('=== Step 1: fetch a real, long ID list (chr1 protein-coding genes) ===')
chr1_df = query_raw(ds, attributes=['ensembl_gene_id'],
                     filters={'chromosome_name': '1', 'biotype': 'protein_coding'})
long_ids = chr1_df.iloc[:, 0].tolist()
print(f'Got {len(long_ids)} real chr1 protein-coding gene IDs')

print('\n=== Step 2: bulk ID mapping with the FULL long list through query_raw()/ds.get() (GET) ===')
approx_url_len = sum(len(i) + 1 for i in long_ids)
print(f'Approx filter-value length alone: {approx_url_len} chars (excludes rest of XML + URL-encoding overhead)')
try:
    big_df = query_raw(ds, attributes=['ensembl_gene_id', 'external_gene_name', 'hgnc_id'],
                        filters={'ensembl_gene_id': long_ids})
    print(f'OK: long-ID-list query succeeded, {len(big_df)} rows returned for {len(long_ids)} input IDs')
    long_list_result = 'OK'
except Exception as e:
    print(f'FAILED: long-ID-list query raised {type(e).__name__}: {e}')
    long_list_result = f'{type(e).__name__}: {e}'

# --- 2. Unknown ID mixed with a real one ---
print('\n=== Step 3: unknown/fake Ensembl ID mixed with a real one ===')
mixed_ids = ['ENSG00000141510', 'ENSG99999999999']  # TP53 (real) + fabricated (fake)
try:
    mixed_df = query_raw(ds, attributes=['ensembl_gene_id', 'external_gene_name'],
                          filters={'ensembl_gene_id': mixed_ids})
    found_ids = set(mixed_df['Gene stable ID'])
    print(f'OK: {len(mixed_df)} rows; real ID found: {"ENSG00000141510" in found_ids}; '
          f'fake ID silently dropped (not errored): {"ENSG99999999999" not in found_ids}')
    unknown_id_result = 'silently dropped, no crash'
except Exception as e:
    print(f'FAILED: mixed real/fake ID query raised {type(e).__name__}: {e}')
    unknown_id_result = f'{type(e).__name__}: {e}'

# --- 3. Empty list filter value ---
print('\n=== Step 4: empty list as a filter value ===')
try:
    empty_df = query_raw(ds, attributes=['ensembl_gene_id', 'external_gene_name'],
                          filters={'ensembl_gene_id': []})
    print(f'OK (no exception): empty-list filter returned {len(empty_df)} rows, columns={list(empty_df.columns)}')
    empty_list_result = f'no exception, {len(empty_df)} rows'
except Exception as e:
    print(f'FAILED/raised: empty-list filter raised {type(e).__name__}: {e}')
    empty_list_result = f'{type(e).__name__}: {e}'

print('\n=== SUMMARY ===')
print('long_ids_count      :', len(long_ids))
print('long_list_result    :', long_list_result)
print('unknown_id_result   :', unknown_id_result)
print('empty_list_result   :', empty_list_result)
