#!/usr/bin/env python3
"""Fresh independent CODONML run against the fixed candidate parser."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

env = pathlib.Path("/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction")
candidate = pathlib.Path("/mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction")
source = pathlib.Path("/mnt/openscience/audits/bio-comparative-genomics-ancestral-reconstruction/reaudit-opt10-20260928/evidence/codon-paml")
out = pathlib.Path("/mnt/openscience/audits/bio-comparative-genomics-ancestral-reconstruction/final-reaudit-opt10-20260929/evidence/real-codon-paml")
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(candidate / "scripts"))
import codeml_asr

for name in ("alignment.phy", "tree.nwk"):
    shutil.copy2(source / name, out / name)
ctl = codeml_asr.write_codeml_ctl("alignment.phy", "tree.nwk", str(out), seqtype="codon")
proc = subprocess.run([str(env / "conda-env/bin/codeml"), pathlib.Path(ctl).name],
                      cwd=out, text=True, capture_output=True, timeout=300)
rst = out / "rst"
if proc.returncode != 0 or not rst.is_file():
    raise RuntimeError(f"CODONML failed: rc={proc.returncode}; stdout={proc.stdout}; stderr={proc.stderr}")
parsed = codeml_asr.parse_rst_posteriors(rst)
if len(parsed) != 7 or any(len(rows) != 110 for rows in parsed.values()):
    raise AssertionError("Expected 7 nodes x 110 sites from fresh CODONML rst")
for rows in parsed.values():
    for row in rows:
        if not 0 <= row["prob"] <= 1 or not 0 <= row["amino_acid_probability"] <= 1:
            raise AssertionError("Posterior outside [0,1]")
        if row["prob"] > row["amino_acid_probability"] + 0.002:
            raise AssertionError("Codon posterior exceeds amino-acid posterior")
result = {
    "status": "PASS_FRESH_CODONML_4_10_10",
    "returncode": proc.returncode,
    "stdout": proc.stdout,
    "stderr": proc.stderr,
    "rst_bytes": rst.stat().st_size,
    "rst_sha256": hashlib.sha256(rst.read_bytes()).hexdigest(),
    "alignment_sha256": hashlib.sha256((out / "alignment.phy").read_bytes()).hexdigest(),
    "tree_sha256": hashlib.sha256((out / "tree.nwk").read_bytes()).hexdigest(),
    "nodes": len(parsed),
    "sites_per_node": 110,
    "codon_probability_records": sum(map(len, parsed.values())),
    "Node10_sites_1_2": parsed[10][:2],
}
(out / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps({key: value for key, value in result.items() if key not in {"stdout", "stderr"}}, indent=2))
