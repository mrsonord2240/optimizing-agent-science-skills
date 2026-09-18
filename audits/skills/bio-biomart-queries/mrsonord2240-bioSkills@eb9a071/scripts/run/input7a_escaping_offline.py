"""Input 7a (Adversarial, offline) -- is the hand-built XML safe for a filter value that
needs XML escaping? A user could paste a gene list containing '&', '<', '>' or '"' by
copy-paste accident (e.g. from an HTML table). query_raw() builds the XML with
ElementTree.set() + ElementTree.tostring(), which auto-escapes attribute values -- confirm
that holds, and that the resulting query is still well-formed XML the server could parse.

No network needed: captures the exact bytes query_raw() would send via a FakeDataset.
"""
from xml.etree import ElementTree
from types import SimpleNamespace

ns = {}
exec(open('block_2.txt', encoding='utf-8').read(), ns)
query_raw = ns['query_raw']

captured = {}


class CapturingDataset:
    name = 'hsapiens_gene_ensembl'

    def get(self, query):
        captured['query_bytes'] = query
        # Return a minimal valid TSV so query_raw() doesn't raise on the response side --
        # we're only checking the outgoing XML here.
        return SimpleNamespace(text='Gene stable ID\tGene name\nENSG00000141510\tTP53\n')


nasty_values = ['TP53 & BRCA1', 'A<B>C', 'quote"inside', "apostrophe's-name"]
ds = CapturingDataset()
df = query_raw(ds, attributes=['ensembl_gene_id'], filters={'external_gene_name': nasty_values})

raw = captured['query_bytes']
print('Raw outgoing query bytes:')
print(raw.decode() if isinstance(raw, bytes) else raw)

# The critical check: is the outgoing XML well-formed? If ElementTree.tostring() failed to
# escape correctly, this parse would raise ParseError.
parsed = ElementTree.fromstring(raw)
filter_el = parsed.find('.//Filter')
print('\nParsed back Filter value attribute:', repr(filter_el.get('value')))

assert filter_el.get('value') == ','.join(nasty_values), 'round-trip value mismatch'
print('\nOK: special characters (&, <, >, \") round-trip safely through ElementTree escaping; XML is well-formed.')
