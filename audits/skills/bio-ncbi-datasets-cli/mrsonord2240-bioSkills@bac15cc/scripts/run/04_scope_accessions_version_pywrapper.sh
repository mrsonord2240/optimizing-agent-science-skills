#!/bin/bash
# Re-audit inputs 6/7 (Scope Boundary + Adversarial, regression), dataformat version quirk
# regression, and the Python wrapper snake_case fix, checked against a live response. bac15cc.
set -euo pipefail
export PATH="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli:$PATH"

echo "=== regression: no SRA subcommand exists ==="
datasets.exe download --help | grep -i sra || echo "no SRA subcommand found (confirmed)"

echo "=== regression: nonexistent + malformed accessions ==="
datasets.exe summary genome accession GCF_999999999.1   # {"total_count": 0}, exit 0
datasets.exe summary genome accession NOT_AN_ACCESSION || true   # exit 1, clear error

echo "=== regression: dataformat version quirk ==="
dataformat.exe version   # still prints "undefined", exit 0 -- matches SKILL.md's documented note

echo "=== NEW: untested workflow -- virus download (SKILL.md's scope table names it, none of"
echo "    the original 7 inputs exercised it) ==="
datasets.exe download virus genome taxon "SARS-CoV-2" --refseq --filename sarscov2.zip --no-progressbar
unzip -l sarscov2.zip

echo "=== regression: Python wrapper snake_case field fix, live E. coli response ==="
datasets.exe summary genome taxon "Escherichia coli" --reference --as-json-lines > ecoli.jsonl
python -c "
import json
with open('ecoli.jsonl', encoding='utf-8') as f:
    genomes = [json.loads(l) for l in f if l.strip()]
print(f'{len(genomes)} reference E. coli assemblies')
for g in genomes[:3]:
    acc = g.get('accession')
    n50 = g.get('assembly_stats', {}).get('contig_n50')
    camel = g.get('assemblyStats', {}).get('contigN50')
    print(f'  {acc}  N50(snake_case)={n50}  N50(camelCase, should be None)={camel}')
"
# Result: snake_case resolves real N50 values; camelCase is None on both real records --
# confirms the fix (assembly_stats/contig_n50) is correct and the pre-fix bug was real.
