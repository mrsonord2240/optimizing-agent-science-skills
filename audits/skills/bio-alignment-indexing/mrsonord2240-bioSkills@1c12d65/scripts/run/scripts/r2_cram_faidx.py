#!/usr/bin/env python3
"""Input 2 (variant A, REGRESSION on the fixed Skill): index a CRAM, region-fetch with the new CRAM section's recipes,
idxstats, REF_PATH / @SQ UR semantics, fetch_regions.py --reference, FASTA index.
Data: REAL nf-core human chr22 slice CRAM + FASTA (public-data/human); truth = same reads in the BAM + plain-python FASTA parse.
Run in WSL from run/:  python scripts/r2_cram_faidx.py
"""
import os, sys, shutil, io, contextlib, time
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam

AFD = os.environ["AFDATA"]
W = "work/r2"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
for f in ["test.paired_end.sorted.cram", "genome.fasta", "test.paired_end.sorted.bam"]:
    shutil.copy(f"{AFD}/human/{f}", f"{W}/{f}")
shutil.copytree("skill/examples", f"{W}/examples")
CR = f"{W}/test.paired_end.sorted.cram"; BM = f"{W}/test.paired_end.sorted.bam"; FA = f"{W}/genome.fasta"

# --- 'Index CRAM' -------------------------------------------------------------------------------------
rc, o, e = out(f"samtools index {CR}")
check("samtools index x.cram -> x.cram.crai without a reference", rc == 0 and os.path.getsize(CR + ".crai") > 0, f"rc={rc} err={e[:120]!r}")
bam_n = int(out(f"samtools index {BM} && samtools view -c {BM} chr22:1952-4700")[1])

# --- 'CRAM' section claims, each verified ------------------------------------------------------------------
rc, o, e = out(f"samtools view -T {FA} {CR} chr22:1952-4700 | wc -l")
check("SKILL `samtools view -T ref.fa in.cram region` returns records == BAM count 5642", rc == 0 and int(o) == bam_n == 5642, f"lines={o} bam={bam_n}")
rc, o, e = out(f"samtools view {CR} chr22:1952-4700 | wc -l")
rc2, o2, e2 = out(f"samtools view {CR} chr22:1952-4700 2>&1 >/dev/null | head -3")
check("SKILL claim: without a reachable reference `samtools view` prints no records and says 'Failed to populate reference'", int(o) == 0 and "Failed to populate reference" in o2, f"lines={o} msg={o2[:200]!r}")
rc, o, e = out(f"samtools view -c {CR} chr22:1952-4700")
check("SKILL claim: `samtools view -c` still counts a CRAM without a reference (5642)", o == "5642", f"n={o} rc={rc} err={e[:80]!r}")

# pysam recipe: the shipped block executed verbatim with paths substituted
blk = block_containing("reference_filename='ref.fa'", "python")
code = blk.replace("input.cram", CR).replace("ref.fa", FA).replace("'chr1', 999, 2000", "'chr22', 1951, 4700") + "\nprint(n)"
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec("import pysam\n" + code, {})
check("SKILL pysam CRAM recipe (mode 'rc', reference_filename=) count == 5642", buf.getvalue().strip() == "5642", buf.getvalue())
try:
    with pysam.AlignmentFile(CR, "rc") as c:
        n = c.count("chr22", 1951, 4700)
    check("SKILL claim: pysam without reference raises OSError 'truncated file'", False, f"returned {n} silently")
except OSError as ex:
    check("SKILL claim: pysam without reference raises OSError 'truncated file'", "truncated" in str(ex), f"{type(ex).__name__}: {ex}")
with pysam.AlignmentFile(CR, "rc", reference_filename=FA) as c:
    st = [(s.contig, s.mapped, s.unmapped) for s in c.get_index_statistics()]
check("SKILL claim: get_index_statistics() on CRAM silently gives 0 mapped", st and st[0][1] == 0, st)
rc, o, e = out(f"samtools idxstats {CR}")
check("SKILL: `samtools idxstats x.cram` gives chr22 5642 mapped", "chr22\t40001\t5642\t0" in o, o.replace("\n", " | "))
pi = pysam.idxstats(CR)
check("SKILL: `pysam.idxstats('x.cram')` gives chr22 5642 mapped", "chr22\t40001\t5642\t0" in pi, pi.replace("\n", " | "))
diffs = []
for s, t in [(1952, 2000), (2500, 2600), (3000, 3100), (4000, 4617), (1, 1951), (4618, 40001)]:
    a = int(out(f"samtools view -c -T {FA} {CR} chr22:{s}-{t}")[1]); b = int(out(f"samtools view -c {BM} chr22:{s}-{t}")[1])
    if a != b: diffs.append((s, t, a, b))
check("6 sub-regions: CRAM(.crai) counts == BAM(.bai) counts", not diffs, diffs)

# --- REF_PATH: the SKILL says 'or REF_PATH / the @SQ UR: path' -----------------------------------------------------
rc, o, e = out(f"samtools view -H {CR} | grep '^@SQ'")
info(f"CRAM @SQ line: {o!r}")
rc, o, e = out(f"mkdir -p {W}/rp_plain && cp {FA} {FA}.fai {W}/rp_plain/ && REF_PATH={os.path.abspath(W)}/rp_plain samtools view {CR} chr22:1952-1960 | wc -l")
plain_lines = int(o)
check("REF_PATH pointing at a directory that holds genome.fasta (plain FASTA) does NOT give records (REF_PATH is an MD5 cache, not a FASTA dir)", plain_lines == 0, f"lines={plain_lines}")
md5 = out(f"samtools dict {FA} | grep -o 'M5:[0-9a-f]*' | cut -d: -f2")[1]
d = os.path.abspath(W) + "/rp_md5"; os.makedirs(d, exist_ok=True)
seq_only = "".join(l.strip() for l in open(FA) if not l.startswith(">")).upper()
open(f"{d}/{md5}", "w").write(seq_only)          # flat MD5-named file: what REF_PATH=<dir> expects
rc, o, e = out(f"REF_PATH={d} samtools view {CR} chr22:1952-1960 | wc -l")
check("REF_PATH=<dir holding a file named by the reference MD5> gives the 2 records in chr22:1952-1960", o == "2", f"lines={o} md5={md5}")
# @SQ UR: honoured? re-encode with an absolute reference path so UR is a real local path
rc, o, e = out(f"samtools view -C -T {os.path.abspath(FA)} -o {W}/ur.cram {BM} && samtools index {W}/ur.cram && samtools view -H {W}/ur.cram | grep '^@SQ'")
info(f"CRAM re-encoded from BAM: @SQ={o!r} rc={rc}")
rc, o, e = out(f"samtools view {W}/ur.cram chr22:1952-1960 | wc -l")
check("@SQ UR: pointing at an existing local FASTA is used without -T (2 records)", o == "2", f"lines={o}")

# --- shipped example on CRAM ---------------------------------------------------------------------------------------
rc, o, e = out(f"python {W}/examples/fetch_regions.py {CR} chr22:1952-2000 --reference {FA}")
exp = int(out(f"samtools view -c {BM} chr22:1952-2000")[1])
tot = [l for l in o.splitlines() if l.startswith("Total reads")]
check("fetch_regions.py on a .cram with --reference: Total == BAM count", rc == 0 and tot and int(tot[0].split(":")[-1]) == exp, f"rc={rc} tot={tot} exp={exp} err={e[-150:]!r}")
m0 = os.path.getmtime(CR + ".crai"); rc, o, e = out(f"python {W}/examples/fetch_regions.py {CR} chr22:1952-2000 --reference {FA}")
check("fetch_regions.py on CRAM does not re-index a fresh .crai", os.path.getmtime(CR + ".crai") == m0 and "Indexing" not in e, e[-100:])
rc, o, e = out(f"python {W}/examples/fetch_regions.py {CR} chr22:1952-2000")
check("fetch_regions.py on CRAM without --reference gives a clean message with a --reference hint (no traceback)", rc != 0 and "--reference" in e and "Traceback" not in e, f"rc={rc} err={e[-200:]!r}")

# --- staleness on a CRAM (shipped ensure_indexed on cram) ---------------------------------------------------------
ns = {}; exec(block_containing("def ensure_indexed"), ns)
shutil.copy(CR, f"{W}/s.cram"); out(f"samtools index {W}/s.cram"); time.sleep(1.1)
shutil.copy(CR, f"{W}/s.cram"); old = os.path.getmtime(f"{W}/s.cram.crai")   # cram rewritten -> newer than crai
ns["ensure_indexed"](f"{W}/s.cram")
check("ensure_indexed rebuilds a stale .crai", os.path.getmtime(f"{W}/s.cram.crai") > old and not os.path.exists(f"{W}/s.cram.bai"), sorted(x for x in os.listdir(W) if x.startswith("s.")))

# --- FASTA index -------------------------------------------------------------------------------------------------------
rc, o, e = out(f"samtools faidx {FA}")
fai = open(FA + ".fai").read().split()
check("samtools faidx creates .fai chr22 40001", rc == 0 and fai[0] == "chr22" and fai[1] == "40001", fai[:5])
seq = "".join(l.strip() for l in open(FA) if not l.startswith(">")).upper()
rc, o, e = out(f"samtools faidx {FA} chr22:1000-2000")
fa_seq = "".join(l for l in o.splitlines() if not l.startswith(">")).upper()
check("samtools faidx chr22:1000-2000 == plain-python seq[999:2000] (1001 bp)", fa_seq == seq[999:2000] and len(fa_seq) == 1001, len(fa_seq))
blk = block_containing("FastaFile", "python").replace("reference.fa", FA).replace("'chr1'", "'chr22'")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec("import pysam\n" + blk, {})
check("SKILL FastaFile snippet fetch(999,2000) == faidx chr22:1000-2000 (fixed off-by-one)", buf.getvalue().strip().upper() == fa_seq, len(buf.getvalue().strip()))
os.remove(FA + ".fai")
with pysam.FastaFile(FA) as ref: pass
check("pysam.FastaFile builds a missing .fai (Quick Reference 'Automatic with FastaFile')", os.path.exists(FA + ".fai"))
rc, o, e = out(f"samtools faidx {FA} chr1:1-10")
check("samtools faidx on unknown contig fails loudly", rc != 0, f"rc={rc} err={e[:100]!r}")
dump("out/r2_results.json")
