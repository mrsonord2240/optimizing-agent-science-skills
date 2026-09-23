import subprocess

datasets = r"F:\OpenScience\audit-envs\database-access\tools\ncbi-datasets-cli\datasets.exe"
result = subprocess.run([datasets, "summary", "genome", "accession", "GCF_999999999.1", "--as-json-lines"], capture_output=True, text=True)
assert result.returncode == 0, (result.returncode, result.stderr)
assert result.stdout.strip() == "", result.stdout
print("EMPTY_ACCESSION_GUARDRAIL=PASS exit=0 records=0")
