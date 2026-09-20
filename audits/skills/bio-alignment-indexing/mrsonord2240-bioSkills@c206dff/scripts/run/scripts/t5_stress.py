#!/usr/bin/env python3
"""Input 5 (stress / multi-part): index freshness, .csi-vs-.bai precedence, the SKILL's own staleness + batch snippets,
`-L` vs `-M` index use, threads claim, idxstats semantics (secondary / supplementary / PE orphans), real ARTIC nanopore BAM.
Data: REAL 1000G HG00349 slice, REAL ARTIC nanopore BAM, SYNTHETIC semantics.bam (10 records, hand-known flags),
SYNTHETIC big.bam (1.2 M reads on a 200 Mbp contig, positions in data/big.positions.txt).
Run in WSL from run/:  python scripts/t5_stress.py"""
import os, sys, shutil, time, random, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam

AFD = os.environ["AFDATA"]
W = "work/t5"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
shutil.copy(f"{AFD}/1000g/HG00349.chr20_1400000-1500000.bam", f"{W}/hg.bam")
shutil.copy(f"{AFD}/sarscov2/sars-cov-2_v5.3.2.nanopore.bam", f"{W}/nano.bam")
shutil.copy("data/semantics.bam", f"{W}/sem.bam")
shutil.copy("data/big.bam", f"{W}/big.bam")
REG = "chr20:1400000-1500000"

def scount(bam, region=""):
    rc, o, e = out(f"samtools view -c {bam} {region}")
    return (int(o) if rc == 0 and o.isdigit() else None), e

# ================= A. STALE INDEX ===========================================================
out(f"samtools index {W}/hg.bam")
n_before, _ = scount(f"{W}/hg.bam", "chr20:1440001-1460000")
# B = a different BAM with the same name (half the reads), index NOT rebuilt
out(f"samtools view -b -s 3.5 -o {W}/half.bam {W}/hg.bam")
shutil.copy(f"{W}/hg.bam", f"{W}/orig.bam"); shutil.copy(f"{W}/hg.bam.bai", f"{W}/orig.bam.bai")
time.sleep(1.1)
shutil.copy(f"{W}/half.bam", f"{W}/hg.bam")            # BAM replaced -> mtime newer than hg.bam.bai
rc, o, e = out(f"samtools view -c {W}/hg.bam chr20:1440001-1460000")
stale_n = o
info(f"STALE index run: rc={rc} count={o!r} stderr={e[:300]!r}")
# truth: re-index a copy
shutil.copy(f"{W}/half.bam", f"{W}/half2.bam"); out(f"samtools index {W}/half2.bam")
true_n, _ = scount(f"{W}/half2.bam", "chr20:1440001-1460000")
full_scan = sum(1 for r in pysam.AlignmentFile(f"{W}/half.bam", "rb").fetch(until_eof=True) if r.reference_id >= 0 and r.reference_name == "chr20" and r.reference_start < 1460000 and (r.reference_end or r.reference_start + 1) > 1440000)
check("full-scan truth == freshly re-indexed copy for the replaced BAM", true_n == full_scan, f"{true_n} vs {full_scan}")
check("stale .bai: samtools warns on stderr that the index is older than the data (mtime check in htslib)", "older than the data" in e or "older than" in e, e[:200])
check("stale .bai: region count is WRONG or errors (SKILL: 'wrong (or zero) reads')", (rc != 0) or (o != str(true_n)), f"stale={o!r} rc={rc} truth={true_n}")
rc2, o2, e2 = out(f"samtools idxstats {W}/hg.bam")
tot_stale = sum(int(l.split('\t')[2]) for l in o2.splitlines())
tot_true = int(out(f"samtools view -c -F 4 {W}/half.bam")[1])
check("stale .bai: idxstats silently reports the OLD totals", tot_stale != tot_true, f"idxstats mapped sum={tot_stale}, true={tot_true}, stderr={e2[:100]!r}")
try:
    b = pysam.AlignmentFile(f"{W}/hg.bam", "rb")
    pn = sum(1 for _ in b.fetch("chr20", 1440000, 1460000))
    b.close()
    info(f"pysam fetch on stale index: {pn} (truth {true_n})")
    check("pysam fetch on stale index also wrong (no warning surfaced to Python)", pn != true_n, f"{pn} vs {true_n}")
except Exception as ex:
    info(f"pysam fetch on stale index raised {type(ex).__name__}: {ex}")
    check("pysam fetch on stale index errors or is wrong", True, f"{type(ex).__name__}: {ex}")

# --- SKILL 'Index Staleness' snippet verbatim (bash), on the stale BAM
snippet = f'''cd {W}; if [ hg.bam -nt hg.bam.bai ]; then echo "Index older than BAM; re-indexing"; samtools index hg.bam; fi'''
rc, o, e = out(snippet)
n_fix, _ = scount(f"{W}/hg.bam", "chr20:1440001-1460000")
check("SKILL staleness snippet detects and fixes the stale .bai (count == truth after)", "re-indexing" in o and n_fix == true_n, f"{o!r} n_after={n_fix} truth={true_n}")
# snippet on FRESH index: nothing
rc, o, e = out(snippet)
check("SKILL staleness snippet is quiet when index is fresh", "re-indexing" not in o, o)
# --- snippet on a CSI-only BAM: -nt against a MISSING file is always true
shutil.copy(f"{W}/half.bam", f"{W}/csionly.bam"); out(f"samtools index -c {W}/csionly.bam")
rc, o, e = out(f'cd {W}; if [ csionly.bam -nt csionly.bam.bai ]; then echo "Index older than BAM; re-indexing"; samtools index csionly.bam; fi; ls csionly.bam*')
check("SKILL staleness snippet on a CSI-only BAM: false 'stale' alarm (no .bai exists) and it creates a redundant .bai", "re-indexing" in o and os.path.exists(f"{W}/csionly.bam.bai"), o.replace("\n", " | "))

# ================= B. .csi vs .bai PRECEDENCE ============================================
# fixtures: A = full BAM (orig.bam), B = half BAM. Give the SAME bam name both a correct index of one kind and a WRONG index of the other kind.
def make_pair(kind_correct):
    d = f"{W}/prec_{kind_correct}"; os.makedirs(d)
    shutil.copy(f"{W}/half.bam", f"{d}/x.bam")
    # index of the OTHER content (full orig.bam), built under a temp name
    shutil.copy(f"{W}/orig.bam", f"{d}/wrong.bam")
    if kind_correct == "csi":
        out(f"samtools index -c {d}/x.bam"); out(f"samtools index {d}/wrong.bam"); shutil.move(f"{d}/wrong.bam.bai", f"{d}/x.bam.bai")
    else:
        out(f"samtools index {d}/x.bam"); out(f"samtools index -c {d}/wrong.bam"); shutil.move(f"{d}/wrong.bam.csi", f"{d}/x.bam.csi")
    os.remove(f"{d}/wrong.bam")
    os.utime(f"{d}/x.bam", (time.time() - 100, time.time() - 100))     # BAM older than both indexes -> no staleness warning noise
    return d
for kind in ["csi", "bai"]:
    d = make_pair(kind)
    rc, o, e = out(f"samtools view -c {d}/x.bam chr20:1440001-1460000")
    try:
        b = pysam.AlignmentFile(f"{d}/x.bam", "rb")
        try: pn = b.count("chr20", 1440000, 1460000)
        except Exception as ex: pn = f"ERR {type(ex).__name__}: {str(ex)[:60]}"
        try: b.close()
        except Exception as ex: pn = f"{pn} (close: {type(ex).__name__})"
    except Exception as ex:
        pn = f"ERR open {type(ex).__name__}"
    info(f"precedence fixture (correct={kind}, other kind wrong): samtools={o!r} pysam={pn} truth={true_n} err={e[:100]!r}")
    if kind == "csi":
        check("htslib prefers .csi over .bai when both exist (SKILL claim): correct .csi + wrong .bai gives the correct count", o == str(true_n) and pn == true_n, f"samtools={o} pysam={pn} truth={true_n}")
    else:
        check("htslib prefers .csi over .bai when both exist (converse): wrong .csi + correct .bai gives the WRONG count", o != str(true_n), f"samtools={o} pysam={pn} truth={true_n}")

# The SKILL's own two snippets interacting: CSI-only BAM modified -> staleness snippet builds a fresh BAI -> stale CSI still wins
d = f"{W}/trap"; os.makedirs(d)
shutil.copy(f"{W}/orig.bam", f"{d}/t.bam"); out(f"samtools index -c {d}/t.bam")
time.sleep(1.1); shutil.copy(f"{W}/half.bam", f"{d}/t.bam")     # BAM replaced; CSI now stale
out(f'cd {d}; if [ t.bam -nt t.bam.bai ]; then echo re-indexing; samtools index t.bam; fi')   # SKILL snippet
rc, o, e = out(f"samtools view -c {d}/t.bam chr20:1440001-1460000")
files = sorted(os.listdir(d))
check("TRAP: after the SKILL's staleness snippet on a CSI-indexed BAM, region counts are still wrong (stale .csi beats the fresh .bai)", o != str(true_n), f"count={o!r} truth={true_n} files={files} err={e[:120]!r}")

# ================= C. htsjdk precedence (SKILL: 'htsjdk/Java prefers .bai') ==================
def gatk_count(d):
    for f in ("gout.bam", "gout.bai", "gerr.txt"):
        if os.path.exists(f"{d}/{f}"): os.remove(f"{d}/{f}")
    out(f"cd {d} && gatk PrintReads -I x.bam -L chr20:1440001-1460000 -O gout.bam > /dev/null 2> gerr.txt")
    err = open(f"{d}/gerr.txt", errors="replace").read()
    exc = [l for l in err.splitlines() if "Exception" in l][:1]
    n = out(f"samtools view -c {d}/gout.bam")[1] if os.path.exists(f"{d}/gout.bam") else "no output"
    return n, exc
n_a, exc_a = gatk_count(f"{W}/prec_csi")     # correct .csi + WRONG .bai
n_b, exc_b = gatk_count(f"{W}/prec_bai")     # correct .bai + WRONG .csi
info(f"GATK/htsjdk correct-CSI+wrong-BAI: records={n_a} exc={exc_a}; correct-BAI+wrong-CSI: records={n_b} exc={exc_b}; truth={true_n}")
check("htsjdk (GATK PrintReads -L) prefers .bai over .csi: wrong .bai -> no/garbled records, correct .bai (+ wrong .csi) -> truth", n_a != str(true_n) and n_b == str(true_n), f"csi-correct/bai-wrong={n_a} {exc_a}; bai-correct/csi-wrong={n_b}; truth={true_n}")

# ================= D. SKILL batch-indexing loop from usage-guide (verbatim) =====================
bd = f"{W}/batch"; os.makedirs(bd)
shutil.copy(f"{W}/half2.bam", f"{bd}/a_ok.bam"); shutil.copy(f"{W}/half2.bam.bai", f"{bd}/a_ok.bam.bai")
shutil.copy(f"{W}/half.bam", f"{bd}/b_csi.bam"); out(f"samtools index -c {bd}/b_csi.bam")
shutil.copy(f"{W}/half.bam", f"{bd}/c_none.bam")
shutil.copy(f"{AFD}/human/test.paired_end.umi_unsorted.bam", f"{bd}/d_unsorted.bam")
loop = '''cd batch; for bam in *.bam; do
    if [ ! -f "${bam}.bai" ]; then
        samtools index "$bam"
    fi
done; ls'''
open(f"{W}/loop.sh", "w").write(loop + "\n")
rc, o, e = out(f"cd {W} && bash loop.sh 2>&1")
info("batch loop output:\n" + o)
check("batch loop: unsorted BAM makes the loop print an error but continue to other files", "failed to create index" in o and os.path.exists(f"{bd}/c_none.bam.bai"), "")
check("batch loop: CSI-only BAM gets a redundant .bai (loop only tests for .bai)", os.path.exists(f"{bd}/b_csi.bam.bai") and os.path.exists(f"{bd}/b_csi.bam.csi"), sorted(os.listdir(bd)))

# ================= E. -L vs -M vs region: is the index used? ======================
positions = [int(x) for x in open("data/big.positions.txt").read().split()]
def tb(s, e_):   # 0-based half-open BED interval; reads are 100 bp
    return sum(1 for p in positions if p < e_ and p + 100 > s)
out(f"samtools index {W}/big.bam")
bed = f"{W}/early.bed"; open(bed, "w").write("chr1\t0\t200000\nchr1\t5000000\t5100000\n")
truth_bed = tb(0, 200000) + tb(5000000, 5100000)          # BED regions do not overlap, so no double counting
size = os.path.getsize(f"{W}/big.bam")
shutil.copy(f"{W}/big.bam", f"{W}/corrupt.bam"); shutil.copy(f"{W}/big.bam.bai", f"{W}/corrupt.bam.bai")
with open(f"{W}/corrupt.bam", "r+b") as fh:                # damage 100 kB at 80% of the file (positions ~160 Mbp)
    fh.seek(int(size * 0.8)); fh.write(os.urandom(100_000))
os.utime(f"{W}/corrupt.bam", (time.time() - 1000, time.time() - 1000))
rcs = {}
for label, cmd in [("region arg (index)", f"samtools view -c {W}/corrupt.bam chr1:1-200000 chr1:5000001-5100000"),
                   ("-L bed (no -M)", f"samtools view -c -L {bed} {W}/corrupt.bam"),
                   ("-M -L bed", f"samtools view -c -M -L {bed} {W}/corrupt.bam"),
                   ("--region-file", f"samtools view -c --region-file {bed} {W}/corrupt.bam"),
                   ("full scan (control)", f"samtools view -c {W}/corrupt.bam")]:
    rc, o, e = out(cmd)
    rcs[label] = (rc, o)
    info(f"corrupt-tail BAM, {label}: rc={rc} out={o!r} err={e[:120]!r}")
check("region argument uses the index: succeeds on a BAM with a damaged tail and equals truth", rcs["region arg (index)"][0] == 0 and rcs["region arg (index)"][1] == str(truth_bed), f"{rcs['region arg (index)']} truth={truth_bed}")
check("-M -L bed uses the index (succeeds on damaged tail, == truth)", rcs["-M -L bed"][0] == 0 and rcs["-M -L bed"][1] == str(truth_bed), f"{rcs['-M -L bed']} truth={truth_bed}")
check("--region-file uses the index (succeeds on damaged tail, == truth)", rcs["--region-file"][0] == 0 and rcs["--region-file"][1] == str(truth_bed), f"{rcs['--region-file']}")
check("plain -L bed does NOT use the index: it scans the whole file (fails on the damaged tail) -- SKILL lists it under 'Using Indices for Region Access'", rcs["-L bed (no -M)"][0] != 0 or rcs["-L bed (no -M)"][1] != str(truth_bed), f"{rcs['-L bed (no -M)']}; full scan control={rcs['full scan (control)']}")
# timing on the intact file
def timeit(cmd, n=3):
    ts = []
    for _ in range(n):
        t = time.time(); subprocess.run(cmd, shell=True, capture_output=True, executable="/bin/bash"); ts.append(time.time() - t)
    return min(ts)
t_L = timeit(f"samtools view -c -L {bed} {W}/big.bam"); t_M = timeit(f"samtools view -c -M -L {bed} {W}/big.bam")
n_L = out(f"samtools view -c -L {bed} {W}/big.bam")[1]; n_M = out(f"samtools view -c -M -L {bed} {W}/big.bam")[1]
info(f"intact 1.2M-read BAM: -L {t_L:.2f}s n={n_L}; -M -L {t_M:.2f}s n={n_M}; truth={truth_bed}")
check("intact BAM: -L and -M -L give the same count == truth", n_L == n_M == str(truth_bed), f"{n_L} {n_M} truth={truth_bed}")
check("-M -L is faster than -L on a 1.2 M-read BAM (index actually used)", t_M < t_L, f"{t_M:.2f}s vs {t_L:.2f}s")

# ================= F. threads claim ================================================
def index_time(th):
    ts = []
    for _ in range(3):
        if os.path.exists(f"{W}/big.bam.bai"): os.remove(f"{W}/big.bam.bai")
        t = time.time(); subprocess.run(f"samtools index -@ {th} {W}/big.bam", shell=True, capture_output=True, executable="/bin/bash"); ts.append(time.time() - t)
    return min(ts)
t1, t4, t8 = index_time(0), index_time(4), index_time(8)
info(f"index times on the 43 MB / 1.2 M-read BAM (nproc={os.cpu_count()}): -@0 {t1:.2f}s  -@4 {t4:.2f}s  -@8 {t8:.2f}s")
check("index -@ 4 is faster than single thread (SKILL: 'significantly speeds up')", t4 < t1, f"{t1:.2f} -> {t4:.2f}")
shutil.copy(f"{W}/big.bam.bai", f"{W}/thr8.bai"); os.remove(f"{W}/big.bam.bai"); out(f"samtools index {W}/big.bam")
check("-@ 8 BAI bytes identical to single-thread BAI", md5(f"{W}/thr8.bai") == md5(f"{W}/big.bam.bai"))

# ================= G. idxstats semantics ==========================================
out(f"samtools index {W}/sem.bam")
rc, o, e = out(f"samtools idxstats {W}/sem.bam")
info("semantics.bam idxstats: " + o.replace("\n", " | "))
check("idxstats chrA: 7 mapped (2 pair + 1 R1 + 4 s1 incl. 1 secondary + 2 supplementary), 1 unmapped (orphan R2 placed on chrA); * row: 0 0 2", o == "chrA\t10000\t7\t1\n*\t0\t0\t2", o)
unm = int(out(f"samtools view -c -f 4 -F 2304 {W}/sem.bam")[1])
check("SKILL unmapped cross-check: idxstats col4 sum (1+2) == view -c -f 4 -F 2304 (3)", unm == 3, unm)
prim_region = int(out(f"samtools view -c -F 2304 {W}/sem.bam chrA")[1])
prim_true = int(out(f"samtools view -c -F 2308 {W}/sem.bam")[1])
check("SKILL 'primary only' recipe `view -c -F 2304 file chr` counts primary MAPPED reads (4)?", prim_region == 4, f"-F 2304 chrA = {prim_region} (includes the placed unmapped orphan); -F 2308 = {prim_true}")
sec = int(out(f"samtools view -c -f 256 {W}/sem.bam")[1]); sup = int(out(f"samtools view -c -f 2048 {W}/sem.bam")[1])
check("hand count: 1 secondary + 2 supplementary records exist", sec == 1 and sup == 2, f"{sec} {sup}")
with pysam.AlignmentFile(f"{W}/sem.bam", "rb") as b:
    st = [(s.contig, s.mapped, s.unmapped) for s in b.get_index_statistics()]
    nc = b.count(until_eof=False) if False else None
check("pysam.get_index_statistics == idxstats (chrA 7 mapped 1 unmapped)", st == [("chrA", 7, 1)], st)

# real nanopore BAM: SKILL says idxstats 'overcounts' input reads on long-read data
out(f"samtools index {W}/nano.bam")
rc, o, e = out(f"samtools idxstats {W}/nano.bam")
row = [l.split("\t") for l in o.splitlines()][0]
nrec = int(out(f"samtools view -c {W}/nano.bam")[1]); nprim = int(out(f"samtools view -c -F 2308 {W}/nano.bam")[1]); nsup = int(out(f"samtools view -c -f 2048 {W}/nano.bam")[1]); nsec = int(out(f"samtools view -c -f 256 {W}/nano.bam")[1])
names = out(f"samtools view {W}/nano.bam | cut -f1 | sort -u | wc -l")[1]
info(f"ARTIC nanopore BAM: idxstats={row[:4]} records={nrec} primary_mapped={nprim} supplementary={nsup} secondary={nsec} distinct_qnames={names}")
check("real nanopore BAM: idxstats mapped == all non-unmapped records (primary+secondary+supp)", int(row[2]) == nrec - int(row[3]) and int(row[2]) == nprim + nsup + nsec, f"idxstats mapped={row[2]}, primary={nprim}, +sec={nsec}, +supp={nsup}")
dump("out/t5_results.json")
