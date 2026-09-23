"""Probe whether the shipped meta-analysis rejects unequal gene universes."""
from pathlib import Path
import shutil
import subprocess
import sys

RUN = Path(__file__).resolve().parent
SKILL = Path(r"F:\OpenScience\wt\crispr-screens-in-vivo-screens\crispr-screens\in-vivo-screens\examples\per_animal_meta_analysis.py")
CASE = RUN / "mismatched_animals"
CASE.mkdir(exist_ok=True)
for n in range(1, 7):
    source = RUN / f"animal_{n}.gene_summary.txt"
    target = CASE / source.name
    if n == 6:
        lines = source.read_text(encoding="utf-8").splitlines()
        target.write_text("\n".join([lines[0]] + [line for line in lines[1:] if not line.startswith("Gene010\t")]) + "\n", encoding="utf-8")
    else:
        shutil.copyfile(source, target)
completed = subprocess.run([sys.executable, str(SKILL)], cwd=CASE, text=True, capture_output=True, check=True)
(CASE / "stdout.log").write_text(completed.stdout, encoding="utf-8")
all_rows = (CASE / "in_vivo_meta_all.tsv").read_text(encoding="utf-8").splitlines()
header = all_rows[0].split("\t")
gene010 = next(row.split("\t") for row in all_rows[1:] if row.startswith("Gene010\t"))
animals = gene010[header.index("n_animals")]
assert animals == "5.0", f"expected the malformed case to expose five rows, observed {animals}"
print("mismatched_universe_accepted=true; Gene010_n_animals=" + animals)
