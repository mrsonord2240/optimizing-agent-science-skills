"""Detection matrix: planted-defect fixtures (SYNTHETIC) + real public BAMs (valid) vs every integrity check the Skill
teaches: samtools quickcheck, full decode, Picard ValidateSamFile (legacy KEY=VALUE syntax as in SKILL.md), the SKILL's
CI one-liner, and the two shipped example validators.  Judged by OUTPUT content, and rc recorded separately.
Run in WSL: python matrix.py
"""
import json
import os
import re
import subprocess
import sys

RUN = "/mnt/openscience/audits/bio-alignment-validation/run"
PD = "/mnt/openscience/audit-envs/alignment-files/public-data"
DATA = f"{RUN}/data"
OUT = f"{RUN}/out"
PYV = f"{RUN}/skill/examples/validate_alignment.py"
SHV = f"{RUN}/skill/examples/validate_alignment.sh"
REF = f"{PD}/human/genome.fasta"

truth = json.load(open(f"{DATA}/fixtures.json"))

targets = []  # (label, path, expected_bad, ref, kind)
for k, v in sorted(truth.items()):
    targets.append((k, f"{DATA}/{k}", v["expected_bad"], REF, "planted"))
real = [
    ("REAL human/test.paired_end.sorted.bam", f"{PD}/human/test.paired_end.sorted.bam", REF),
    ("REAL human/test.paired_end.name.sorted.bam", f"{PD}/human/test.paired_end.name.sorted.bam", REF),
    ("REAL human/test.rna.paired_end.sorted.bam", f"{PD}/human/test.rna.paired_end.sorted.bam", REF),
    ("REAL human/test.paired_end.umi_unsorted.bam", f"{PD}/human/test.paired_end.umi_unsorted.bam", None),
    ("REAL 1000g/HG00349.chr20 slice", f"{PD}/1000g/HG00349.chr20_1400000-1500000.bam", None),
    ("REAL sarscov2/nanopore v5.3.2", f"{PD}/sarscov2/sars-cov-2_v5.3.2.nanopore.bam", f"{PD}/sarscov2/MN908947.3.fasta"),
    ("REAL sarscov2/test.paired_end.sorted.bam", f"{PD}/sarscov2/test.paired_end.sorted.bam", f"{PD}/sarscov2/genome.fasta"),
    ("REAL sarscov2/test.single_end.sorted.bam", f"{PD}/sarscov2/test.single_end.sorted.bam", f"{PD}/sarscov2/genome.fasta"),
    ("REAL derived/planted_dups.bam", f"{PD}/derived/planted_dups.bam", REF),
]
for lab, p, r in real:
    targets.append((lab, p, False, r, "real"))


def sh(cmd, timeout=180):
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or ""), (p.stderr or "")


def first(s, n=1, maxlen=110):
    ls = [l for l in s.strip().splitlines() if l.strip()]
    return " | ".join(l[:maxlen] for l in ls[:n])


rows = []
for label, path, bad, ref, kind in targets:
    row = {"label": label, "kind": kind, "expected_bad": bad}
    # A quickcheck
    rc, o, e = sh(f"samtools quickcheck -v '{path}'")
    row["quickcheck"] = {"rc": rc, "out": first(o + e)}
    rc, o, e = sh(f"samtools quickcheck -u -v '{path}'")
    row["quickcheck_u"] = {"rc": rc, "out": first(o + e)}
    # B full decode
    rc, o, e = sh(f"samtools view -c '{path}'")
    row["decode"] = {"rc": rc, "count": o.strip(), "err": first(e, 2)}
    # C Picard ValidateSamFile, legacy syntax exactly as SKILL.md
    rarg = f"R='{ref}'" if ref else ""
    rc, o, e = sh(f"picard ValidateSamFile I='{path}' MODE=SUMMARY {rarg} 2>&1")
    txt = o + e
    errs = re.findall(r"^(ERROR|WARNING):(\w+)\s+(\d+)", txt, re.M)
    row["picard"] = {"rc": rc, "found": [f"{a}:{b}={c}" for a, b, c in errs],
                     "verdict": ("No errors found" in txt), "tail": first("\n".join(l for l in txt.splitlines() if "Exception" in l or "ERROR" in l and "picard" not in l.lower()), 1)}
    # D Skill CI one-liner (verbatim logic), threshold 1000
    ci = f"test -s '{path}' && samtools quickcheck -v '{path}' && [ $(samtools view -c -F 2304 '{path}') -gt 1000 ] || {{ echo BAM_FAILED_INTEGRITY; exit 1; }}"
    rc, o, e = sh(ci)
    row["ci_oneliner"] = {"rc": rc, "out": first(o + e)}
    # E shipped python validator
    rc, o, e = sh(f"python '{PYV}' '{path}'")
    tail = [l for l in o.splitlines() if l.strip()]
    verdict = ""
    if "All metrics within normal range" in o:
        verdict = "ALL_OK"
    elif "WARNINGS:" in o:
        verdict = [l for l in tail if l.startswith("WARNINGS")][0]
    else:
        verdict = "NO_VERDICT"
    mapline = [l for l in tail if l.startswith("Mapped:")]
    row["py_validator"] = {"rc": rc, "verdict": verdict, "mapped_line": mapline[0] if mapline else "",
                           "stderr": first(e.replace("\r", ""), 1, 150)}
    # F shipped shell validator
    rc, o, e = sh(f"bash '{SHV}' '{path}'")
    row["sh_validator"] = {"rc": rc, "stderr_lines": len([l for l in e.splitlines() if l.strip()]),
                           "stderr": first(e, 1, 150), "mapping": first("\n".join(l for l in o.splitlines() if l.startswith("Mapped:")))}
    rows.append(row)
    print(label, "| qc", row["quickcheck"]["rc"], "| decode", row["decode"]["rc"], "| picard", row["picard"]["rc"], row["picard"]["found"][:3],
          "| ci", row["ci_oneliner"]["rc"], "| py", row["py_validator"]["rc"], row["py_validator"]["verdict"][:60], flush=True)

json.dump(rows, open(f"{OUT}/matrix.json", "w"), indent=1)
print("written", len(rows))
