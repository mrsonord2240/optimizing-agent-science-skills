from pathlib import Path
import csv
skill = Path(r'F:\OpenScience\wt\microbiome-amplicon-processing\microbiome\amplicon-processing\SKILL.md').read_text(encoding='utf-8')
truth = list(csv.DictReader(open(r'F:\OpenScience\audit-envs\microbiome-metagenomics-analyst\datagen\amplicon\truth.tsv', encoding='utf-8'), delimiter='\t'))
assert 'taxonomy-assignment' in skill
assert 'Do not substitute a flat relative-abundance cutoff' in skill
assert 'ASV is an exact sequence, not a cell, genome, or species' in skill
assert any(x['role'] == 'kit_contaminant' for x in truth)
print('SCOPE_ABUNDANCE_PASS taxonomy_routing=true abundance_shortcut_named=true')
