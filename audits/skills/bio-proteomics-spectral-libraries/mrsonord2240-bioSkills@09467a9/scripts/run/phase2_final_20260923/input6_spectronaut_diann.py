"""Fresh Spectronaut-to-DIA-NN conversion and out-of-range iRT rejection test."""
import csv
import json
import subprocess
import sys
from pathlib import Path

run = Path(__file__).resolve().parent
root = Path(r"F:\OpenScience\wt\proteomics-spectral-libraries\proteomics\spectral-libraries")
fields = ["ModifiedPeptide", "iRT", "RelativeIntensity", "FragmentMz", "FragmentNumber", "PrecursorMz", "PrecursorCharge", "FragmentCharge", "FragmentType", "Genes"]
valid, output, invalid, rejected = [run / x for x in ("input6_spectronaut.tsv", "input6_diann.tsv", "input6_bad_rt.tsv", "input6_bad.stderr")]
rows = [{"ModifiedPeptide": "LGGNEQVTR", "iRT": -24.92, "RelativeIntensity": 0.8, "FragmentMz": 500.2, "FragmentNumber": 4, "PrecursorMz": 487.3, "PrecursorCharge": 2, "FragmentCharge": 1, "FragmentType": "y", "Genes": "GENE1"},
        {"ModifiedPeptide": "VEATFGVDESNAK", "iRT": 12.39, "RelativeIntensity": 0.2, "FragmentMz": 620.3, "FragmentNumber": 5, "PrecursorMz": 682.8, "PrecursorCharge": 2, "FragmentCharge": 1, "FragmentType": "y", "Genes": "GENE2"}]
for path, payload in ((valid, rows), (invalid, [dict(rows[0], iRT=5000.0)])):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(payload)
subprocess.run([sys.executable, str(root / "scripts" / "spectronaut_to_diann.py"), "--in", str(valid), "--out", str(output)], check=True)
converted = list(csv.DictReader(output.open(encoding="utf-8"), delimiter="\t"))
assert len(converted) == 2 and "LibraryIntensity" in converted[0] and "ProductMz" in converted[0]
bad = subprocess.run([sys.executable, str(root / "scripts" / "spectronaut_to_diann.py"), "--in", str(invalid), "--out", str(run / "must_not_write.tsv")], capture_output=True, text=True)
rejected.write_text(bad.stderr, encoding="utf-8")
assert bad.returncode != 0 and "RT not in iRT units" in bad.stderr
assert not (run / "must_not_write.tsv").exists()
print(json.dumps({"converted_rows": len(converted), "renamed_columns": ["LibraryIntensity", "ProductMz", "FragmentSeriesNumber"], "bad_rt_returncode": bad.returncode, "bad_rt_rejected": True}))
