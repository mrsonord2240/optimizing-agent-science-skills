#!/usr/bin/env python3
"""Input 4 (variant B, REGRESSION on the fixed Skill): wheat-scale genome (contig > 2^29 = 537 Mbp).
Tests every quantitative claim in the FIXED 'Index Types' / 'Which Index for Which Genome' / large-genome bullets / 'Common Errors'.
Data: SYNTHETIC BAMs (data/wheat_like.bam, big2g.bam, huge_3g.sam) built by make_synth.py; read positions known exactly so truth is a hand list.
Plus: the LN=3,000,000,000 header case the fixed text says 'cannot be stored in BAM at all'.
Run in WSL from run/:  python scripts/r4_large_genome.py"""
import os, sys, shutil, gzip, struct, re
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam

W = "work/r4"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
for f in ["wheat_like.bam", "big2g.bam", "huge_3g.sam"]:
    shutil.copy(f"data/{f}", f"{W}/{f}")

def csi_params(path):
    d = gzip.open(path).read()
    assert d[:4] == b"CSI\x01", d[:4]
    min_shift, depth = struct.unpack("<ii", d[4:12])
    return min_shift, depth, min_shift + 3 * depth

chr3b_pos1 = [5001, 536870001, 600000001, 700000001, 830000001]
def truth3b(s1, e1):
    return sum(1 for p in chr3b_pos1 if p <= e1 and p + 99 >= s1)
queries = [(1, 10000), (536870001 - 50, 536870001 + 50), (599999900, 600000100), (650000000, 750000000), (830000000, 830829764), (600000200, 699999999)]

# ---- 1. SKILL bullet: BAI on a contig >2^29 fails loudly, no .bai, exit 1, message text -------------------
rc, o, e = out(f"samtools index {W}/wheat_like.bam")
check("SKILL: BAI on >2^29 contig fails loudly: exit 1, no .bai written", rc == 1 and not os.path.exists(f"{W}/wheat_like.bam.bai"), f"rc={rc}")
check("SKILL quoted message 'cannot be stored in a bai index. Try using a csi index' appears", "cannot be stored in a bai index. Try using a csi index" in e, e[:250])
try:
    pysam.index(f"{W}/wheat_like.bam"); check("pysam.index (BAI) on >537 Mbp contig raises", False)
except Exception as ex:
    check("pysam.index (BAI) on >537 Mbp contig raises SamtoolsError", True, f"{type(ex).__name__}: {str(ex)[:120]}")

# ---- 2. SKILL: `samtools index -c` depth auto-sized, worked on 830 Mbp and 2.0 Gbp -------------------------
shutil.copy(f"{W}/wheat_like.bam", f"{W}/dflt.bam")
rc, o, e = out(f"samtools index -c {W}/dflt.bam")
ms, dp, cov = csi_params(f"{W}/dflt.bam.csi")
check("default `samtools index -c` (min_shift 14) succeeds on the 830 Mbp contig, depth auto-sized (covers > 830 Mbp)", rc == 0 and ms == 14 and 2 ** cov > 830829764, f"min_shift={ms} depth={dp} covers 2^{cov}")
bad = []
with pysam.AlignmentFile(f"{W}/dflt.bam", "rb") as b:
    for s, e_ in queries:
        n_cli = int(out(f"samtools view -c {W}/dflt.bam chr3B:{s}-{e_}")[1]); n_py = b.count("chr3B", s - 1, e_)
        t = truth3b(s, e_)
        if not (n_cli == n_py == t): bad.append((s, e_, t, n_cli, n_py))
check("default -c CSI: 6 chr3B region queries == hand-computed truth (samtools + pysam)", not bad, bad)
# ---- 3. SKILL: '-m 18 gave depth 4 = 2^30 on an 830 Mbp contig, not 2^33' ------------------------------------
shutil.copy(f"{W}/wheat_like.bam", f"{W}/m18.bam")
rc, o, e = out(f"samtools index -c -m 18 {W}/m18.bam")
ms18, dp18, cov18 = csi_params(f"{W}/m18.bam.csi")
check("SKILL claim: `-c -m 18` on the 830 Mbp contig gives depth 4 = 2^30 (not 2^33)", rc == 0 and ms18 == 18 and dp18 == 4 and cov18 == 30, f"min_shift={ms18} depth={dp18} => 2^{cov18}")
check("`-c -m 18` still answers all queries == truth", all(int(out(f"samtools view -c {W}/m18.bam chr3B:{s}-{e_}")[1]) == truth3b(s, e_) for s, e_ in queries))
shutil.copy(f"{W}/wheat_like.bam", f"{W}/py.bam"); pysam.index("-c", f"{W}/py.bam")
with pysam.AlignmentFile(f"{W}/py.bam", "rb") as b:
    n = b.count("chr3B", 829999999, 830000200)
check("pysam.index('-c', f) then count at 830,000,000 == 1", n == 1, n)

# ---- 4. 2.0 Gbp contig ------------------------------------------------------------------------------------------
shutil.copy(f"{W}/big2g.bam", f"{W}/g_dflt.bam"); shutil.copy(f"{W}/big2g.bam", f"{W}/g_m18.bam")
out(f"samtools index -c {W}/g_dflt.bam"); out(f"samtools index -c -m 18 {W}/g_m18.bam")
msg, dpg, covg = csi_params(f"{W}/g_dflt.bam.csi"); msg18, dpg18, covg18 = csi_params(f"{W}/g_m18.bam.csi")
check("SKILL: default -c on 2.0 Gbp: depth 6 (2^32); -m 18: depth 5 (2^33)", (msg, dpg) == (14, 6) and (msg18, dpg18) == (18, 5), f"default={msg},{dpg} m18={msg18},{dpg18}")
for name in ["g_dflt", "g_m18"]:
    n = int(out(f"samtools view -c {W}/{name}.bam big2g:1899999901-1900000100")[1]); m = int(out(f"samtools view -c {W}/{name}.bam big2g:600000000-800000000")[1])
    check(f"2.0 Gbp contig {name}: read at 1.9e9 found (1) and read at 7e8 found (1)", n == 1 and m == 1, f"n={n} m={m}")
rc, o, e = out(f"samtools index {W}/big2g.bam")
check("BAI on the 2.0 Gbp contig refuses (loud)", rc != 0, f"rc={rc}")

# ---- 5. > 2^31-1: what exactly fails? --------------------------------------------------------------------------------
rc, o, e = out(f"samtools view -b -o {W}/huge.bam {W}/huge_3g.sam")
check("SKILL: read POSITIONED beyond 2^31-1 fails at write time with 'Positional data is too large for BAM format'", rc != 0 and "Positional data is too large for BAM format" in e, f"rc={rc} err={e[:160]!r}")
# 3 Gbp header, only low-position reads
T = "\t"; NL = "\n"
with open(f"{W}/huge_lowpos.sam", "w") as fh:
    fh.write(f"@HD{T}VN:1.6{T}SO:coordinate{NL}@SQ{T}SN:huge3g{T}LN:3000000000{NL}")
    fh.write(T.join(["r1", "0", "huge3g", "1000", "60", "100M", "*", "0", "0", "ACGT" * 25, "I" * 100]) + NL)
    fh.write(T.join(["r2", "0", "huge3g", "2000000000", "60", "100M", "*", "0", "0", "ACGT" * 25, "I" * 100]) + NL)
rc, o, e = out(f"samtools view -b -o {W}/huge_lowpos.bam {W}/huge_lowpos.sam")
hd = out(f"samtools view -H {W}/huge_lowpos.bam | grep '^@SQ'")[1] if rc == 0 else ""
check("A BAM with an LN=3,000,000,000 header and reads at positions < 2^31-1 IS writable (LN survives)", rc == 0 and "LN:3000000000" in hd, f"rc={rc} header={hd!r} err={e[:120]!r}")
if rc == 0:
    rc2, o2, e2 = out(f"samtools index -c {W}/huge_lowpos.bam")
    n1 = out(f"samtools view -c {W}/huge_lowpos.bam huge3g:1000-1100")[1]; n2 = out(f"samtools view -c {W}/huge_lowpos.bam huge3g:2000000000-2000000100")[1]
    ms3, dp3, cov3 = csi_params(f"{W}/huge_lowpos.bam.csi") if os.path.exists(f"{W}/huge_lowpos.bam.csi") else (None, None, None)
    info(f"3 Gbp header, low reads: index -c rc={rc2} err={e2[:150]!r} csi=(min_shift {ms3}, depth {dp3}) counts {n1},{n2}")
    check("that 3 Gbp-header BAM can be CSI-indexed and both low reads retrieved (=> 'cannot be stored in BAM at all' is an overstatement; only positions > 2^31-1 fail)", rc2 == 0 and n1 == "1" and n2 == "1", f"index rc={rc2} counts={n1},{n2}")
# is the SKILL wording exact?
row = [l for l in SKILL_MD.splitlines() if l.startswith("| Pine")][0]
info("SKILL row: " + row)
bul = [l for l in SKILL_MD.splitlines() if "2^31-1" in l]
info("SKILL 2^31-1 lines:\n" + "\n".join(bul))
dump("out/r4_results.json")
