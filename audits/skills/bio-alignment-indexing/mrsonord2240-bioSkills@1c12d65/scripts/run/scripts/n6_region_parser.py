#!/usr/bin/env python3
"""Input 6 (NEW, stress): fetch_regions.py's own region parser vs `samtools view -c` vs a full-scan truth.
Forms: chr:s-e, chr:s-e with thousands commas, bare contig, chr:s-, chr:s, chr:-e, {braced}, contigs containing ':' / '-' / ',' / '.',
0-based vs 1-based edges (read start/end +-1), start=0, end<start, region past contig end.
Data: REAL human chr22 slice, REAL 1000G chr20 slice (header has HLA-A*01:01:01:01-style contigs), REAL SARS-CoV-2 ARTIC BAM (contig MN908947.3),
REAL RNA BAM (spliced reads), SYNTHETIC weird-contig BAM (data built here; ground truth = full scan).
Run in WSL from run/:  python scripts/n6_region_parser.py"""
import os, sys, shutil, random, subprocess, io, contextlib
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam

AFD = os.environ["AFDATA"]
W = "work/n6"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
shutil.copytree("skill/examples", f"{W}/examples")
sys.path.insert(0, f"{W}/examples")
import fetch_regions as fr     # the SHIPPED example, imported from a copy

# ---- fixtures ---------------------------------------------------------------------------------------------------------
files = {
    "human": f"{AFD}/human/test.paired_end.sorted.bam",
    "1000g": f"{AFD}/1000g/HG00349.chr20_1400000-1500000.bam",
    "artic": f"{AFD}/sarscov2/sars-cov-2_v5.3.2.nanopore.bam",
    "rna": f"{AFD}/human/test.rna.paired_end.sorted.bam",
}
for k, v in files.items():
    shutil.copy(v, f"{W}/{k}.bam")
    if os.path.exists(v + ".bai"): shutil.copy(v + ".bai", f"{W}/{k}.bam.bai")
    else: out(f"samtools index {W}/{k}.bam")
# synthetic weird-contig BAM: contigs with ':' '-' ',' '.' and one that looks like a region
hdr = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [
    {"SN": "chr1", "LN": 100000}, {"SN": "a:1-5", "LN": 5000}, {"SN": "ctg,1", "LN": 5000}, {"SN": "12:34", "LN": 5000},
    {"SN": "HLA-A*01:01:01:01", "LN": 3503}, {"SN": "x-y", "LN": 5000}]})
def rec(name, tid, pos, ln=100):
    a = pysam.AlignedSegment(hdr); a.query_name = name; a.flag = 0; a.reference_id = tid; a.reference_start = pos
    a.mapping_quality = 60; a.cigarstring = f"{ln}M"; a.query_sequence = "A" * ln; a.query_qualities = pysam.qualitystring_to_array("I" * ln); return a
random.seed(11)
with pysam.AlignmentFile(f"{W}/weird.bam", "wb", header=hdr) as f:      # SYNTHETIC
    for tid, ln in [(0, 100000), (1, 5000), (2, 5000), (3, 5000), (4, 3503), (5, 5000)]:
        for p in sorted(random.sample(range(0, ln - 100), 30)):
            f.write(rec(f"r{tid}_{p}", tid, p))
out(f"samtools index {W}/weird.bam")
files["weird"] = None

def load(bam):
    recs = []
    with pysam.AlignmentFile(f"{W}/{bam}.bam", "rb") as b:
        refs = list(b.references); lens = dict(zip(b.references, b.lengths))
        for r in b.fetch(until_eof=True):
            if r.reference_id < 0: continue
            st = r.reference_start; en = r.reference_end if r.reference_end is not None else st + 1
            recs.append((r.reference_name, st, en))
    return refs, lens, recs

def truth(recs, contig, s1, e1):
    s0 = (s1 - 1) if s1 else 0
    return sum(1 for c, st, en in recs if c == contig and st < e1 and en > s0)

def ex_count(bam, region):
    """count as the shipped fetch_regions.py would (its own parse_region + fetch); returns int or ('ERR', text)"""
    with pysam.AlignmentFile(f"{W}/{bam}.bam", "rb") as aln:
        try:
            c, s, e = fr.parse_region(region, aln.references)
        except ValueError as ex:
            return ("REJECT", str(ex))
        try:
            return sum(1 for _ in aln.fetch(c, s, e))
        except Exception as ex:
            return ("CRASH", f"{type(ex).__name__}: {ex}")

def sam_count(bam, region):
    rc, o, e = out(f"samtools view -c {W}/{bam}.bam '{region}'")
    return (int(o) if rc == 0 and o.isdigit() else None), ("Continue anyway" in e or "invalid region" in e)

def fmt_commas(n): return f"{n:,}"

sets = {}
mism, rejects_ok, crashes, both_zero_bad = [], [], [], []
nchk = 0
for bam in ["human", "1000g", "artic", "rna", "weird"]:
    refs, lens, recs = load(bam)
    contigs_with_reads = sorted({c for c, _, _ in recs})
    cases = []
    for c in contigs_with_reads:
        L = lens[c]
        rs = [x for x in recs if x[0] == c]
        picks = random.sample(rs, min(6, len(rs)))
        for (_, st, en) in picks:
            p1 = st + 1                                       # 1-based first base of the read
            e1 = en                                           # 1-based last base
            for (a, b) in [(p1, e1), (p1 - 1, p1 - 1), (p1, p1), (e1, e1), (e1 + 1, e1 + 1), (p1 - 5, p1 - 1), (max(p1 - 300, 1), p1 + 300)]:
                if a >= 1: cases.append((c, a, b))
        for _ in range(8):
            a = random.randint(1, L); b = min(L, a + random.choice([0, 10, 500, 5000, 100000])); cases.append((c, a, b))
        cases.append((c, 1, L)); cases.append((c, 1, L + 50000))
    for (c, a, b) in cases:
        forms = {
            "c:s-e": f"{c}:{a}-{b}",
            "c:s-e (commas)": f"{c}:{fmt_commas(a)}-{fmt_commas(b)}",
            "c:s-": f"{c}:{a}-",
            "c:s": f"{c}:{a}",
            "braced": "{" + c + "}" + f":{a}-{b}",
        }
        for label, reg in forms.items():
            nchk += 1
            t = truth(recs, c, a, b if label in ("c:s-e", "c:s-e (commas)", "braced") else 10 ** 12)
            sc, sam_warn = sam_count(bam, reg)
            ec = ex_count(bam, reg)
            if isinstance(ec, tuple):
                if ec[0] == "REJECT":
                    rejects_ok.append((bam, reg, sc, ec[1]))
                    continue
                crashes.append((bam, reg, sc, ec)); continue
            if not (ec == t == sc):
                mism.append((bam, reg, "truth", t, "samtools", sc, "example", ec))
    # whole contig, bare
    for c in contigs_with_reads:
        nchk += 1
        t = truth(recs, c, 1, 10 ** 12); sc, _ = sam_count(bam, c); ec = ex_count(bam, c)
        if not (t == sc == ec): mism.append((bam, c, "bare contig", "truth", t, "samtools", sc, "example", ec))
    info(f"{bam}: {len(cases)} base regions x 5 forms, {len(refs)} contigs, {len(recs)} placed records")

info(f"total region strings compared: {nchk}")
check("count(shipped parser+fetch) == samtools view -c == full-scan truth on every accepted region (5 forms x ~2000 regions, 5 BAMs)", not mism, f"{len(mism)} mismatches; first: {mism[:3]}")
check("no accepted-by-samtools region string is REJECTED by the example's parser (comma/braced/open-ended/colon contigs)", not rejects_ok, f"{len(rejects_ok)} rejected; first: {rejects_ok[:4]}")
check("no region string makes the example crash with an uncaught exception", not crashes, f"{len(crashes)} crashes; first: {crashes[:3]}")

# ---- specific edge strings ---------------------------------------------------------------------------------------------
def line(reg, bam="human"):
    return sam_count(bam, reg), ex_count(bam, reg)
edge = [("human", "chr22:0-100"), ("human", "chr22:5000-4000"), ("human", "chr22:1952-1952"), ("human", "chr22:1951-1951"),
        ("human", "chr22:-2000"), ("human", "chr22:1952-99999999"), ("human", "chr22:abc"), ("human", "chr22:12-x"), ("human", "chr22:"),
        ("weird", "ctg,1"), ("weird", "ctg,1:1-5000"), ("weird", "a:1-5"), ("weird", "a:1-5:1-2500"), ("weird", "12:34:100-4000"), ("weird", "x-y:1-5000"),
        ("weird", "HLA-A*01:01:01:01:1-1500"), ("weird", "HLA-A*01:01:01"), ("weird", "chr1:1-1000,2000"), ("artic", "MN908947.3:100-2000")]
lines = []
for bam, reg in edge:
    (sc, warn), ec = line(reg, bam)
    lines.append((bam, reg, sc, warn, ec))
    info(f"[{bam}] {reg!r}: samtools={sc} (warn={warn}) | example={ec}")
d = {(b, r): (sc, warn, ec) for b, r, sc, warn, ec in lines}
check("chr22:0-100 (start=0): example does not crash with an uncaught ValueError", not (isinstance(d[('human', 'chr22:0-100')][2], tuple) and d[('human', 'chr22:0-100')][2][0] == "CRASH"), d[('human', 'chr22:0-100')])
check("chr22:5000-4000 (end<start): example exits cleanly (no uncaught ValueError traceback)", not (isinstance(d[('human', 'chr22:5000-4000')][2], tuple) and d[('human', 'chr22:5000-4000')][2][0] == "CRASH"), d[('human', 'chr22:5000-4000')])
check("chr22:1952-1952 single base and 1951-1951 (0-based/1-based edge): example == samtools", d[('human', 'chr22:1952-1952')][0] == d[('human', 'chr22:1952-1952')][2] and d[('human', 'chr22:1951-1951')][0] == d[('human', 'chr22:1951-1951')][2], f"{d[('human','chr22:1952-1952')]} {d[('human','chr22:1951-1951')]}")
check("chr22:-2000 (open start): example == samtools", d[('human', 'chr22:-2000')][0] == d[('human', 'chr22:-2000')][2], d[('human', 'chr22:-2000')])
check("region past contig end (chr22:1952-99999999): example == samtools", d[('human', 'chr22:1952-99999999')][0] == d[('human', 'chr22:1952-99999999')][2], d[('human', 'chr22:1952-99999999')])
check("contig name containing a comma ('ctg,1') is accepted by the example as it is by samtools", d[('weird', 'ctg,1')][0] == d[('weird', 'ctg,1')][2], d[('weird', 'ctg,1')])
check("contig 'a:1-5' (looks like a region) with and without coordinates: example == samtools", d[('weird', 'a:1-5')][0] == d[('weird', 'a:1-5')][2] and d[('weird', 'a:1-5:1-2500')][0] == d[('weird', 'a:1-5:1-2500')][2], f"{d[('weird','a:1-5')]} {d[('weird','a:1-5:1-2500')]}")
check("contig '12:34' and 'x-y' with coordinates: example == samtools", d[('weird', '12:34:100-4000')][0] == d[('weird', '12:34:100-4000')][2] and d[('weird', 'x-y:1-5000')][0] == d[('weird', 'x-y:1-5000')][2], f"{d[('weird','12:34:100-4000')]} {d[('weird','x-y:1-5000')]}")
check("garbage coordinates 'chr22:abc' / 'chr22:12-x' are rejected by the example with a message (samtools: warning + 0)", all(isinstance(d[('human', r)][2], tuple) and d[('human', r)][2][0] == "REJECT" for r in ("chr22:abc", "chr22:12-x")), f"{d[('human','chr22:abc')]} {d[('human','chr22:12-x')]}")

# ---- end-to-end (subprocess) on a handful, exit codes + messages ---------------------------------------------------------------
def run_cli(bam, reg):
    return out(f"python {W}/examples/fetch_regions.py {W}/{bam}.bam '{reg}'")
rc, o, e = run_cli("weird", "a:1-5:1-2500"); tot = [l for l in o.splitlines() if l.startswith("Total")]
check("CLI end-to-end: 'a:1-5:1-2500' Total == samtools view -c", rc == 0 and tot and tot[0].split(":")[-1].strip() == str(sam_count("weird", "a:1-5:1-2500")[0]), f"rc={rc} {tot} sam={sam_count('weird','a:1-5:1-2500')}")
rc, o, e = run_cli("human", "chr99:1-100"); check("CLI: unknown contig exits 1 with a one-line 'Bad region' message", rc == 1 and "Bad region" in e and "Traceback" not in e, f"rc={rc} err={e[-160:]!r}")
rc, o, e = out(f"samtools view -c {W}/human.bam 'chr22:0-4000'"); info(f"samtools chr22:0-4000 -> {o}; example -> {ex_count('human','chr22:0-4000')}")
rc, o, e = run_cli("human", "chr22:0-100"); check("CLI: chr22:0-100 exits with a clean message, not a traceback", "Traceback" not in e, f"rc={rc} err={e[-200:]!r}")
rc, o, e = run_cli("human", "chr22:5000-4000"); check("CLI: chr22:5000-4000 exits with a clean message, not a traceback", "Traceback" not in e, f"rc={rc} err={e[-200:]!r}")
dump("out/n6_results.json")
