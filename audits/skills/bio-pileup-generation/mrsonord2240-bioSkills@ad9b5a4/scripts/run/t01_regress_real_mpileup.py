#!/usr/bin/env python3
"""Input 1 (Canonical, REGRESSION of the pre-fix input 1, REAL data): text pileup of the nf-core human chr22 slice with -r/-l/-q/-Q,
what each column and symbol means, and a cross-check of depth against another tool.  Re-run against the FIXED Skill; every
documented claim in 'Output Format', 'Read Bases Encoding', 'Quality Filtering', 'Pileup Options and Defaults' and the pysam table
is asserted against an independent computation (samtools depth, pysam, bcftools, own decoder of the base column)."""
import os, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam

BAM, REF, I = HBAM, HREF, 1
SK = open(SKILL + "/SKILL.md", encoding="utf-8").read()


def mp(opts="", region="-r chr22:1952-4617", bam=BAM, ref=REF):
    rc, out, err = sh(f"samtools mpileup -f {ref} {opts} {region} {bam}")
    return rc, mpileup_rows(out), err


rc, rows, err = mp()
check(I, "basic mpileup with -r runs and prints rows", rc == 0 and len(rows) > 1000, f"rc={rc} rows={len(rows)} stderr={err.strip()[:60]!r}")
check(I, "Output Format: 6 columns for one BAM", all(len(r) == 6 for r in rows), Counter(len(r) for r in rows))
fa = pysam.FastaFile(REF)
check(I, "col3 = FASTA base (upper-case here), col2 1-based", all(fa.fetch("chr22", int(r[1]) - 1, int(r[1])).upper() == r[2] for r in rows))
bad = [r[:2] for r in rows if r[3] != "0" and (parse_bases(r[4], r[2])[0] != int(r[3]) or len(r[5]) != int(r[3]))]
check(I, "Output Format table: col4 depth == number of read symbols in col5 == number of chars in col6", not bad, bad[:3])
# documented depth-0 rows: 'chr22 1952 T 0 * *'
z = [r for r in rows if r[3] == "0"]
check(I, "Output Format: the Skill's example 'chr22 1952 T 0 * *' is real: exact row present, col5 and col6 both '*'",
      ["chr22", "1952", "T", "0", "*", "*"] in z, f"{len(z)} depth-0 rows, first {z[:2]}")
check(I, "SKILL.md text contains the depth-0 explanation and the exact example row", "chr22 1952 T 0 * *" in SK and "depth 0 and `*` in columns 5 and 6" in SK)
# MAPQ char
mq = Counter(ord(m.group(1)) - 33 for r in rows for m in re.finditer(r"\^(.)", r[4]))
bmq = Counter(a.mapping_quality for a in pysam.AlignmentFile(BAM).fetch("chr22") if not (a.is_unmapped or a.is_secondary or a.is_qcfail or a.is_duplicate))
check(I, "'^Q' MAPQ+33: decoded MAPQs are a subset of the BAM's MAPQs; MAPQ 60 -> '^]'", set(mq) <= set(bmq) and any("^]" in r[4] for r in rows), f"{dict(mq)}")

# -------- depth with everything off == samtools depth -a -J ; pysam equivalent
_, raw, _ = mp("-B -Q 0 -q 0 -x -A -d 1000000 -a")
_, depout, _ = sh(f"samtools depth -a -J -Q 0 -q 0 -r chr22:1952-4617 {BAM}")
dep = {int(l.split()[1]): int(l.split()[2]) for l in depout.splitlines()}
mpd = {int(r[1]): int(r[3]) for r in raw}
d = [(p, mpd.get(p), dep[p]) for p in dep if mpd.get(p) != dep[p]]
check(I, "mpileup -B -Q0 -q0 -x -A -a depth == samtools depth -a -J at every position (independent tool)", not d and len(mpd) == len(dep), f"positions={len(dep)} diffs={d[:3]} max={max(dep.values())}")

# -------- Skill's pysam table on the human BAM: len(pileups) vs mpileup, position by position
def pysam_depth(kind="pileups", _fa=False, **kw):
    dd = {}
    if _fa:
        kw["fastafile"] = pysam.FastaFile(REF)
    with pysam.AlignmentFile(BAM) as b:
        for col in b.pileup("chr22", 1951, 4617, truncate=True, **kw):
            dd[col.pos + 1] = len(col.pileups) if kind == "pileups" else col.n
    return dd


_, r_def, _ = mp()
_, r_B, _ = mp("-B")
m_def = {int(r[1]): int(r[3]) for r in r_def}
m_B = {int(r[1]): int(r[3]) for r in r_B}
n_pl = pysam_depth("pileups")
n_n = pysam_depth("n")
baq = pysam_depth("pileups", _fa=True, stepper="samtools")
nd = lambda A, B: sum(1 for p in A if A[p] != B.get(p, 0))
check(I, "pysam defaults == samtools mpileup -B, position by position (len(pileups)); Skill: 'pysam defaults equal -B'", nd(m_B, n_pl) == 0, f"{nd(m_B, n_pl)} of {len(m_B)} differ; sum {sum(m_B.values())} vs {sum(n_pl.values())}")
check(I, "stepper='samtools' + fastafile == samtools mpileup default (BAQ), position by position", nd(m_def, baq) == 0, f"{nd(m_def, baq)} of {len(m_def)} differ; sum {sum(m_def.values())} vs {sum(baq.values())}")
nn = nd(m_def, n_n)
check(I, "Skill claim reproduced: pileup_column.n differs from the default mpileup depth at 1087 of 1157 positions on this BAM", nn == 1087 and len(m_def) == 1157, f"n differs at {nn} of {len(m_def)} (vs -B: {nd(m_B, n_n)})")
allfa = pysam_depth("pileups", _fa=True)   # stepper 'all' + fastafile: Skill says BAQ is NOT applied
check(I, "Skill claim: stepper='all' + fastafile does NOT apply BAQ (== mpileup -B, != default) ", nd(m_B, allfa) == 0 and nd(m_def, allfa) > 0, f"vs -B {nd(m_B, allfa)} differ; vs default {nd(m_def, allfa)} differ")

# -------- -q / -Q vs independent counts
def indep(minq=0, minQ=0):
    e = Counter()
    for a in pysam.AlignmentFile(BAM).fetch("chr22"):
        if a.is_unmapped or a.is_secondary or a.is_qcfail or a.is_duplicate or a.mapping_quality < minq:
            continue
        for qp, rp in a.get_aligned_pairs():
            if rp is not None and (qp is None or a.query_qualities[qp] >= minQ):
                e[rp + 1] += 1
    return e
for q in (20, 60):
    _, r, _ = mp(f"-B -Q 0 -x -A -q {q}")
    dq = {int(x[1]): int(x[3]) for x in r}
    e = indep(minq=q)
    check(I, f"-q {q}: depth == independent count of reads with MAPQ>={q}", all(dq[p] == e.get(p, 0) for p in dq), f"sum {sum(dq.values())}")
for Q in (13, 20, 30):
    _, r, _ = mp(f"-B -x -A -Q {Q}")
    dq = {int(x[1]): int(x[3]) for x in r}
    e = indep(minQ=Q)
    check(I, f"-Q {Q}: depth == independent count of bases with baseQ>={Q}", all(dq[p] == e.get(p, 0) for p in dq), f"sum {sum(dq.values())}")
# Skill: -Q 13 is the samtools default
_, r13, _ = mp("-Q 13")
check(I, "Options table: samtools default -Q is 13 (explicit -Q 13 output identical to default)", r13 == r_def)
_, r0, _ = mp("-Q 0")
check(I, "Options table: -Q 0 changes the output (default silently drops low-quality bases)", r0 != r_def and sum(int(x[3]) for x in r0) > sum(int(x[3]) for x in r_def), f"{sum(int(x[3]) for x in r0)} vs {sum(int(x[3]) for x in r_def)}")
# default flags: --ff
_, rf, _ = mp("-B -Q 0 -x -A --ff 0 -a")
_, rd, _ = mp("-B -Q 0 -x -A -a")
_, rn, _ = mp("-B -Q 0 -x -A --ff UNMAP,SECONDARY,QCFAIL,DUP -a")
s_ff0, s_def, s_named = (sum(int(x[3]) for x in q) for q in (rf, rd, rn))
check(I, "Options table: default --ff is UNMAP,SECONDARY,QCFAIL,DUP (explicit named list == default; --ff 0 adds reads)", rd == rn and s_ff0 > s_def, f"--ff 0 sum {s_ff0} vs default {s_def}; named==default {rd == rn}")
flags = Counter(a.flag for a in pysam.AlignmentFile(BAM).fetch("chr22"))
extra = sum(v for k, v in flags.items() if k & 0x700)
print("flag distribution:", dict(flags))

# -------- region / BED / multi-BAM
_, r1, _ = mp(region="-r chr22:3000-3000")
check(I, "-r single position -> exactly one row at 3000", len(r1) == 1 and r1[0][1] == "3000")
_, r2, _ = mp(region="-r chr22:3,000-3,005")
check(I, "-r accepts thousands separators", len(r2) == 6)
_, r3, e3 = mp(region="-r chr22:16570000-16590000")
check(I, "SKILL-style far region on the renumbered slice: 0 rows, no error (env trap)", len(r3) == 0)
_, r4, e4 = mp(region="-r 22:3000-3005")
check(I, "Common Errors: '[E::mpileup] fail to parse region '22:3000-3005'' is the real message for a contig mismatch",
      "[E::mpileup] fail to parse region '22:3000-3005'" in e4 and "fail to parse region '22:3000-3005'" in SK, e4.strip()[:120])
bed = os.path.join(WORK, "t.bed")
open(bed, "w").write("chr22\t2999\t3003\nchr22\t3099\t3101\n")
rc, out, err = sh(f"samtools mpileup -f {REF} -l {bed} {BAM}")
check(I, "-l BED (0-based half-open) -> 1-based positions 3000-3003, 3100-3101", [int(x[1]) for x in mpileup_rows(out)] == [3000, 3001, 3002, 3003, 3100, 3101])
rc, out, err = sh(f"samtools mpileup -f {REF} -r chr22:3000-3002 {BAM} {BAM}")
check(I, "Output Format: '3 shared columns, then 3 per input BAM' -> 9 columns for two BAMs", all(len(x) == 9 for x in mpileup_rows(out)) and "3 shared columns, then 3 columns per input BAM" in SK)
# -------- bcftools DP vs samtools depth minus '*'
rc, out, err = sh(f"bcftools mpileup -f {REF} -r chr22:1952-4617 -B -Q 0 -q 0 -x -A -d 1000000 -a FORMAT/DP --ns UNMAP,SECONDARY,QCFAIL,DUP -Ov {BAM} | grep -v '^#' | cut -f2,10")
bd = {int(l.split("\t")[0]): int(l.split("\t")[1].split(":")[1]) for l in out.splitlines()}
ndel = {int(r[1]): parse_bases(r[4], r[2])[1]["*"] for r in raw}
check(I, "bcftools mpileup FORMAT/DP == samtools depth minus '*' deletion slots at every position (second tool)", all(bd[p] == mpd[p] - ndel.get(p, 0) for p in bd), f"{len(bd)} positions")

# -------- 1000G rows quoted in the Skill's Output Format
G = "/mnt/openscience/audit-envs/alignment-files/public-data/1000g"
rc, out, err = sh(f"samtools mpileup -f {G}/chr20_padded_1500000.fa -r chr20:1400300-1400301 {G}/HG00349.chr20_1400000-1500000.bam")
rows_g = out.strip().splitlines()
check(I, "Output Format example rows equal real 1000G output",
      rows_g == ["chr20\t1400300\tG\t6\t,,,.,,\tBBB<BB", "chr20\t1400301\tC\t6\t,,,.,,\tBB<BBB"] and "chr20   1400300  G    6    ,,,.,,    BBB<BB" in SK, rows_g)
# -------- symbol table claims that can be verified without planted data
_, allrows, _ = mp()
sym_seen = Counter(ch for r in allrows for ch in re.sub(r"\^.|[+-]\d+[A-Za-z]+", "", r[4]))
print("symbols present in this real BAM's pileup:", dict(sym_seen))
summary(I)
