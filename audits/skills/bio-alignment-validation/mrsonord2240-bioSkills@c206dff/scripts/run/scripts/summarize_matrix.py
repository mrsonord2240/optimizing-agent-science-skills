"""Build the tool x planted-defect detection table (markdown) from out/matrix.json + out/matrix_idx.json. Windows or WSL python."""
import json, os
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = json.load(open(f"{RUN}/out/matrix.json", encoding="utf-8"))
mi = {r["label"]: r for r in json.load(open(f"{RUN}/out/matrix_idx.json", encoding="utf-8"))}


def cell(det, crash=False):
    return "CRASH" if crash else ("flag" if det else "-")


rows = []
tot = {k: [0, 0] for k in ("quickcheck", "decode", "picard", "ci", "py")}
fp = {k: [] for k in tot}
for r in m:
    lab = r["label"]
    bad = r["expected_bad"]
    qc = r["quickcheck"]["rc"] != 0
    dc = r["decode"]["rc"] != 0
    pc = r["picard"]["rc"] != 0
    ci = r["ci_oneliner"]["rc"] != 0
    key = "planted:" + lab if r["kind"] == "planted" else None
    py_res = None
    if r["kind"] == "planted":
        py_res = mi.get("planted:" + lab)
    else:
        # match real by path fragment
        mp = {"human/test.paired_end.sorted.bam": "real:human_PE", "human/test.paired_end.name.sorted.bam": "real:human_PE_namesorted",
              "human/test.rna.paired_end.sorted.bam": "real:human_RNA", "human/test.paired_end.umi_unsorted.bam": "real:human_UMI_unsorted",
              "1000g/HG00349.chr20 slice": "real:1000g_chr20", "sarscov2/nanopore v5.3.2": "real:sars_nanopore",
              "sarscov2/test.paired_end.sorted.bam": "real:sars_PE", "sarscov2/test.single_end.sorted.bam": "real:sars_SE",
              "derived/planted_dups.bam": "real:planted_dups"}
        py_res = mi.get(mp.get(lab.replace("REAL ", "")))
    pyv = py_res["py"]["verdict"] if py_res else "?"
    py_rc = py_res["py"]["rc"] if py_res else None
    py_det = pyv.startswith("WARNINGS")
    py_crash = (py_rc not in (0, None)) and not py_det
    py_crash_reason = py_res["py"]["err_last"][:40] if py_crash else ""
    incidental = py_crash and "without index" in (py_res["py"]["err_last"] if py_res else "")  # unindexable file: crash is not a content finding
    vals = {"quickcheck": qc, "decode": dc, "picard": pc, "ci": ci, "py": py_det or (py_crash and not incidental)}
    for k, v in vals.items():
        if bad:
            tot[k][1] += 1
            tot[k][0] += 1 if v else 0
        elif v:
            fp[k].append(lab)
    rows.append((lab, bad, qc, dc, pc, ci, "warn" if py_det else ("CRASH: " + py_crash_reason if py_crash else "ok(silent)")))

out = ["| file | truth | quickcheck | full decode | Picard ValidateSamFile | SKILL CI one-liner | shipped py validator (indexed copy) |", "|---|---|---|---|---|---|---|"]
for lab, bad, qc, dc, pc, ci, py in rows:
    out.append(f"| {lab} | {'BAD' if bad else 'valid'} | {'flag' if qc else '-'} | {'flag' if dc else '-'} | {'flag' if pc else '-'} | {'flag' if ci else '-'} | {py} |")
out.append("")
out.append("Detection of the planted-BAD files (for the python validator: WARNINGS verdict or a content-related crash counts; the 'no index' crashes on unindexable files do not): ")
for k, (a, b) in tot.items():
    out.append(f"- {k}: {a}/{b}")
out.append("")
out.append("Flagged although expected VALID:")
for k, v in fp.items():
    out.append(f"- {k}: {v}")
open(f"{RUN}/out/matrix_summary.md", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
