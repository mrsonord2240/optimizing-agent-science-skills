"""ID mapping to the reviewed-only target, and the client's own result shape."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, r'F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access\scripts')
import uniprot_client as uc
m = uc.map_ids(['ENSG00000141510', 'ENSG00000171862', 'ENSG00000139618'], to_db='UniProtKB-Swiss-Prot')
print('Swiss-Prot target rows:', [(r['from'], r['to'] if isinstance(r['to'], str) else r['to'].get('primaryAccession')) for r in m['results']], 'failedIds:', m.get('failedIds'))
m2 = uc.map_ids(['ENSG00000141510'], to_db='UniProtKB')
r0 = m2['results'][0]
print('to_db=UniProtKB result[0] keys / to type:', sorted(r0), type(r0['to']).__name__)
