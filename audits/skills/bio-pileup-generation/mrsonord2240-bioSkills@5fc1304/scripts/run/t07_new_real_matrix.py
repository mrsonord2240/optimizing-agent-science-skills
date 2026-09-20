#!/usr/bin/env python3
"""Input 7 (NEW, re-auditor): the fixer's central claim — 'the pysam parameters in the Skill's table reproduce samtools mpileup
position by position' — re-tested on MY data: 4 real BAMs (human chr22 DNA, human chr22 spliced RNA-seq, 1000G chr20, ARTIC nanopore),
the two synthetic BAMs, and probes for the claims that were NOT in the fixer's list: no stepper argument + fastafile and BAQ, stepper='nofilter'
vs --ff 0, flag_require vs --rf, existing-BQ-tag reuse vs -E, max_depth=0. Also the usage-guide dedup (nothing lost) as a token diff."""
import os, re, shutil, sys, time
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions
import pysam

I = 7
P = AFDATA
W = WORK + "/t07"; os.makedirs(W, exist_ok=True)
SK = open(SKILL + "/SKILL.md", encoding="utf-8").read()
UG = open(SKILL + "/usage-guide.md", encoding="utf-8").read()
pt = load_functions("SKILL.md")["pileup_text"]
G1K = P + "/1000g/HG00349.chr20_1400000-1500000.bam"; G1KREF = P + "/1000g/chr20_padded_1500000.fa"
for src, name in ((P + "/sarscov2/sars-cov-2_v5.3.2.nanopore.bam", "artic.bam"), (HUMAN + "/test.rna.paired_end.sorted.bam", "rna.bam")):
    shutil.copy(src, f"{W}/{name}")
    sh(f"samtools index {W}/{name}", check=True)
ART, ARTREF, RNA = W + "/artic.bam", P + "/sarscov2/MN908947.3.fasta", W + "/rna.bam"
DS = [("human chr22 DNA", HBAM, HREF, "chr22", 0, 4700),
      ("human chr22 RNA-seq (spliced)", RNA, HREF, "chr22", 0, 40001),
      ("1000G chr20", G1K, G1KREF, "chr20", 1400000, 1500000),
      ("ARTIC nanopore", ART, ARTREF, "MN908947.3", 0, 29903),
      ("synthetic syn.bam", SYN, SYNREF, "synA", 0, 1000),
      ("synthetic new.bam", NEW, NEWREF, "nA", 0, 1500)]

# ---------- A. depth: Skill table rows, pysam bam.pileup vs samtools mpileup, position by position
TABLE = [  # (label, samtools options, pysam kwargs, needs fastafile)
    ("`-f ref` default (BAQ): stepper='samtools' + fastafile", "", dict(stepper="samtools"), True),
    ("pysam defaults == `-B`", "-B", {}, False),
    ("`-Q 13` == min_base_quality=13 (with -B)", "-B -Q 13", dict(min_base_quality=13), False),
    ("`-Q 0` == min_base_quality=0 (with -B)", "-B -Q 0", dict(min_base_quality=0), False),
    ("`-q 20` == min_mapping_quality=20 (-B)", "-B -q 20", dict(min_mapping_quality=20), False),
    ("`-x` == ignore_overlaps=False (-B)", "-B -x", dict(ignore_overlaps=False), False),
    ("`-A` == ignore_orphans=False (-B)", "-B -A", dict(ignore_orphans=False), False),
    ("`--ff 0` == flag_filter=0 (-B)", "-B --ff 0", dict(flag_filter=0), False),
    ("`-d 20` == max_depth=20 (-B)", "-B -d 20", dict(max_depth=20), False),
    ("`-E` == redo_baq=True + stepper='samtools' + fastafile", "-E", dict(stepper="samtools", redo_baq=True), True),
    ("`-C 50` == adjust_capq_threshold=50 + stepper='samtools' + fastafile", "-C 50", dict(stepper="samtools", adjust_capq_threshold=50), True),
    ("everything off: -B -Q0 -q0 -x -A --ff 0", "-B -Q 0 -q 0 -x -A --ff 0", dict(min_base_quality=0, min_mapping_quality=0, ignore_overlaps=False, ignore_orphans=False, flag_filter=0), False),
]
for dname, bam, ref, c, s, e in DS:
    tot_ok = 0
    fails = []
    mpd_cache = {}
    for label, mo, kw, fa in TABLE:
        mpd, _, rc, err = mp_rows(ref, bam, mo, f"{c}:{s + 1}-{e}", extra="-d 1000000" if "-d" not in mo else "")
        kw2 = dict(kw)
        if fa:
            kw2["_fasta"] = True
        if "max_depth" not in kw2:
            kw2["max_depth"] = 1000000
        d, dn = py_depth(bam, ref, c, s, e, **kw2)
        pos = set(p for (_, p) in mpd) | set(d)
        diffs = [(p, mpd.get((c, p), [0, 0, 0, 0])[3], d.get(p, 0)) for p in sorted(pos) if int(mpd.get((c, p), [0, 0, 0, 0])[3]) != d.get(p, 0)]
        if diffs:
            fails.append((label, len(diffs), len(pos), diffs[:2]))
        else:
            tot_ok += 1
    check(I, f"A depth, {dname}: {len(TABLE)} Skill-table rows, pysam len(pileups) == samtools mpileup depth at every position", not fails, f"{tot_ok}/{len(TABLE)} rows equal" + ("" if not fails else f"; FAIL {fails[:3]}"))

# ---------- B. pileup_text row-for-row on real data
def rows_eq(dname, bam, ref, c, s, e, mo, kw):
    mpd, _, rc, err = mp_rows(ref, bam, mo, f"{c}:{s + 1}-{e}")
    py = {}
    t = time.time()
    for line in pt(bam, ref, c, s, e, **kw):
        f = line.split("\t")
        py[(f[0], int(f[1]))] = f
    keys = set(mpd) | set(py)
    diff = [(k, mpd.get(k, [None] * 6)[3:], py.get(k, [None] * 6)[3:]) for k in sorted(keys) if mpd.get(k) != py.get(k)]
    check(I, f"B pileup_text == samtools mpileup {mo or 'default'!r}, {dname}: row-for-row", not diff, f"rows={len(keys)} differ={len(diff)} ({time.time() - t:.1f}s)" + (f" first={diff[:1]}" if diff else ""))
    return len(keys)

n_rows = 0
for dname, bam, ref, c, s, e in DS[:4]:
    n_rows += rows_eq(dname, bam, ref, c, s, e, "", {})
    n_rows += rows_eq(dname, bam, ref, c, s, e, "-B", dict(compute_baq=False))
n_rows += rows_eq("human chr22 DNA", HBAM, HREF, "chr22", 0, 4700, "-q 20 -Q 20 -x -A", dict(min_mapping_quality=20, min_base_quality=20, ignore_overlaps=False, ignore_orphans=False))
n_rows += rows_eq("1000G chr20", G1K, G1KREF, "chr20", 1400000, 1500000, "--ff 0 -Q 0", dict(flag_filter=0, min_base_quality=0))
print("total rows compared row-for-row on real data:", n_rows)

# ---------- C. claims outside the fixer's list: stepper / BAQ
def depth_at(bam, ref, contig, pos1, **kw):
    d, dn = py_depth(bam, ref, contig, pos1 - 1, pos1, **kw)
    return d.get(pos1)


cands = {
    "no stepper argument, no fastafile": dict(),
    "no stepper argument + fastafile": dict(_fasta=True),
    "stepper='samtools', no fastafile": dict(stepper="samtools"),
    "stepper='samtools' + fastafile": dict(stepper="samtools", _fasta=True),
    "stepper='samtools' + fastafile + compute_baq=False": dict(stepper="samtools", _fasta=True, compute_baq=False),
    "no stepper argument + fastafile + compute_baq=False": dict(_fasta=True, compute_baq=False),
    "no stepper argument + fastafile + redo_baq=True": dict(_fasta=True, redo_baq=True),
}
K_ALL_FA = "no stepper argument + fastafile"
got = {k: depth_at(SYN, SYNREF, "synA", 250, **v) for k, v in cands.items()}
mp_def = mp_rows(SYNREF, SYN, "", "synA:250-250")[0][("synA", 250)][3]
mp_B = mp_rows(SYNREF, SYN, "-B", "synA:250-250")[0][("synA", 250)][3]
print("depth at synA:250 (deletion reads: BAQ hides them, mpileup default", mp_def, "vs -B", mp_B, "):")
for k, v in got.items():
    print("   ", k, "->", v)
check(I, "pysam stepper='samtools' + fastafile applies BAQ (== mpileup default 4) and compute_baq=False restores -B (8)", got["stepper='samtools' + fastafile"] == int(mp_def) == 4 and got["stepper='samtools' + fastafile + compute_baq=False"] == int(mp_B) == 8, got)
# UPDATED for round 2: the Skill now says BAQ follows fastafile under either stepper
check(I, "Round-2 SKILL claim 'BAQ is switched on by fastafile' (called WITHOUT a stepper argument; pysam 0.24.1's default is 'samtools', not 'all': see input 7 / 11_baq_rf.py): depth at synA:250 with no stepper argument + fastafile equals the BAQ depth 4",
      got[K_ALL_FA] == int(mp_def) == 4, f"no-stepper-arg+fastafile gives {got[K_ALL_FA]} (mpileup -B {mp_B}, default {mp_def})")
check(I, "SKILL claim 'pysam defaults equal `-B`': pileup() with no stepper argument and no fastafile equals -B", got["no stepper argument, no fastafile"] == int(mp_B), got["no stepper argument, no fastafile"])
# ---------- D. stepper='nofilter' vs --ff 0 (new.bam nA:1120: 6 normal, 2 supplementary, 2 dup, 2 orphan(65), 2 mate-unmapped(73), 2 proper(99))
m = {o: int(mp_rows(NEWREF, NEW, o, "nA:1120-1120")[0][("nA", 1120)][3]) for o in ("-B", "-B --ff 0", "-B --ff 0 -A", "-B -A")}
p = {k: depth_at(NEW, NEWREF, "nA", 1120, **kw) for k, kw in {"default": {}, "flag_filter=0": dict(flag_filter=0), "flag_filter=0, ignore_orphans=False": dict(flag_filter=0, ignore_orphans=False), "stepper='nofilter'": dict(stepper="nofilter")}.items()}
print("mpileup:", m, "| pysam:", p)
check(I, "Skill table: `--ff 0` == flag_filter=0 (12); `--ff 0 -A` == flag_filter=0 + ignore_orphans=False (16); default 10", m["-B --ff 0"] == p["flag_filter=0"] == 12 and m["-B --ff 0 -A"] == p["flag_filter=0, ignore_orphans=False"] == 16 and p["default"] == 10, (m, p))
check(I, "Skill claim: stepper='nofilter' also drops the orphan filter so it is NOT `--ff 0` (nofilter == 16 == --ff 0 -A, != 12)", p["stepper='nofilter'"] == 16 and p["stepper='nofilter'"] != m["-B --ff 0"], p)
# ---------- E. flag_require vs --rf (multi-bit)
fz, fzref = DATA + "/fz_clean.bam", DATA + "/fz_clean.fa"
res = {}
for rf in (16, 17, 3, 2049):
    mpd, _, _, _ = mp_rows(fzref, fz, f"-B --rf {rf}", "fz1")
    d, _ = py_depth(fz, fzref, "fz1", 0, 3000, flag_require=rf)
    nd = sum(1 for k in set(p for (_, p) in mpd) | set(d) if int(mpd.get(("fz1", k), [0, 0, 0, 0])[3]) != d.get(k, 0))
    res[rf] = nd
print("positions where samtools --rf N and pysam flag_require=N disagree (fz_clean, fz1):", res)
check(I, "Skill table: `--rf FLAGS` == flag_require=INT holds for single-bit masks (16) AND multi-bit masks (17, 3, 2049)", all(v == 0 for v in res.values()), res)
# bcftools --nu vs samtools --rf, single reads set
b_nu = sh(f"bcftools mpileup -f {NEWREF} -r nA:1120 --nu 65 -a FORMAT/DP -B -A {NEW} | grep -v '^#' | cut -f10")[1].strip()
s_rf = mp_rows(NEWREF, NEW, "-B -A --rf 65", "nA:1120-1120")[0][("nA", 1120)][3]
print("nA:1120 with mask 65: samtools --rf 65 -A depth", s_rf, "| bcftools --nu 65 DP", b_nu)
b_nu_dp = int(b_nu.split(":")[1])
# UPDATED for round 2 (bcftools calls now pass -A like the samtools call, so orphan handling is equal): the row is now `--rf` (bcftools `--lu`) = any bit; `--nu` = ALL bits (a different, documented rule)
b_lu = sh(f"bcftools mpileup -f {NEWREF} -r nA:1120 --lu 65 -a FORMAT/DP -B -A {NEW} | grep -v '^#' | cut -f10")[1].strip()
b_lu_dp = int(b_lu.split(":")[1])
# (this position does not discriminate any-bit from all-bit -- input 9 (11_baq_rf.py) does, on 6 masks against independent subsets)
check(I, "Round-2 Options table: `--rf` (bcftools `--lu`) keeps any-bit reads: samtools --rf 65 == bcftools --lu 65 at nA:1120",
      b_lu_dp == int(s_rf), f"samtools --rf 65 keeps {s_rf} reads (any bit set); bcftools --lu 65 keeps {b_lu_dp}; bcftools --nu 65 keeps {b_nu_dp} (skips reads with ANY bit unset = requires ALL bits; bcftools help: 'Skip reads with any of the bits unset')")

# ---------- F. existing BQ tag: reuse vs -E vs -B
bq = W + "/bq.bam"
with pysam.AlignmentFile(SYN) as src, pysam.AlignmentFile(bq, "wb", template=src) as out:
    for a in src.fetch():
        if a.query_name.startswith("snpF") and int(a.query_name[4:]) < 5:
            a.set_tag("BQ", "h" * a.query_length, "Z")          # 'h' = 64+40: subtract 40 from every base quality
        out.write(a)
sh(f"samtools index {bq}")
mdef = int(mp_rows(SYNREF, bq, "", "synA:100-100")[0][("synA", 100)][3])
mE = int(mp_rows(SYNREF, bq, "-E", "synA:100-100")[0][("synA", 100)][3])
mB = int(mp_rows(SYNREF, bq, "-B", "synA:100-100")[0][("synA", 100)][3])
pdef = depth_at(bq, SYNREF, "synA", 100, stepper="samtools", _fasta=True)
pE = depth_at(bq, SYNREF, "synA", 100, stepper="samtools", _fasta=True, redo_baq=True)
print("BQ-tag test: samtools default", mdef, "-E", mE, "-B", mB, "| pysam samtools+fasta", pdef, "redo_baq", pE)
check(I, "BAQ table: an existing BQ tag is reused by default (5 reads with BQ='h' lose their bases: depth 35), `-E` recomputes and ignores it (40), `-B` ignores it (40)", (mdef, mE, mB) == (35, 40, 40), (mdef, mE, mB))
check(I, "pysam table: stepper='samtools' + fastafile reuses the BQ tag like the default (35); redo_baq=True == -E (40)", (pdef, pE) == (35, 40), (pdef, pE))

# ---------- G. usage-guide dedup: everything the old guide's code needs is still reachable
old = open("/mnt/openscience/audits/_pre-fix-20260920/bio-pileup-generation/run/skill/usage-guide.md", encoding="utf-8").read()
tok = lambda t: set(re.findall(r"--?[A-Za-z][\w-]*|\b[a-z_][a-z_0-9]*(?=\()|\b[a-z_]+(?==)|\bbcftools \w+|\bsamtools \w+|\.[a-z_]+\b|FORMAT/\w+|INFO/\w+", t))
code_old = "\n".join(re.findall(r"```(?:bash|python)?\n(.*?)```", old, flags=re.S))
code_old = "\n".join(l for l in code_old.splitlines() if not l.lstrip().startswith("#"))   # comments are prose, not commands
lost = sorted(t for t in tok(code_old) if t not in tok(SK + "\n" + UG))
print("tokens in the OLD usage-guide code blocks that no longer occur anywhere in the new SKILL.md + usage-guide.md:", lost)
intended = {"count_alleles", "min_qual", "-d 1000"}       # count_alleles replaced by allele_counts; the -d 1000 advice was dropped on purpose
lost2 = [t for t in lost if t not in intended]
check(I, "Dedup: every flag / function / tag used by the old usage-guide code still occurs in SKILL.md or the new guide (only the replaced count_alleles/min_qual left)", not lost2, lost2)
old_prompts = re.findall(r"^> \"(.*)\"", old, flags=re.M)
new_prompts = re.findall(r"^> \"(.*)\"", UG, flags=re.M)
gone = [x for x in old_prompts if x not in new_prompts]
print("old prompts removed/reworded:", gone, "| new prompts not in old:", [x for x in new_prompts if x not in old_prompts])
check(I, "Dedup: the guide keeps its 9 example prompts (2 reworded to bcftools mpileup), Quick Start and 'What the Agent Will Do'", len(new_prompts) == len(old_prompts) == 9 and "## What the Agent Will Do" in UG and "## Quick Start" in UG, (len(old_prompts), len(new_prompts)))
# what an agent asked 'which reads support the alt allele' would lose: query_name/strand print
check(I, "Dedup (UPDATED for round 2): the old 'Access Individual Reads' variant printed read name + strand; the fixed SKILL.md Access Reads snippet prints them again (query_name, is_reverse)", "query_name" in SK and "is_reverse" in SK.split("Access Reads at Position")[1].split("### Count Alleles")[0], f"query_name in SKILL.md: {'query_name' in SK}")
sh(f"rm -rf {W}")
summary(I)
