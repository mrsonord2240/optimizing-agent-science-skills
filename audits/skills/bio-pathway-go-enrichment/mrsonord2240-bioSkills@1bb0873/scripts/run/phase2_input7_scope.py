#!/usr/bin/env python3
"""Static source/scope checks for Phase 2 input 7; no source files are modified."""
from pathlib import Path

skill = Path('/mnt/openscience/wt/pathway-go-enrichment/pathway-analysis/go-enrichment/SKILL.md')
guide = skill.with_name('usage-guide.md')
examples = skill.parent / 'examples'
text = skill.read_text(encoding='utf-8')
guide_text = guide.read_text(encoding='utf-8')
goseq_fence = next(block for block in text.split('```r') if "required <- c('goseq'" in block).split('```', 1)[0]

checks = {
    'frontmatter_name': text.startswith('---\nname: bio-pathway-go-enrichment\n'),
    'explicit_universe': 'universe      = universe_ids' in text,
    'explicit_bp': "ont           = 'BP'" in text,
    'no_implicit_hg38_goseq': "nullp(de_genes, 'hg38', 'ensGene')" not in goseq_fence,
    'local_goseq_route': 'TxDb.Hsapiens.UCSC.hg38.knownGene' in text and 'gene2cat = gene2cat' in text,
    'references_present': text.count('\n- ') >= 9,
    'scope_routes_gsea': '-> gsea' in text,
    'usage_guide_present': guide.exists() and 'BiocManager::install(version = \'3.20\'' in guide_text,
    'examples_present': (examples / 'go_enrichment_basic.R').exists() and (examples / 'go_all_ontologies.R').exists(),
    'no_medical_diagnosis': 'diagnose' not in text.lower() and 'prescribe' not in text.lower(),
}
for name, passed in checks.items():
    print(f'{name}={passed}')
if not all(checks.values()):
    raise SystemExit('INPUT7_FAIL')
print('INPUT7_OK static_checks=', len(checks))
