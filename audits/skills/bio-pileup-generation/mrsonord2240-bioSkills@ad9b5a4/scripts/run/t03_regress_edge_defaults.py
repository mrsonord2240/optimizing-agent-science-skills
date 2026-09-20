#!/usr/bin/env python3
"""Input 3 (Edge, REGRESSION of pre-fix input 3): exact symbol decoding and the silent defaults, on planted synthetic data
(data/syn.bam truth in data/truth.json, data/deep.bam 9000x), then the shipped example on hostile region strings.
Every documented default in the fixed 'Pileup Options and Defaults' table is asserted from samtools 1.24 / bcftools 1.24 / pysam 0.24.1
behaviour, not from their help text alone (help text is also grepped)."""
import json, os, re, subprocess, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam

I = 3
DEEP, DF = DATA + "/deep.bam", DATA + "/deep.fa"
T = json.load(open(DATA + "/truth.json"))["truth"]["events"]
SK = open(SKILL + "/SKILL.md", encoding="utf-8").read()


def row(opts, contig, pos, bam=SYN, ref=SYNREF):
    d, _, rc, err = mp_rows(ref, bam, opts, f"{contig}:{pos}-{pos}")
    return d.get((contig, pos))


sy = lambda r: parse_bases(r[4], r[2])[1]
# ---- A. symbols
r = row("", "synA", 100); c = sy(r); s = T["snp"]
check(I, "SNP synA:100: '.' x14, ',' x16, 'C' x6, 'c' x4, depth 40", (c["ref_fwd"], c["ref_rev"], c["C"], c["c"], int(r[3])) == (14, 16, 6, 4, 40), dict(c))
r = row("", "synA", 81)
check(I, "'^]' x40 at read start (MAPQ 60 + 33 = ']')", r[4].count("^]") == 40)
r = row("", "synA", 130)
check(I, "'$' x40 at read end", sy(r)["$"] == 40)
r = row("", "synA", 200); c = sy(r)
check(I, "insertion row 200: '+2AC' x3, '+2ac' x2, depth 10 (Skill symbol table)", c["+AC"] == 3 and c["+ac"] == 2 and r[3] == "10", dict(c))
r = row("-B", "synA", 250); c = sy(r)
check(I, "-B deletion row 250: '-3CGT' x2, '-3cgt' x2, depth 8", c["-CGT"] == 2 and c["-cgt"] == 2 and r[3] == "8", dict(c))
r = row("", "synA", 250)
check(I, "Skill claim (BAQ section): default text pileup hides the deletion: depth 8 -> 4, no '-3CGT' marker", r[3] == "4" and sy(r)["delmark"] == 0, r[3:5])
check(I, "deleted bases synA:251-253 are '*' x4 with depth 8", all(sy(row("", "synA", p))["*"] == 4 and row("", "synA", p)[3] == "8" for p in (251, 252, 253)))
r = row("--reverse-del", "synA", 252)
check(I, "'#' for reverse-strand deletions with --reverse-del (Skill symbol table)", sy(r)["#"] == 2 and "--reverse-del" in SK, r[4])
r = row("", "synA", 400); c = sy(r)
check(I, "splice N-gap synA:400: '>' x2, '<' x1, depth 3", c[">"] == 2 and c["<"] == 1 and r[3] == "3")
d, _, _, _ = mp_rows(SYNREF, SYN, "", "synA:396-405")
check(I, "soft-clipped TTTTT never appear in rows 396-405", all(not re.search("[ACGTacgt]", re.sub(r"\^.", "", d[("synA", p)][4])) for p in range(396, 406)))
# ---- B. defaults
check(I, "default flags: depth 10 at synA:825 (DUP/SECONDARY/QCFAIL/UNMAP dropped); --ff 0 -> 16; --ff DUP -> 13",
      (row("", "synA", 825)[3], row("--ff 0", "synA", 825)[3], row("--ff DUP", "synA", 825)[3]) == ("10", "16", "13"), (row("", "synA", 825)[3], row("--ff 0", "synA", 825)[3], row("--ff DUP", "synA", 825)[3]))
check(I, "-q 10 drops 5 MAPQ-5 reads at synA:625 (10 -> 5)", (row("", "synA", 625)[3], row("-q 10", "synA", 625)[3]) == ("10", "5"))
check(I, "Options table -Q 13 default: synA:725 depth 4 default, 10 with -Q 0", (row("", "synA", 725)[3], row("-Q 0", "synA", 725)[3]) == ("4", "10"))
check(I, "overlap removal: depth 5 default vs 10 with -x / --disable-overlap-removal / --ignore-overlaps-removal",
      row("", "synA", 930)[3] == "5" and all(row(f, "synA", 930)[3] == "10" for f in ("-x", "--disable-overlap-removal", "--ignore-overlaps-removal")))
rc, out, err = sh(f"bcftools mpileup -f {SYNREF} -r synA:930 --ignore-overlaps -a FORMAT/DP {SYN} | grep -v '^#' | cut -f10")
rcd, outd, _ = sh(f"bcftools mpileup -f {SYNREF} -r synA:930 -a FORMAT/DP {SYN} | grep -v '^#' | cut -f10")
check(I, "bcftools spelling --ignore-overlaps works: DP 10 vs 5 default", out.strip().split(":")[1] == "10" and outd.strip().split(":")[1] == "5", f"{outd.strip()} / {out.strip()}")
check(I, "orphans (flag 65): dropped by default, 4 with -A (Skill table)", (row("", "synA", 985) is None or row("", "synA", 985)[3] == "0") and row("-A", "synA", 985)[3] == "4")
# bcftools defaults from behaviour: --ns default drops DUP, -Q default 1, --max-BQ 60
rc, out, err = sh(f"bcftools mpileup -f {SYNREF} -r synA:825 -a FORMAT/DP {SYN} | grep -v '^#' | cut -f10")
rc2, out2, err2 = sh(f"bcftools mpileup -f {SYNREF} -r synA:825 --ns 0 -a FORMAT/DP {SYN} | grep -v '^#' | cut -f10")
check(I, "bcftools default --ns = UNMAP,SECONDARY,QCFAIL,DUP: DP 10 default vs 16 with --ns 0 (Skill table: '--ff (bcftools --ns)')", out.strip().split(":")[1] == "10" and out2.strip().split(":")[1] == "16", f"{out.strip()} / {out2.strip()}")
rcq, outq, _ = sh(f"bcftools mpileup -f {SYNREF} -r synA:725 -B -a FORMAT/DP {SYN} | grep -v '^#' | cut -f10")
rcq5, outq5, _ = sh(f"bcftools mpileup -f {SYNREF} -r synA:725 -B -Q 5 -a FORMAT/DP {SYN} | grep -v '^#' | cut -f10")
rcq6, outq6, _ = sh(f"bcftools mpileup -f {SYNREF} -r synA:725 -B -Q 6 -a FORMAT/DP {SYN} | grep -v '^#' | cut -f10")
check(I, "bcftools default min-BQ is 1 (Q5 bases kept: DP 10 default, 10 at -Q 5, 4 at -Q 6); samtools default 13 drops them", outq.strip().split(":")[1] == "10" and outq5.strip().split(":")[1] == "10" and outq6.strip().split(":")[1] == "4", f"{outq.strip()} {outq5.strip()} {outq6.strip()}")
_, hs, _ = sh("samtools mpileup --help 2>&1")
_, hb, _ = sh("bcftools mpileup --help 2>&1")
print("help text extract (samtools mpileup):", [l.strip() for l in hs.splitlines() if re.search(r"--min-BQ|--max-depth|--excl-flags|--ff|--min-MQ|--max-BQ", l)][:6])
print("help text extract (bcftools mpileup):", [l.strip() for l in hb.splitlines() if re.search(r"--max-BQ|--ns|--min-BQ|--max-depth|--excl-flags|--incl-flags|--ignore-overlaps", l)][:8])
# ---- C. -a / -aa
def nrows(opts):
    rc, out, _ = sh(f"samtools mpileup -f {SYNREF} {opts} {SYN}")
    rr = mpileup_rows(out)
    return Counter(x[0] for x in rr), rr
cd, _ = nrows(""); ca, _ = nrows("-a"); caa, rowsaa = nrows("-aa")
check(I, "Options table: -a = every position of contigs that have reads (synA 1000, synC 300; no synB); -aa also the read-less contig synB (500 rows)",
      ca["synA"] == 1000 and ca["synC"] == 300 and "synB" not in ca and caa["synB"] == 500 and cd["synA"] < 1000 and "synB" not in cd, (dict(cd), dict(ca), dict(caa)))
zr = [x for x in rowsaa if x[0] == "synB"][0]
check(I, "zero-depth row: 'synB 1 <ref> 0 * *'", zr[3] == "0" and zr[4] == "*" and zr[5] == "*")
# ---- D. max depth
def dep(tool, opts):
    if tool == "s":
        rc, out, err = sh(f"samtools mpileup -f {DF} {opts} -r synD:1-1 {DEEP}")
        return int(mpileup_rows(out)[0][3]), err.strip()[-90:]
    rc, out, err = sh(f"bcftools mpileup -f {DF} {opts} -r synD:1 -a FORMAT/DP {DEEP} | grep -v '^#' | cut -f10")
    return int(out.strip().split(":")[1]), err.strip()[-90:]
ds = {o: dep("s", o)[0] for o in ("", "-d 8000", "-d 0", "-d 1000000", "-d 250")}
db = {o: dep("b", o)[0] for o in ("", "-d 250", "-d 0", "-d 1000000", "-d 100000")}
check(I, "samtools: default caps 9000 reads at 8000; -d 0 and -d 1000000 give 9000; -d 250 gives 250", ds == {"": 8000, "-d 8000": 8000, "-d 0": 9000, "-d 1000000": 9000, "-d 250": 250}, ds)
check(I, "bcftools: default 250; -d 0, -d 1000000, -d 100000 give 9000 (Skill cheat sheet 'Capture / exome: -d 0' now safe)", db == {"": 250, "-d 250": 250, "-d 0": 9000, "-d 1000000": 9000, "-d 100000": 9000}, db)
with pysam.AlignmentFile(DEEP) as b:
    got = {}
    for k, kw in (("default", {}), ("max_depth=0", dict(max_depth=0)), ("max_depth=8000", dict(max_depth=8000)), ("max_depth=1000000", dict(max_depth=1000000)), ("max_depth=250", dict(max_depth=250))):
        it = b.pileup("synD", 0, 1, truncate=True, **kw)
        col = next(it)
        got[k] = (len(col.pileups), col.n)
        del it
check(I, "Skill claim: pysam max_depth default 8000 and max_depth=0 is NOT unlimited (still 8000); max_depth=1000000 -> 9000",
      got["default"][0] == 8000 and got["max_depth=0"][0] == 8000 and got["max_depth=1000000"][0] == 9000 and got["max_depth=250"][0] == 250, got)
sh_c = subprocess.run(f"echo", shell=True)
# cheat-sheet rows all run on deep.bam and none caps at 250
rows_cs = {"germline `-q 20 -Q 20 -d 0`": "-q 20 -Q 20 -d 0", "exome `-q 20 -Q 20 -d 0`": "-q 20 -Q 20 -d 0", "tumor `-q 1 -Q 13 -d 0 -B`": "-q 1 -Q 13 -d 0 -B",
           "ARTIC `-aa -A -d 600000 -B -Q 20`": "-aa -A -d 600000 -B -Q 20", "ONT `-q 30 -Q 0 -B -d 0`": "-q 30 -Q 0 -B -d 0"}
ok = {}
for k, o in rows_cs.items():
    ok[k] = dep("s", o)[0]
check(I, "cheat sheet rows on the 9000x BAM never cap (depth 9000 for every row that sets -d 0 / -d 600000)", all(v == 9000 for v in ok.values()) and "Capture / exome | `-q 20 -Q 20 -d 0`" in SK.replace("  ", " "), ok)
# ---- E. BAQ and no -f
o1 = [x for x in mpileup_rows(sh(f"samtools mpileup -f {SYNREF} -r synA:150-300 {SYN}")[1])]
o2 = [x for x in mpileup_rows(sh(f"samtools mpileup -B -f {SYNREF} -r synA:150-300 {SYN}")[1])]
check(I, "BAQ default changes qualities near the planted indels vs -B", any(a[5] != b[5] for a, b in zip(o1, o2)))
rc, out, err = sh(f"samtools mpileup -r synA:100-100 {SYN}")
check(I, "Common Errors: samtools mpileup without -f succeeds with reference column N", rc == 0 and mpileup_rows(out)[0][2] == "N", out[:40])
rc, out, err = sh(f"bcftools mpileup -r synA:100 {SYN} 2>&1 | head -3")
check(I, "Common Errors: bcftools mpileup without -f refuses: 'requires the --fasta-ref option'", "requires the --fasta-ref option" in out and "requires the --fasta-ref option" in SK, out[:120])
rc, out, err = sh(f"samtools mpileup -B -E -f {SYNREF} -r synA:100-100 {SYN} 2>&1")
check(I, "BAQ table: -B and -E cannot be combined (Skill) -> samtools refuses", "cannot be combined" in out and "cannot be combined with `-B`" in SK and "cannot combine with `-E`" in SK, out.strip()[:100])
rc, out, err = sh(f"samtools mpileup -g -f {SYNREF} {SYN} 2>&1 | head -2")
check(I, "Deprecation section: samtools mpileup -g no longer exists (removed in 1.15)", "invalid option" in out, out.strip()[:80])

# ---- F. shipped example on hostile input
W = WORK + "/t03"; os.makedirs(W, exist_ok=True)
EX = SKILL + "/examples/allele_counts.py"
def run(args):
    r = subprocess.run(f"python {EX} {args}", shell=True, capture_output=True, text=True, executable="/bin/bash")
    return r.returncode, r.stdout.strip(), r.stderr.strip()
sh(f"cp {SYN} {W}/noidx.bam")     # BAM without its index
sh(f"printf 'not a bam\\n' > {W}/garbage.bam")
cases = {
    "range synA:100-110": (f"{SYN} synA:100-110", "ranges are not supported"),
    "missing colon": (f"{SYN} synA100", "expected <contig>:<1-based position>"),
    "position 0": (f"{SYN} synA:0", "expected <contig>:<1-based position>"),
    "unknown contig": (f"{SYN} nosuch:100", "is not in the BAM header"),
    "unindexed BAM": (f"{W}/noidx.bam synA:100", "has no index"),
    "garbage file": (f"{W}/garbage.bam synA:100", "cannot read"),
    "nonexistent file": (f"{W}/nope.bam synA:100", "cannot read"),
    "letters as position": (f"{SYN} synA:abc", "expected <contig>:<1-based position>"),
    "empty position": (f"{SYN} synA:", "expected <contig>:<1-based position>"),
}
for name, (args, needle) in cases.items():
    rc, out, err = run(args)
    check(I, f"example, {name}: rc 1, last stderr line is 'Error: ...' naming the problem, no traceback", rc == 1 and "Traceback" not in err and err.splitlines()[-1].startswith("Error:") and needle in err.splitlines()[-1], f"rc={rc} err={err[-140:]!r}")
rc, out, err = run(f"{SYN} synA:1,000")
check(I, "example: thousands separator synA:1,000 accepted (position 1000; real depth from mpileup)", rc == 0 and "Position: synA:1000" in out, out.replace("\n", "|")[:100])
rc, out, err = run(f"{SYN} synA:5000")
print("example beyond contig end synA:5000 ->", rc, out.replace("\n", "|")[:100], err[:100])
check(I, "example: position beyond contig end does not print a traceback", "Traceback" not in err, f"rc={rc} out={out[:60]!r} err={err[:80]!r}")
rc, out, err = run(f"{SYN}")
check(I, "example: missing region -> usage line, rc 1", rc == 1 and "Usage" in out)
sh(f"rm -f {W}/*.bam")
summary(I)
