# Input 4 (Edge) -- "Before I prefetch this new run, check whether it would exceed the
# default 20 GB prefetch limit, and tell me what flag to use if it would."
# Real accession found via ENA search (base_count>30e9, WGS, human) -- NOT downloaded,
# only its declared size is checked, per the Skill's own guidance: "query metadata first
# with pysradb metadata" for unknown-size runs.
from pysradb import SRAweb

ACC = "ERR10075183"
DEFAULT_MAX_SIZE_BYTES = 20 * 1024**3  # prefetch's default --max-size 20G

db = SRAweb()
meta = db.sra_metadata(ACC, detailed=True)
print(meta[['run_accession','run_total_bases','run_total_spots']].to_string(index=False))

# pysradb's detailed metadata does not surface a byte-size column directly (confirmed by
# the columns actually returned) -- cross-check against ENA portal API's fastq_bytes field,
# which IS what the Skill's own decision matters against (compressed download size).
import subprocess, json
out = subprocess.run(
    ["curl", "-s", f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={ACC}&result=read_run&fields=fastq_bytes&format=tsv"],
    capture_output=True, text=True
).stdout
print(out)
line = out.strip().split("\n")[-1]
bytes_list = [int(x) for x in line.split("\t")[1].split(";")]
total_bytes = sum(bytes_list)
print(f"{ACC}: total FASTQ bytes = {total_bytes:,} ({total_bytes/1024**3:.1f} GiB)")
print(f"Default prefetch --max-size = {DEFAULT_MAX_SIZE_BYTES:,} bytes (20 GiB)")
if total_bytes > DEFAULT_MAX_SIZE_BYTES:
    print("VERDICT: exceeds default --max-size 20G -- prefetch would SILENTLY SKIP this run.")
    print("Required flag: prefetch " + ACC + " --max-size 100G  (or larger; run is ~%.0fG)" % (total_bytes/1024**3))
else:
    print("VERDICT: within default 20G limit.")
