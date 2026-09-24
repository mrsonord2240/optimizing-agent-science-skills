"""NEW fixtures matrix (Family N planted defects + Family L threshold ladder), see make_new_fixtures.py.
Family N: quickcheck | decode | Picard ValidateSamFile (with and without R= where the defect needs it) | SKILL CI one-liner |
          both validators (rc + verdict + contract).
Family L: both validators vs the independently computed expected grades/verdict/rc; per-metric grade lines and printed
          values are compared with the expected values.  py and sh must agree with each other and with the truth.
Run in WSL: python matrix_new.py
"""
import json
import re
import subprocess

RUN = "/mnt/openscience/audits/bio-alignment-validation/run"
PD = "/mnt/openscience/audit-envs/alignment-files/public-data"
D = f"{RUN}/data/new"
PYV = f"{RUN}/skill/examples/validate_alignment.py"
SHV = f"{RUN}/skill/examples/validate_alignment.sh"
HREF = f"{PD}/human/genome.fasta"
CI = open(f"{RUN}/snip/SKILL_02_bash.txt", encoding="utf-8").read()
truthN = json.load(open(f"{D}/fixtures_new.json"))
truthL = json.load(open(f"{D}/ladder_truth.json"))


def sh(cmd, timeout=300):
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout or "", p.stderr or ""


def first(s, n=1, maxlen=120):
    ls = [l for l in s.strip().splitlines() if l.strip()]
    return " | ".join(l[:maxlen] for l in ls[:n])


def picard(path, ref):
    rarg = f"R='{ref}'" if ref else ""
    rc, o, e = sh(f"picard ValidateSamFile I='{path}' MODE=SUMMARY {rarg} 2>&1")
    txt = o + e
    errs = re.findall(r"^(ERROR|WARNING):(\w+)\s+(\d+)", txt, re.M)
    return {"rc": rc, "found": [f"{a}:{b}={c}" for a, b, c in errs], "no_errors": "No errors found" in txt,
            "exception": first("\n".join(l for l in txt.splitlines() if "Exception" in l), 1, 160)}


def verdict_of(out):
    if re.search(r"^FAIL:", out, re.M):
        return "FAIL"
    if re.search(r"^WARN:", out, re.M):
        return "WARN"
    if "All metrics within normal range" in out:
        return "PASS"
    return "NONE"


def grades(out):
    return dict(re.findall(r"(Mapping rate|Proper pairing|Strand balance|Mean MAPQ): (PASS|WARN|FAIL)", out))


def validator(tag, path):
    cmd = f"python '{PYV}' '{path}'" if tag == "py" else f"bash '{SHV}' '{path}'"
    rc, o, e = sh(cmd)
    v = verdict_of(o)
    exp_rc = {"FAIL": 1, "WARN": 0, "PASS": 0, "NONE": 2}[v]
    vals = {}
    m = re.search(r"Mapped: (\d+)(?: / (\d+) primary records)? ?\(([\d.]+)%\)", o)
    vals["map"] = float(m.group(3)) if m else None
    m = re.search(r"Properly paired: .*?\(([\d.]+)%", o)
    vals["pair"] = float(m.group(1)) if m else None
    m = re.search(r"Forward fraction F/\(F\+R\): ([\d.]+)", o)
    vals["strand"] = float(m.group(1)) if m else None
    m = re.search(r"Mean MAPQ: ([\d.]+)", o)
    vals["mapq"] = float(m.group(1)) if m else None
    return {"rc": rc, "verdict": v, "contract_agrees": rc == exp_rc, "grades": grades(o), "values": vals,
            "stderr": first(e, 1, 160), "fail_line": first("\n".join(l for l in o.splitlines() if l.startswith(("FAIL:", "WARN:"))), 2)}


rows = {"N": [], "L": []}
for name, t in sorted(truthN.items()):
    path = f"{D}/{name}"
    r = {"file": name, "defect": t["defect"], "expected_bad": t["expected_bad"]}
    rc, o, e = sh(f"samtools quickcheck -v '{path}'")
    r["quickcheck_rc"] = rc
    rc, o, e = sh(f"samtools view -c '{path}'")
    r["decode_rc"] = rc
    r["decode_err"] = first(e, 1)
    open(f"{RUN}/out/_ci.sh", "w", encoding="utf-8", newline="\n").write(CI.replace("in.bam", path))
    rc, o, e = sh(f"bash {RUN}/out/_ci.sh")
    r["ci_rc"] = rc
    r["picard_noR"] = picard(path, None)
    if t.get("human_ref"):
        r["picard_R"] = picard(path, HREF)
    r["py"] = validator("py", path)
    r["sh"] = validator("sh", path)
    rows["N"].append(r)
    pc = r.get("picard_R") or r["picard_noR"]
    print(f"{name:30s} qc={r['quickcheck_rc']} dec={r['decode_rc']} ci={r['ci_rc']} picard(noR)={'OK' if r['picard_noR']['no_errors'] else r['picard_noR']['found'][:3] or r['picard_noR']['exception']} "
          + (f"picard(R)={'OK' if pc['no_errors'] else pc['found'][:3]} " if t.get('human_ref') else "")
          + f"| py rc={r['py']['rc']} {r['py']['verdict']} | sh rc={r['sh']['rc']} {r['sh']['verdict']}", flush=True)

for name, t in sorted(truthL.items()):
    path = f"{D}/{name}.bam"
    r = {"file": name, "expected": t}
    for tag in ("py", "sh"):
        v = validator(tag, path)
        r[tag] = v
        gexp = {"map": "Mapping rate", "pair": "Proper pairing", "strand": "Strand balance", "mapq": "Mean MAPQ"}
        gmatch = all(v["grades"].get(gexp[k]) == g for k, g in t["grades"].items())
        vals_ok = {}
        for k, exp in t["metrics"].items():
            got = v["values"].get(k)
            tol = {"map": 0.006, "pair": 0.006, "strand": 0.0006, "mapq": 0.06}[k]
            vals_ok[k] = (got is not None and abs(got - exp) <= tol)
        v["grades_match_truth"] = gmatch
        v["values_match_truth"] = vals_ok
        v["overall_ok"] = (v["verdict"] == t["overall"] and v["rc"] == t["expected_rc"] and gmatch and all(vals_ok.values()) and v["contract_agrees"])
    rows["L"].append(r)
    print(f"{name:20s} truth {t['overall']:4s} rc{t['expected_rc']} | py {r['py']['verdict']:4s} rc{r['py']['rc']} ok={r['py']['overall_ok']} | sh {r['sh']['verdict']:4s} rc{r['sh']['rc']} ok={r['sh']['overall_ok']}", flush=True)

json.dump(rows, open(f"{RUN}/out/matrix_new.json", "w"), indent=1)
print("written")
