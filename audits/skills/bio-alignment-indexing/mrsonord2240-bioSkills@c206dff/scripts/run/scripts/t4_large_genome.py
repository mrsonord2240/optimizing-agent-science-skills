#!/usr/bin/env python3
"""Input 4 (variant B): wheat-scale genome (contig > 2^29 = 537 Mbp). Tests every quantitative claim in the SKILL's
'Index Types' / 'Which Index for Which Genome' / 'Common Errors' sections.
Data: SYNTHETIC BAMs (run/data/wheat_like.bam, big2g.bam, huge_3g.sam) built by make_synth.py; read positions known exactly
so truth is a hand list, not a tool's output.
Run in WSL from run/:  python scripts/t4_large_genome.py"""
import os, sys, shutil, gzip, struct
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam

W = "work/t4"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
for f in ["wheat_like.bam", "big2g.bam", "huge_3g.sam"]:
    shutil.copy(f"data/{f}", f"{W}/{f}")

def csi_params(path):
    d = gzip.open(path).read()
    assert d[:4] == b"CSI\x01", d[:4]
    min_shift, depth = struct.unpack("<ii", d[4:12])
    return min_shift, depth, min_shift + 3 * depth

# hand truth: chr3B reads at 5000, 536870000, 600000000, 700000000, 830000000 (0-based starts, 100M, so 1-based 5001, ...)
chr3b_pos1 = [5001, 536870001, 600000001, 700000001, 830000001]
def truth3b(s1, e1):   # 1-based inclusive region, reads span [p, p+99]
    return sum(1 for p in chr3b_pos1 if p <= e1 and p + 99 >= s1)
queries = [(1, 10000), (536870001 - 50, 536870001 + 50), (599999900, 600000100), (650000000, 750000000), (830000000, 830829764), (600000200, 699999999)]

# ---- 1. SKILL claim: plain BAI on a contig >537 Mbp 'silently truncates reads' ------------------------------------
rc, o, e = out(f"samtools index {W}/wheat_like.bam")
info(f"BAI on wheat_like: rc={rc}\n{e}")
check("SKILL 'BAI silently truncates reads' -- is it silent? samtools index on >2^29 contig fails LOUDLY and writes no .bai", rc != 0 and not os.path.exists(f"{W}/wheat_like.bam.bai"), f"rc={rc} err={e[:220]!r}")
check("error message tells the user to use CSI", "csi" in e.lower(), e[:220])
try:
    pysam.index(f"{W}/wheat_like.bam"); check("pysam.index on >537 Mbp contig raises", False)
except Exception as ex:
    check("pysam.index (BAI) on >537 Mbp contig raises SamtoolsError", True, f"{type(ex).__name__}: {str(ex)[:120]}")

# ---- 2. SKILL: 'samtools index -c file.bam' default CSI 'matches BAI bin layout: 2^29' -----------------------------
shutil.copy(f"{W}/wheat_like.bam", f"{W}/dflt.bam")
rc, o, e = out(f"samtools index -c {W}/dflt.bam")
check("default `samtools index -c` (min_shift 14) succeeds on the 830 Mbp contig", rc == 0 and os.path.exists(f"{W}/dflt.bam.csi"), f"rc={rc} err={e[:200]!r}")
ms, dp, cov = csi_params(f"{W}/dflt.bam.csi")
info(f"default -c CSI: min_shift={ms} depth={dp} -> covers 2^{cov} = {2**cov:,} bp per contig")
check("default -c CSI covers > 2^29 (htslib auto-raises depth), contradicting 'matches BAI bin layout: 2^29 per contig'", cov > 29, f"min_shift={ms} depth={dp} covers 2^{cov}")
bad = []
with pysam.AlignmentFile(f"{W}/dflt.bam", "rb") as b:
    for s, e_ in queries:
        n_cli = int(out(f"samtools view -c {W}/dflt.bam chr3B:{s}-{e_}")[1]); n_py = b.count("chr3B", s - 1, e_)
        t = truth3b(s, e_)
        if not (n_cli == n_py == t): bad.append((s, e_, t, n_cli, n_py))
check("default -c CSI: 6 chr3B region queries == hand-computed truth (samtools + pysam)", not bad, bad)
rc, o, e = out(f"samtools view -c {W}/dflt.bam chr1A:590000001-594102056")
check("chr1A read at 590,000,000 retrievable with default -c CSI", o == "1", f"n={o}")

# ---- 3. SKILL: 'samtools index -c -m 18' -----------------------------------------------------------------------
shutil.copy(f"{W}/wheat_like.bam", f"{W}/m18.bam")
rc, o, e = out(f"samtools index -c -m 18 {W}/m18.bam")
ms18, dp18, cov18 = csi_params(f"{W}/m18.bam.csi")
info(f"-c -m 18 CSI: min_shift={ms18} depth={dp18} -> 2^{cov18}")
check("`-c -m 18` works, counts == truth", rc == 0 and all(int(out(f"samtools view -c {W}/m18.bam chr3B:{s}-{e_}")[1]) == truth3b(s, e_) for s, e_ in queries), f"rc={rc} err={e[:100]!r}")
check("SKILL comment '2^(18+15) = 2^33 ~8.5 Gbp per contig' equals min_shift+3*depth as stored (depth is NOT fixed at 5)", cov18 == 33, f"stored min_shift={ms18} depth={dp18} => 2^{cov18}; default -c => 2^{cov}")
# size/idxstats
rc, o, e = out(f"samtools idxstats {W}/m18.bam")
check("idxstats on CSI-indexed BAM: chr1A 4 mapped, chr3B 5 mapped", "chr1A\t594102056\t4\t0" in o and "chr3B\t830829764\t5\t0" in o, o.replace("\n", " | "))
# pysam route from SKILL
shutil.copy(f"{W}/wheat_like.bam", f"{W}/py.bam")
pysam.index("-c", f"{W}/py.bam")
with pysam.AlignmentFile(f"{W}/py.bam", "rb") as b:
    n = b.count("chr3B", 829999999, 830000200)
check("pysam.index('-c', f) then count at 830,000,000 == 1", n == 1, n)

# ---- 4. contig near 2^31 (2.0 Gbp) -----------------------------------------------------------------------------
shutil.copy(f"{W}/big2g.bam", f"{W}/g_dflt.bam"); shutil.copy(f"{W}/big2g.bam", f"{W}/g_m18.bam")
rc1, _, e1 = out(f"samtools index -c {W}/g_dflt.bam"); rc2, _, e2 = out(f"samtools index -c -m 18 {W}/g_m18.bam")
info(f"2.0 Gbp contig: -c rc={rc1} {e1[:100]!r}; -c -m 18 rc={rc2} {e2[:100]!r}")
for name in ["g_dflt", "g_m18"]:
    n = int(out(f"samtools view -c {W}/{name}.bam big2g:1899999901-1900000100")[1])
    m = int(out(f"samtools view -c {W}/{name}.bam big2g:600000000-800000000")[1])
    check(f"2.0 Gbp contig {name}: read at 1.9e9 found (1) and read at 7e8 found in [6e8,8e8] (1)", n == 1 and m == 1, f"n={n} m={m}")
rc, o, e = out(f"samtools index {W}/big2g.bam")
check("BAI on the 2.0 Gbp contig refuses too (control)", rc != 0, f"rc={rc}")

# ---- 5. multi-Gbp contig (axolotl / pine): SKILL table row says 'CSI with larger -m' ------------------------------------
rc, o, e = out(f"samtools view -b -o {W}/huge.bam {W}/huge_3g.sam")
info(f"SAM->BAM with LN=3,000,000,000 and a read at 2.5e9: rc={rc}\n{e}")
n_records = int(out(f"samtools view -c {W}/huge.bam")[1]) if os.path.exists(f"{W}/huge.bam") and os.path.getsize(f"{W}/huge.bam") > 0 else -1
rc2, o2, e2 = out(f"samtools index -c -m 18 {W}/huge.bam") if n_records >= 0 else (-1, "", "no bam produced")
info(f"index -c -m 18 on that BAM: rc={rc2} {e2[:200]!r}")
check("BAM format can carry a multi-Gbp contig at all (SKILL table: 'Pine, fir, axolotl... multi-Gbp | CSI with larger -m')", rc == 0 and n_records == 2 and rc2 == 0, f"view rc={rc} records={n_records} err={e[:160]!r}")

# ---- 6. same 3 Gbp header but the only read is at pos 1000: is the LN itself storable in BAM? -------------------------
T = "\t"; NL = "\n"
with open(f"{W}/huge_lowpos.sam", "w") as fh:
    fh.write(f"@HD{T}VN:1.6{T}SO:coordinate{NL}@SQ{T}SN:huge3g{T}LN:3000000000{NL}")
    fh.write(T.join(["r1", "0", "huge3g", "1000", "60", "100M", "*", "0", "0", "ACGT" * 25, "I" * 100]) + NL)
rc, o, e = out(f"samtools view -b -o {W}/huge_lowpos.bam {W}/huge_lowpos.sam")
hd = out(f"samtools view -H {W}/huge_lowpos.bam | grep '^@SQ'")[1] if rc == 0 else ""
info(f"3 Gbp LN with a low-position read: rc={rc} err={e[:160]!r} header={hd!r}")
check("BAM stores LN=3,000,000,000 unchanged (BAM l_ref is int32)", rc == 0 and "LN:3000000000" in hd, f"rc={rc} header={hd!r} err={e[:120]!r}")
dump("out/t4_results.json")
