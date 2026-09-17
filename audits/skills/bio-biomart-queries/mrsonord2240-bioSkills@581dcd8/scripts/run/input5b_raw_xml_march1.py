'''Input 5, raw-XML workaround: bypass pybiomart's broken high-level filter validation
(confirmed above) by building the martservice XML query directly -- to (a) confirm the
external_gene_name filter itself is valid server-side (isolating the defect to pybiomart's
client, not BioMart/Ensembl), and (b) test SKILL.md's own documented "Symbol-based filter
misses HGNC renames" failure mode for MARCH1 (renamed to MARCHF1 in 2020) against TP53 as a
working control.'''
import requests

XML_TMPL = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query virtualSchemaName="default" formatter="TSV" header="1" uniqueRows="1" datasetConfigVersion="0.6">
  <Dataset name="hsapiens_gene_ensembl" interface="default">
    <Filter name="external_gene_name" value="{genes}"/>
    <Attribute name="ensembl_gene_id"/>
    <Attribute name="external_gene_name"/>
  </Dataset>
</Query>'''

for label, genes in [('TP53 (control, current symbol)', 'TP53'),
                      ('MARCH1 (renamed to MARCHF1 in 2020)', 'MARCH1')]:
    xml = XML_TMPL.format(genes=genes)
    resp = requests.get('https://www.ensembl.org/biomart/martservice',
                         params={'query': xml}, timeout=40)
    body = resp.text.strip()
    print(f'--- {label} ---')
    print(f'HTTP {resp.status_code}, body: {body!r}')
