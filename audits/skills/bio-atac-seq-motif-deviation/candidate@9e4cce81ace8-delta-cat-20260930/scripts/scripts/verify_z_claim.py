"""Re-verify the SKILL.md claim 'between GM12878 and K562 the top motifs reached |z| of about 7 per sample'
against the prior re-audit bulk runs (reaudit-run/bulk_A and bulk_B, shipped script unmodified).
Also checks the run's script is byte-identical to the candidate script."""
import csv
import hashlib
import sys

PRIOR = "F:/OpenScience/audits/bio-atac-seq-motif-deviation/reaudit-run"
CAND = "F:/OpenScience/wt/atac-motif-deviation/skills/bio-atac-seq-motif-deviation"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


import glob
for s in glob.glob(CAND + "/scripts/*"):
    print("candidate script", s.split("/")[-1], sha(s))
print("bulk_A s.R", sha(PRIOR + "/bulk_A/s.R"))

for run in ("bulk_A", "bulk_B"):
    rows = list(csv.reader(open(f"{PRIOR}/{run}/chromvar_deviations.csv", encoding="utf-8")))
    hdr, body = rows[0], rows[1:]
    vals = []
    for r in body:
        for j, v in enumerate(r[1:], 1):
            try:
                vals.append((abs(float(v)), float(v), r[0], hdr[j]))
            except ValueError:
                pass
    vals.sort(reverse=True)
    print(f"{run}: header={hdr[:3]}... motifs={len(body)} samples={len(hdr) - 1} values={len(vals)}")
    print(f"{run}: max|z|={vals[0][0]:.3f} ({vals[0][2]} {vals[0][3]}); n|z|>9={sum(v[0] > 9 for v in vals)}; "
          f"n|z|>7={sum(v[0] > 7 for v in vals)}; n|z|>6={sum(v[0] > 6 for v in vals)}")
    for v in vals[:8]:
        print(f"   {v[1]:+.3f} {v[2]} {v[3]}")
    # per-sample max
    for j, s in enumerate(hdr[1:], 1):
        m = max(abs(float(r[j])) for r in body if r[j] not in ("", "NA"))
        print(f"   sample {s}: max|z|={m:.3f}")
    d = list(csv.DictReader(open(f"{PRIOR}/{run}/chromvar_differential.csv", encoding="utf-8")))
    lfc = max(abs(float(r["logFC"])) for r in d)
    print(f"{run}: differential max|logFC|={lfc:.3f}")
sys.exit(0)
