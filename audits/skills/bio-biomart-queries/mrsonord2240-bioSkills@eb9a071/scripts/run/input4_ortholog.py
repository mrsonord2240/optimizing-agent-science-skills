# Input 4 (Variant B, regression of pre-fix Input 4)
# Assembled from SKILL.md fenced blocks: setup_lite (server/mart/ds, see input2 comment) +
# block_2 (query_raw def) + block_5 (ortholog wide-table pattern).
exec(open('setup_lite.txt', encoding='utf-8').read())
exec(open('block_2.txt', encoding='utf-8').read())
exec(open('block_5.txt', encoding='utf-8').read())

assert len(df) > 0, 'ortholog query returned zero rows'
print('OK: chr17 ortholog rows =', len(df), '; 1:1 mouse+zebrafish rows =', len(df_one2one))
print(df_one2one.head(8).to_string(index=False))
