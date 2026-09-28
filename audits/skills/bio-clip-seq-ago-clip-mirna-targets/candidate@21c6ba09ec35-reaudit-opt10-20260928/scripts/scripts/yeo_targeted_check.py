#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

TOOLING = Path("/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets")
SOURCE = TOOLING / "sources/chim-eCLIP"
SCRIPT = SOURCE / "bin/targeted_miR_umi.py"
CWL = SOURCE / "cwl/extract_r2_umi.cwl"

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    r1, r2, output = root / "r1.fq.gz", root / "r2.fq.gz", root / "out.fq"
    header = "@read1 description\n"
    with gzip.open(r1, "wt") as handle:
        handle.write(header + "ACGTACGTACGT\n+\nIIIIIIIIIIII\n")
    with gzip.open(r2, "wt") as handle:
        handle.write(header + "AACCGGTTAAZZ\n+\nIIIIIIIIIIII\n")
    result = subprocess.run(
        ["/usr/bin/python3", str(SCRIPT), "--read1", str(r1), "--read2", str(r2), "--output_file", str(output)],
        text=True, capture_output=True,
    )
    first_header = output.read_text(encoding="utf-8").splitlines()[0] if output.exists() else ""

cwl_text = CWL.read_text(encoding="utf-8")
script_text = SCRIPT.read_text(encoding="utf-8")
payload = {
    "source_commit": "75fe74e90e6e4ca670a5af76836d80db09bdbcb1",
    "script_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
    "cwl_sha256": hashlib.sha256(CWL.read_bytes()).hexdigest(),
    "script_default_umi_length_10": "default=10" in script_text,
    "cwl_prose_says_9nt": "first 9nt of R2" in cwl_text,
    "cwl_supplies_umi_length": "umi_length" in cwl_text,
    "live_returncode": result.returncode,
    "live_header": first_header,
    "live_prefix_length": len(first_header.split("_")[-1].split()[0]) if "_" in first_header else None,
    "conclusion": "Pinned targeted CWL prose says 9 nt, executable defaults to 10 nt, CWL does not override, and the live default extracts 10 nt.",
}
print(json.dumps(payload, indent=2, sort_keys=True))

