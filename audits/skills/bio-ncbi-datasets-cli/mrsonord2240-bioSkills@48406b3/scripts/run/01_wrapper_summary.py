import importlib.util
from pathlib import Path

source = Path(r"F:\OpenScience\wt\ncbi-datasets-cli\database-access\ncbi-datasets-cli\scripts\datasets_wrapper.py")
spec = importlib.util.spec_from_file_location("fresh_datasets_wrapper", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
rows = module.datasets_summary("genome", "accession", "GCF_000005845.2")
assert rows and rows[0]["accession"] == "GCF_000005845.2", rows[:1]
print(f"WRAPPER_SUMMARY=PASS records={len(rows)} accession={rows[0]['accession']}")
