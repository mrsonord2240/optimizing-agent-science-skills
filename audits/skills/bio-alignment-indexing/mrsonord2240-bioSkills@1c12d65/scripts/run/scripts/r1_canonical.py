#!/usr/bin/env python3
"""Input 1 (canonical, REGRESSION on fixed Skill): index a real coordinate-sorted BAM (BAI and CSI), fetch regions, idxstats cross-check.
Data: REAL 1000 Genomes HG00349 chr20 slice (public-data/1000g) and REAL nf-core human chr22 slice.
Run in WSL from run/:  python scripts/r1_canonical.py
Every command is copied from the FIXED SKILL.md; ground truth = full scan without index (pysam until_eof) and bedtools.
"""
import os, sys, shutil, random, glob
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam
from pathlib import Path

AFD = os.environ["AFDATA"]
W = "work/t1"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
shutil.copy(f"{AFD}/1000g/HG00349.chr20_1400000-1500000.bam", f"{W}/hg.bam")   # NO .bai copied on purpose
shutil.copy(f"{AFD}/human/test.paired_end.sorted.bam", f"{W}/h22.bam")
shutil.copytree("skill/examples", f"{W}/examples")

# ---- 1. sort-order check from SKILL 'Index Requirements' ------------------------------------
rc, o, e = out(f"samtools view -H {W}/hg.bam | grep '^@HD'")
check("HD line shows SO:coordinate (SKILL 'Check sort order')", "SO:coordinate" in o, o)

# ---- 2. samtools index (BAI) -----------------------------------------------------------------
rc, o, e = out(f"samtools index {W}/hg.bam")
check("samtools index creates hg.bam.bai (non-empty)", os.path.getsize(f"{W}/hg.bam.bai") > 0 if os.path.exists(f"{W}/hg.bam.bai") else False, f"rc={rc} err={e!r}")
# BAI is deterministic and equals what pysam.index writes
shutil.copy(f"{W}/hg.bam.bai", f"{W}/hg.first.bai")
rc, o, e = out(f"samtools index {W}/hg.bam")
check("re-running samtools index is idempotent (identical bytes)", md5(f"{W}/hg.bam.bai") == md5(f"{W}/hg.first.bai"))

# ---- 3. pysam.index('input.bam') writes same BAI ------------------------------------------------
shutil.copy(f"{W}/hg.bam", f"{W}/hgp.bam")
pysam.index(f"{W}/hgp.bam")
check("pysam.index('x.bam') creates x.bam.bai", os.path.exists(f"{W}/hgp.bam.bai"))
check("pysam BAI bytes == samtools BAI bytes", md5(f"{W}/hgp.bam.bai") == md5(f"{W}/hg.bam.bai"))

# ---- 4. CSI via samtools index -c and pysam.index('-c', ...) -----------------------------------
shutil.copy(f"{W}/hg.bam", f"{W}/hgc.bam")
out(f"samtools index -c {W}/hgc.bam")
check("samtools index -c creates hgc.bam.csi", os.path.exists(f"{W}/hgc.bam.csi"), os.listdir(W))
check("-c does NOT create a .bai", not os.path.exists(f"{W}/hgc.bam.bai"))
shutil.copy(f"{W}/hg.bam", f"{W}/hgpc.bam")
pysam.index("-c", f"{W}/hgpc.bam")
check("pysam.index('-c', x) produces x.bam.csi", os.path.exists(f"{W}/hgpc.bam.csi"))
check("pysam CSI bytes == samtools CSI bytes", md5(f"{W}/hgpc.bam.csi") == md5(f"{W}/hgc.bam.csi"))

# ---- 5. threads and explicit output name -----------------------------------------------------
shutil.copy(f"{W}/hg.bam", f"{W}/hgt.bam")
rc, o, e = out(f"samtools index -@ 4 {W}/hgt.bam")
check("samtools index -@ 4 works and gives the same BAI", md5(f"{W}/hgt.bam.bai") == md5(f"{W}/hg.bam.bai"), f"rc={rc} {e!r}")
shutil.copy(f"{W}/hg.bam", f"{W}/hgo.bam")
rc, o, e = out(f"samtools index {W}/hgo.bam {W}/hgo_custom.bai")
check("samtools index in.bam output.bai writes output.bai", os.path.exists(f"{W}/hgo_custom.bai") and not os.path.exists(f"{W}/hgo.bam.bai"), f"rc={rc} {e!r}")
# fixed SKILL: custom-named index needs -X / index_filename= ; default lookup fails
rc, o, e = out(f"samtools view -c {W}/hgo.bam chr20:1400000-1410000")
check("region query on BAM whose index has a custom name fails by default (SKILL: 'Could not retrieve index file')", rc != 0 and "Could not retrieve index file" in e, f"rc={rc} err={e[:150]!r}")
rc, o, e = out(f"samtools view -c -X {W}/hgo.bam {W}/hgo_custom.bai chr20:1400000-1410000")
n_std = out(f"samtools view -c {W}/hg.bam chr20:1400000-1410000")[1]
check("SKILL 'samtools view -X input.bam output.bai region' works and == standard count", rc == 0 and o == n_std and int(o) > 0, f"-X n={o} std={n_std} rc={rc}")
with pysam.AlignmentFile(f"{W}/hgo.bam", "rb", index_filename=f"{W}/hgo_custom.bai") as b:
    pn = b.count("chr20", 1399999, 1410000)
check("SKILL pysam.AlignmentFile(..., index_filename='output.bai') count == standard", str(pn) == n_std, f"{pn} vs {n_std}")

# ---- 6. 'input.bai' alternative location ---------------------------------------------------------
shutil.copy(f"{W}/hg.bam", f"{W}/alt.bam"); shutil.copy(f"{W}/hg.bam.bai", f"{W}/alt.bai")
rc, o, e = out(f"samtools view -c {W}/alt.bam chr20:1400000-1410000")
check("samtools finds alt.bai for alt.bam (SKILL 'Index File Locations')", rc == 0 and int(o) > 0, f"rc={rc} n={o} err={e[:100]!r}")
shutil.copy(f"{W}/hg.bam", f"{W}/alt2.bam"); shutil.copy(f"{W}/hg.bam.bai", f"{W}/alt2.bam.bai")

# ---- 7. region queries vs. ground truth (50 random regions, 4 methods) ---------------------------
random.seed(7)
regions = []
for _ in range(50):
    s = random.randint(1400000, 1499000); w = random.choice([1, 50, 300, 2000, 20000])
    regions.append(("chr20", s, min(s + w, 1500000)))
regions += [("chr20", 1400000, 1500000), ("chr20", 1, 1399999), ("chr20", 1499990, 1500000)]

# ground truth WITHOUT index: full scan
recs = []
with pysam.AlignmentFile(f"{W}/hg.bam", "rb") as bam:
    for r in bam.fetch(until_eof=True):
        if r.reference_id < 0: continue
        st = r.reference_start
        en = r.reference_end if r.reference_end is not None else st + 1
        recs.append((bam.get_reference_name(r.reference_id), st, en, r.is_unmapped))

def truth(chrom, s1, e1):
    s0, e0 = s1 - 1, e1   # 1-based inclusive -> 0-based half-open
    return sum(1 for c, st, en, u in recs if c == chrom and st < e0 and en > s0)

bad = []
with pysam.AlignmentFile(f"{W}/hg.bam", "rb") as bai_bam, pysam.AlignmentFile(f"{W}/hgc.bam", "rb") as csi_bam:
    for chrom, s, e in regions:
        t = truth(chrom, s, e)
        cli = int(out(f"samtools view -c {W}/hg.bam {chrom}:{s}-{e}")[1])
        cli_csi = int(out(f"samtools view -c {W}/hgc.bam {chrom}:{s}-{e}")[1])
        fetch_n = sum(1 for _ in bai_bam.fetch(chrom, s - 1, e))
        cnt = bai_bam.count(chrom, s - 1, e)
        csi_n = csi_bam.count(chrom, s - 1, e)
        if not (t == cli == cli_csi == fetch_n == cnt == csi_n):
            bad.append((chrom, s, e, t, cli, cli_csi, fetch_n, cnt, csi_n))
check(f"{len(regions)} regions: full-scan truth == samtools view -c (BAI) == (CSI) == pysam fetch == pysam count == pysam CSI", not bad, f"mismatches={bad[:3]}")
info(f"whole-slice truth={truth('chr20',1400000,1500000)} records overlapping")

# second independent tool: bedtools (mapped only, full scan)
rc, o, e = out(f"bedtools bamtobed -i {W}/hg.bam | awk '$1==\"chr20\" && $2<1450000 && $3>1440000' | wc -l")
mapped_cli = int(out(f"samtools view -F 4 -c {W}/hg.bam chr20:1440001-1450000")[1])
check("bedtools full-scan count == samtools view -F 4 -c region (chr20:1440001-1450000)", int(o) == mapped_cli, f"bedtools={o} samtools={mapped_cli}")

# ---- 8. shipped example fetch_regions.py, run from a COPY ---------------------------------------
rc, o, e = out(f"python {W}/examples/fetch_regions.py {W}/hg.bam chr20:1440001-1440500")
tot = [l for l in o.splitlines() if l.startswith("Total reads")]
exp = int(out(f"samtools view -c {W}/hg.bam chr20:1440001-1440500")[1])
check("fetch_regions.py Total == samtools view -c", rc == 0 and tot and int(tot[0].split(":")[-1]) == exp, f"rc={rc} tot={tot} expected={exp} err={e[:100]!r}")
lines = [l.split("\t") for l in o.splitlines() if "\t" in l]
sam = [l.split("\t") for l in out(f"samtools view {W}/hg.bam chr20:1440001-1440500 | cut -f1,2,4")[1].splitlines()]
mine = sorted((a[0], int(a[1])) for a in lines)
ref = sorted((a[0], int(a[2])) for a in sam)
check("fetch_regions.py (qname, 1-based pos) list identical to samtools view -> cut -f1,4", mine == ref, f"{len(mine)} vs {len(ref)}")
strand_ok = sorted((a[0], a[2]) for a in lines) == sorted((a[0], '-' if int(a[1]) & 16 else '+') for a in sam)
check("fetch_regions.py strand column == flag 0x10", strand_ok)

# on a BAM without any index the example auto-indexes (BAI)
shutil.copy(f"{W}/hg.bam", f"{W}/noidx.bam")
rc, o, e = out(f"python {W}/examples/fetch_regions.py {W}/noidx.bam chr20:1440001-1440500")
rc, o2, e2 = out(f"python {W}/examples/fetch_regions.py {W}/noidx2.bam chr20:1440001-1440500") if False else (rc, o, e)
check("fetch_regions.py auto-indexes a BAM with no index and prints Indexing on stderr", rc == 0 and os.path.exists(f"{W}/noidx.bam.bai") and "Indexing" in e, f"rc={rc} bai={os.path.exists(f'{W}/noidx.bam.bai')}")

# ---- 9. SKILL helper ensure_indexed (extracted verbatim from shipped SKILL.md) ---------------------------------
ns = {}
exec(block_containing("def ensure_indexed"), ns)
ei = ns["ensure_indexed"]
def mt(p): return os.path.getmtime(p)
d9 = f"{W}/e9"; os.makedirs(d9)
for nm in ("a", "b", "c"): shutil.copy(f"{W}/hg.bam", f"{d9}/{nm}.bam")
shutil.copy(f"{W}/hg.bam.bai", f"{d9}/a.bam.bai"); before = mt(f"{d9}/a.bam.bai"); ei(f"{d9}/a.bam")
check("ensure_indexed leaves a fresh .bam.bai untouched (mtime unchanged)", mt(f"{d9}/a.bam.bai") == before)
ei(f"{d9}/b.bam")
check("ensure_indexed creates a BAI when none exists", os.path.exists(f"{d9}/b.bam.bai") and md5(f"{d9}/b.bam.bai") == md5(f"{W}/hg.bam.bai"))
shutil.copy(f"{W}/hgc.bam.csi", f"{d9}/c.bam.csi"); before = mt(f"{d9}/c.bam.csi"); ei(f"{d9}/c.bam")
check("ensure_indexed accepts a CSI-only BAM as indexed (no redundant .bai, CSI untouched)", not os.path.exists(f"{d9}/c.bam.bai") and mt(f"{d9}/c.bam.csi") == before, sorted(os.listdir(d9)))
shutil.copy(f"{W}/hg.bam", f"{d9}/alt.bam"); shutil.copy(f"{W}/hg.bam.bai", f"{d9}/alt.bai"); ei(f"{d9}/alt.bam")
check("ensure_indexed treats input.bai (alt location) as an index (does not rebuild)", not os.path.exists(f"{d9}/alt.bam.bai"), sorted(x for x in os.listdir(d9) if x.startswith("alt")))

# ---- 10. multiple regions in one samtools view; -c; pysam multi-region loop from SKILL ------------
rc, o, e = out(f"samtools view -c {W}/hg.bam chr20:1400000-1401000 chr20:1450000-1451000")
a = int(out(f"samtools view -c {W}/hg.bam chr20:1400000-1401000")[1]); b = int(out(f"samtools view -c {W}/hg.bam chr20:1450000-1451000")[1])
check("multi-region view count == sum of the two regions (regions do not overlap)", int(o) == a + b, f"{o} vs {a}+{b}")
# overlapping regions -> duplicates
rc, o, e = out(f"samtools view -c {W}/hg.bam chr20:1400000-1401000 chr20:1400500-1401500")
u = int(out(f"samtools view -c {W}/hg.bam chr20:1400000-1401500")[1])
info(f"overlapping regions without -M: {o} records vs union {u} (duplicates expected: {int(o)-u})")

# ---- 11. idxstats / get_index_statistics / unmapped cross-check ------------------------------------
rc, o, e = out(f"samtools idxstats {W}/hg.bam")
rows = [l.split("\t") for l in o.splitlines()]
c20 = [r for r in rows if r[0] == "chr20"][0]
info(f"idxstats rows={len(rows)} chr20 row={c20}; star={rows[-1]}")
with pysam.AlignmentFile(f"{W}/hg.bam", "rb") as bam:
    st = {s.contig: (s.mapped, s.unmapped) for s in bam.get_index_statistics()}
    total_records = sum(1 for _ in bam.fetch(until_eof=True))
check("pysam get_index_statistics == samtools idxstats for chr20", st["chr20"] == (int(c20[2]), int(c20[3])), f"{st['chr20']} vs {c20[2:]}")
sum3 = sum(int(r[2]) for r in rows); sum4 = sum(int(r[3]) for r in rows)
check("idxstats total (mapped+unmapped) == number of records in a full scan", sum3 + sum4 == total_records, f"{sum3}+{sum4} vs {total_records}")
sk = int(out(f"samtools view -c -f 4 -F 2304 {W}/hg.bam")[1])
check("SKILL cross-check: idxstats unmapped sum == samtools view -c -f 4 -F 2304", sum4 == sk, f"idxstats={sum4} view={sk}")
prim_mapped = int(out(f"samtools view -c -F 2308 {W}/hg.bam")[1])
allmap = int(out(f"samtools view -c -F 4 {W}/hg.bam")[1])
check("idxstats mapped sum == records with -F 4 (includes secondary/supplementary, per SKILL caveat)", sum3 == allmap, f"{sum3} vs {allmap}; primary-only mapped={prim_mapped}")
tot = out(f"samtools idxstats {W}/hg.bam | awk '{{sum += $3}} END {{print sum}}'")[1]
check("SKILL 'Sum Total Mapped Reads' awk == sum of column 3", int(tot) == sum3, tot)

# ---- 12. human chr22 slice: same pipeline -----------------------------------------------------------
out(f"samtools index {W}/h22.bam")
n_all = int(out(f"samtools view -c {W}/h22.bam chr22:1952-4700")[1])
with pysam.AlignmentFile(f"{W}/h22.bam", "rb") as b:
    n_scan = sum(1 for r in b.fetch(until_eof=True) if r.reference_id >= 0)   # scan first: until_eof continues from the current file position
with pysam.AlignmentFile(f"{W}/h22.bam", "rb") as b:
    n_py = b.count("chr22", 1951, 4700)
rc, o, e = out(f"samtools idxstats {W}/h22.bam")
info("human idxstats:\n" + o)
check("human chr22 slice: view -c region (5642) == pysam.count == full scan of placed reads", n_all == n_py == n_scan == 5642, f"view={n_all} count={n_py} scan={n_scan}")
u_view = int(out(f"samtools view -c -f 4 -F 2304 {W}/h22.bam")[1])
u_idx = sum(int(l.split('\t')[3]) for l in o.splitlines())
check("human slice: SKILL unmapped cross-check equal", u_view == u_idx, f"view={u_view} idxstats={u_idx}")


# ================= 13. Skill pysam / awk snippets on real human BAM (was t1b) ================
W = "work/t1b"; shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
shutil.copy(f"{AFD}/human/test.paired_end.sorted.bam", f"{W}/input.bam"); shutil.copy(f"{AFD}/human/test.paired_end.sorted.bam.bai", f"{W}/input.bam.bai")
BAM = f"{W}/input.bam"

# --- SKILL 'Fetch Multiple Regions' verbatim (chrom renamed to the real contig) ------------------------------------
regions = [('chr22', 1952, 2100), ('chr22', 3000, 3100), ('chr22', 30000, 31000)]
got = {}
with pysam.AlignmentFile(BAM, 'rb') as bam:
    for chrom, start, end in regions:
        count = sum(1 for _ in bam.fetch(chrom, start, end))
        got[(chrom, start, end)] = count
        print(f'{chrom}:{start}-{end}: {count} reads')
exp = {r: int(out(f"samtools view -c {BAM} {r[0]}:{r[1]+1}-{r[2]}")[1]) for r in regions}
check("SKILL 'Fetch Multiple Regions' (0-based half-open) == samtools view -c chr:start+1-end", got == exp, f"{got} vs {exp}")

# --- SKILL 'Get Reads Covering Position' verbatim vs samtools depth (independent) -------------------------------------
pos = 3000
names = []
with pysam.AlignmentFile(BAM, 'rb') as bam:
    for read in bam.fetch('chr22', pos, pos + 1):
        if read.reference_start <= pos < read.reference_end:
            names.append(read.query_name)
rc, o, e = out(f"samtools depth -a -J -q 0 -Q 0 -G 0 -r chr22:{pos+1}-{pos+1} {BAM}")
depth = int(o.split()[-1]) if rc == 0 and o else None
info(f"covering-position snippet: {len(names)} reads; samtools depth -J -G 0 at 1-based {pos+1}: {depth} ({o!r} {e[:80]!r})")
check("SKILL 'Get Reads Covering Position' count == samtools depth (all flags, incl. deletions) at that base", len(names) == depth, f"{len(names)} vs {depth}")

# --- SKILL 'pysam idxstats' snippet (shipped block, executed verbatim) -------------------------------------------------
import io, contextlib
blk = block_containing("get_index_statistics()", "python").replace("input.bam", BAM)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(blk, {"pysam": pysam})
check("SKILL pysam idxstats snippet prints 'chr22: 5642 mapped, 0 unmapped'", buf.getvalue().strip() == "chr22: 5642 mapped, 0 unmapped", buf.getvalue())

# --- SKILL 'Count Reads in Region' verbatim ------------------------------------------------------------------------------
with pysam.AlignmentFile(BAM, 'rb') as bam:
    count = bam.count('chr22', 1951, 4700)
check("SKILL 'Count Reads in Region' == 5642", count == 5642, count)

# --- SKILL 'Mitochondrial Fraction' awk (extracted from shipped SKILL.md) on chrM, MT, no-MT and empty BAMs --------------
awk_cmd = [l for l in block_containing("(chr)?(M|MT)", "bash").splitlines() if "awk" in l][0]
def mito(bam):
    return out(awk_cmd.replace("input.bam", bam))
hdr = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "1", "LN": 100000}, {"SN": "MT", "LN": 16569}]})
def rec(hdr, name, tid, pos):
    a = pysam.AlignedSegment(hdr); a.query_name = name; a.flag = 0; a.reference_id = tid; a.reference_start = pos
    a.mapping_quality = 60; a.cigarstring = "50M"; a.query_sequence = "A" * 50; a.query_qualities = pysam.qualitystring_to_array("I" * 50); return a
with pysam.AlignmentFile(f"{W}/mt_ens.bam", "wb", header=hdr) as f:      # SYNTHETIC: 100 reads on contig 1, 50 on MT
    for i in range(100): f.write(rec(hdr, f"a{i}", 0, i * 10))
    for i in range(50): f.write(rec(hdr, f"m{i}", 1, i * 10))
out(f"samtools index {W}/mt_ens.bam")
rc, o, e = mito(f"{W}/mt_ens.bam"); check("SKILL mito awk on 'MT' contig (true 33.33%)", o == "MT: 33.33%", f"{o!r} rc={rc}")
hdr2 = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "chr1", "LN": 100000}, {"SN": "chrM", "LN": 16569}]})
with pysam.AlignmentFile(f"{W}/mt_ucsc.bam", "wb", header=hdr2) as f:    # SYNTHETIC: 50 chr1, 50 chrM
    for i in range(50): f.write(rec(hdr2, f"a{i}", 0, i * 10))
    for i in range(50): f.write(rec(hdr2, f"m{i}", 1, i * 10))
out(f"samtools index {W}/mt_ucsc.bam")
rc, o, e = mito(f"{W}/mt_ucsc.bam"); check("SKILL mito awk on 'chrM' contig (true 50.00%)", o == "MT: 50.00%", f"{o!r}")
# a contig that merely starts with chrM-like text must not count (chrMx) and a BAM with no MT prints nothing (not 0.00%)
rc, o, e = mito(BAM); check("SKILL mito awk on a BAM with no MT/chrM contig prints 0.00% (true) without error", rc == 0 and e == "" and o in ("MT: 0.00%",), f"{o!r} err={e!r}")
out(f"samtools view -H {BAM} | samtools view -b -o {W}/empty.bam -"); out(f"samtools index {W}/empty.bam")
rc, o, e = mito(f"{W}/empty.bam"); check("SKILL mito awk on an empty BAM: no division-by-zero, no output", rc == 0 and o == "" and e == "", f"rc={rc} out={o!r} err={e!r}")
# total-mapped awk
rc, o, e = out(f"samtools idxstats {BAM} | awk '{{sum += $3}} END {{print sum}}'"); check("SKILL 'Sum Total Mapped Reads' on human slice == 5642", o == "5642", o)
dump("out/r1_results.json")
