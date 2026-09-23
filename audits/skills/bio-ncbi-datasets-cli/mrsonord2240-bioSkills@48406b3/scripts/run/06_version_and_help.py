import subprocess

datasets = r"F:\OpenScience\audit-envs\database-access\tools\ncbi-datasets-cli\datasets.exe"
dataformat = r"F:\OpenScience\audit-envs\database-access\tools\ncbi-datasets-cli\dataformat.exe"
version = subprocess.run([datasets, "--version"], capture_output=True, text=True, check=True).stdout.strip()
help_text = subprocess.run([dataformat, "tsv", "genome", "--help"], capture_output=True, text=True, check=True).stdout
assert "18.37.0" in version, version
for field in ("assminfo-level", "assmstats-scaffold-n50", "assmstats-contig-n50"):
    assert field in help_text, field
print("VERSION_AND_FIELD_CATALOG=PASS " + version)
