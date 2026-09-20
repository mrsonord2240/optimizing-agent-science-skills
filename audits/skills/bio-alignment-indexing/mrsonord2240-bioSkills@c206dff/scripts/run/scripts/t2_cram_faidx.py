#!/usr/bin/env python3
"""Input 2 (variant A): index a CRAM (.crai), region-fetch from it, get idxstats, index + fetch from the reference FASTA.
Data: REAL nf-core human chr22 slice CRAM + its FASTA (public-data/human). Truth: same reads in the BAM, plain-python FASTA parse.
Run in WSL from run/:  python scripts/t2_cram_faidx.py
"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam
from pathlib import Path

AFD = os.environ["AFDATA"]
W = "work/t2"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
for f in ["test.paired_end.sorted.cram", "genome.fasta", "test.paired_end.sorted.bam"]:
    shutil.copy(f"{AFD}/human/{f}", f"{W}/{f}")
shutil.copytree("skill/examples", f"{W}/examples")
CR = f"{W}/test.paired_end.sorted.cram"; BM = f"{W}/test.paired_end.sorted.bam"; FA = f"{W}/genome.fasta"

# ---- index the CRAM (SKILL 'Index CRAM') --------------------------------------------------------
rc, o, e = out(f"samtools index {CR}")
check("samtools index x.cram -> x.cram.crai (no reference supplied)", rc == 0 and os.path.exists(CR + ".crai"), f"rc={rc} err={e[:150]!r}")
rc, o, e = out(f"samtools index -c {CR} {W}/x.csi")
check("samtools index -c on CRAM: what happens? (SKILL only documents .crai for CRAM)", True, f"rc={rc} err={e[:200]!r}")
rc, o, e = out(f"samtools index -c {CR}")
info(f"index -c on cram: rc={rc} err={e[:200]!r} files={sorted(x for x in os.listdir(W) if 'cram' in x)}")

# ---- region query without a reference ------------------------------------------------------------
rc, o, e = out(f"samtools view -c {CR} chr22:1952-4700")
check("region count on CRAM WITHOUT -T (SKILL gives no -T; real behaviour)", True, f"rc={rc} out={o!r} err={e[:250]!r}")
no_ref_ok = rc == 0
rc, o, e = out(f"samtools view -c -T {FA} {CR} chr22:1952-4700")
bam_n = int(out(f"samtools index {BM} && samtools view -c {BM} chr22:1952-4700")[1])
check("CRAM region count with -T == BAM region count (5642)", rc == 0 and int(o) == bam_n == 5642, f"cram={o} bam={bam_n} err={e[:120]!r}")
# sub-region equivalence with BAM (5 windows)
diffs = []
for s, t in [(1952, 2000), (2500, 2600), (3000, 3100), (4000, 4617), (1, 1951), (4618, 40001)]:
    a = int(out(f"samtools view -c -T {FA} {CR} chr22:{s}-{t}")[1]); b = int(out(f"samtools view -c {BM} chr22:{s}-{t}")[1])
    if a != b: diffs.append((s, t, a, b))
check("6 sub-regions: CRAM(.crai) counts == BAM(.bai) counts", not diffs, diffs)

# ---- idxstats on CRAM ------------------------------------------------------------------------------
rc, o, e = out(f"samtools idxstats {CR}")
check("samtools idxstats on CRAM gives chr22 row 5642 mapped", rc == 0 and "chr22\t40001\t5642\t0" in o, f"rc={rc} out={o!r} err={e[:120]!r}")

# ---- pysam on CRAM ---------------------------------------------------------------------------------
try:
    with pysam.AlignmentFile(CR, "rb") as c:
        n = c.count("chr22", 1951, 4700)
    check("pysam.AlignmentFile(cram,'rb').count without reference_filename", True, f"n={n}")
except Exception as ex:
    check("pysam.AlignmentFile(cram,'rb').count without reference_filename (SKILL pattern)", False, f"{type(ex).__name__}: {str(ex)[:200]}")
with pysam.AlignmentFile(CR, "rb", reference_filename=FA) as c:
    n = c.count("chr22", 1951, 4700)
    st = [(s.contig, s.mapped, s.unmapped) for s in c.get_index_statistics()]
check("pysam CRAM with reference_filename: count == 5642 and index stats chr22 5642", n == 5642 and st[0][:2] == ("chr22", 5642), f"n={n} stats={st}")

# ---- shipped example against CRAM -----------------------------------------------------------------
rc, o, e = out(f"python {W}/examples/fetch_regions.py {CR} chr22:1952-2000")
info(f"fetch_regions.py on CRAM: rc={rc} last stdout={o.splitlines()[-1:] } err={e[-300:]!r}")
check("shipped fetch_regions.py works on a .cram (SKILL: 'Index CRAM' section; example says 'BAM' only)", rc == 0 and "Total reads" in o, f"rc={rc}")
crai_before = os.path.getmtime(CR + ".crai")
def is_indexed(bam_path):     # verbatim from SKILL.md
    bam_path = Path(bam_path)
    return (bam_path.with_suffix('.bam.bai').exists() or
            Path(str(bam_path) + '.bai').exists() or
            bam_path.with_suffix('.bam.csi').exists())
check("SKILL is_indexed returns True for a CRAM that has a .crai", is_indexed(CR), f"returned {is_indexed(CR)}")

# ---- FASTA index --------------------------------------------------------------------------------------
rc, o, e = out(f"samtools faidx {FA}")
fai = open(FA + ".fai").read().split()
check("samtools faidx creates genome.fasta.fai with contig chr22 length 40001", rc == 0 and fai[0] == "chr22" and fai[1] == "40001", fai[:5])
# ground truth: plain-python FASTA parse
seq = "".join(l.strip() for l in open(FA) if not l.startswith(">")).upper()
check("plain FASTA parse length == 40001", len(seq) == 40001, len(seq))
rc, o, e = out(f"samtools faidx {FA} chr22:1000-2000")
fa_seq = "".join(l for l in o.splitlines() if not l.startswith(">")).upper()
check("samtools faidx chr22:1000-2000 == seq[999:2000] (1-based inclusive, 1001 bp)", fa_seq == seq[999:2000] and len(fa_seq) == 1001, len(fa_seq))
with pysam.FastaFile(FA) as ref:
    a = ref.fetch("chr22", 999, 2000).upper()      # usage-guide.md
    b = ref.fetch("chr22", 1000, 2000).upper()     # SKILL.md
    ln = ref.get_reference_length("chr22")
check("usage-guide FastaFile.fetch('chr22',999,2000) == faidx chr22:1000-2000", a == fa_seq, len(a))
check("SKILL.md FastaFile.fetch('chr22',1000,2000) is NOT the same interval as faidx chr22:1000-2000 (off-by-one, 1000 bp vs 1001)", b != fa_seq and len(b) == 1000, f"len={len(b)} equal={b == fa_seq}")
check("get_reference_length == 40001", ln == 40001, ln)
# FastaFile auto-creates the .fai
os.remove(FA + ".fai")
with pysam.FastaFile(FA) as ref:
    pass
check("pysam.FastaFile builds the missing .fai automatically ('Automatic with FastaFile')", os.path.exists(FA + ".fai"))
# faidx of an unknown contig
rc, o, e = out(f"samtools faidx {FA} chr1:1-10")
check("samtools faidx on unknown contig fails loudly", rc != 0, f"rc={rc} err={e[:150]!r} out={o!r}")
dump("out/t2_results.json")
