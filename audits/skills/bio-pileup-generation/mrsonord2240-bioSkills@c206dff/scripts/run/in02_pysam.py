#!/usr/bin/env python3
"""Input 2 (Variant A): 'Count alleles / allele frequency at a position and make a text pileup with pysam' -- the pysam half of the Skill.
Every function is loaded VERBATIM from the (copied) SKILL.md / usage-guide.md through snippets.py; module-level snippets are exec'd
after substituting only file names and coordinates.  Truth = planted synthetic design (data/truth.json) and real-data samtools mpileup."""
import contextlib, io, json, os, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions, block_containing
import pysam

I = 2
SYN = DATA + "/syn.bam"; SYNREF = DATA + "/syn.fa"
BAM = HUMAN + "/test.paired_end.sorted.bam"; REF = HUMAN + "/genome.fasta"
truth = json.load(open(DATA + "/truth.json"))["truth"]["events"]
skill = load_functions("SKILL.md")
usage = load_functions("usage-guide.md")
print("SKILL.md functions:", sorted(skill), "| usage-guide functions:", sorted(usage))

def run_snippet(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<snippet>", "exec"), {})
    return buf.getvalue()

# ---------- A. module-level SKILL.md snippets, substituted to the synthetic BAM
blk = block_containing("SKILL.md", "for pileup_column in bam.pileup('chr1', 1000000, 1001000):")
code = blk.replace("input.bam", SYN).replace("'chr1', 1000000, 1001000", "'synA', 100, 110")
out = run_snippet(code)
lines = [l for l in out.splitlines() if l.startswith("synA:")]
positions = [int(re.match(r"synA:(\d+)", l).group(1)) for l in lines]
print("SKILL 'Basic Pileup' (no truncate) printed", len(lines), "columns, pos range", min(positions), "-", max(positions))
check(I, "SKILL 'Basic Pileup' snippet prints only columns inside the requested region 100-110", all(100 <= p < 110 for p in positions),
      f"requested 10 columns, got {len(lines)} covering {min(positions)}-{max(positions)} (no truncate=True; reads overhang)")

blk = block_containing("SKILL.md", "for pileup_read in pileup_column.pileups:\n            if pileup_read.is_del:\n                print('  Deletion')")
code = blk.replace("input.bam", SYN).replace("'chr1', 1000000, 1000001", "'synA', 99, 100")
out = run_snippet(code)
cnt = Counter(re.findall(r"^  ([ACGT]) \(Q(\d+)\)", out, flags=re.M))
print(dict(cnt), out.splitlines()[:2])
ev = truth["snp"]
check(I, "SKILL 'Access Reads at Position' at synA:100 lists 30 ref (T) and 10 alt (C) reads, all Q40",
      cnt.get((ev["ref"], "40")) == 30 and cnt.get((ev["alt"], "40")) == 10, dict(cnt))
check(I, "'Access Reads' snippet's printed `Depth:` line equals reads listed", f"Depth: {sum(cnt.values())}" in out, [l for l in out.splitlines() if l.startswith("Depth")])

blk = block_containing("SKILL.md", "min_mapping_quality=20,\n                                     min_base_quality=20")
code = blk.replace("input.bam", SYN).replace("'chr1', 1000000, 1001000", "'synA', 700, 750")
out = run_snippet(code)
d = {int(a): int(b) for a, b in re.findall(r"^(\d+): (\d+)$", out, flags=re.M)}
# planted: 10 reads at 701..750, 6 have Q5 alt base at pos 725 -> 4 usable bases at 0-based 724
check(I, "SKILL 'Pileup with Quality Filtering' (min_base_quality=20): printed depth at synA:725 == bases that pass Q20 (4)",
      d.get(724) == 4, f"printed pos 724 -> n={d.get(724)} (6 of 10 bases at this column are Q5 and are filtered; n ignores base-quality filter)")

# ---------- B. SKILL.md functions vs planted truth
ac = skill["allele_counts"]; af = skill["allele_frequency"]
r = ac(SYN, "synA", 99)
check(I, "SKILL allele_counts(synA, 0-based 99) == planted {T:30, C:10}", r == {ev["ref"]: 30, ev["alt"]: 10}, r)
r1 = ac(SYN, "synA", 100)  # what an agent does when the user says 'position synA:100' (1-based) -> off by one
check(I, "SKILL allele_counts called with the 1-based coordinate the user gave (100) reports the SNP", r1.get(ev["alt"], 0) == 10,
      f"returned {r1} = base at 1-based 101 (function/docstring never states 0-based; usage-guide Tips does)")
fr = af(SYN, "synA", 99)
check(I, "SKILL allele_frequency(synA, 99) == {T:0.75, C:0.25}", abs(fr.get(ev["alt"], 0) - 0.25) < 1e-9 and abs(fr.get(ev["ref"], 0) - 0.75) < 1e-9, fr)
lb = truth["lowbq"]
r = ac(SYN, "synA", lb["pos"] - 1)
check(I, "SKILL allele_counts default (pysam min_base_quality=13) drops the six Q5 alt bases at synA:725 -> only 4 ref", r == {lb["ref"]: 4}, r)
r = af(SYN, "synA", lb["pos"] - 1, min_qual=0)
check(I, "allele_frequency(min_qual=0) at synA:725 includes the six Q5 alt bases (alt frac 0.6)", abs(r.get(lb["alt"], 0) - 0.6) < 1e-9, r)
ins = truth["ins"]; dele = truth["del"]
r = ac(SYN, "synA", ins["after_pos"] - 1)
check(I, "allele_counts at synA:200 (5 of 10 reads carry a +2 insertion) reports the insertion", any(k for k in r if len(k) > 1 and k != "DEL"), f"{r} -> insertion invisible (`indel` attribute never read)")
r = ac(SYN, "synA", 250)  # 1-based 251 : first deleted base
check(I, "allele_counts at synA:251 == {DEL:4, ref:4}", r.get("DEL") == 4 and sum(r.values()) == 8, r)
r = ac(SYN, "synA", 399)
check(I, "allele_counts inside a spliced (N) region returns empty dict and does not crash", r == {}, r)
ov = truth["overlap"]
r = ac(SYN, "synA", ov["pos"] - 1)
check(I, "allele_counts at overlap site 930 (5 pairs, R1 ref / R2 alt): total = 5 (overlap removal on by default)", sum(r.values()) == 5, f"{r} (mpileup default: '..ttt' -> 2 ref + 3 alt)")
_, out, _ = sh(f"samtools mpileup -B -f {SYNREF} -r synA:930-930 {SYN}")
_, mc = parse_bases(mpileup_rows(out)[0][4], "C")
sm = {"C": mc["ref_fwd"] + mc["ref_rev"] + mc["C"] + mc["c"], "T": mc["T"] + mc["t"]}
check(I, "SKILL allele_counts at 930 == samtools mpileup -B parse (same overlap arbitration)", r == {k: v for k, v in sm.items() if v}, f"pysam {r} mpileup {sm}")

# ---------- C. SKILL allele_counts vs samtools mpileup -B at sampled real positions (all 1181 covered positions would be slow; every 12th + all indel sites)
_, out, _ = sh(f"samtools mpileup -B -f {REF} -r chr22:1952-4617 {BAM}")
rows = [r for r in mpileup_rows(out) if r[3] != "0"]
indel_sites = [int(r[1]) for r in rows if "*" in r[4] or "+" in r[4] or "-" in r[4]]
sample = sorted(set([int(r[1]) for r in rows[::12]] + indel_sites[:15]))
bad = []
for p in sample:
    row = [r for r in rows if int(r[1]) == p][0]
    n, c = parse_bases(row[4], row[2])
    exp = Counter()
    exp[row[2]] += c["ref_fwd"] + c["ref_rev"]
    for b in "ACGTN":
        exp[b] += c[b] + c[b.lower()]
    if c["*"]:
        exp["DEL"] += c["*"]
    exp = {k: v for k, v in exp.items() if v}
    got = ac(BAM, "chr22", p - 1)
    if got != exp:
        bad.append((p, got, exp))
check(I, f"SKILL allele_counts == samtools mpileup -B parse at {len(sample)} real positions (incl. {len(indel_sites[:15])} indel sites)", not bad, bad[:2])

# ---------- D. pileup_text vs samtools mpileup (the SKILL 'Generate Pileup Text' helper)
pt = skill["pileup_text"]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    pt(SYN, SYNREF, "synA", 0, 1000)
ptxt = [l.split("\t") for l in buf.getvalue().splitlines()]
_, out, _ = sh(f"samtools mpileup -B -f {SYNREF} -r synA:1-1000 {SYN}")
mrows = {int(r[1]): r for r in mpileup_rows(out)}
print("pileup_text sample:", ptxt[99], "| mpileup:", mrows.get(100)[:5])
check(I, "pileup_text emits the 6-column pileup format (chrom,pos,ref,depth,bases,quals)", all(len(r) == 6 for r in ptxt), Counter(len(r) for r in ptxt))
dep_bad = [(int(r[1]), int(r[3]), len(r[4])) for r in ptxt if int(r[3]) != len(r[4])]
check(I, "pileup_text depth column == number of symbols in its own bases column", not dep_bad, f"{len(dep_bad)} rows inconsistent, e.g. {dep_bad[:3]} (depth uses pileup_column.n)")
dep_mp = [(int(r[1]), int(r[3]), int(mrows[int(r[1])][3])) for r in ptxt if int(r[1]) in mrows and int(r[3]) != int(mrows[int(r[1])][3])]
check(I, "pileup_text depth == samtools mpileup depth at every position", not dep_mp, f"{len(dep_mp)} positions differ e.g. {dep_mp[:3]}")
def sym_multiset(s):
    n, c = parse_bases(s, "")
    m = Counter()
    for k, v in c.items():
        if k == "ref_fwd": m["."] += v
        elif k == "ref_rev": m[","] += v
        elif k in "ACGTNacgtn*<>": m[k] += v
    return m
sym_bad = []
for r in ptxt:
    p = int(r[1])
    if p in mrows:
        a = Counter(r[4]) if r[4] else Counter()
        b2 = sym_multiset(mrows[p][4])
        # mpileup marks reverse-strand ref-skip '<' and forward '>' ; pileup_text emits '>' for every ref-skip
        if a != b2:
            sym_bad.append((p, dict(a), dict(b2)))
check(I, "pileup_text base column has the same symbol multiset as samtools mpileup at every covered position", not sym_bad,
      f"{len(sym_bad)} positions differ; first: {sym_bad[:3]}")
row400 = [r for r in ptxt if r[1] == "400"][0]
check(I, "pileup_text reports spliced (N) reads as '>'/'<' (SKILL: is_refskip branch) at synA:400", set(row400[4]) <= set("<>"), f"emitted {row400[4]!r}; mpileup {mrows[400][4]!r} (pysam sets is_del=True for ref-skips, so the is_del branch fires first and writes '*')")
mk_missing = [p for p, r in mrows.items() if ("^" in r[4] or "$" in r[4] or "+" in r[4] or "-" in r[4])]
has_mk = any(("^" in r[4] or "$" in r[4] or "+" in r[4]) for r in ptxt)
check(I, "pileup_text reproduces read-start/end markers (^,$) and indel text (+N/-N) that the Skill's own encoding table lists", has_mk,
      f"{len(mk_missing)} mpileup rows carry ^ $ + or -; pileup_text emits none, and no quality column")
check(I, "pileup_text emits the base-quality column (column 6 in the Skill's format table)", len(ptxt[0]) >= 6 and len(ptxt[0][5]) > 0, f"columns={len(ptxt[0])}")

# ---------- E. usage-guide count_alleles / find_variants
find_variants = usage["find_variants"]; count_alleles = usage["count_alleles"]
c = count_alleles(SYN, "synA", 99)
check(I, "usage-guide count_alleles(min_qual=20) at synA:100 == {T:30,C:10}", c == {ev["ref"]: 30, ev["alt"]: 10}, c)
v = find_variants(SYN, SYNREF, "synA", 0, 1000)
print("find_variants on syn:", v)
got = {(x["pos"], x["ref"], x["alt"], x["alt_count"]) for x in v}
check(I, "usage-guide find_variants recovers the planted SNP synA:100 T>C (depth 40, alt 10, freq 0.25)", (100, ev["ref"], ev["alt"], 10) in got and any(abs(x["freq"] - 0.25) < 1e-9 and x["depth"] == 40 for x in v), got)
check(I, "find_variants reports no false variants (only the planted SNP passes depth>=10, alt>=0.1, Q>=20)", got == {(100, ev["ref"], ev["alt"], 10)}, got)
v2 = find_variants(SYN, SYNREF, "synA", 0, 1000, min_depth=3, min_alt_freq=0.1)
missed = {"ins@200", "del@251"}
check(I, "find_variants can see the planted 2 bp insertion and 3 bp deletion (Skill claims 'SNP/indel detection')", False,
      f"min_depth=3 output positions {sorted({x['pos'] for x in v2})}: indels are never reported (only `alignment.query_sequence[qpos]`; `indel` field unused)")
# real data cross-check of find_variants against mpileup -B -Q20 parse
vr = find_variants(BAM, REF, "chr22", 1951, 4617)
_, out, _ = sh(f"samtools mpileup -B -Q 20 -q 0 -f {REF} -r chr22:1952-4617 {BAM}")
exp = set()
for r in mpileup_rows(out):
    if r[3] == "0":
        continue
    n, cc = parse_bases(r[4], r[2])
    tot = sum(cc[k] for k in "ACGTNacgtn") + cc["ref_fwd"] + cc["ref_rev"]
    if tot < 10:
        continue
    for b in "ACGTN":
        k = cc[b] + cc[b.lower()]
        if b != r[2] and k / tot >= 0.1:
            exp.add((int(r[1]), b, k))
gotr = {(x["pos"], x["alt"], x["alt_count"]) for x in vr}
print(f"find_variants real chr22: {len(gotr)} sites; mpileup-derived {len(exp)}; only-in-skill {sorted(gotr - exp)[:5]}; only-in-mpileup {sorted(exp - gotr)[:5]}")
check(I, "find_variants on real human BAM == independent mpileup -B -Q20 parse (same alt sites and counts)", gotr == exp, f"skill {len(gotr)} vs mpileup {len(exp)}")

# ---------- F. shipped example script, run from the COPY
ex = SKILL + "/examples/allele_counts.py"
rc, out, err = sh(f"python {ex} {SYN} synA:100")
print(out, err[:200])
check(I, "examples/allele_counts.py synA:100 (from copy) prints T:30 (75.0%) and C:10 (25.0%)", rc == 0 and "T: 30 (75.0%)" in out and "C: 10 (25.0%)" in out and "Total depth: 40" in out, out.replace("\n", " | "))
rc, out, err = sh(f"python {ex} {BAM} chr22:3000")
_, mo, _ = sh(f"samtools mpileup -B -q 20 -Q 20 -f {REF} -r chr22:3000-3000 {BAM}")
r0 = mpileup_rows(mo)[0]
print("example on real chr22:3000:", out.replace("\n", " | "), "| mpileup -B -q20 -Q20 col4:", r0[3])
tot = re.search(r"Total depth: (\d+)", out)
check(I, "examples/allele_counts.py total depth at real chr22:3000 == samtools mpileup -B -q20 -Q20 depth", rc == 0 and tot and int(tot.group(1)) == int(r0[3]), f"example {tot.group(1) if tot else None} vs mpileup {r0[3]}")
summary(I)
