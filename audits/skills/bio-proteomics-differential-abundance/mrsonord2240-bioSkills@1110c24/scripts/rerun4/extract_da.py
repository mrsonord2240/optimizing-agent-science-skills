"""Write each fenced block of the differential-abundance SKILL.md to
rerun4/blocks/ verbatim."""
import os
import sys

sys.path.insert(0, r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4")
from extract import blocks  # noqa: E402

SKILL, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
names = {
    ("limma Workflow (R)", 0): "limma.R",
    ("Minimum-fold-change testing", 0): "treat.R",
    ("DEqMS Workflow (R)", 0): "deqms.R",
    ("proDA Workflow (R)", 0): "proda.R",
    ("msqrob2 Workflow (R) -- Peptide Table In, Protein Calls Out", 0): "msqrob2.R",
    ("msqrob2 Workflow (R) -- Peptide Table In, Protein Calls Out", 1): "msqrob_aggregate.R",
    ("MSstats Workflow (R) -- Feature-Level Mixed Model", 0): "msstats.R",
    ("Check the contrast is centred before reading any feature-level result", 0): "centring.R",
    ("Python Workflow", 0): "python_wf.py",
    ("Fold-Change Reporting", 0): "fc_report.R",
}
seen = {}
for h, lang, body in blocks(SKILL):
    k = seen.get(h, 0)
    seen[h] = k + 1
    fn = names.get((h, k))
    if fn is None:
        print(f"  (unmapped: {h} #{k})")
        continue
    p = os.path.join(OUT, fn)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    print(f"  wrote {fn}  ({len(body.splitlines())} lines, {lang})")
