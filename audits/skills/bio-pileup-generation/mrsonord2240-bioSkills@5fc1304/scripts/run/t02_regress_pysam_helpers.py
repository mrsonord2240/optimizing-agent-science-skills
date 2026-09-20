#!/usr/bin/env python3
"""Input 2 (Variant A, REGRESSION of pre-fix input 2): pysam allele counts / frequency / find_variants / pileup_text on the
planted-truth synthetic BAM (data/syn.bam, truth in data/truth.json) and the real human BAM, run against the FIXED Skill.
Functions are loaded VERBATIM from the copied SKILL.md; module-level snippets are exec'd with only paths/coordinates substituted."""
import contextlib, io, json, os, re, subprocess, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions, block_containing, python_blocks
import pysam

I = 2
truth = json.load(open(DATA + "/truth.json"))["truth"]["events"]
skill = load_functions("SKILL.md")
ug_blocks = python_blocks("usage-guide.md")
SK = open(SKILL + "/SKILL.md", encoding="utf-8").read()
UG = open(SKILL + "/usage-guide.md", encoding="utf-8").read()
print("SKILL.md functions:", sorted(skill), "| python blocks in usage-guide.md:", len(ug_blocks))
check(I, "usage-guide.md no longer carries code that duplicates SKILL.md (0 python blocks) and SKILL.md has no stale count_alleles/min_qual API", len(ug_blocks) == 0 and "count_alleles" not in SK and "min_qual" not in SK)


def run_snippet(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<snippet>", "exec"), {})
    return buf.getvalue()


# A. module-level snippets
blk = block_containing("SKILL.md", "for pileup_column in bam.pileup('chr1', 1000000, 1001000, truncate=True):\n        print(f'{pileup_column.reference_name}")
out = run_snippet(blk.replace("input.bam", SYN).replace("'chr1', 1000000, 1001000", "'synA', 100, 110"))
cols = [(int(m.group(1)), int(m.group(2))) for m in re.finditer(r"^synA:(\d+) depth=(\d+)$", out, flags=re.M)]
mpd, _, _, _ = mp_rows(SYNREF, SYN, "-B", "synA:101-110")
check(I, "Basic Pileup snippet (truncate=True): exactly the 10 requested columns 101..110 (1-based printed) with mpileup -B depths",
      [p for p, _ in cols] == list(range(101, 111)) and all(mpd[("synA", p)][3] == str(d) for p, d in cols), cols[:3])
blk = block_containing("SKILL.md", "if pileup_read.is_refskip:\n                print('  Reference skip')")
o1 = run_snippet(blk.replace("input.bam", SYN).replace("'chr1', 1000000, 1000001", "'synA', 99, 100"))
# UPDATED for round 2: snippet now prints "  <qname> <strand> <base> (Q<q>)"
cnt = Counter((b, q) for _n, _s, b, q in re.findall(r"^  (\S+) ([+-]) ([ACGT]) \(Q(\d+)\)", o1, flags=re.M))
ev = truth["snp"]
check(I, "Access Reads snippet at synA:100 lists 30 ref and 10 alt reads, all Q40, 'Depth: 40'", cnt.get((ev["ref"], "40")) == 30 and cnt.get((ev["alt"], "40")) == 10 and "Depth: 40" in o1, dict(cnt))
o2 = run_snippet(blk.replace("input.bam", SYN).replace("'chr1', 1000000, 1000001", "'synA', 399, 400"))
check(I, "Access Reads snippet in the spliced region synA:400: 3 'Reference skip', no 'Deletion' (Skill: is_refskip first)", o2.count("Reference skip") == 3 and "Deletion" not in o2, o2.replace("\n", "|"))
o3 = run_snippet(blk.replace("input.bam", SYN).replace("'chr1', 1000000, 1000001", "'synA', 250, 251"))
check(I, "Access Reads snippet at the real deletion synA:251: 4 'Deletion' + 4 bases (deletion still reported)", o3.count("Deletion") == 4 and "Reference skip" not in o3, o3.replace("\n", "|")[:120])
blk = block_containing("SKILL.md", "min_mapping_quality=20,\n                                     min_base_quality=20")
o4 = run_snippet(blk.replace("input.bam", SYN).replace("'chr1', 1000000, 1001000", "'synA', 700, 750"))
d = {int(a): int(b) for a, b in re.findall(r"^(\d+): (\d+)$", o4, flags=re.M)}
mq, _, _, _ = mp_rows(SYNREF, SYN, "-B -q 20 -Q 20", "synA:700-750")
check(I, "Quality Filtering snippet prints the real depth: synA:725 -> 4 (6 Q5 bases filtered) and every printed depth == mpileup -B -q20 -Q20",
      d.get(725) == 4 and all(mq[("synA", p)][3] == str(v) for p, v in d.items() if ("synA", p) in mq), f"725 -> {d.get(725)}")

# B. helpers vs planted truth
ac, af, fv, pt = skill["allele_counts"], skill["allele_frequency"], skill["find_variants"], skill["pileup_text"]
r = ac(SYN, "synA", 99)
check(I, "allele_counts(synA, 99) == planted {T:30, C:10}", r == {ev["ref"]: 30, ev["alt"]: 10}, r)
fr = af(SYN, "synA", 99)
check(I, "allele_frequency == {T:0.75, C:0.25}", abs(fr[ev["alt"]] - .25) < 1e-9 and abs(fr[ev["ref"]] - .75) < 1e-9, fr)
check(I, "docstring + call examples state 0-based / 1-based (pos - 1 pattern)", "0-based pos: pass 1-based position minus 1" in SK and "1000000 - 1" in SK)
lb = truth["lowbq"]
check(I, "allele_counts default drops six Q5 alt bases at synA:725 (only 4 ref); min_base_quality=0 keeps them (alt 6)",
      ac(SYN, "synA", 724) == {lb["ref"]: 4} and ac(SYN, "synA", 724, min_base_quality=0, ignore_overlaps=False).get(lb["alt"]) == 6, (ac(SYN, "synA", 724), ac(SYN, "synA", 724, min_base_quality=0)))
r = ac(SYN, "synA", truth["ins"]["after_pos"] - 1)
check(I, "SNV-only scope: allele_counts at the insertion site synA:200 -> {'A': 10}; docstring states insertions are not counted", r == {"A": 10} and "SNVs only" in SK, r)
r = ac(SYN, "synA", 250)
check(I, "allele_counts at the deleted base synA:251 == {DEL:4, ref:4}", r.get("DEL") == 4 and sum(r.values()) == 8, r)
r = ac(SYN, "synA", 399)
check(I, "allele_counts inside a spliced region synA:400 == {} (ref skips not counted, was {'DEL': 3} before the fix)", r == {}, r)
r = ac(SYN, "synA", truth["overlap"]["pos"] - 1)
mrows, _, _, _ = mp_rows(SYNREF, SYN, "-B", "synA:930-930")
_, mc = parse_bases(mrows[("synA", 930)][4], "C")
check(I, "allele_counts at the overlap site 930 (5 pairs, R1 ref/R2 alt) == mpileup -B parse", sum(r.values()) == 5 and r == {"C": mc["ref_fwd"] + mc["ref_rev"] + mc["C"] + mc["c"], "T": mc["T"] + mc["t"]}, (r, dict(mc)))
# all covered real positions == mpileup -B
def mp_counts(row):
    _, c = parse_bases(row[4], row[2])
    refn = c["ref_fwd"] + c["ref_rev"]
    out = Counter()
    for k, v in c.items():
        if len(k) == 1 and k.upper() in "ACGTN" and k not in ("^", "$"):
            out[k.upper()] += v
    out[row[2].upper()] += refn
    out["DEL"] += c["*"] + c["#"]
    return {k: v for k, v in out.items() if v}

with pysam.AlignmentFile(HBAM) as b:
    mpr, _, _, _ = mp_rows(HREF, HBAM, "-B", "chr22:1952-4617")
    sample = sorted(mpr)[::11][:110]
    bad = []
    for (c, p) in sample:
        got = ac(HBAM, c, p - 1)
        if got != mp_counts(mpr[(c, p)]):
            bad.append((p, got, mp_counts(mpr[(c, p)])))
check(I, "allele_counts == parse of samtools mpileup -B at 110 real chr22 positions (incl. indel sites)", not bad, bad[:2])

# find_variants
v = fv(SYN, SYNREF, "synA", 0, 1000)
check(I, "find_variants recovers only the planted SNP synA:100 T>C depth 40 alt 10 freq 0.25", [(x["pos"], x["ref"], x["alt"], x["alt_count"], x["depth"]) for x in v] == [(100, "T", "C", 10, 40)], v)
v = fv(SYN, SYNREF, "synA", 0, 1000, min_depth=3)
print("find_variants min_depth=3 output positions:", [(x["pos"], x["ref"], x["alt"], x["alt_count"], x["depth"]) for x in v])
check(I, "find_variants is SNV-only as stated: nothing at the planted indels (200, 250) and none inside the splice (326-525)", not any(x["pos"] in (200, 250) or 326 <= x["pos"] <= 525 for x in v), [x["pos"] for x in v])
rv = fv(HBAM, HREF, "chr22", 1951, 4617)
mp_v = []
for (c, p), row in sorted(mpr.items()):
    q, _, _, _ = mp_rows(HREF, HBAM, "-B -Q 20", f"chr22:{p}-{p}")
    r2 = q.get((c, p))
    if not r2:
        continue
    cn = mp_counts(r2)
    tot = sum(n for k, n in cn.items() if k != "DEL")
    if tot >= 10:
        for base, n in cn.items():
            if base != "DEL" and base != r2[2].upper() and n / tot >= 0.1:
                mp_v.append((p, r2[2].upper(), base, n))
sk_v = sorted((x["pos"], x["ref"], x["alt"], x["alt_count"]) for x in rv)
check(I, "find_variants on real chr22 == independent mpileup -B -Q20 parse (same alt sites and counts)", sk_v == sorted(mp_v), f"skill {len(sk_v)} vs mpileup {len(mp_v)}: {sk_v[:3]}")

# C. pileup_text on planted data: hand counts + row-for-row
def rows_pt(**kw):
    return {int(l.split("\t")[1]): l.split("\t") for l in pt(SYN, SYNREF, "synA", 0, 1000, **kw)}

pB = rows_pt(compute_baq=False)
pD = rows_pt()
mB, _, _, _ = mp_rows(SYNREF, SYN, "-B", "synA")
mD, _, _, _ = mp_rows(SYNREF, SYN, "", "synA")
same = lambda P, M: [k for k in M if P.get(k[1]) != M[k]] + [k for k in P if ("synA", k) not in M]
check(I, "pileup_text default (BAQ) == samtools mpileup, row-for-row on synA (623 rows, splice/indel/overlap/flag events)", not same(pD, mD), f"{len(mD)} rows; diffs {same(pD, mD)[:3]}")
check(I, "pileup_text compute_baq=False == samtools mpileup -B, row-for-row", not same(pB, mB), f"{len(mB)} rows; diffs {same(pB, mB)[:3]}")
c200 = Counter(re.findall(r"\+\d+[ACGTacgt]+", pB[200][4]))
check(I, "pileup_text hand counts: '+2AC' x3 and '+2ac' x2 at synA:200 (depth 10)", c200 == Counter({"+2AC": 3, "+2ac": 2}) and pB[200][3] == "10", (dict(c200), pB[200][3]))
c250 = Counter(re.findall(r"-\d+[ACGTacgt]+", pB[250][4]))
check(I, "pileup_text -B hand counts: '-3CGT' x2 and '-3cgt' x2 at synA:250 (depth 8); default BAQ hides them (depth 4, no marker) as the Skill says",
      c250 == Counter({"-3CGT": 2, "-3cgt": 2}) and pB[250][3] == "8" and pD[250][3] == "4" and "-" not in pD[250][4], (dict(c250), pB[250][3], pD[250][3:5]))
check(I, "pileup_text spliced site synA:400: '>><' (was '***'); depth 3", sorted(pB[400][4].replace("^]", "")) == sorted(">><") and pB[400][3] == "3", pB[400][4])
check(I, "pileup_text emits '^]' (MAPQ 60) and '$' markers and a quality column; zero-depth row format",
      all(("^]" in pB[81][4], "$" in pB[130][4], len(pB[81][5]) == int(pB[81][3]))), (pB[81][4][:12], pB[130][4][:8]))
# also with -q 20 -Q 20 -x -A
mQ, _, _, _ = mp_rows(SYNREF, SYN, "-q 20 -Q 20 -x -A", "synA")
pQ = rows_pt(min_mapping_quality=20, min_base_quality=20, ignore_overlaps=False, ignore_orphans=False)
check(I, "pileup_text(-q 20 -Q 20 -x -A equivalents) == samtools mpileup on synA", not same(pQ, mQ), same(pQ, mQ)[:3])

# D. shipped example
def ex(args):
    r = subprocess.run(f"python {SKILL}/examples/allele_counts.py {args}", shell=True, capture_output=True, text=True, executable="/bin/bash")
    return r.returncode, r.stdout, r.stderr
rc, out, err = ex(f"{SYN} synA:100")
check(I, "examples/allele_counts.py synA:100 -> T 30 (75.0%) / C 10 (25.0%), depth 40, rc 0", rc == 0 and "Total depth: 40" in out and "T: 30 (75.0%)" in out and "C: 10 (25.0%)" in out, out.replace("\n", "|"))
rc, out, err = ex(f"{HBAM} chr22:3000")
q3, _, _, _ = mp_rows(HREF, HBAM, "-B -q 20 -Q 20", "chr22:3000-3000")
check(I, "examples/allele_counts.py real chr22:3000 total depth == samtools mpileup -B -q20 -Q20 (781)", f"Total depth: {q3[('chr22', 3000)][3]}" in out and "Total depth: 781" in out, out.replace("\n", "|")[:100])
rc, out, err = ex(f"{SYN} synA:400")
check(I, "examples/allele_counts.py at the spliced synA:400: depth 0 (skips not counted)", rc == 0 and "Total depth: 0" in out, out.replace("\n", "|"))
summary(I)
