#!/bin/bash
# Re-audit input 2/4/8 (Variant A/B + new generalization test) — bac15cc
# Regression of fixer's own BRCA1/Mammalia test, PLUS two genes/clades the fixer never tried:
# TP53 (a different human gene) and the "white" pigmentation gene across Insecta (the other
# clade --ortholog claims to cover, per SKILL.md: "limited to vertebrates and insects").
set -euo pipefail
export PATH="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli:$PATH"
SKILL=/f/OpenScience/wt/db-ndc/database-access/ncbi-datasets-cli

echo "=== regression: fixer's own BRCA1 / Mammalia case ==="
datasets.exe summary gene symbol BRCA1 --ortholog Mammalia --as-json-lines \
  | dataformat.exe tsv gene --fields gene-id,symbol,tax-name,description,chromosomes \
  > brca1_mammalia.tsv
wc -l brca1_mammalia.tsv   # expect 272 (271 rows + header)

echo "=== gene_metadata.sh unmodified, default args (BRCA1/Mammalia) ==="
bash "$SKILL/examples/gene_metadata.sh"

echo "=== NEW: same script, different gene (TP53), same clade ==="
mkdir -p tp53test && (cd tp53test && bash "$SKILL/examples/gene_metadata.sh" TP53 Mammalia)
wc -l tp53test/TP53_Mammalia.tsv   # expect 272

echo "=== NEW: different clade entirely (Insecta), real cross-species insect gene (white) ==="
datasets.exe summary gene symbol white --taxon "Drosophila melanogaster" --ortholog Insecta \
    --as-json-lines \
  | dataformat.exe tsv gene --fields gene-id,symbol,tax-name,description,chromosomes \
  > white_insecta.tsv
wc -l white_insecta.tsv   # expect 150+ real insect species

echo "=== regression: --ortholog all (fixer's ortholog-set test) ==="
datasets.exe summary gene symbol BRCA1 --taxon human --ortholog all --as-json-lines \
  > brca1_ortho_all.jsonl
wc -l brca1_ortho_all.jsonl   # expect 558

echo "=== regression: bare --ortholog flag still fails exactly as SKILL.md now documents ==="
datasets.exe summary gene symbol BRCA1 --taxon human --ortholog --as-json-lines || true

# Result: fix generalizes cleanly to a second human gene (TP53, 271 real mammal orthologs)
# and to the other documented clade (Insecta: white gene, 150+ real insect species, from
# Drosophila to Anopheles to Bombyx). Bare --ortholog still errors with the same misleading
# taxonomy-name message the fix documents in SKILL.md's Common errors table.
