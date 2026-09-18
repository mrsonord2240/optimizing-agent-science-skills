"""Diagnose exactly what body Ensembl is returning for the unknown-ID and empty-list
filter queries -- input7c's guard fired for both, but that could be a genuine live-outage
coincidence (this whole session has seen repeated intermittent 429/500/outage responses) OR
a real, reproducible BioMart behavior for these specific unusual queries. This calls
ds.get() directly (bypassing query_raw()'s guard) to print the raw response text/status.
"""
exec(open('setup_lite.txt', encoding='utf-8').read())
from xml.etree import ElementTree


def build_query(attributes, filters):
    root = ElementTree.Element('Query')
    root.set('virtualSchemaName', 'default')
    root.set('formatter', 'TSV')
    root.set('header', '1')
    root.set('uniqueRows', '1')
    root.set('datasetConfigVersion', '0.6')
    dataset_el = ElementTree.SubElement(root, 'Dataset')
    dataset_el.set('name', ds.name)
    dataset_el.set('interface', 'default')
    for name, value in filters.items():
        f = ElementTree.SubElement(dataset_el, 'Filter')
        f.set('name', name)
        f.set('value', ','.join(value) if isinstance(value, (list, tuple)) else str(value))
    for name in attributes:
        a = ElementTree.SubElement(dataset_el, 'Attribute')
        a.set('name', name)
    return ElementTree.tostring(root)


print('=== RAW: unknown/fake ID mixed with a real one ===')
q1 = build_query(['ensembl_gene_id', 'external_gene_name'],
                  {'ensembl_gene_id': ['ENSG00000141510', 'ENSG99999999999']})
r1 = ds.get(query=q1)
print('HTTP status:', r1.status_code)
print('Body repr (first 500 chars):', repr(r1.text[:500]))
print('Body length:', len(r1.text))

print('\n=== RAW: empty list as filter value ===')
q2 = build_query(['ensembl_gene_id', 'external_gene_name'], {'ensembl_gene_id': []})
r2 = ds.get(query=q2)
print('HTTP status:', r2.status_code)
print('Body repr (first 500 chars):', repr(r2.text[:500]))
print('Body length:', len(r2.text))

print('\n=== CONTROL: known-good 2-real-gene query for comparison ===')
q3 = build_query(['ensembl_gene_id', 'external_gene_name'],
                  {'ensembl_gene_id': ['ENSG00000141510', 'ENSG00000012048']})
r3 = ds.get(query=q3)
print('HTTP status:', r3.status_code)
print('Body repr (first 500 chars):', repr(r3.text[:500]))
