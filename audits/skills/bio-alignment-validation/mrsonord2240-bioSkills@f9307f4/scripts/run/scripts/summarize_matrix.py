"""Summarise out/matrix.json (21+2 regression fixtures + 9 real BAMs) and out/matrix_new.json (new fixtures + ladder).
Windows or WSL python.  Prints detection counts, false positives, contract disagreements.
"""
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "out"
m = json.load(open(OUT / "matrix.json", encoding="utf-8"))
n = json.load(open(OUT / "matrix_new.json", encoding="utf-8"))


def pic_flag(p):
    return (not p["no_errors"]) or bool(p.get("found")) or bool(p.get("exception")) or p["rc"] != 0


print("=== REGRESSION: 21 planted-defect files (expected_bad, excluding the 2 controls) ===")
bad = [r for r in m if r["kind"] == "planted" and r["expected_bad"]]
ctl = [r for r in m if r["kind"] == "planted" and not r["expected_bad"]]
real = [r for r in m if r["kind"] == "real"]
print("n planted-bad:", len(bad), " controls:", [r["label"] for r in ctl], " real:", len(real))
tools = {
    "quickcheck": lambda r: r["quickcheck"]["rc"] != 0,
    "samtools view -c": lambda r: r["decode"]["rc"] != 0,
    "Picard ValidateSamFile": lambda r: pic_flag(r["picard"]),
    "CI one-liner": lambda r: r["ci_oneliner"]["rc"] != 0,
    "validate_alignment.py (rc!=0)": lambda r: r["py"]["rc"] != 0,
    "validate_alignment.sh (rc!=0)": lambda r: r["sh"]["rc"] != 0,
}
for t, f in tools.items():
    caught = [r["label"] for r in bad if f(r)]
    missed = [r["label"] for r in bad if not f(r)]
    fp_ctl = [r["label"] for r in ctl if f(r)]
    fp_real = [r["label"] for r in real if f(r)]
    print(f"{t:32s} caught {len(caught):2d}/{len(bad)} | flags on controls: {fp_ctl} | flags on real valid: {fp_real}")
    if t in ("quickcheck", "samtools view -c", "Picard ValidateSamFile", "CI one-liner"):
        print("     caught:", caught)
        print("     missed:", missed)
print()
print("=== validator contract (printed verdict agrees with rc), all 32 files ===")
for tag in ("py", "sh"):
    dis = [(r["label"], r[tag]["rc"], r[tag]["verdict"]) for r in m if not r[tag]["contract_agrees"]]
    print(tag, "disagreements:", dis)
print("py vs sh rc differ:", [(r["label"], r["py"]["rc"], r["sh"]["rc"]) for r in m if r["py"]["rc"] != r["sh"]["rc"]])
print("mapping% printed vs flagstat truth (files where both exist):")
for r in m:
    t = r["truth"]["mapped_pct"]
    for tag in ("py", "sh"):
        p = r[tag]["mapped_pct_printed"]
        if t is not None and p is not None and abs(float(p) - t) > 0.006:
            print("  MISMATCH", r["label"], tag, p, t)
print("stderr noise: files with >1 stderr line -> ", [(r["label"], tag, r[tag]["stderr_lines"]) for r in m for tag in ("py", "sh") if r[tag]["stderr_lines"] > 1])
print()
print("=== NEW planted (13 files incl. 2 valid) ===")
N = n["N"]
badN = [r for r in N if r["expected_bad"]]
okN = [r for r in N if not r["expected_bad"]]


def real_flag(p):
    """Picard 'caught' on the 1000G-based set: anything beyond MATE_NOT_FOUND (the region slice's own noise, also on the valid control) or an abort"""
    types = {f.split(":")[1].split("=")[0] for f in p.get("found", [])}
    return bool(types - {"MATE_NOT_FOUND"}) or (not p["no_errors"] and not p.get("found"))


def pn(r):
    return real_flag(r.get("picard_R") or r["picard_noR"])


tN = {
    "quickcheck": lambda r: r["quickcheck_rc"] != 0,
    "samtools view -c": lambda r: r["decode_rc"] != 0,
    "Picard, beyond slice noise (R= only where fixture needs it)": pn,
    "Picard (never R=)": lambda r: real_flag(r["picard_noR"]),
    "CI one-liner": lambda r: r["ci_rc"] != 0,
    "validate_alignment.py (rc!=0)": lambda r: r["py"]["rc"] != 0,
    "validate_alignment.sh (rc!=0)": lambda r: r["sh"]["rc"] != 0,
}
for t, f in tN.items():
    print(f"{t:40s} caught {sum(1 for r in badN if f(r)):2d}/{len(badN)}  missed: {[r['file'] for r in badN if not f(r)]}  flags on valid ones: {[r['file'] for r in okN if f(r)]}")
print("Contract disagreements (new N):", [(r["file"], tag) for r in N for tag in ("py", "sh") if not r[tag]["contract_agrees"]])
print()
print("=== LADDER (12 files): validators vs independent truth ===")
L = n["L"]
for tag in ("py", "sh"):
    print(tag, "overall_ok:", sum(1 for r in L if r[tag]["overall_ok"]), "/", len(L), " failures:", [r["file"] for r in L if not r[tag]["overall_ok"]])
