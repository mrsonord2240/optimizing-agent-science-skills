#!/usr/bin/env python3
"""Input 2 supplement: CRAM in a directory with NO sibling BAM; what does the SKILL's helper / example / pysam do?
Run in WSL from run/:  python scripts/t2b_cram_probe.py"""
import os, sys, shutil, time
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam
from pathlib import Path

AFD = os.environ["AFDATA"]
W = "work/t2b"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
shutil.copy(f"{AFD}/human/test.paired_end.sorted.cram", f"{W}/s.cram")
shutil.copy(f"{AFD}/human/genome.fasta", f"{W}/genome.fasta")
shutil.copytree("skill/examples", f"{W}/examples")
CR = f"{W}/s.cram"; FA = f"{W}/genome.fasta"

def is_indexed(bam_path):     # verbatim from SKILL.md
    bam_path = Path(bam_path)
    return (bam_path.with_suffix('.bam.bai').exists() or
            Path(str(bam_path) + '.bai').exists() or
            bam_path.with_suffix('.bam.csi').exists())

out(f"samtools index {CR}")
check(".crai exists next to s.cram", os.path.exists(CR + ".crai"))
check("SKILL is_indexed(s.cram) with a real .crai present (CRAM-only dir)", is_indexed(CR), f"returned {is_indexed(CR)}  <- helper only knows .bai/.csi")

# CLI record output without -T (count works, retrieval does not?)
rc, o, e = out(f"samtools view {CR} chr22:1952-1960 | wc -l")
info(f"samtools view (no -T, records out): rc={rc} lines={o} err={e[:200]!r}")
rc2, o2, e2 = out(f"samtools view -T {FA} {CR} chr22:1952-1960 | wc -l")
check("samtools view -T ref works and prints records", int(o2) > 0, f"lines={o2} err={e2[:100]!r}")
rc3, o3, e3 = out(f"REF_PATH={W}/rp samtools view {CR} chr22:1952-1960 | wc -l")

# shipped example on CRAM: does it re-index every call?
m0 = None
for i in range(2):
    rc, o, e = out(f"python {W}/examples/fetch_regions.py {CR} chr22:1952-1960")
    info(f"run {i}: rc={rc} stdout_has_Indexing={'Indexing' in o} tail={o.splitlines()[-1:] } err_tail={e[-120:]!r}")
check("fetch_regions.py on CRAM does not re-index on the second call", "Indexing" not in o, "prints 'Indexing ...' on every call because ensure_indexed only looks for .bam.bai")
# with reference supplied through env var htslib understands
rc, o, e = out(f"mkdir -p {W}/rp; REF_PATH={os.path.abspath(W)}/ python {W}/examples/fetch_regions.py {CR} chr22:1952-1960")
info(f"example with REF_PATH unset-by-design: rc={rc}")

# pysam.index on CRAM writes .crai; get_index_statistics on CRAM
with pysam.AlignmentFile(CR, "rb", reference_filename=FA) as c:
    st = [(s.contig, s.mapped, s.unmapped) for s in c.get_index_statistics()]
    n = c.count("chr22")
rc, o, e = out(f"samtools idxstats {CR}")
check("pysam get_index_statistics(CRAM) equals samtools idxstats(CRAM) (5642 mapped)", st[0][1] == 5642, f"pysam={st} samtools={o.splitlines()}")
info(f"pysam c.count('chr22')={n} (fetch works, stats do not)")
# same on BAM for contrast
shutil.copy(f"{AFD}/human/test.paired_end.sorted.bam", f"{W}/s.bam"); shutil.copy(f"{AFD}/human/test.paired_end.sorted.bam.bai", f"{W}/s.bam.bai")
with pysam.AlignmentFile(f"{W}/s.bam", "rb") as b:
    st2 = [(s.contig, s.mapped, s.unmapped) for s in b.get_index_statistics()]
check("pysam get_index_statistics(BAM) chr22 == 5642", st2[0][1] == 5642, st2)
# usage-guide percent snippet on CRAM
with pysam.AlignmentFile(CR, "rb", reference_filename=FA) as bam:
    stats = bam.get_index_statistics()
    total_mapped = sum(s.mapped for s in stats)
    info(f"usage-guide 'Index Statistics' snippet on CRAM: total_mapped={total_mapped} (silently 0)")
dump("out/t2b_results.json")
