# Input 3 (Edge): "My collaborator sent GRCh37 coordinates (rs334 = 11-5248232-T-A) and a chrX gene (DMD). Is the
# variant absent from gnomAD, and what is DMD's LOF constraint?" Build/version edge cases. Live gnomAD GraphQL.
import json, sys, time
sys.path.insert(0, '..')
import requests
from skill_code import query_variant, grpmax_faf95, apply_bs1_ba1, query_gene_constraint, GNOMAD_API

for ds in ('gnomad_r4', 'gnomad_r2_1'):
    p = query_variant('11', 5248232, 'T', 'A', dataset=ds)
    print(f'query_variant(GRCh37 coords, dataset={ds}) ->', 'None' if p is None else {k: (p.get(k) or {}).get('af') for k in ('exome', 'genome')})
    print('   grpmax_faf95 ->', grpmax_faf95(p), '-> apply_bs1_ba1 ->', apply_bs1_ba1(grpmax_faf95(p)['faf95'], 1e-4))
    time.sleep(0.5)
raw = requests.post(GNOMAD_API, json={'query': '{ variant(variantId: "11-5248232-T-A", dataset: gnomad_r4) { variant_id } }'}, timeout=30).json()
print('raw r4 response for GRCh37 id:', json.dumps(raw)[:300])
time.sleep(0.5)
for gsym in ('DMD', 'SCN2A'):
    g = query_gene_constraint(gsym)
    print(f'\nSKILL.md query_gene_constraint({gsym}) ->', json.dumps(g)[:500])
    time.sleep(0.5)
# does the gene constraint field exist for chrX in the default (GRCh38 -> v4) endpoint?
r = requests.post(GNOMAD_API, json={'query': '{ gene(gene_symbol: "DMD", reference_genome: GRCh38) { chrom gnomad_constraint { oe_lof_upper pli } } }'}, timeout=30).json()
print('\nraw DMD GRCh38 constraint:', json.dumps(r)[:300])
r = requests.post(GNOMAD_API, json={'query': '{ gene(gene_symbol: "DMD", reference_genome: GRCh37) { chrom gnomad_constraint { oe_lof_upper pli } } }'}, timeout=30).json()
print('raw DMD GRCh37 (v2) constraint:', json.dumps(r)[:300])
