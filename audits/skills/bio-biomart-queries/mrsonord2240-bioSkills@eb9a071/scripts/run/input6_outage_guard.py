"""Input 6 (Adversarial) -- does query_raw()'s outage-page guard actually fire?

This is the auditor's own input, not a regression of the pre-fix report. It does not depend
on live Ensembl: it monkeypatches Dataset.get() (the same method query_raw() calls) to return
canned Response objects that reproduce the exact failure modes documented in this env's
TOOLS.md (Notes #4): a 'Service unavailable' HTML page served as HTTP 200, an empty 200 body,
and a real 'Query ERROR' BioMart error body. If the guard is real, all three must raise
RuntimeError with the guard's own message instead of returning garbage. A fourth case (a
genuine TSV body) must NOT raise, to prove the guard doesn't also reject good data.

query_raw() is imported verbatim from the shipped SKILL.md (block_2.txt), not retyped.
"""
import sys
from types import SimpleNamespace

sys.path.insert(0, '.')
ns = {}
exec(open('block_2.txt', encoding='utf-8').read(), ns)
query_raw = ns['query_raw']


class FakeDataset:
    """Stand-in for a pybiomart Dataset -- only .name and .get() are used by query_raw()."""
    def __init__(self, canned_text):
        self.name = 'hsapiens_gene_ensembl'
        self._canned_text = canned_text

    def get(self, query):
        return SimpleNamespace(text=self._canned_text)


cases = {
    'outage_html_200': (
        '<html><head><title>Ensembl - Service unavailable</title></head>'
        '<body><h1>Sorry, Ensembl is currently unavailable</h1></body></html>'
    ),
    'empty_200': '',
    'whitespace_only_200': '   \n  \n',
    'query_error_body': (
        'Query ERROR: caught BioMart::Exception::Usage: Too many attributes selected '
        'for External References'
    ),
    'genuine_tsv': 'Gene stable ID\tGene name\nENSG00000141510\tTP53\n',
}

results = {}
for label, body in cases.items():
    ds = FakeDataset(body)
    try:
        df = query_raw(ds, attributes=['ensembl_gene_id'], filters={'ensembl_gene_id': ['X']})
        results[label] = f'NO EXCEPTION -- returned DataFrame shape {df.shape}'
    except RuntimeError as e:
        results[label] = f'RuntimeError: {e}'
    except Exception as e:
        results[label] = f'UNEXPECTED {type(e).__name__}: {e}'

for label, outcome in results.items():
    print(f'{label:20s} -> {outcome}')

# Assertions
assert results['outage_html_200'].startswith('RuntimeError'), 'HTML outage page was NOT caught'
assert results['empty_200'].startswith('RuntimeError'), 'empty body was NOT caught'
assert results['whitespace_only_200'].startswith('RuntimeError'), 'whitespace-only body was NOT caught'
assert results['query_error_body'].startswith('RuntimeError'), 'Query ERROR body was NOT caught'
assert results['genuine_tsv'].startswith('NO EXCEPTION'), 'guard incorrectly rejected valid TSV'
print('\nALL GUARD ASSERTIONS PASSED')
