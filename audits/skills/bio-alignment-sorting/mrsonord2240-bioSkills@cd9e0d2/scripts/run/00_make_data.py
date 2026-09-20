#!/usr/bin/env python
"""SYNTHETIC test data for the bio-alignment-sorting audit (all reads here are invented, except
shuffled_real.bam / shuffled_umi.bam which are record-shuffled copies of REAL nf-core BAMs).
Run in WSL: python 00_make_data.py
Outputs go to run/data/ .
"""
import os, random, sys
import pysam

RUN = "/mnt/openscience/audits/bio-alignment-sorting/run"
AFD = "/mnt/openscience/audit-envs/alignment-files/public-data"
D = f"{RUN}/data"
os.makedirs(D, exist_ok=True)
random.seed(20260920)

# ---------- 1. synthetic multi-contig BAM, unsorted, names with mixed digit widths -------------
hdr = {
    "HD": {"VN": "1.6", "SO": "unsorted"},
    "SQ": [{"SN": "chr1", "LN": 5000}, {"SN": "chr2", "LN": 5000}, {"SN": "chr10", "LN": 5000}],
    "RG": [{"ID": "rg1", "SM": "s1", "PL": "ILLUMINA", "PU": "lane1"}],
}
h = pysam.AlignmentHeader.from_dict(hdr)
L = 50
recs = []
def mk(name, flag, tid, pos, mtid, mpos, tlen, cb=None, rx=None):
    a = pysam.AlignedSegment(h)
    a.query_name = name
    a.flag = flag
    a.reference_id = tid
    a.reference_start = pos
    a.mapping_quality = 60 if tid >= 0 else 0
    a.cigarstring = f"{L}M" if tid >= 0 else None
    a.query_sequence = "".join(random.choice("ACGT") for _ in range(L))
    a.query_qualities = pysam.qualitystring_to_array("I" * L)
    a.next_reference_id = mtid
    a.next_reference_start = mpos
    a.template_length = tlen
    a.set_tag("RG", "rg1")
    if cb: a.set_tag("CB", cb)
    if rx: a.set_tag("RX", rx)
    return a

cbs = ["AAAC", "AAAG", "CCCT", "GGGA", "TTTA", "ACGT"]
n = 0
for i in list(range(1, 60)) + [99, 100, 101, 110, 200, 1000]:
    name = f"read{i}"
    tid = random.choice([0, 1, 2])
    p1 = random.randrange(0, 4000)
    p2 = p1 + random.randrange(60, 300)
    cb = random.choice(cbs)
    # a few pairs share position exactly (tie-break exposure)
    if i % 10 == 0:
        p1, p2 = 100, 200
    recs.append(mk(name, 99, tid, p1, tid, p2, p2 + L - p1, cb=cb, rx=cb))
    recs.append(mk(name, 147, tid, p2, tid, p1, -(p2 + L - p1), cb=cb, rx=cb))
# cross-contig pair
recs.append(mk("xcontig1", 65, 0, 4000, 2, 10, 0, cb="AAAC"))
recs.append(mk("xcontig1", 129, 2, 10, 0, 4000, 0, cb="AAAC"))
# unmapped pairs (flag 77/141)
for i in range(5):
    recs.append(mk(f"unm{i}", 77, -1, -1, -1, -1, 0))
    recs.append(mk(f"unm{i}", 141, -1, -1, -1, -1, 0))
# unmapped read whose mate is mapped (placed at mate's position)
recs.append(mk("half1", 73, 1, 1234, 1, 1234, 0))
u = mk("half1", 133, 1, 1234, 1, 1234, 0)
u.cigarstring = None; u.mapping_quality = 0
recs.append(u)
random.shuffle(recs)
with pysam.AlignmentFile(f"{D}/synth_multi.unsorted.bam", "wb", header=h) as o:
    for r in recs:
        o.write(r)
print("synth_multi.unsorted.bam", len(recs), "records")

# ---------- 2. two coordinate-sorted BAMs with COLLIDING RG ids but different content ----------
for tag, pu, sm, contig in (("A", "lane1", "sampleA", 0), ("B", "lane7", "sampleB", 0)):
    hh = pysam.AlignmentHeader.from_dict({
        "HD": {"VN": "1.6", "SO": "coordinate"},
        "SQ": [{"SN": "chr1", "LN": 5000}],
        "RG": [{"ID": "L1", "SM": sm, "PL": "ILLUMINA", "PU": pu}],
    })
    rs = []
    for i in range(20):
        a = pysam.AlignedSegment(hh)
        a.query_name = f"{tag}_{i}"; a.flag = 0; a.reference_id = 0
        a.reference_start = i * 100 + (7 if tag == "B" else 0)
        a.mapping_quality = 60; a.cigarstring = f"{L}M"
        a.query_sequence = "".join(random.choice("ACGT") for _ in range(L))
        a.query_qualities = pysam.qualitystring_to_array("I" * L)
        a.set_tag("RG", "L1")
        rs.append(a)
    rs.sort(key=lambda r: r.reference_start)
    with pysam.AlignmentFile(f"{D}/rgcollide_{tag}.bam", "wb", header=hh) as o:
        for r in rs: o.write(r)
    pysam.index(f"{D}/rgcollide_{tag}.bam")

# ---------- 3. real BAMs, record-shuffled -------------------------------------------------------
def shuffled(src, dst):
    with pysam.AlignmentFile(src, "rb") as i:
        hd = i.header.to_dict()
        rs = list(i)
    hd["HD"] = {"VN": "1.6", "SO": "unsorted"}
    random.shuffle(rs)
    with pysam.AlignmentFile(dst, "wb", header=pysam.AlignmentHeader.from_dict(hd)) as o:
        for r in rs:
            o.write(r)
    print(dst, len(rs), "records")
shuffled(f"{AFD}/human/test.paired_end.sorted.bam", f"{D}/shuffled_real.bam")
shuffled(f"{AFD}/1000g/HG00349.chr20_1400000-1500000.bam", f"{D}/shuffled_1000g.bam")
