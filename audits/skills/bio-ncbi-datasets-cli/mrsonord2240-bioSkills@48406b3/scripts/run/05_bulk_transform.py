import subprocess
from pathlib import Path

source = Path(r"F:\OpenScience\wt\ncbi-datasets-cli\database-access\ncbi-datasets-cli\examples\bulk_dehydrated.sh").read_text()
assert '"\\n  out="$3' in source
fixture = Path(r"F:\OpenScience\audits\bio-ncbi-datasets-cli\data\fetch.txt")
fixture.write_text("https://example.test/a.fna\t0\tdata/A/a.fna\nhttps://example.test/b.gff\t0\tdata/B/b.gff\n")
awk = subprocess.run(["awk", "-F\\t", '{print $1"\\n  out="$3}', str(fixture)], capture_output=True, text=True, check=True)
assert "out=data/A/a.fna" in awk.stdout and "out=data/B/b.gff" in awk.stdout, awk.stdout
assert "out=0" not in awk.stdout, awk.stdout
print("BULK_FETCH_TRANSFORM=PASS uses-column-3")
