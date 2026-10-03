"""Re-check of the batch_symbols per-symbol error text (full message)."""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'F:/OpenScience/wt/dbaccess-ensembl-rest/skills/bio-ensembl-rest/scripts')
import ensembl_client as c
for k, v in c.batch_symbols('human', ['BRCA1', 'MARCH1', 'NOTAGENE']).items():
    print(k, v.get('id') or v.get('error'))
