#!/usr/bin/env python3
"""Input 1 (Canonical, REAL data): 'Generate a text pileup of my BAM, region + MAPQ/baseQ filters, and tell me what the columns mean.'
Runs the SKILL.md / usage-guide samtools mpileup commands verbatim (paths substituted) on nf-core human chr22 slice
(reads at chr22:1952-4617 only) and checks the output against independent computations:
pysam pileup, samtools depth, bcftools mpileup -a DP, own parser of the base column, FASTA reference."""
import os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam

BAM = HUMAN + "/test.paired_end.sorted.bam"
REF = HUMAN + "/genome.fasta"
I = 1

def mp(opts, region="-r chr22:1952-4617", bam=BAM):
    rc, out, err = sh(f"samtools mpileup -f {REF} {opts} {region} {bam}")
    return rc, mpileup_rows(out), err

# --- A. SKILL.md "Basic pileup" with -r (region) : format
rc, rows, err = mp("")
check(I, "basic mpileup with -r runs and prints rows", rc == 0 and len(rows) > 1000, f"rc={rc} rows={len(rows)} stderr={err.strip()[:60]!r}")
check(I, "every row has exactly 6 columns (SKILL 'Output Format')", all(len(r) == 6 for r in rows), Counter(len(r) for r in rows))
fa = pysam.FastaFile(REF)
ok_ref = all(fa.fetch("chr22", int(r[1]) - 1, int(r[1])).upper() == r[2] for r in rows)
check(I, "col3 = reference base from FASTA, col2 is 1-based", ok_ref)
bad_len = [r[:2] for r in rows if r[3] != "0" and (parse_bases(r[4], r[2])[0] != int(r[3]) or len(r[5]) != int(r[3]))]
check(I, "col4 depth == number of read-slot symbols in col5 == number of quality chars in col6", not bad_len, bad_len[:3])
# zero-depth rows with '*' exist in default output
zero = [r for r in rows if r[3] == "0"]
check(I, "default output contains depth-0 rows (reads present but all bases filtered by default -Q 13)", len(zero) > 0,
      f"{len(zero)} zero-depth rows, e.g. {zero[0][:2] if zero else None}; SKILL never mentions default -Q=13 nor these rows")
# MAPQ char after ^
starts = [(r[1], r[4]) for r in rows if "^" in r[4]]
import re
mq = Counter(ord(m.group(1)) - 33 for _, s in starts for m in re.finditer(r"\^(.)", s))
print("MAPQ decoded from ^ chars:", dict(mq))
# real check: MAPQ values from BAM records
b = pysam.AlignmentFile(BAM)
bam_mq = Counter(a.mapping_quality for a in b.fetch("chr22") if not a.is_unmapped and not a.is_secondary and not a.is_duplicate and not a.is_qcfail)
check(I, "MAPQ values seen after '^' are a subset of MAPQs present in the BAM", set(mq) <= set(bam_mq), f"bam={dict(bam_mq)} pileup={dict(mq)}")

# --- B. depth vs independent tools. mpileup with everything switched off == samtools depth -J (-Q 0, -q 0), overlaps not removed
rc, rows_raw, _ = mp("-B -Q 0 -q 0 -x -A -d 1000000 -a")
_, depout, _ = sh(f"samtools depth -a -J -Q 0 -q 0 -r chr22:1952-4617 {BAM}")
dep = {int(l.split()[1]): int(l.split()[2]) for l in depout.splitlines()}
mpd = {int(r[1]): int(r[3]) for r in rows_raw}
diff = [(p, mpd.get(p), dep.get(p)) for p in dep if mpd.get(p) != dep[p]]
check(I, "mpileup -B -Q0 -q0 -x -A -a depth == samtools depth -a -J -Q0 at every position", not diff and len(mpd) == len(dep),
      f"positions={len(dep)} diffs={diff[:3]} maxdepth={max(dep.values())}")
# pysam equivalent
def pysam_depth(what="n", **kw):
    """what='n' -> PileupColumn.n (what SKILL prints as depth); 'pileups' -> len(col.pileups)"""
    d = {}
    with pysam.AlignmentFile(BAM) as bam:
        for col in bam.pileup("chr22", 1951, 4617, truncate=True, **kw):
            d[col.pos + 1] = col.n if what == "n" else len(col.pileups)
    return d
pd_raw = pysam_depth(min_base_quality=0, ignore_overlaps=False, ignore_orphans=False, max_depth=1000000, compute_baq=False)
diff = [(p, mpd.get(p), pd_raw.get(p, 0)) for p in mpd if mpd[p] != pd_raw.get(p, 0)]
check(I, "pysam pileup(min_base_quality=0, ignore_overlaps=False, ignore_orphans=False, max_depth=1e6) depth == mpileup all-off depth",
      not diff, f"diffs={diff[:3]} n={len(diff)}")

# --- C. DEFAULT mpileup vs pysam. SKILL.md prints `depth={pileup_column.n}` in every pysam example.
_, rows_def, _ = mp("")
mpdef = {int(r[1]): int(r[3]) for r in rows_def}
_, rows_nobaq, _ = mp("-B")
mpnb = {int(r[1]): int(r[3]) for r in rows_nobaq}
pd_n = pysam_depth("n")          # SKILL.md 'Basic Pileup' / 'Access Reads' / usage-guide 'Basic Pileup Iteration'
pd_pl = pysam_depth("pileups")
nd_n = sum(1 for p in mpdef if mpdef[p] != pd_n.get(p, 0))
print(f"mpileup default: rows={len(mpdef)} sumdepth={sum(mpdef.values())}; pysam default col.n sum={sum(pd_n.values())}; len(col.pileups) sum={sum(pd_pl.values())}")
check(I, "SKILL pysam `pileup_column.n` (default args) == samtools mpileup default depth column", nd_n == 0,
      f"{nd_n}/{len(mpdef)} positions differ; sum mpileup={sum(mpdef.values())} vs col.n={sum(pd_n.values())} (n ignores overlap removal + min_base_quality)")
nd_pl = sum(1 for p in mpnb if mpnb[p] != pd_pl.get(p, 0))
check(I, "len(col.pileups) with pysam defaults == samtools mpileup -B (no BAQ, -Q13, overlap removal) depth", nd_pl == 0, f"{nd_pl} positions differ; sum mpileup -B={sum(mpnb.values())}")
fa2 = pysam.FastaFile(REF)
pd_baq = {}
with pysam.AlignmentFile(BAM) as bam:
    for col in bam.pileup("chr22", 1951, 4617, truncate=True, fastafile=fa2, stepper="samtools"):
        pd_baq[col.pos + 1] = len(col.pileups)
nd2 = sum(1 for p in mpdef if mpdef[p] != pd_baq.get(p, 0))
check(I, "len(col.pileups) with stepper='samtools', fastafile=ref (BAQ on) == samtools mpileup default depth", nd2 == 0,
      f"{nd2} positions differ; sum pysam={sum(pd_baq.values())}")
# depth == number of symbols in col 5 for pysam text?  (checked again in input 2)

# --- D. quality options (-q, -Q): counts vs independent filtering with pysam
def mp_depth(opts):
    _, r, _ = mp(opts)
    return {int(x[1]): int(x[3]) for x in r}
d_q0 = mp_depth("-B -Q 0 -x -A -q 0")
mqs = Counter(a.mapping_quality for a in pysam.AlignmentFile(BAM).fetch("chr22"))
print("MAPQ distribution in BAM:", dict(mqs))
for q in (20, 60):
    dq = mp_depth(f"-B -Q 0 -x -A -q {q}")
    exp = Counter()
    for a in pysam.AlignmentFile(BAM).fetch("chr22"):
        if a.is_unmapped or a.is_secondary or a.is_qcfail or a.is_duplicate or a.mapping_quality < q:
            continue
        for qp, rp in a.get_aligned_pairs():
            if rp is not None:   # aligned or deleted reference position (mpileup depth counts '*')
                exp[rp + 1] += 1
    nd = [p for p in dq if dq[p] != exp.get(p, 0)]
    check(I, f"-q {q}: mpileup depth == independent count of reads with MAPQ>={q}", not nd, f"sum={sum(dq.values())} vs sum_all={sum(d_q0.values())} diffs={nd[:3]}")
for Qv in (20, 30):
    dQ = mp_depth(f"-B -x -A -Q {Qv}")
    exp = Counter()
    for a in pysam.AlignmentFile(BAM).fetch("chr22"):
        if a.is_unmapped or a.is_secondary or a.is_qcfail or a.is_duplicate:
            continue
        for qp, rp in a.get_aligned_pairs():
            if rp is None:
                continue
            if qp is None or a.query_qualities[qp] >= Qv:   # deleted bases carry no quality: assume counted
                exp[rp + 1] += 1
    nd = [p for p in dQ if dQ[p] != exp.get(p, 0)]
    check(I, f"-Q {Qv}: mpileup depth == independent count of bases with baseQ>={Qv}", not nd, f"sum={sum(dQ.values())} diffs={nd[:3]}")

# --- E. default flag exclusion and depth cap claims (SKILL says only 'default -d 8000')
_, r_ff, _ = mp("-B -Q 0 -x -A --ff 0 -a")
d_ff0 = {int(x[1]): int(x[3]) for x in r_ff}
check(I, "--ff 0 (no excluded flags) raises total depth vs default flags (duplicates/secondary are in this BAM)", sum(d_ff0.values()) > sum(d_q0.values()),
      f"sum ff0={sum(d_ff0.values())} default-excl={sum(d_q0.values())}; SKILL never lists the default excluded flags UNMAP,SECONDARY,QCFAIL,DUP")
flags = Counter(a.flag for a in pysam.AlignmentFile(BAM).fetch("chr22"))
print("flag distribution:", dict(flags))

# --- F. region / BED parsing
_, r1, e = mp("", region="-r chr22:3000-3000")
check(I, "-r chr22:3000-3000 gives exactly one row at 3000", len(r1) == 1 and r1[0][1] == "3000", [x[:4] for x in r1])
_, r2, e = mp("", region="-r chr22:3,000-3,005")
check(I, "-r with thousands separators (chr22:3,000-3,005) accepted -> 6 rows", len(r2) == 6, len(r2))
_, r3, e = mp("", region="-r chr22:16570000-16590000")
check(I, "SKILL-style far region on the renumbered slice returns 0 rows without error (trap)", len(r3) == 0, f"rows={len(r3)} stderr={e.strip()[:80]!r}")
_, r4, e = mp("", region="-r 22:3000-3005")
check(I, "wrong contig name '22' vs 'chr22' => error message (troubleshooting 'chromosome name match')", len(r4) == 0 and ("fail" in e.lower() or "error" in e.lower() or "region" in e.lower()), e.strip()[:150])
bed = os.path.join(WORK, "t.bed")
open(bed, "w").write("chr22" + chr(9) + "2999" + chr(9) + "3003" + chr(10) + "chr22" + chr(9) + "3099" + chr(9) + "3101" + chr(10))
rc, out, err = sh(f"samtools mpileup -f {REF} -l {bed} {BAM}")
pos = [int(x[1]) for x in mpileup_rows(out)]
check(I, "-l BED (0-based half-open) yields 1-based positions 3000-3003 and 3100-3101", pos == [3000, 3001, 3002, 3003, 3100, 3101], pos)
# --- G. multiple BAMs: 3 + 3N columns (SKILL says '6 columns per sample')
rc, out, err = sh(f"samtools mpileup -f {REF} -r chr22:3000-3002 {BAM} {BAM}")
r = mpileup_rows(out)
check(I, "two BAMs => 9 columns (3 + 3*N), i.e. SKILL 'Text pileup format (6 columns per sample)' is imprecise", all(len(x) == 9 for x in r), Counter(len(x) for x in r))
# --- H. bcftools mpileup DP == samtools mpileup all-off depth ?  (bcftools excludes deletions? compare)
rc, out, err = sh(f"bcftools mpileup -f {REF} -r chr22:1952-4617 -B -Q 0 -q 0 -x -A -d 1000000 -a FORMAT/DP --ns UNMAP,SECONDARY,QCFAIL,DUP -Ov {BAM} | grep -v '^#' | cut -f2,10")
bd = {}
for l in out.splitlines():
    p, f = l.split("\t")
    bd[int(p)] = int(f.split(":")[1]) if ":" in f else None
ndel = {int(r[1]): parse_bases(r[4], r[2])[1]["*"] for r in rows_raw}
nd = [p for p in bd if bd[p] != mpd.get(p) - ndel.get(p, 0)]
nd_raw = [p for p in bd if bd[p] != mpd.get(p)]
print("bcftools DP vs samtools depth: positions", len(bd), "differ", len(nd_raw), [(p, bd[p], mpd.get(p), ndel.get(p)) for p in nd_raw[:5]])
check(I, "bcftools mpileup FORMAT/DP == samtools mpileup depth (filters off)", len(nd_raw) == 0, f"{len(nd_raw)} of {len(bd)} positions differ (bcftools excludes deleted-base reads)")
check(I, "bcftools mpileup FORMAT/DP == samtools mpileup depth minus '*' deletion slots", len(nd) == 0, f"{len(nd)} differ")
summary(I)
