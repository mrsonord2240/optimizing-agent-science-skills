#!/usr/bin/env python3
"""Input 7 (NEW, adversarial): the shipped ensure_index (bash) and ensure_indexed (Python) under mtime and layout edge cases:
equal mtimes, BAM only slightly newer, both .bai and .csi present (fresh/stale/mixed), alt-name x.bai / x.csi, .crai, file names with
spaces/parentheses, symlinked BAM, `set -euo pipefail`, extra options (-@ 4), truncated-but-fresh index, restored-old-mtime BAM,
empty directory, non-default CSI -m, a BAM that cannot be indexed (unsorted) after its stale index was deleted.
Data: REAL 1000G HG00349 chr20 slice (half-BAM = `samtools view -s` for a differing second content), REAL human chr22 slice + CRAM + FASTA,
REAL unsorted UMI BAM. Truth: count of region reads from a freshly built index of the same content, and a full scan.
Run in WSL from run/:  python scripts/n7_ensure_index_edges.py"""
import os, sys, shutil, time, gzip, struct
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam

AFD = os.environ["AFDATA"]
W = os.path.abspath("work/n7")
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
REG = "chr20:1440001-1460000"
shutil.copy(f"{AFD}/1000g/HG00349.chr20_1400000-1500000.bam", f"{W}/full.bam")
out(f"samtools view -b -s 3.5 -o {W}/half.bam {W}/full.bam")
def truth(bam):     # full-scan truth, independent of any index
    n = 0
    with pysam.AlignmentFile(bam, "rb") as b:
        for r in b.fetch(until_eof=True):
            if r.reference_id >= 0 and r.reference_name == "chr20" and r.reference_start < 1460000 and (r.reference_end or r.reference_start + 1) > 1440000: n += 1
    return n
T_FULL, T_HALF = truth(f"{W}/full.bam"), truth(f"{W}/half.bam")
check("fixture: full-scan truths differ (full != half) so a stale index is detectable", T_FULL != T_HALF, f"full={T_FULL} half={T_HALF}")
def cnt(bam):
    rc, o, e = out(f"samtools view -c '{bam}' {REG}"); return (int(o) if rc == 0 and o.isdigit() else f"rc={rc} {e[:80]}")

EI = block_containing("ensure_index() {", "bash")
FUNC = EI.split("for f in *.bam")[0]
open(f"{W}/ei_func.sh", "w").write(FUNC)
def ei(d, body, pre=""):
    open(f"{W}/call.sh", "w").write(f"{pre}\nsource {W}/ei_func.sh\ncd '{d}'\n{body}\n")
    return out(f"bash {W}/call.sh")
ns = {}; exec(block_containing("def ensure_indexed"), ns); ensure_indexed = ns["ensure_indexed"]
def mk(name, src="full.bam"):
    d = f"{W}/{name}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d); return d
def replace_content(d, fname, src):     # new content, mtime newer than any existing index
    time.sleep(1.1); shutil.copy(f"{W}/{src}", f"{d}/{fname}")

# --- 1. equal mtimes: fresh (not stale) ---------------------------------------------------------------------------------
d = mk("c1"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index {d}/x.bam")
t0 = int(time.time()) - 100   # whole seconds: this drvfs mount truncates sub-second utime, so use an integer second for both files
os.utime(f"{d}/x.bam", (t0, t0)); os.utime(f"{d}/x.bam.bai", (t0, t0))
info(f"mtimes ns: bam={os.stat(f'{d}/x.bam').st_mtime_ns} bai={os.stat(f'{d}/x.bam.bai').st_mtime_ns}")
m0 = os.path.getmtime(f"{d}/x.bam.bai"); ei(d, "ensure_index x.bam"); ensure_indexed(f"{d}/x.bam")
check("equal mtimes (index == BAM): both helpers treat it as fresh (no rebuild)", os.path.getmtime(f"{d}/x.bam.bai") == m0, "")

# --- 2. BAM 2 s newer than the index -> stale, both helpers rebuild ----------------------------------------------------------
for who in ("bash", "python"):
    d = mk(f"c2{who}"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index {d}/x.bam")
    replace_content(d, "x.bam", "half.bam")
    (ei(d, "ensure_index x.bam") if who == "bash" else ensure_indexed(f"{d}/x.bam"))
    check(f"BAM replaced (newer than BAI): {who} helper rebuilds; count == half truth", cnt(f"{d}/x.bam") == T_HALF, f"{cnt(f'{d}/x.bam')} vs {T_HALF}")

# --- 3. both .bai and .csi present ------------------------------------------------------------------------------------------
for who in ("bash", "python"):
    call = (lambda d: ei(d, "ensure_index x.bam")) if who == "bash" else (lambda d: ensure_indexed(f"{d}/x.bam"))
    # 3a both fresh -> untouched
    d = mk(f"c3a{who}"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index {d}/x.bam"); out(f"samtools index -c {d}/x.bam")
    ms = (os.path.getmtime(f"{d}/x.bam.bai"), os.path.getmtime(f"{d}/x.bam.csi")); call(d)
    check(f"[{who}] .bai + .csi both fresh: left untouched", ms == (os.path.getmtime(f"{d}/x.bam.bai"), os.path.getmtime(f"{d}/x.bam.csi")) and cnt(f"{d}/x.bam") == T_FULL)
    # 3b both stale -> replaced by a single CSI (keeps CSI), count correct
    replace_content(d, "x.bam", "half.bam"); call(d)
    check(f"[{who}] .bai + .csi both stale: rebuilt; count == truth; files", cnt(f"{d}/x.bam") == T_HALF, f"{sorted(os.listdir(d))}")
    info(f"[{who}] after 3b files: {sorted(os.listdir(d))}")
    # 3c stale .bai + fresh .csi
    d = mk(f"c3c{who}"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index {d}/x.bam"); time.sleep(1.1)
    shutil.copy(f"{W}/half.bam", f"{d}/x.bam"); out(f"samtools index -c {d}/x.bam")     # x.bam replaced; .csi fresh, .bai stale
    call(d)
    check(f"[{who}] stale .bai beside fresh .csi: count == truth after helper; no error", cnt(f"{d}/x.bam") == T_HALF, f"{cnt(f'{d}/x.bam')} {sorted(os.listdir(d))}")

# --- 4. alt names x.bai / x.csi --------------------------------------------------------------------------------------------------
d = mk("c4"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index {d}/x.bam {d}/x.bai"); m0 = os.path.getmtime(f"{d}/x.bai")
ei(d, "ensure_index x.bam"); ensure_indexed(f"{d}/x.bam")
check("alt name x.bai fresh: not rebuilt, no x.bam.bai created; count == truth", os.path.getmtime(f"{d}/x.bai") == m0 and not os.path.exists(f"{d}/x.bam.bai") and cnt(f"{d}/x.bam") == T_FULL, sorted(os.listdir(d)))
replace_content(d, "x.bam", "half.bam"); ei(d, "ensure_index x.bam")
check("alt name x.bai STALE: ensure_index deletes it and rebuilds; count == truth", cnt(f"{d}/x.bam") == T_HALF and not os.path.exists(f"{d}/x.bai"), sorted(os.listdir(d)))

# --- 5. .crai / x.crai ---------------------------------------------------------------------------------------------------------------
d = mk("c5"); cr = f"{d}/s.cram"; shutil.copy(f"{AFD}/human/test.paired_end.sorted.cram", cr); out(f"samtools index {cr} {d}/s.crai")
m0 = os.path.getmtime(f"{d}/s.crai"); ei(d, "ensure_index s.cram"); ensure_indexed(cr)
check("CRAM with alt-name s.crai fresh: neither helper rebuilds or adds s.cram.crai", os.path.getmtime(f"{d}/s.crai") == m0 and not os.path.exists(cr + ".crai"), sorted(os.listdir(d)))
time.sleep(1.1); shutil.copy(f"{AFD}/human/test.paired_end.sorted.cram", cr); ei(d, "ensure_index s.cram")
rc, o, e = out(f"samtools view -c {cr} chr22:1952-4700")
check("CRAM with stale s.crai: bash ensure_index rebuilds (s.cram.crai present, s.crai gone) and count 5642", os.path.exists(cr + ".crai") and not os.path.exists(f"{d}/s.crai") and o == "5642", f"{sorted(os.listdir(d))} n={o}")

# --- 6. awkward file names ------------------------------------------------------------------------------------------------------------
d = mk("c6"); nm = "my sample (1) [x].bam"; shutil.copy(f"{W}/full.bam", f"{d}/{nm}")
rc, o, e = ei(d, f"ensure_index '{nm}'")
check("file name with spaces/parentheses/brackets: bash ensure_index builds the BAI", os.path.exists(f"{d}/{nm}.bai"), f"rc={rc} err={e[:100]!r} {sorted(os.listdir(d))}")
d2 = mk("c6b"); shutil.copy(f"{W}/full.bam", f"{d2}/{nm}"); ensure_indexed(f"{d2}/{nm}")
check("file name with spaces/parentheses/brackets: python ensure_indexed builds the BAI", os.path.exists(f"{d2}/{nm}.bai"))
rc, o, e = ei(d, "for f in *.bam; do ensure_index \"$f\"; done; ls")
check("batch loop over a spaced name is a no-op when fresh and does not split the name", "my sample (1) [x].bam.bai" in o and rc == 0, f"rc={rc} out={o!r} err={e[:100]!r}")

# --- 7. symlinked BAM ------------------------------------------------------------------------------------------------------------------------
d = mk("c7"); os.makedirs(f"{d}/store"); shutil.copy(f"{W}/full.bam", f"{d}/store/x.bam"); os.symlink(f"{d}/store/x.bam", f"{d}/x.bam")
ei(d, "ensure_index x.bam"); ensure_indexed(f"{d}/x.bam")
check("symlinked BAM: index created beside the link, count == truth", os.path.exists(f"{d}/x.bam.bai") and cnt(f"{d}/x.bam") == T_FULL, sorted(os.listdir(d)))

# --- 8. set -euo pipefail (agents often add it) ---------------------------------------------------------------------------------------------------
d = mk("c8"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index {d}/x.bam"); shutil.copy(f"{W}/full.bam", f"{d}/y.bam")
rc, o, e = ei(d, "for f in *.bam; do ensure_index \"$f\"; done; echo DONE; ls", pre="set -euo pipefail")
check("under `set -euo pipefail`: batch loop (fresh + missing) completes (prints DONE) and indexes y.bam", "DONE" in o and os.path.exists(f"{d}/y.bam.bai"), f"rc={rc} out={o!r} err={e[:150]!r}")
d = mk("c8b"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index {d}/x.bam")
rc, o, e = ei(d, "ensure_index x.bam; echo DONE", pre="set -euo pipefail")
check("under `set -euo pipefail`: fresh-index no-op returns success (prints DONE)", "DONE" in o and rc == 0, f"rc={rc} out={o!r}")
d = mk("c8c"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam")
rc, o, e = ei(d, "ensure_index x.bam; echo DONE", pre="set -euo pipefail")
check("under `set -euo pipefail` and `set -u`: no-index case builds and prints DONE (no unbound variable)", "DONE" in o and os.path.exists(f"{d}/x.bam.bai"), f"rc={rc} out={o!r} err={e[:150]!r}")

# --- 9. extra options -------------------------------------------------------------------------------------------------------------------------------------
d = mk("c9"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); rc, o, e = ei(d, "ensure_index x.bam -@ 4")
check("documented extra options: `ensure_index x.bam -@ 4` works", rc == 0 and os.path.exists(f"{d}/x.bam.bai"), f"rc={rc} err={e[:120]!r}")
# the doc comment says 'file.bam [extra samtools-index options]': options BEFORE the file?
d = mk("c9b"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); rc, o, e = ei(d, "ensure_index x.bam -c")
check("`ensure_index x.bam -c` (force CSI on first build) creates x.bam.csi", os.path.exists(f"{d}/x.bam.csi"), f"rc={rc} {sorted(os.listdir(d))} err={e[:100]!r}")

# --- 10. limitations: truncated-but-fresh index, restored old mtime -------------------------------------------------------------------------------------------
d = mk("c10"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index {d}/x.bam")
sz = os.path.getsize(f"{d}/x.bam.bai")
with open(f"{d}/x.bam.bai", "r+b") as fh: fh.truncate(sz // 3)
os.utime(f"{d}/x.bam.bai", None); ei(d, "ensure_index x.bam")
info(f"truncated fresh .bai ({sz}->{sz//3} bytes) after ensure_index: count={cnt(f'{d}/x.bam')} (truth {T_FULL})")
trunc_ok = cnt(f"{d}/x.bam") == T_FULL
check("LIMITATION probe: a truncated but fresh .bai is NOT detected by ensure_index (mtime only)", not trunc_ok, f"count={cnt(f'{d}/x.bam')} truth={T_FULL}")
d = mk("c10b"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index {d}/x.bam"); time.sleep(1.1)
shutil.copy(f"{W}/half.bam", f"{d}/x.bam"); os.utime(f"{d}/x.bam", (time.time() - 3600, time.time() - 3600))       # cp -p / rsync -t / backup restore: old mtime
ei(d, "ensure_index x.bam")
info(f"replaced BAM with OLD mtime: count={cnt(f'{d}/x.bam')} (truth {T_HALF})")
check("LIMITATION probe: replaced BAM carrying an OLDER mtime than its index is not detected (mtime heuristic, same as htslib)", cnt(f"{d}/x.bam") != T_HALF, f"count={cnt(f'{d}/x.bam')} truth={T_HALF}")

# --- 11. custom CSI -m is preserved --------------------------------------------------------------------------------------------------------------------------------
d = mk("c11"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index -c -m 12 {d}/x.bam")
def ms_of(p):
    b = gzip.open(p).read(); return struct.unpack("<ii", b[4:12])
before = ms_of(f"{d}/x.bam.csi"); replace_content(d, "x.bam", "half.bam"); ei(d, "ensure_index x.bam"); after = ms_of(f"{d}/x.bam.csi")
info(f"CSI (min_shift, depth) before {before}, after stale-rebuild {after}")
check("stale CSI built with -m 12 is rebuilt as CSI with min_shift 12 preserved and still answers correctly", cnt(f"{d}/x.bam") == T_HALF and after[0] == 12, f"before={before} after={after}")

# --- 12. empty dir / nonexistent / unsorted after stale --------------------------------------------------------------------------------------------------
d = mk("c12"); rc, o, e = ei(d, "for f in *.bam; do ensure_index \"$f\"; done")
info(f"batch loop in a directory with no BAMs: rc={rc} err={e[:160]!r}")
check("batch loop in a directory without *.bam is a successful no-op with nullglob", rc == 0 and not e, f"rc={rc} err={e[:160]!r}")
d = mk("c12b"); shutil.copy(f"{W}/full.bam", f"{d}/x.bam"); out(f"samtools index {d}/x.bam"); time.sleep(1.1)
shutil.copy(f"{AFD}/human/test.paired_end.umi_unsorted.bam", f"{d}/x.bam"); rc, o, e = ei(d, "ensure_index x.bam")
info(f"stale BAM replaced by an UNSORTED BAM: rc={rc}; files after: {sorted(os.listdir(d))}; err={e[:200]!r}")
check("stale index + unsorted replacement: helper fails loudly (rc!=0, 'failed to create index') and leaves no index (old one removed, none wrong)", rc != 0 and "failed to create index" in e and not any(f.endswith((".bai", ".csi")) for f in os.listdir(d)), f"rc={rc} files={sorted(os.listdir(d))}")
try:
    d = mk("c12c"); shutil.copy(f"{AFD}/human/test.paired_end.umi_unsorted.bam", f"{d}/x.bam"); ensure_indexed(f"{d}/x.bam")
    check("python ensure_indexed on an unsorted BAM raises", False, "no exception")
except Exception as ex:
    check("python ensure_indexed on an unsorted BAM raises a clear exception", "index" in str(ex).lower(), f"{type(ex).__name__}: {str(ex)[:150]}")

dump("out/n7_results.json")
