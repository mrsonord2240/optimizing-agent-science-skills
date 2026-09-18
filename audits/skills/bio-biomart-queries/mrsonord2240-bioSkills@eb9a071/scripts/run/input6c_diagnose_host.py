"""Deeper diagnosis of the Input 6 plants BioMart failure: virtual_schema is genuinely
'default' per the server's own registry response, so that wasn't the cause. Check the
actual host/port/path pybiomart is sending the query to -- registry metadata for a mart
can point to a different host than the Server() was constructed with.
"""
from pybiomart import Server

plant_server = Server(host='http://plants.ensembl.org')
plant_mart = plant_server['plants_mart']
print('plant_mart.host:', plant_mart.host)
print('plant_mart.port:', plant_mart.port)
print('plant_mart.path:', plant_mart.path)
print('plant_mart.url:', plant_mart.url)

plant_ds = plant_mart['athaliana_eg_gene']
print('\nplant_ds.host:', plant_ds.host)
print('plant_ds.port:', plant_ds.port)
print('plant_ds.path:', plant_ds.path)
print('plant_ds.url:', plant_ds.url)
print('plant_ds._virtual_schema:', plant_ds._virtual_schema)

# What does pybiomart's OWN ds.query() do (the thing query_raw() is deliberately
# bypassing for the id_list bug) -- does the high-level path work for a simple,
# non-id_list filter on this same dataset/host?
print('\n=== Try pybiomart\'s own high-level ds.query() (bypasses nothing) ===')
try:
    df = plant_ds.query(attributes=['ensembl_gene_id'], filters={'chromosome_name': '1'})
    print('ds.query() SUCCEEDED:', len(df), 'rows')
    print(df.head(3).to_string(index=False))
except Exception as e:
    print(f'ds.query() FAILED: {type(e).__name__}: {e}')
