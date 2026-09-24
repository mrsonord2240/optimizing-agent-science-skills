#!/usr/bin/env python3
"""Input 7 supplement (NEW): does the shipped bash ensure_index (which checks BAM *and* CRAM index names for every file) delete a SIBLING
file's index? Layout: sample.bam + sample.cram in one folder, each with an alternate-style name (sample.bai / sample.crai) or standard names.
Data: REAL human chr22 slice BAM + CRAM. Run in WSL from run/:  python scripts/n7b_sibling_index_probe.py"""
import os, sys, shutil, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(__file__))
from common import *

AFD = os.environ["AFDATA"]
W = os.path.abspath("work/n7b"); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
FUNC = block_containing("ensure_index() {", "bash").split("for f in *.bam")[0]
open(f"{W}/f.sh", "w").write(FUNC)
def ei(d, body):
    open(f"{W}/c.sh", "w").write(f"source {W}/f.sh\ncd '{d}'\n{body}\n"); return out(f"bash {W}/c.sh")
def fixture(name, alt):
    d = f"{W}/{name}"; os.makedirs(d)
    shutil.copy(f"{AFD}/human/test.paired_end.sorted.bam", f"{d}/sample.bam"); shutil.copy(f"{AFD}/human/test.paired_end.sorted.cram", f"{d}/sample.cram")
    if alt: out(f"samtools index {d}/sample.bam {d}/sample.bai"); out(f"samtools index {d}/sample.cram {d}/sample.crai")
    else:   out(f"samtools index {d}/sample.bam"); out(f"samtools index {d}/sample.cram")
    return d
# A. standard names: refresh the CRAM only (touch it newer) -> BAM index must survive
d = fixture("std", alt=False); time.sleep(1.1); os.utime(f"{d}/sample.cram", None); ei(d, "ensure_index sample.cram")
check("standard names (sample.bam.bai + sample.cram.crai): re-indexing a stale CRAM leaves the BAM's index alone", os.path.exists(f"{d}/sample.bam.bai") and os.path.exists(f"{d}/sample.cram.crai"), sorted(os.listdir(d)))
# B. alternate names: sample.bai belongs to the BAM, sample.crai to the CRAM
d = fixture("alt", alt=True); time.sleep(1.1); os.utime(f"{d}/sample.cram", None)
rc, o, e = ei(d, "ensure_index sample.cram")
info(f"alt names, stale CRAM: files after = {sorted(os.listdir(d))}")
check("alternate names (sample.bai for the BAM, sample.crai for the CRAM): refreshing the CRAM index does not delete sample.bai (the BAM's index)", os.path.exists(f"{d}/sample.bai"), sorted(os.listdir(d)))
d = fixture("alt2", alt=True); time.sleep(1.1); os.utime(f"{d}/sample.bam", None)
rc, o, e = ei(d, "ensure_index sample.bam")
info(f"alt names, stale BAM: files after = {sorted(os.listdir(d))}")
check("alternate names: refreshing the BAM index does not delete sample.crai (the CRAM's index)", os.path.exists(f"{d}/sample.crai"), sorted(os.listdir(d)))
dump("out/n7b_results.json")
