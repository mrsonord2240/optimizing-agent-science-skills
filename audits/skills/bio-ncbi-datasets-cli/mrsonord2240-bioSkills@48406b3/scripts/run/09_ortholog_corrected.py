import json
import subprocess

datasets = r"F:\OpenScience\audit-envs\database-access\tools\ncbi-datasets-cli\datasets.exe"
result = subprocess.run([datasets, "summary", "gene", "symbol", "BRCA1", "--ortholog", "Mammalia", "--as-json-lines"], capture_output=True, text=True, check=True)
rows = [json.loads(line) for line in result.stdout.splitlines() if line]
assert len(rows) > 100, len(rows)
assert any(row.get("symbol") == "BRCA1" for row in rows)
assert len({row.get("tax_id") for row in rows}) > 100
print(f"ORTHOLOG_MAMMALIA=PASS records={len(rows)}")
