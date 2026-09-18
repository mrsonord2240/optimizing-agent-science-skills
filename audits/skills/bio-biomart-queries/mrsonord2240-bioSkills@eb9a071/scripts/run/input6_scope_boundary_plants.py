"""Input 6 (Scope Boundary) -- SKILL.md's tool-listing bullet (added/kept in this fix, per
the fix log's "Redundancy pass" note) claims: "Non-vertebrate species: swap the host for the
Ensembl Genomes BioMart, e.g. Server(host='http://plants.ensembl.org')". This is presented
as supported but sits right at the edge of the Skill's Ensembl-vertebrate-gene-mart-centric
examples (every other pattern in SKILL.md hardcodes hsapiens_gene_ensembl). Does the same
query_raw() helper actually work, unmodified, against a different BioMart host and a real
plant gene, or does the claim not hold up?
"""
exec(open('block_2.txt', encoding='utf-8').read())

from pybiomart import Server

print('=== Discover plants.ensembl.org marts/datasets ===')
plant_server = Server(host='http://plants.ensembl.org')
print('Marts:', list(plant_server.marts.keys()))
plant_mart = plant_server[list(plant_server.marts.keys())[0]]
print('First mart datasets (first 10):', list(plant_mart.datasets.keys())[:10])

# Arabidopsis thaliana is the standard plant reference genome; its Ensembl Plants dataset
# is conventionally named athaliana_eg_gene.
candidates = [d for d in plant_mart.datasets if 'athaliana' in d.lower()]
print('Arabidopsis-matching dataset(s):', candidates)
assert candidates, 'No Arabidopsis dataset found in Ensembl Plants BioMart -- cannot test this claim'
plant_ds = plant_mart[candidates[0]]

print(f'\n=== Query {candidates[0]} via query_raw() (same helper, no modification) ===')
df = query_raw(plant_ds,
    attributes=['ensembl_gene_id', 'chromosome_name', 'start_position', 'end_position'],
    filters={'chromosome_name': '1'},
)
print(f'OK: {len(df)} chr1 Arabidopsis gene rows returned via the unmodified query_raw() helper')
print(df.head(5).to_string(index=False))
assert len(df) > 0, 'Ensembl Plants query returned zero rows'
