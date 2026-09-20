#!/usr/bin/env python3
"""Input 3 (edge): unsorted input, missing index, lying @HD, contig names with ':', comma / 0-based / wrong-name regions,
empty BAM. Checks the SKILL's 'Common Errors' table strings against the installed tools (samtools 1.24, pysam 0.24.1).
Data: REAL unsorted UMI BAM (public-data/human) + REAL human chr22 BAM + SYNTHETIC hla_contig.bam / empty BAM.
Run in WSL from run/:  python scripts/t3_edge.py"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam

AFD = os.environ["AFDATA"]
W = "work/t3"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
shutil.copy(f"{AFD}/human/test.paired_end.umi_unsorted.bam", f"{W}/umi.bam")
shutil.copy(f"{AFD}/human/test.paired_end.sorted.bam", f"{W}/h22.bam"); shutil.copy(f"{AFD}/human/test.paired_end.sorted.bam.bai", f"{W}/h22.bam.bai")
shutil.copy(f"{AFD}/human/test.paired_end.name.sorted.bam", f"{W}/qname.bam")
shutil.copy("data/hla_contig.bam", f"{W}/hla.bam")
shutil.copytree("skill/examples", f"{W}/examples")

# ---- A. unsorted BAM: SKILL says `samtools view -H | grep ^@HD` should show SO:coordinate ------------
rc, o, e = out(f"samtools view -H {W}/umi.bam | grep -c '^@HD'")
info(f"unsorted UMI BAM @HD lines: {o} (real BAM has no @HD, so the SKILL's sort check prints nothing)")
rc, o, e = out(f"samtools view -H {W}/qname.bam | grep '^@HD'")
check("queryname-sorted BAM: @HD shows SO:queryname (SKILL check distinguishes it)", "SO:queryname" in o, o)
# ---- B. index unsorted: error text vs SKILL table ------------------------------------------------------
rc, o, e = out(f"samtools index {W}/umi.bam")
info(f"samtools index on unsorted: rc={rc}\n{e}")
check("samtools index on an unsorted BAM fails (rc!=0) and writes no index", rc != 0 and not os.path.exists(f"{W}/umi.bam.bai"), f"rc={rc}")
check("stderr contains SKILL table text 'file is not sorted'", "file is not sorted" in e, e[:200])
check("stderr contains usage-guide text 'file is not coordinate sorted'", "not coordinate sorted" in e, e[:200])
check("stderr says what actually happens (unsorted / failed to create index)", ("Unsorted" in e or "unsorted" in e or "failed to create index" in e or "not sorted" in e), e[:200])
try:
    pysam.index(f"{W}/umi.bam")
    check("pysam.index on unsorted raises", False, "no exception")
except Exception as ex:
    check("pysam.index on an unsorted BAM raises an exception", True, f"{type(ex).__name__}: {str(ex)[:160]}")

# ---- C. Skill remedy: sort then index ----------------------------------------------------------------------
rc, o, e = out(f"samtools sort -o {W}/umi.sorted.bam {W}/umi.bam && samtools index {W}/umi.sorted.bam")
check("sort -> index remedy from SKILL works", rc == 0 and os.path.exists(f"{W}/umi.sorted.bam.bai"), f"rc={rc} err={e[:100]!r}")
rc, o, e = out(f"samtools idxstats {W}/umi.sorted.bam")
info("umi idxstats:\n" + o)
n_all = int(out(f"samtools view -c {W}/umi.bam")[1])
tot = sum(int(l.split('\t')[2]) + int(l.split('\t')[3]) for l in o.splitlines())
check("idxstats (mapped+unmapped) of sorted+indexed UMI BAM == records in unsorted input (15788)", tot == n_all == 15788, f"{tot} vs {n_all}")
contig = o.splitlines()[0].split("\t")[0]
info(f"UMI BAM contig name: {contig!r}")
# contig name that looks like a region
rc, o, e = out(f"samtools view -c {W}/umi.sorted.bam '{contig}'")
check("samtools view -c '<contig-with-colon-name>' returns the whole-contig count", rc == 0 and int(o) == 15788, f"rc={rc} n={o}")
whole = int(o) if rc == 0 else -1
rc, o, e = out(f"samtools view -c {W}/umi.sorted.bam '{{{contig}}}:100-200'")
info(f"brace syntax {{contig}}:100-200 -> rc={rc} n={o} err={e[:100]!r}")

# ---- D. SKILL's example on contig with ':' (HLA style, synthetic) -------------------------------------------
out(f"samtools index {W}/hla.bam")
rc, o, e = out(f"samtools view -c {W}/hla.bam 'HLA-A*01:01:01:01'")
check("samtools view -c 'HLA-A*01:01:01:01' (whole contig) == 3", rc == 0 and o == "3", f"rc={rc} n={o} err={e[:100]!r}")
rc, o, e = out(f"samtools view -c {W}/hla.bam 'HLA-A*01:01:01:01:1-1500'")
info(f"HLA region with coords: rc={rc} n={o} err={e[:150]!r}")
rc, o, e = out(f"samtools view -c {W}/hla.bam '{{HLA-A*01:01:01:01}}:1-1500'")
check("brace syntax {HLA-A*01:01:01:01}:1-1500 == 2 (reads at 10, 1000)", rc == 0 and o == "2", f"n={o}")
rc, o, e = out(f"python {W}/examples/fetch_regions.py {W}/hla.bam 'HLA-A*01:01:01:01:1-1500'")
check("shipped fetch_regions.py handles a contig name that contains ':'", rc == 0 and "Total reads" in o, f"rc={rc} err={e.splitlines()[-1:] }")
rc, o, e = out(f"python {W}/examples/fetch_regions.py {W}/hla.bam 'chr1:1-1000'")
check("fetch_regions.py on ordinary contig (control) == 2 reads", rc == 0 and "Total reads in chr1:1-1000: 2" in o, o.splitlines()[-1:])

# ---- E. other region-format edge cases against the example vs samtools ---------------------------------------
for reg, label in [("chr22:1,952-4,700", "comma thousands separators"), ("chr22", "bare contig, no coordinates"),
                   ("chr22:1952", "start only"), ("chr22:1952-", "open end"), ("chr22:0-100", "0-based start"),
                   ("chr22:5000-4000", "end before start")]:
    rs, os_, es = out(f"samtools view -c {W}/h22.bam '{reg}'")
    rf, of, ef = out(f"python {W}/examples/fetch_regions.py {W}/h22.bam '{reg}'")
    info(f"[{label}] {reg!r}: samtools rc={rs} out={os_!r} err={es[:90]!r} | example rc={rf} tail={of.splitlines()[-1:]} err={ef.splitlines()[-1:]}")
    if label in ("comma thousands separators", "bare contig, no coordinates"):
        check(f"shipped example accepts region form {reg!r} that samtools accepts", rs == 0 and rf == 0, f"samtools rc={rs} n={os_}; example rc={rf}")

# ---- F. wrong contig naming (SKILL 'Contig-Naming Sanity Check') -----------------------------------------------
rc, o, e = out(f"samtools view -c {W}/h22.bam 22:1-4000")
info(f"samtools view -c 22:1-4000 (BAM uses chr22): rc={rc} n={o!r} err={e[:150]!r}")
check("samtools reports the wrong contig loudly (rc!=0 or warning) rather than silent 0", rc != 0 or "unknown reference" in e or "not found" in e, f"rc={rc} out={o!r} err={e[:120]!r}")
with pysam.AlignmentFile(f"{W}/h22.bam", "rb") as b:
    try:
        n = b.count("22", 0, 4000)
        check("pysam count on wrong contig raises", False, f"returned {n}")
    except Exception as ex:
        check("pysam count on wrong contig raises (ValueError)", True, f"{type(ex).__name__}: {ex}")
    try:
        list(b.fetch("chr22", 5000, 4000)); check("pysam fetch start>end raises", False)
    except Exception as ex:
        check("pysam fetch start>end raises", True, f"{type(ex).__name__}: {ex}")
    n0 = sum(1 for _ in b.fetch("chr22", 0, 1951))
    check("pysam fetch before first read returns 0 (no error)", n0 == 0, n0)

# ---- G. missing index -----------------------------------------------------------------------------------------
shutil.copy(f"{W}/h22.bam", f"{W}/noidx.bam")
rc, o, e = out(f"samtools view {W}/noidx.bam chr22:1-100")
check("SKILL table text 'random alignment retrieval only works for indexed BAM' (case-insensitive) present", "andom alignment retrieval only works for indexed" in e, e[:250])
check("SKILL/usage-guide text 'could not retrieve index file' present (case-insensitive)", "ould not retrieve index file" in e, e[:250])
rc, o, e = out(f"samtools idxstats {W}/noidx.bam")
info(f"idxstats without index: rc={rc} err={e[:200]!r}")
rows_slow = o.splitlines()
check("idxstats without an index warns on stderr ('reverting to slow method') and still returns chr22 5642 (full-scan fallback, not a failure; SKILL does not mention this)", "reverting to slow method" in e and "chr22	40001	5642	0" in rows_slow, f"rc={rc} out={o!r}")
with pysam.AlignmentFile(f"{W}/noidx.bam", "rb") as b:
    try:
        list(b.fetch("chr22", 0, 100)); check("pysam fetch without index raises", False)
    except Exception as ex:
        check("pysam fetch without index raises", True, f"{type(ex).__name__}: {ex}")
    try:
        st = b.get_index_statistics(); check("pysam get_index_statistics without index raises (or empty)", True, f"{type(st)} {list(st)[:2]}")
    except Exception as ex:
        check("pysam get_index_statistics without index raises", True, f"{type(ex).__name__}: {ex}")

# ---- H. header lies about sort order ------------------------------------------------------------------------------
rc, o, e = out(f"samtools view -h {W}/umi.bam | sed '1i @HD\\tVN:1.6\\tSO:coordinate' | samtools view -b -o {W}/liar.bam -")
rc, o, e = out(f"samtools view -H {W}/liar.bam | grep '^@HD'")
info(f"liar header: {o}")
rc, o, e = out(f"samtools index {W}/liar.bam")
check("BAM whose @HD claims SO:coordinate but is not sorted: samtools index still refuses", rc != 0, f"rc={rc} err={e[:160]!r}  (header check alone would have passed)")

# ---- I. empty BAM -------------------------------------------------------------------------------------------------
rc, o, e = out(f"samtools view -H {W}/h22.bam | samtools view -b -o {W}/empty.bam -")
rc, o, e = out(f"samtools index {W}/empty.bam && samtools idxstats {W}/empty.bam")
info(f"empty BAM index+idxstats: rc={rc} out={o!r} err={e[:120]!r}")
check("header-only BAM: index succeeds and idxstats prints chr22 0 0 0", rc == 0 and "chr22\t40001\t0\t0" in o, f"rc={rc} out={o!r}")
# ---- J. usage-guide mito fraction awk on a BAM with no chrM/MT -------------------------------------------------------
rc, o, e = out(f"samtools idxstats {W}/h22.bam | awk '/^chrM/ {{mt=$3}} {{total+=$3}} END {{printf \"MT: %.2f%%\\n\", mt/total*100}}'")
info(f"usage-guide MT fraction on BAM without chrM: {o!r} (silent 0.00%: chrM absent, and 'MT' naming would also be missed)")
rc, o, e = out(f"samtools idxstats {W}/empty.bam | awk '/^chrM/ {{mt=$3}} {{total+=$3}} END {{printf \"MT: %.2f%%\\n\", mt/total*100}}'")
info(f"usage-guide MT fraction on an empty BAM: rc={rc} out={o!r} err={e[:100]!r} (division by zero)")
dump("out/t3_results.json")
