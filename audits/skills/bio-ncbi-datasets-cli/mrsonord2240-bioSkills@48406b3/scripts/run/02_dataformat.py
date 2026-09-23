import subprocess

datasets = r"F:\OpenScience\audit-envs\database-access\tools\ncbi-datasets-cli\datasets.exe"
dataformat = r"F:\OpenScience\audit-envs\database-access\tools\ncbi-datasets-cli\dataformat.exe"
raw = subprocess.run([datasets, "summary", "genome", "accession", "GCF_000005845.2", "--as-json-lines"], capture_output=True, text=True, check=True)
formatted = subprocess.run([dataformat, "tsv", "genome", "--fields", "accession,organism-name,assminfo-level,assmstats-contig-n50"], input=raw.stdout, capture_output=True, text=True, check=True)
lines = formatted.stdout.strip().splitlines()
assert len(lines) == 2, lines
assert lines[0].split("\t") == ["Assembly Accession", "Organism Name", "Assembly Level", "Contig N50"], lines[0]
assert lines[1].startswith("GCF_000005845.2\t"), lines[1]
print("DATAFORMAT=PASS fields=current-18.37.0")
