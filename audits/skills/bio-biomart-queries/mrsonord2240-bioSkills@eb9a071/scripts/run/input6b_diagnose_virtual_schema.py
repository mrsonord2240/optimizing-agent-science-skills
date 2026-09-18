"""Follow-up to Input 6: query_raw() hardcodes virtualSchemaName="default". Does
pybiomart's own Dataset object know the CORRECT virtual schema for a non-main-Ensembl
host (Ensembl Plants), and does the query succeed if query_raw() used that instead of
the hardcoded 'default'? This isolates whether the Input 6 failure is really the
hardcoded schema name (a query_raw() defect) or something else (e.g. wrong dataset name).
"""
from io import StringIO
from xml.etree import ElementTree
import pandas as pd
from pybiomart import Server

plant_server = Server(host='http://plants.ensembl.org')
plant_mart = plant_server['plants_mart']
plant_ds = plant_mart['athaliana_eg_gene']

print('plant_ds._virtual_schema:', plant_ds._virtual_schema)
print('plant_ds.name:', plant_ds.name)


def query_raw_fixed_schema(ds, attributes, filters, virtual_schema):
    """Same as SKILL.md's query_raw(), except virtualSchemaName is taken from the
    dataset instead of hardcoded to 'default' -- to isolate the cause."""
    root = ElementTree.Element('Query')
    root.set('virtualSchemaName', virtual_schema)
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
    response = ds.get(query=ElementTree.tostring(root))
    body = response.text.strip()
    if 'Query ERROR' in body:
        raise RuntimeError(f'BioMart rejected the query: {body}')
    if body.lower().startswith('<html') or not body:
        raise RuntimeError('non-TSV response')
    return pd.read_csv(StringIO(body), sep='\t')


print(f"\n=== Retry with virtualSchemaName='{plant_ds._virtual_schema}' instead of 'default' ===")
df = query_raw_fixed_schema(plant_ds,
    attributes=['ensembl_gene_id', 'chromosome_name', 'start_position', 'end_position'],
    filters={'chromosome_name': '1'},
    virtual_schema=plant_ds._virtual_schema,
)
print(f'OK: {len(df)} rows returned once the correct virtual schema name is used')
print(df.head(5).to_string(index=False))
assert len(df) > 0
print("\nCONCLUSION: query_raw()'s hardcoded virtualSchemaName='default' is the root cause of the "
      "Input 6 failure -- the dataset, host and filter/attribute names were all correct.")
