#!/usr/bin/env python3
"""Input 3 (Edge): 'Decode the base column exactly (ins/del/splice/^/$), and tell me what the defaults silently drop (flags, MAPQ,
baseQ/BAQ, overlaps, orphans, zero-depth rows, max depth)'.  Ground truth = planted synthetic BAM (data/truth.json); no sample uses
tool output as its own oracle."""
import json, os, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam

I = 3
SYN = DATA + "/syn.bam"; SF = DATA + "/syn.fa"
DEEP = DATA + "/deep.bam"; DF = DATA + "/deep.fa"
T = json.load(open(DATA + "/truth.json"))["truth"]["events"]

def mp(opts, region, bam=SYN, ref=SF):
    rc, out, err = sh(f"samtools mpileup {('-f ' + ref) if ref else ''} {opts} {('-r ' + region) if region else ''} {bam}")
    return {int(r[1]) if False else (r[0], int(r[1])): r for r in mpileup_rows(out)}, err

def row(opts, contig, pos, bam=SYN, ref=SF):
    d, e = mp(opts, f"{contig}:{pos}-{pos}", bam, ref)
    return d.get((contig, pos)), e

# ---------------- A. symbol decoding vs planted truth
r, _ = row("", "synA", 100)
n, c = parse_bases(r[4], r[2])
s = T["snp"]
check(I, "SNP synA:100: '.' x14, ',' x16, alt forward 'C' x6, alt reverse 'c' x4, depth 40", (c["ref_fwd"], c["ref_rev"], c["C"], c["c"], int(r[3])) == (s["ref_fwd"], s["ref_rev"], 6, 4, 40), dict(c))
r, _ = row("", "synA", 81)
n, c = parse_bases(r[4], r[2])
check(I, "'^Q' at read start: 40 read starts at synA:81, each '^]' (MAPQ 60 + 33 = ']')", c["^"] == 40 and r[4].count("^]") == 40, f"^ count {c['^']}, '^]' count {r[4].count('^]')}")
r, _ = row("", "synA", 130)
check(I, "'$' at read end: 40 read ends at synA:130 (the '$' precedes the end position's next row, i.e. belongs to the last base)", parse_bases(r[4], r[2])[1]["$"] == 40, r[4][:60])
r, _ = row("", "synA", 200)
n, c = parse_bases(r[4], r[2])
check(I, "insertion after synA:200 appears on row 200 as '+2AC' x3 (fwd) and '+2ac' x2 (rev); depth 10 (insertion adds no depth)", c["+AC"] == 3 and c["+ac"] == 2 and r[3] == "10", f"{dict(c)} depth={r[3]}")
r, _ = row("-B", "synA", 250)
n, c = parse_bases(r[4], r[2])
dseq = T["del"]["deleted_seq"]
check(I, f"with -B: deletion of synA:251-253 appears on row 250 as '-3{dseq}' x2 (fwd) and '-3{dseq.lower()}' x2 (rev), depth 8", c["-" + dseq] == 2 and c["-" + dseq.lower()] == 2 and r[3] == "8", f"{dict(c)} depth={r[3]}")
r, _ = row("", "synA", 250)
n, c = parse_bases(r[4], r[2])
check(I, "DEFAULT (BAQ on): the same deletion reads are dropped at 248-250 (baseQ after BAQ < 13): depth 4, no '-3CGT' marker -- the deletion is invisible in default text pileup", r[3] == "4" and c["delmark"] == 0, f"depth={r[3]} marks={c['delmark']} (SKILL says BAQ 'hurts indel detection sensitivity' but not that default mpileup text loses the indel)")
rows_del = [row("", "synA", p)[0] for p in (251, 252, 253)]
check(I, "deleted bases at synA:251-253 shown as '*' x4 with depth 8 (deleted reads stay in depth)", all(parse_bases(x[4], x[2])[1]["*"] == 4 and x[3] == "8" for x in rows_del), [(x[3], x[4][:20]) for x in rows_del])
r, _ = row("--reverse-del", "synA", 252)
check(I, "--reverse-del marks reverse-strand deletions '#' (option not in the Skill)", parse_bases(r[4], r[2])[1]["#"] == 2, r[4])
r, _ = row("", "synA", 400)
n, c = parse_bases(r[4], r[2])
check(I, "splice N-gap: at synA:400 '>' x2 (fwd) and '<' x1 (rev), depth 3", c[">"] == 2 and c["<"] == 1 and r[3] == "3", f"{dict(c)} depth={r[3]}")
d, _ = mp("", "synA:396-405")
check(I, "soft-clip: the clipped 'TTTTT' never appear in rows 396-405 (no T/t/A/C/G letters; only '.' ',' '^]' and ref-skips)", all(not re.search("[ACGTacgt]", re.sub(r'\^.', '', d[("synA", p)][4])) for p in range(396, 406)), {p: d[("synA", p)][4] for p in (399, 401, 402)})

# ---------------- B. what the DEFAULTS drop (none of this is stated in the Skill)
r, _ = row("", "synA", 825)
check(I, "default excluded flags: depth 10 at synA:825 (3 DUP, 2 SECONDARY, 1 QCFAIL, 2 UNMAP silently excluded)", r[3] == "10", r[3])
r16, _ = row("--ff 0", "synA", 825)
check(I, "--ff 0 makes them visible: depth 16 (unmapped stay excluded)", r16[3] == "16", r16[3])
r13, _ = row("--ff DUP", "synA", 825)
check(I, "--ff DUP alone (named flag) -> depth 13 (10 + 2 secondary + 1 qcfail)", r13[3] == "13", r13[3])
rq0, _ = row("", "synA", 625); rq10, _ = row("-q 10", "synA", 625)
check(I, "-q 10 drops the 5 MAPQ-5 reads at synA:625 (depth 10 -> 5); '^&' shows MAPQ 5", rq0[3] == "10" and rq10[3] == "5" and row("", "synA", 601)[0][4].count("^&") == 5, f"{rq0[3]}->{rq10[3]}")
rb, _ = row("", "synA", 725)
rb0, _ = row("-Q 0", "synA", 725); rbB, _ = row("-B -Q 0", "synA", 725); rbBq, _ = row("-B", "synA", 725)
check(I, "baseQ: default -Q 13 drops the six Q5 bases at synA:725 (depth 4); -Q 0 restores 10 (6 alt)", rb[3] == "4" and rb0[3] == "10" and rbBq[3] == "4", f"default={rb[3]} -Q0={rb0[3]} -B={rbBq[3]} -B -Q0={rbB[3]}")
ro, _ = row("", "synA", 930); rox, _ = row("-x", "synA", 930)
check(I, "overlap removal: depth 5 by default vs 10 with -x at synA:930", ro[3] == "5" and rox[3] == "10", f"{ro[3]} vs {rox[3]}")
for flag in ("--disable-overlap-removal", "--ignore-overlaps-removal"):
    rr, _ = row(flag, "synA", 930)
    check(I, f"long option {flag} (samtools) accepted", rr is not None and rr[3] == "10", rr and rr[3])
rc, out, err = sh(f"bcftools mpileup -f {SF} -r synA:930 --ignore-overlaps -a FORMAT/DP {SYN} | grep -v '^#' | cut -f10")
rcd, outd, _ = sh(f"bcftools mpileup -f {SF} -r synA:930 -a FORMAT/DP {SYN} | grep -v '^#' | cut -f10")
print("bcftools DP overlaps default / --ignore-overlaps:", outd.strip(), out.strip())
check(I, "bcftools mpileup --ignore-overlaps is the bcftools spelling (accepted) and changes DP 5 -> 10", "5" in outd.split(":")[1] and out.strip().split(":")[1] == "10", f"{outd.strip()} / {out.strip()}")
ro0, _ = row("", "synA", 985); roA, _ = row("-A", "synA", 985)
d0, _ = mp("", "synA:971-1000")
check(I, "orphans (flag 65, paired not proper): depth 0 rows / no data by default, 4 with -A", (ro0 is None or ro0[3] == "0") and roA[3] == "4", f"default={ro0[3] if ro0 else None} -A={roA[3]}")

# ---------------- C. zero-depth rows: -a / -aa
def nrows(opts):
    rc, out, _ = sh(f"samtools mpileup -f {SF} {opts} {SYN}")
    rr = mpileup_rows(out)
    return Counter(x[0] for x in rr), rr
cd, rows0 = nrows("")
ca, rowsa = nrows("-a")
caa, rowsaa = nrows("-aa")
print("rows per contig default / -a / -aa:", dict(cd), dict(ca), dict(caa))
check(I, "default mpileup omits uncovered positions (synA rows < 1000) and empty contigs", cd["synA"] < 1000 and "synB" not in cd, dict(cd))
check(I, "-a: every position of contigs that have reads (synA 1000, synC 300), no rows for read-less synB", ca["synA"] == 1000 and ca["synC"] == 300 and "synB" not in ca, dict(ca))
check(I, "-aa additionally emits the read-less contig synB (500 rows, depth 0)", caa["synB"] == 500 and caa["synA"] == 1000 and caa["synC"] == 300, dict(caa))
zr = [x for x in rowsaa if x[0] == "synB"][0]
check(I, "zero-depth row format: 'synB 1 <ref> 0 * *'", zr[3] == "0" and zr[4] == "*" and zr[5] == "*" and zr[2] == pysam.FastaFile(SF).fetch("synB", 0, 1).upper(), zr)

# ---------------- D. max depth (Skill: 'Default 8000 silently truncates')
def depth_at(opts, tool="samtools", pos=1):
    if tool == "samtools":
        rc, out, err = sh(f"samtools mpileup -f {DF} {opts} -r synD:{pos}-{pos} {DEEP}")
        rr = mpileup_rows(out)
        return int(rr[0][3]) if rr else None, err.strip()[-80:]
    rc, out, err = sh(f"bcftools mpileup -f {DF} {opts} -r synD:{pos} -a FORMAT/DP {DEEP} | grep -v '^#' | cut -f10")
    return (int(out.strip().split(':')[1]) if out.strip() else None), err.strip()[-80:]
d_def, _ = depth_at("")
d_0, _ = depth_at("-d 0")
d_big, _ = depth_at("-d 1000000")
d_250, _ = depth_at("-d 250")
check(I, "samtools mpileup default caps 9000 reads at 8000 (Skill: 'default -d 8000 silently truncates')", d_def == 8000, d_def)
check(I, "samtools mpileup -d 0 = no cap (Skill cheat-sheet uses -d 0): depth 9000", d_0 == 9000, d_0)
check(I, "samtools mpileup -d 1000000 -> 9000", d_big == 9000, d_big)
check(I, "Skill cheat-sheet 'Capture / exome: -d 250' truncates 9000-deep amplicon-like data to 250 (contradicts its own 'Critical Trap')", d_250 == 250, f"depth {d_250}")
b_def, _ = depth_at("", "bcftools")
b_big, _ = depth_at("-d 1000000", "bcftools")
b_0, e0 = depth_at("-d 0", "bcftools")
check(I, "bcftools mpileup default -d 250 caps DP at 250 (Skill claim)", b_def == 250, b_def)
check(I, "bcftools mpileup -d 1000000 -> DP 9000 (Skill recommendation)", b_big == 9000, b_big)
print("bcftools -d 0 gives DP =", b_0, e0)
check(I, "bcftools mpileup -d 0 (Skill uses `-d 0` only for samtools; check if it is 'no cap' here too)", b_0 == 9000, f"DP={b_0}")
pys = pysam.AlignmentFile(DEEP)
col = next(pys.pileup("synD", 0, 1, truncate=True))
col2 = next(pysam.AlignmentFile(DEEP).pileup("synD", 0, 1, truncate=True, max_depth=1000000))
check(I, "SKILL pysam snippets (no max_depth) also truncate at 8000 silently: n=8000 with defaults, 9000 with max_depth=1e6", col.n == 8000 and col2.n == 9000, f"defaults n={col.n}, max_depth=1e6 n={col2.n}")

# ---------------- E. BAQ (Skill: 'BAQ on by default with -f ... reduces base quality near indels')
_, o_def, _ = sh(f"samtools mpileup -f {SF} -r synA:150-300 {SYN}")
_, o_B, _ = sh(f"samtools mpileup -B -f {SF} -r synA:150-300 {SYN}")
dq = {}
for a, b in zip(mpileup_rows(o_def), mpileup_rows(o_B)):
    if a[5] != b[5]:
        dq[int(a[1])] = (a[5][:6], b[5][:6])
print("positions with different base-quality strings default vs -B (150-300):", len(dq), list(dq.items())[:6])
check(I, "BAQ (default with -f) alters base qualities near the planted indels at synA:200/250 versus -B", len(dq) > 0 and any(190 <= p <= 260 for p in dq), f"{len(dq)} positions differ, e.g. {list(dq.items())[:3]}")
rc, out, err = sh(f"samtools mpileup -r synA:100-100 {SYN}")
print("mpileup without -f rc, out, err:", rc, out.strip()[:80], err.strip()[:80])
check(I, "Common Errors row 'No FASTA reference | Missing -f' : samtools mpileup without -f actually succeeds (reference column N)", rc == 0 and mpileup_rows(out)[0][2] == "N", f"rc={rc} out={out.strip()[:60]!r}")
rc, out, err = sh(f"bcftools mpileup -r synA:100 {SYN} | head -3")
print("bcftools mpileup without -f:", out[:100], err.strip()[:200])
check(I, "bcftools mpileup without -f emits a specific error", "reference" in (out + err).lower() or "-f" in (out + err), (out + err).strip()[:150])
summary(I)
