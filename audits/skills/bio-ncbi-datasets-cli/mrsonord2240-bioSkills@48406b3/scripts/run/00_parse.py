import ast
from pathlib import Path

source = Path(r"F:\OpenScience\wt\ncbi-datasets-cli\database-access\ncbi-datasets-cli")
ast.parse((source / "scripts" / "datasets_wrapper.py").read_text())
bulk = (source / "examples" / "bulk_dehydrated.sh").read_text()
assert "set -euo pipefail" in bulk
assert "awk -F'\\t'" in bulk and '"\\n  out="$3' in bulk
for reference in ("dehydrated-bulk.md", "gene-orthologs.md", "virus-genomes.md"):
    assert (source / "references" / reference).is_file()
print("PARSE_AND_LAYOUT=PASS")
