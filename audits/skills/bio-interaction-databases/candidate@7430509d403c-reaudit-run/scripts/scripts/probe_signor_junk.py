import sys, warnings
sys.dont_write_bytecode = True
sys.path.insert(0, 'F:/OpenScience/wt/dbaccess-interaction-databases/skills/bio-interaction-databases/scripts')
import interaction_clients as ic
class R:
    def __init__(self, t): self.text = t
for junk in ['No result found.', 'Service temporarily unavailable', '<html><body>502</body></html>']:
    ic._get = lambda *a, _j=junk, **k: R(_j)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        df = ic.signor_for_gene('TP53', uniprot='P04637')
    print(repr(junk), '-> rows', len(df), 'warnings', len(w))
