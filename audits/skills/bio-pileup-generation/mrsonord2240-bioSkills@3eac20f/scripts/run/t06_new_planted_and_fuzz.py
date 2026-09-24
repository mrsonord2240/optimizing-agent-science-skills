#!/usr/bin/env python3
"""Input 6 (NEW, re-auditor): planted-truth BAM written for this re-audit (data/new.bam, own design, hand truth in the
generator docstring) + a randomized differential test. Skill code is loaded VERBATIM from the copied SKILL.md.

A. planted events: hand-derived expectations for symbols, -q/-Q boundaries, flags, overlap, ref N, soft-masked reference,
   clips, colon-named contig  (samtools mpileup, second method = pysam / the Skill's pileup_text)
B. Skill's rewritten pileup_text vs `samtools mpileup` row-for-row on 1,862 random reads, 13 option combinations
C. Skill helpers (allele_counts, find_variants) and examples/allele_counts.py on the planted data
"""
import json, os, re, subprocess, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions
import pysam

I = 6
skill = load_functions("SKILL.md")
pileup_text = skill["pileup_text"]; allele_counts = skill["allele_counts"]; find_variants = skill["find_variants"]
tr = json.load(open(DATA + "/new_truth.json"))["truth"]
fa = pysam.FastaFile(NEWREF)
print("SKILL.md python functions:", sorted(skill))


def row(opts, contig, pos, ref=NEWREF, bam=NEW):
    d, _, rc, err = mp_rows(ref, bam, opts, f"{contig}:{pos}-{pos}")
    return d.get((contig, pos)), err


def sym(r):
    return parse_bases(r[4], r[2])[1]


# ---------------- A. planted events -----------------
# E1 deletion, strands
r, _ = row("-B", "nA", 110)
c = sym(r)
check(I, "E1 -B: row 110 depth 10 with '-2CC' x3 (fwd) and '-2cc' x3 (rev)", r[3] == "10" and c["-CC"] == 3 and c["-cc"] == 3, f"{r[3:5]} {dict(c)}")
r, _ = row("-B", "nA", 111)
check(I, "E1 -B: row 111 depth 10 with '*' x6 (deleted bases stay in depth)", r[3] == "10" and sym(r)["*"] == 6, r[3:5])
r, _ = row("-B --reverse-del", "nA", 111)
check(I, "E1 --reverse-del: 3 '*' (fwd) + 3 '#' (rev); Skill's symbol table says '#' with --reverse-del on the reverse strand", sym(r)["*"] == 3 and sym(r)["#"] == 3, r[4])
r, _ = row("", "nA", 110)
print("E1 default (BAQ) row 110:", r[3:5], "| -B:", row("-B", "nA", 110)[0][3:5])
# E2 insertions
r, _ = row("-B", "nA", 420)
c = sym(r)
check(I, "E2 -B row 420: depth 10, '+3ACG' x2, '+3acg' x2, '+1T' x2 (insertion adds no depth)",
      r[3] == "10" and c["+ACG"] == 2 and c["+acg"] == 2 and c["+T"] == 2, f"{r[3]} {dict(c)}")
r, _ = row("-B", "nA", 425)
check(I, "E2 -B row 425: second insertion '+2GG' x2", sym(r)["+GG"] == 2, r[4])
# E3 MAPQ boundary
depths = {q: int(row(f"-B -q {q}", "nA", 510)[0][3]) for q in (0, 19, 20, 21, 22)}
check(I, "E3 -q boundary: depth 14 (all), 12 (-q19), 9 (-q20), 6 (-q21), 3 (-q22): 20 kept at -q 20, dropped at -q 21",
      depths[0] == 14 and depths[19] == 12 and depths[20] == 9 and depths[21] == 6 and depths[22] == 3, depths)
r, _ = row("-B", "nA", 501)
check(I, "E3 '^' MAPQ char: MAPQ 255 and 100 are capped to '~' (3 x '^~' incl. MAPQ 93+); MAPQ 0 = '^!'",
      r[4].count("^~") == 2 + 1 and r[4].count("^!") == 2, Counter(re.findall(r"\^(.)", r[4])))
# E4 base quality boundary (-B so BAQ does not touch quals)
dq = {q: int(row(f"-B -Q {q}", "nA", 620)[0][3]) for q in (0, 12, 13, 14, 15)}
check(I, "E4 -Q boundary with -B: Q12 dropped at -Q13, Q13 kept: depth 15 (-Q0), 15 (-Q12), 12 (-Q13), 9 (-Q14), 6 (-Q15 keeps the Q93 x2 + 4 ref)",
      dq[0] == 15 and dq[12] == 15 and dq[13] == 12 and dq[14] == 9 and dq[15] == 6, dq)
r, _ = row("-B -Q 13", "nA", 620)
check(I, "E4 default -Q 13: Skill says 'Min base quality default 13': omitting -Q equals -Q 13 (depth 12 with -B), Q93 prints '~'",
      row("-B", "nA", 620)[0][3] == "12" and "~" in r[5], f"{row('-B','nA',620)[0][3]} quals={r[5]}")
# E5 overlap
r, _ = row("-B", "nA", 730)
rx, _ = row("-B -x", "nA", 730)
check(I, "E5 overlap: depth 6 default (12 pairs' bases -> 6 counted once), 12 with -x; 3 alt 'A' remain",
      r[3] == "6" and rx[3] == "12" and sym(r)["A"] + sym(r)["a"] == 3 and sym(r)["ref_fwd"] + sym(r)["ref_rev"] == 3, f"default {r[3]} {r[4]} | -x {rx[3]}")
# E6 reference N / read N
r, _ = row("", "nA", 802)
check(I, "E6 reference N: col3 'N', read bases print as mismatches 'AAAAAAaaa' (depth 9)", r[2] == "N" and r[3] == "9" and sym(r)["A"] == 6 and sym(r)["a"] == 3, r[2:5])
rd, _ = row("-B", "nA", 790)
r0, _ = row("-B -Q 0", "nA", 790)
check(I, "E6 read-base N: default -Q 13 drops the two Q2 'N' bases (depth 7), -Q 0 keeps them (depth 9); Q40 N stays as 'N'",
      rd[3] == "7" and r0[3] == "9" and sym(rd)["N"] == 1, f"{rd[3:5]} vs {r0[3:5]}")
# E7 soft-masked reference
r, _ = row("", "nA", 920)
check(I, "E7 soft-masked (lowercase) reference: mpileup col3 is printed lowercase 'g' (as in the FASTA)", r[2] == "g", r[2:5])
print("   -> Skill's Output Format table says only 'Reference base'; it does not say soft-masked FASTAs (UCSC hg38) print lowercase.")
# E8 flags
e = tr["E8"]
d8 = {k: int(row(o, "nA", 1120)[0][3]) for k, o in (("default", "-B"), ("A", "-B -A"), ("ff0", "-B --ff 0"), ("ff0_A", "-B --ff 0 -A"))}
check(I, "E8 flags: default 10 (supplementary 2048 and proper-flag reads kept, DUP/orphans dropped), -A 14, --ff 0 12, both 16", d8 == dict(default=10, A=14, ff0=12, ff0_A=16), d8)
# E9 clips
r, _ = row("-B", "nA", 1320)
c = sym(r)
check(I, "E9 soft/hard clips never appear: depth 6, only '.' and ',' at 1320; at read starts (1301/1301) no clipped letters",
      r[3] == "6" and set(re.sub(r"\^.", "", r[4])) <= set(".,"), r[3:5])
# E10 deletion then ref-skip; insertion before deletion
r, _ = row("-B", "nA", 1420)
c = sym(r)
check(I, "E10 at 1420: 3 '>' (fwd reads inside the 50 bp N skip) + 3 ',' (rev reads M10) = depth 6", c[">"] == 3 and c["ref_rev"] == 3 and r[3] == "6", r[4])
r, _ = row("-B", "nA", 1411)
check(I, "E10 deletion 1411-1412: depth 6 with '*' x6 (fwd 10M2D5M50N10M and rev 10M2I2D10M)", sym(r)["*"] == 6 and r[3] == "6", r[4])
print("E10 row 1410 (fwd -2 deletion, rev +2 insertion then D):", row("-B", "nA", 1410)[0][3:5])
# E11 colon contig
rc, out, err = sh(f"samtools mpileup -f {NEWREF} -B -r 'HLA-A*01:01:01:01:120-120' {NEW}")
print("mpileup -r plain colon-contig region rc/out/err:", rc, repr(out[:60]), err.strip()[:120])
rc2, out2, err2 = sh(f"samtools mpileup -f {NEWREF} -B -r '{{HLA-A*01:01:01:01}}:120-120' {NEW}")
row11 = mpileup_rows(out2)
print("brace form:", row11[0][:5] if row11 else None, err2.strip()[:100])
ev = tr["E11"]
check(I, "E11 colon-named contig 'HLA-A*01:01:01:01': `samtools mpileup -r 'HLA-A*01:01:01:01:120-120'` works (last colon splits the region) and the brace form gives the same row",
      rc == 0 and rc2 == 0 and mpileup_rows(out) and mpileup_rows(out)[0][:5] == row11[0][:5] and row11[0][3] == "10", f"plain={mpileup_rows(out)[0][:5] if out.strip() else None} brace depth={row11[0][3] if row11 else None}")

# ---------------- pysam vs samtools on planted data; Skill helpers -----------------
ac = allele_counts(NEW, ev["contig"], ev["pos"] - 1)
check(I, "C allele_counts on colon-named contig (pysam takes the name verbatim): {G:6, A:4}", ac == {ev["ref"]: 6, ev["alt"]: 4}, ac)
e7 = tr["E7"]
ac = allele_counts(NEW, "nA", e7["pos"] - 1)
check(I, "C allele_counts at the soft-masked site nA:920 == {G:5, A:3} (case-insensitive counting)", ac == {e7["ref"]: 5, e7["alt"]: 3}, ac)
ac12 = allele_counts(NEW, "nA", 620 - 1, min_base_quality=12)
ac13 = allele_counts(NEW, "nA", 620 - 1, min_base_quality=13)
ac14 = allele_counts(NEW, "nA", 620 - 1, min_base_quality=14)
check(I, "C allele_counts min_base_quality boundary matches -Q: 12 keeps Q12 (T? alt 11 + ref 4), 13 drops Q12 (alt 8 + ref 4), 14 drops Q13",
      sum(ac12.values()) == 15 and sum(ac13.values()) == 12 and sum(ac14.values()) == 9 and ac13.get("C") == 8, (ac12, ac13, ac14))
ac_q = allele_counts(NEW, "nA", 620 - 1, min_base_quality=0, min_mapping_quality=0)
ac_mq = allele_counts(NEW, "nA", 510 - 1, min_mapping_quality=20)
check(I, "C allele_counts(min_mapping_quality=20) at nA:510 counts 9 reads (MAPQ 20 kept, 19 dropped)", sum(ac_mq.values()) == 9, ac_mq)
fv = find_variants(NEW, NEWREF, "nA", 900, 1000, min_depth=5, min_alt_freq=0.1)
check(I, "C find_variants on the soft-masked block reports exactly the planted nA:920 G>A 3/8 (ref reported upper-case)",
      len(fv) == 1 and fv[0]["pos"] == 920 and fv[0]["ref"] == "G" and fv[0]["alt"] == "A" and fv[0]["alt_count"] == 3 and fv[0]["depth"] == 8, fv)
fv5 = find_variants(NEW, NEWREF, "nA", 700, 800, min_depth=3, min_alt_freq=0.1)
fv5z = find_variants(NEW, NEWREF, "nA", 700, 800, min_depth=3, min_alt_freq=0.1, min_base_quality=0)
print("  with min_base_quality=0 (overlap removal defeated: Skill table warns '-Q 0 with default overlap detection has subtle behavior'):", [(v["pos"], v["alt_count"], v["depth"]) for v in fv5z])
print("find_variants E5 window:", [(v['pos'], v['ref'], v['alt'], v['alt_count'], v['depth']) for v in fv5])
check(I, "C find_variants E5 overlap site nA:730: alt 3 of depth 6 (overlap removal, same as mpileup)",
      any(v["pos"] == 730 and v["alt_count"] == 3 and v["depth"] == 6 for v in fv5), [(v['pos'], v['alt_count'], v['depth']) for v in fv5])
fvN = [(v["pos"], v["ref"], v["alt"], v["alt_count"], v["depth"]) for v in fv5 if v["ref"] == "N" or v["alt"] == "N"]
check(I, "C find_variants reports only real SNVs: no site where the reference is N (nA:800-805) and no read-base 'N' allele (nA:790) is called a variant",
      not fvN, f"artifacts reported: {fvN} (planted truth: only nA:730 G>A)")
fvi = find_variants(NEW, NEWREF, "nA", 400, 450, min_depth=3, min_alt_freq=0.1)
check(I, "C SNV-only scope: find_variants reports nothing at the planted insertions nA:420/425 (docstring says indels are not reported)", fvi == [], fvi)

# example script from the copy
def ex(args):
    r = subprocess.run(f"python {SKILL}/examples/allele_counts.py {args}", shell=True, capture_output=True, text=True, executable="/bin/bash")
    return r.returncode, r.stdout, r.stderr
rc, out, err = ex(f"{NEW} 'HLA-A*01:01:01:01:120'")
check(I, "C examples/allele_counts.py on the colon contig: G 6 (60%) / A 4 (40%), depth 10, rc 0",
      rc == 0 and "Total depth: 10" in out and "G: 6 (60.0%)" in out and "A: 4 (40.0%)" in out, out.replace("\n", " | "))
rc, out, err = ex(f"{NEW} nA:1,420")
check(I, "C examples/allele_counts.py with thousands separator nA:1,420: ref-skip reads not counted (3 fwd '>' skipped): depth 3 (rev reads)", rc == 0 and "Total depth: 3" in out, out.replace("\n", " | ")[:200])

# ---------------- B. differential test pileup_text vs samtools mpileup, row for row -----------------
def diff_test(tag, bam, ref, informational=False, skip=()):
    tot_rows = 0
    results = {}
    with pysam.AlignmentFile(bam) as b:
        contigs = list(zip(b.references, b.lengths))
    for name, mpo, kw in COMBOS:
        nrows = ndiff = nonly_mp = nonly_py = 0
        firsts = []
        classes = Counter()
        for c, L in contigs:
            mpd, _, rc, err = mp_rows(ref, bam, mpo, c)
            py = {}
            for line in pileup_text(bam, ref, c, 0, L, **kw):
                f = line.split("\t")
                py[(f[0], int(f[1]))] = f
            keys = (set(mpd) | set(py)) - set(skip)
            for k in sorted(keys):
                nrows += 1
                a, bb = mpd.get(k), py.get(k)
                if a is None:
                    nonly_py += 1
                    firsts.append(("only-pysam", k, bb))
                elif bb is None:
                    nonly_mp += 1
                    firsts.append(("only-mpileup", k, a))
                elif a != bb:
                    ndiff += 1
                    firsts.append(("differ", k, a[3:], bb[3:]))
                    strip = lambda t: re.sub(r"[+-]\d+[A-Za-z]+", "", t)
                    classes["indel marker only (samtools prints an indel marker after a * / next to another indel; pileup_text does not)" if (strip(a[4]) == strip(bb[4]) and a[3] == bb[3] and a[5] == bb[5]) else "other"] += 1
        results[name] = (nrows, ndiff, nonly_mp, nonly_py, firsts[:2])
        ok = ndiff == 0 and nonly_mp == 0 and nonly_py == 0
        if informational:
            print(f"  [info] {tag} {name}: rows={nrows} differ={ndiff} only-mpileup={nonly_mp} only-pysam={nonly_py} first={firsts[:1]} | classes={dict(classes)}")
        else:
            check(I, f"B {tag} pileup_text == samtools mpileup {name!r}: row-for-row", ok,
                  f"rows={nrows} differ={ndiff} only-mpileup={nonly_mp} only-pysam={nonly_py}" + ("" if ok else f" first={firsts[:2]}"))
    return results

res_clean = diff_test("fuzz-clean", DATA + "/fz_clean.bam", DATA + "/fz_clean.fa")
res_planted = diff_test("planted new.bam (minus row nA:1410)", NEW, NEWREF, skip=[("nA", 1410)])
mr = mp_rows(NEWREF, NEW, "-B", "nA:1410-1410")[0][("nA", 1410)]
pr = next(pileup_text(NEW, NEWREF, "nA", 1409, 1410, compute_baq=False)).split("	")
check(I, "B edge: read with an insertion DIRECTLY followed by a deletion (10M2I2D10M): pileup_text prints the same row as samtools mpileup", mr == pr, f"mpileup {mr[4]!r} vs pileup_text {pr[4]!r}")
print("--- exotic CIGARs (leading/trailing I, adjacent I/D/N): informational, outside anything the Skill claims ---")
res_exotic = diff_test("fuzz-exotic", DATA + "/fz_exotic.bam", DATA + "/fz_exotic.fa", informational=True)

# col.n vs depth claim
with pysam.AlignmentFile(DATA + "/fz_clean.bam") as b:
    ndiff = tot = 0
    for c, L in zip(b.references, b.lengths):
        d, dn = py_depth(DATA + "/fz_clean.bam", DATA + "/fz_clean.fa", c, 0, L)
        for p in d:
            tot += 1
            ndiff += d[p] != dn[p]
check(I, "B Skill claim 'n counts reads before base-quality filter/overlap removal, so it exceeds mpileup depth': n != len(pileups) at many fuzz positions", ndiff > 0, f"{ndiff}/{tot} positions")
summary(I)
