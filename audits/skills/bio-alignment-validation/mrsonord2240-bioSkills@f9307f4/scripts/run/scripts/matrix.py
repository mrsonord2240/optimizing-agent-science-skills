"""Regression + false-positive matrix for the FIXED Skill.
Every planted-defect file (SYNTHETIC, from make_fixtures.py) and every real public BAM is run through:
  quickcheck | full decode (samtools view -c) | Picard ValidateSamFile MODE=SUMMARY R=ref (Skill syntax) |
  the SKILL.md CI one-liner (verbatim, extracted from SKILL.md, default MIN_READS) |
  the shipped validate_alignment.py | the shipped validate_alignment.sh.
The validators are judged on (a) printed verdict vs exit code agreement (contract 0 pass/warn, 1 fail, 2 unreadable/empty),
(b) printed mapping rate vs an independent truth (samtools flagstat 'primary mapped'/'primary' and pysam until_eof).
Run in WSL: python matrix.py [outfile]
"""
import json
import os
import re
import subprocess
import sys
import pysam

RUN = "/mnt/openscience/audits/bio-alignment-validation/run"
PD = "/mnt/openscience/audit-envs/alignment-files/public-data"
DATA = f"{RUN}/data"
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{RUN}/out/matrix.json"
PYV = f"{RUN}/skill/examples/validate_alignment.py"
SHV = f"{RUN}/skill/examples/validate_alignment.sh"
REF = f"{PD}/human/genome.fasta"
CI = open(f"{RUN}/snip/SKILL_02_bash.txt", encoding="utf-8").read()

truth = json.load(open(f"{DATA}/fixtures.json"))
targets = [(k, f"{DATA}/{k}", v["expected_bad"], REF, "planted") for k, v in sorted(truth.items())]
real = [
    ("REAL human/PE.sorted", f"{PD}/human/test.paired_end.sorted.bam", REF),
    ("REAL human/PE.name.sorted", f"{PD}/human/test.paired_end.name.sorted.bam", REF),
    ("REAL human/RNA.PE.sorted", f"{PD}/human/test.rna.paired_end.sorted.bam", REF),
    ("REAL human/PE.umi_unsorted", f"{PD}/human/test.paired_end.umi_unsorted.bam", None),
    ("REAL 1000g/HG00349.chr20", f"{PD}/1000g/HG00349.chr20_1400000-1500000.bam", None),
    ("REAL sarscov2/nanopore", f"{PD}/sarscov2/sars-cov-2_v5.3.2.nanopore.bam", f"{PD}/sarscov2/MN908947.3.fasta"),
    ("REAL sarscov2/PE", f"{PD}/sarscov2/test.paired_end.sorted.bam", f"{PD}/sarscov2/genome.fasta"),
    ("REAL sarscov2/SE", f"{PD}/sarscov2/test.single_end.sorted.bam", f"{PD}/sarscov2/genome.fasta"),
    ("REAL derived/planted_dups", f"{PD}/derived/planted_dups.bam", REF),
]
targets += [(lab, p, False, r, "real") for lab, p, r in real]


def sh(cmd, timeout=300, env=None):
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout or "", p.stderr or ""


def first(s, n=1, maxlen=120):
    ls = [l for l in s.strip().splitlines() if l.strip()]
    return " | ".join(l[:maxlen] for l in ls[:n])


def flagstat_primary(path):
    """independent truth 1: `samtools flagstat` primary / primary mapped / primary paired-mapped etc."""
    rc, o, e = sh(f"samtools flagstat '{path}'")
    if rc != 0:
        return None
    m = {}
    for key, pat in (("total", r"^(\d+) \+ \d+ primary$"), ("mapped", r"^(\d+) \+ \d+ primary mapped"),):
        mm = re.search(pat, o, re.M)
        m[key] = int(mm.group(1)) if mm else None
    return m


def pysam_truth(path):
    """independent truth 2: pysam until_eof, primary records"""
    t = m = 0
    try:
        with pysam.AlignmentFile(path, "rb", check_sq=False) as b:
            for r in b.fetch(until_eof=True):
                if r.is_secondary or r.is_supplementary:
                    continue
                t += 1
                m += 0 if r.is_unmapped else 1
    except Exception as ex:  # noqa: BLE001
        return None
    return {"total": t, "mapped": m}


def verdict_of(out):
    """what the validator PRINTS as its verdict"""
    if re.search(r"^FAIL:", out, re.M):
        return "FAIL"
    if re.search(r"^WARN:", out, re.M):
        return "WARN"
    if "All metrics within normal range" in out:
        return "PASS"
    return "NONE"


rows = []
for label, path, bad, ref, kind in targets:
    row = {"label": label, "kind": kind, "expected_bad": bad}
    rc, o, e = sh(f"samtools quickcheck -v '{path}'")
    row["quickcheck"] = {"rc": rc, "out": first(o + e)}
    rc, o, e = sh(f"samtools view -c '{path}'")
    row["decode"] = {"rc": rc, "count": o.strip(), "err": first(e, 1)}
    rarg = f"R='{ref}'" if ref else ""
    rc, o, e = sh(f"picard ValidateSamFile I='{path}' MODE=SUMMARY {rarg} 2>&1")
    txt = o + e
    errs = re.findall(r"^(ERROR|WARNING):(\w+)\s+(\d+)", txt, re.M)
    row["picard"] = {"rc": rc, "found": [f"{a}:{b}={c}" for a, b, c in errs],
                     "no_errors": ("No errors found" in txt),
                     "exception": first("\n".join(l for l in txt.splitlines() if "Exception" in l), 1)}
    # verbatim CI one-liner from SKILL.md with `in.bam` -> path
    open(f"{RUN}/out/_ci.sh", "w", encoding="utf-8", newline="\n").write(CI.replace("in.bam", path))
    rc, o, e = sh(f"bash {RUN}/out/_ci.sh")
    row["ci_oneliner"] = {"rc": rc, "out": first(o + e)}
    ft, pt = flagstat_primary(path), pysam_truth(path)
    row["truth"] = {"flagstat_primary": ft, "pysam_primary": pt,
                    "mapped_pct": (round(100 * ft["mapped"] / ft["total"], 2) if ft and ft["total"] else None)}
    for tag, cmd in (("py", f"python '{PYV}' '{path}'"), ("sh", f"bash '{SHV}' '{path}'")):
        rc, o, e = sh(cmd)
        mm = re.search(r"Mapped: (\d+)(?: / (\d+) primary records)? ?\(([\d.]+)%\)", o)
        row[tag] = {"rc": rc, "verdict": verdict_of(o), "mapped_pct_printed": mm.group(3) if mm else None,
                    "mapped_n": mm.group(1) if mm else None,
                    "stderr_lines": len([l for l in e.splitlines() if l.strip()]),
                    "stderr": first(e, 1, 160), "fail_line": first("\n".join(l for l in o.splitlines() if l.startswith(("FAIL:", "WARN:"))), 2)}
        # contract: verdict FAIL <-> rc 1 ; PASS/WARN <-> rc 0 ; NONE (error) <-> rc 2
        exp = {"FAIL": 1, "WARN": 0, "PASS": 0, "NONE": 2}[row[tag]["verdict"]]
        row[tag]["contract_agrees"] = (rc == exp)
    rows.append(row)
    print(f"{label:38s} qc={row['quickcheck']['rc']} dec={row['decode']['rc']} pic={'OK' if row['picard']['no_errors'] else len(row['picard']['found'])} "
          f"ci={row['ci_oneliner']['rc']} | py rc={row['py']['rc']} {row['py']['verdict']} {row['py']['mapped_pct_printed']} | "
          f"sh rc={row['sh']['rc']} {row['sh']['verdict']} {row['sh']['mapped_pct_printed']} | truth {row['truth']['mapped_pct']}", flush=True)

json.dump(rows, open(OUT, "w"), indent=1)
print("written", len(rows), "->", OUT)
