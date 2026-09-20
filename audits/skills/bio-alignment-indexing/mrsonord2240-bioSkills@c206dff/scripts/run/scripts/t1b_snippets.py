#!/usr/bin/env python3
"""Input 1 supplement: SKILL/usage-guide pysam + awk snippets run verbatim on real human BAM, verified against independent tools.
Also: usage-guide 'mitochondrial fraction' awk on a SYNTHETIC BAM whose chrM contig is called MT.
Run in WSL from run/:  python scripts/t1b_snippets.py"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from common import *
import pysam

AFD = os.environ["AFDATA"]
W = "work/t1b"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
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

# --- usage-guide 'Index Statistics' pysam snippet verbatim --------------------------------------------------------------
with pysam.AlignmentFile(BAM, 'rb') as bam:
    stats = bam.get_index_statistics()
    total_mapped = sum(s.mapped for s in stats)
    lines = []
    for stat in stats:
        pct = stat.mapped / total_mapped * 100 if total_mapped > 0 else 0
        lines.append(f'{stat.contig}: {stat.mapped:,} ({pct:.1f}%)')
print("\n".join(lines))
check("usage-guide idxstats pysam snippet prints 'chr22: 5,642 (100.0%)'", lines == ["chr22: 5,642 (100.0%)"], lines)

# --- SKILL 'Count Reads in Region' verbatim ------------------------------------------------------------------------------
with pysam.AlignmentFile(BAM, 'rb') as bam:
    count = bam.count('chr22', 1951, 4700)
check("SKILL 'Count Reads in Region' == 5642", count == 5642, count)

# --- usage-guide mito awk on a BAM whose mitochondrial contig is 'MT' (Ensembl style; SKILL itself warns chrM vs MT) -----
hdr = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "1", "LN": 100000}, {"SN": "MT", "LN": 16569}]})
def rec(name, tid, pos):
    a = pysam.AlignedSegment(hdr); a.query_name = name; a.flag = 0; a.reference_id = tid; a.reference_start = pos
    a.mapping_quality = 60; a.cigarstring = "50M"; a.query_sequence = "A" * 50; a.query_qualities = pysam.qualitystring_to_array("I" * 50); return a
with pysam.AlignmentFile(f"{W}/mt_ens.bam", "wb", header=hdr) as f:      # SYNTHETIC: 100 reads on contig 1, 50 on MT
    for i in range(100): f.write(rec(f"a{i}", 0, i * 10))
    for i in range(50): f.write(rec(f"m{i}", 1, i * 10))
out(f"samtools index {W}/mt_ens.bam")
rc, o, e = out(f"samtools idxstats {W}/mt_ens.bam | awk '/^chrM/ {{mt=$3}} {{total+=$3}} END {{printf \"MT: %.2f%%\\n\", mt/total*100}}'")
check("usage-guide mito-fraction awk on an 'MT'-named contig (true value 33.33%) reports the truth", o == "MT: 33.33%", f"printed {o!r}  <- regex /^chrM/ silently misses 'MT'")
dump("out/t1b_results.json")
