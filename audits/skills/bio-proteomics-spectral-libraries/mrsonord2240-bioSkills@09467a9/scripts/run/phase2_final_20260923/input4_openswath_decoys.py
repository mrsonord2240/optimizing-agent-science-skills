"""Fresh OpenSWATH TSV build, TraML conversion, and pseudo-reverse reproducibility check."""
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

run = Path(__file__).resolve().parent
root = Path(r"F:\OpenScience\wt\proteomics-spectral-libraries\proteomics\spectral-libraries")
openms = Path(r"F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\tools\openms\bin")
peptides = run / "input4_peptides.tsv"
library = run / "input4_library.tsv"
traml = run / "input4_library.TraML"
decoys = [run / f"input4_decoy_{i}.TraML" for i in range(3)]
with peptides.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["sequence", "charge", "protein", "irt"], delimiter="\t")
    writer.writeheader()
    writer.writerows([{"sequence": "LGGNEQVTR", "charge": 2, "protein": "P1", "irt": -24.92},
                      {"sequence": "LGGNEQVTR", "charge": 3, "protein": "P1", "irt": -24.92},
                      {"sequence": "VEATFGVDESNAK", "charge": 2, "protein": "P2", "irt": 12.39},
                      {"sequence": "YILAGVENSK", "charge": 2, "protein": "P3", "irt": 19.79}])
subprocess.run([sys.executable, str(root / "scripts" / "build_openswath_tsv.py"), "--peptides", str(peptides), "--out", str(library), "--n-frag", "4"], check=True)
rows = list(csv.DictReader(library.open(encoding="utf-8"), delimiter="\t"))
assert len(rows) == 16
assert {r["transition_group_id"] for r in rows} == {"LGGNEQVTR_2", "LGGNEQVTR_3", "VEATFGVDESNAK_2", "YILAGVENSK_2"}
assert all(r["Annotation"].startswith("y") for r in rows)
subprocess.run([str(openms / "TargetedFileConverter.exe"), "-in", str(library), "-in_type", "tsv", "-out", str(traml), "-out_type", "TraML"], check=True)
text = traml.read_text(encoding="utf-8")
targets = text.count("<Peptide ")
assert targets == 4, targets
hashes = []
for output in decoys:
    subprocess.run([str(openms / "OpenSwathDecoyGenerator.exe"), "-in", str(traml), "-out", str(output), "-method", "pseudo-reverse"], check=True)
    hashes.append(hashlib.sha256(output.read_bytes()).hexdigest())
assert len(set(hashes)) == 1, hashes
decoy_count = decoys[0].read_text(encoding="utf-8").count("<Peptide ") - targets
assert decoy_count == targets, (targets, decoy_count)
print(json.dumps({"transitions": len(rows), "target_peptides": targets, "decoy_peptides": decoy_count, "pseudo_reverse_sha256": hashes[0]}))
