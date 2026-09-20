#!/usr/bin/env python3
"""SYNTHETIC test data for the bio-bam-statistics audit (all generated here, random seed 20260920).

Writes to run/data/:
  synth.bam/.bai/.fa/.truth.json   540-record PE BAM with every flag category, exact planted counts
  deep.bam/.bai/.fa                9500x stack + 500x stack on a 1 kb contig (depth-cap test)
  rf.bam/.bai, rf_noproper.bam     mate-pair (RF orientation) library, proper flag set / unset
  se.bam/.bai                      single-end BAM (55 records, 5 unmapped)
  empty.bam/.bai                   header only
  noindex.bam                      copy of se.bam without an index
Ground truth is written by construction (counters below), NOT by re-parsing flags.
"""
import json, os, random, shutil
import numpy as np
import pysam

random.seed(20260920)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)

def rseq(n):
    return "".join(random.choice("ACGT") for _ in range(n))

CONTIGS = {"synth1": 20000, "synth2": 5000, "chrM": 2000}
REF = {c: rseq(l) for c, l in CONTIGS.items()}
with open(f"{OUT}/synth.fa", "w") as fh:
    for c, s in REF.items():
        fh.write(f">{c}\n{s}\n")
pysam.faidx(f"{OUT}/synth.fa")

hdr = pysam.AlignmentHeader.from_dict({
    "HD": {"VN": "1.6", "SO": "coordinate"},
    "SQ": [{"SN": c, "LN": l} for c, l in CONTIGS.items()],
    "RG": [{"ID": "rg1", "SM": "synth"}],
})
TID = {c: i for i, c in enumerate(CONTIGS)}
RL = 100

def mk(hdr, name, flag, contig, pos0, cigar, mapq, seq, qual, mate_contig, mate_pos0, tlen, tags=()):
    a = pysam.AlignedSegment(hdr)
    a.query_name = name
    a.flag = flag
    a.reference_id = TID[contig] if contig else -1
    a.reference_start = pos0 if contig else -1
    a.mapping_quality = mapq
    a.cigarstring = cigar
    a.query_sequence = seq
    a.query_qualities = pysam.qualitystring_to_array(chr(33 + qual) * len(seq))
    a.next_reference_id = TID[mate_contig] if mate_contig else -1
    a.next_reference_start = mate_pos0 if mate_contig else -1
    a.template_length = tlen
    a.set_tag("NM", 0)
    a.set_tag("RG", "rg1")
    for t, v in tags:
        a.set_tag(t, v)
    return a

recs = []          # (sortkey_contig, pos0, AlignedSegment)
truth_cov = {c: np.zeros(l, dtype=int) for c, l in CONTIGS.items()}      # default samtools-depth style (overlaps double counted)
truth_cov_nooverlap = {c: np.zeros(l, dtype=int) for c, l in CONTIGS.items()}  # each template counts a base once
counts = {}

def add(a, cat):
    recs.append(a)
    counts[cat] = counts.get(cat, 0) + 1

def add_cov(contig, start0, length, counted, second_of_pair_overlap_skip=None):
    """Record which reference bases are covered by a read that samtools depth would count."""
    if counted:
        truth_cov[contig][start0:start0 + length] += 1

def pair(name, contig, p1, ins, flags, mapq, qual, cigar1=None, dup=False, qcfail=False, tag=""):
    """FR proper pair, read1 forward at p1, read2 reverse ending at p1+ins."""
    p2 = p1 + ins - RL
    fl1, fl2 = flags
    if dup:
        fl1 |= 1024; fl2 |= 1024
    if qcfail:
        fl1 |= 512; fl2 |= 512
    ref = REF[contig]
    s1 = ref[p1:p1 + RL]; s2 = ref[p2:p2 + RL]
    c1 = cigar1 or f"{RL}M"
    a1 = mk(hdr, name, fl1, contig, p1, c1, mapq, s1, qual, contig, p2, ins)
    a2 = mk(hdr, name, fl2, contig, p2, f"{RL}M", mapq, s2, qual, contig, p1, -ins)
    add(a1, "records"); add(a2, "records")
    counted = not (dup or qcfail)
    # aligned reference span of read1 (soft clip does not cover reference)
    m1 = int(c1.split("S")[-1].replace("M", "")) if "S" in c1 else RL
    # a soft-clipped read here is written as e.g. 20S80M: reference start stays p1, covers m1 bases
    if counted:
        truth_cov[contig][p1:p1 + m1] += 1
        truth_cov[contig][p2:p2 + RL] += 1
        cov = np.zeros(CONTIGS[contig], dtype=bool)
        cov[p1:p1 + m1] = True; cov[p2:p2 + RL] = True
        truth_cov_nooverlap[contig] += cov.astype(int)

# --- A: 200 proper pairs on synth1, insert 150 (50 bp overlap), first 20 pairs flagged duplicate; 20 soft-clipped read1
for i in range(200):
    p1 = random.randint(1000, 15000)
    orient = random.random() < 0.5
    flags = (99, 147) if orient else (163, 83)
    cig = "20S80M" if 20 <= i < 40 else None
    pair(f"A{i:03d}", "synth1", p1, 150, flags, 60, 30, cigar1=cig, dup=(i < 20))
counts_A = 400
# --- B: 20 pairs chrM insert 200 (no overlap)
for i in range(20):
    pair(f"B{i:03d}", "chrM", random.randint(100, 1500), 200, (99, 147), 60, 30)
# --- C: 10 proper pairs MAPQ 0 on synth2 with base quality 10 (< pysam pileup default min_base_quality=13)
for i in range(10):
    pair(f"C{i:03d}", "synth2", random.randint(100, 4000), 200, (99, 147), 0, 10)
# --- D: 10 QC-fail pairs on synth1
for i in range(10):
    pair(f"D{i:03d}", "synth1", random.randint(1000, 15000), 300, (99, 147), 60, 30, qcfail=True)
# --- E: 5 pairs fully unmapped (no coordinates)
for i in range(5):
    s = rseq(RL); s2 = rseq(RL)
    add(mk(hdr, f"E{i:03d}", 77, None, -1, None, 0, s, 30, None, -1, 0), "records")
    add(mk(hdr, f"E{i:03d}", 141, None, -1, None, 0, s2, 30, None, -1, 0), "records")
# --- F: 5 singletons: read1 mapped, mate unmapped but placed at the same coordinate
for i in range(5):
    p = random.randint(1000, 15000)
    a1 = mk(hdr, f"F{i:03d}", 73, "synth1", p, f"{RL}M", 60, REF["synth1"][p:p + RL], 30, "synth1", p, 0)
    a2 = mk(hdr, f"F{i:03d}", 133, "synth1", p, None, 0, rseq(RL), 30, "synth1", p, 0)
    add(a1, "records"); add(a2, "records")
    truth_cov["synth1"][p:p + RL] += 1
    truth_cov_nooverlap["synth1"][p:p + RL] += 1
# --- G: 10 pairs, mate on a different chromosome (both mapped, not proper)
for i in range(10):
    p = random.randint(1000, 15000); q = random.randint(100, 4000)
    add(mk(hdr, f"G{i:03d}", 97, "synth1", p, f"{RL}M", 60, REF["synth1"][p:p + RL], 30, "synth2", q, 0), "records")
    add(mk(hdr, f"G{i:03d}", 145, "synth2", q, f"{RL}M", 60, REF["synth2"][q:q + RL], 30, "synth1", p, 0), "records")
    truth_cov["synth1"][p:p + RL] += 1; truth_cov_nooverlap["synth1"][p:p + RL] += 1
    truth_cov["synth2"][q:q + RL] += 1; truth_cov_nooverlap["synth2"][q:q + RL] += 1
# --- H: 10 secondary alignments (1+64+256=321) of read1s onto synth2
for i in range(10):
    q = random.randint(100, 4000)
    add(mk(hdr, f"H{i:03d}", 321, "synth2", q, f"{RL}M", 0, REF["synth2"][q:q + RL], 30, None, -1, 0), "records")
# --- I: 10 supplementary alignments (1+64+2048=2113) 50M50S on synth2, MAPQ 30
for i in range(10):
    q = random.randint(100, 4000)
    add(mk(hdr, f"I{i:03d}", 2113, "synth2", q, "50M50S", 30, REF["synth2"][q:q + 50] + rseq(50), 30, None, -1, 0), "records")
    truth_cov["synth2"][q:q + 50] += 1; truth_cov_nooverlap["synth2"][q:q + 50] += 1

def sortkey(a):
    return (a.reference_id if a.reference_id >= 0 else 10**6, a.reference_start)
recs.sort(key=sortkey)
path = f"{OUT}/synth.bam"
with pysam.AlignmentFile(path, "wb", header=hdr) as bam:
    for a in recs:
        bam.write(a)
pysam.index(path)

truth = {
    "note": "SYNTHETIC. counts by construction",
    "total_records": 540,
    "primary": 520, "secondary": 10, "supplementary": 10,
    "unmapped_reads": 15,           # E 10 + F mates 5
    "mapped_flag_not4": 525,        # flagstat 'mapped'
    "primary_mapped": 505,
    "duplicates": 40,
    "qc_fail": 20,
    "paired_in_sequencing_primary": 520,
    "properly_paired": 400 + 40 + 20 + 20,   # A + B + C + D flagged proper  (=480)
    "singletons": 5,
    "mate_diff_chr": 20,            # G both mates
    "mito_mapped_reads_idxstats": 40,
    "per_contig_mapped_idxstats": None,
    "soft_clipped_reads": 20,
    "primary_reads_input_read_count": 520,
    "depth_default": {c: int(v.sum()) for c, v in truth_cov.items()},
    "depth_default_covered_bases": {c: int((v > 0).sum()) for c, v in truth_cov.items()},
    "depth_nooverlap": {c: int(v.sum()) for c, v in truth_cov_nooverlap.items()},
    "depth_nooverlap_covered_bases": {c: int((v > 0).sum()) for c, v in truth_cov_nooverlap.items()},
}
np.save(f"{OUT}/truth_depth_default_synth1.npy", truth_cov["synth1"])
np.save(f"{OUT}/truth_depth_nooverlap_synth1.npy", truth_cov_nooverlap["synth1"])
np.save(f"{OUT}/truth_depth_default_synth2.npy", truth_cov["synth2"])
np.save(f"{OUT}/truth_depth_default_chrM.npy", truth_cov["chrM"])
json.dump(truth, open(f"{OUT}/synth.truth.json", "w"), indent=1)

# ---------------- deep.bam
dh = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "amp", "LN": 1000}]})
dref = rseq(1000)
with open(f"{OUT}/deep.fa", "w") as fh:
    fh.write(f">amp\n{dref}\n")
pysam.faidx(f"{OUT}/deep.fa")
def dmk(name, pos):
    a = pysam.AlignedSegment(dh)
    a.query_name = name; a.flag = 0; a.reference_id = 0; a.reference_start = pos
    a.mapping_quality = 60; a.cigarstring = "100M"; a.query_sequence = dref[pos:pos + 100]
    a.query_qualities = pysam.qualitystring_to_array("I" * 100)
    a.set_tag("NM", 0)
    return a
with pysam.AlignmentFile(f"{OUT}/deep.bam", "wb", header=dh) as bam:
    for i in range(9500):
        bam.write(dmk(f"d{i}", 100))
    for i in range(500):
        bam.write(dmk(f"e{i}", 300))
pysam.index(f"{OUT}/deep.bam")

# ---------------- rf.bam: mate-pair library, RF orientation, 100 pairs, insert 2000
rh = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "big", "LN": 20000}]})
rref = rseq(20000)
def rf_write(path, proper):
    rows = []
    for i in range(100):
        p = 500 + i * 150
        ins = 2000
        right = p + ins - 100
        f_left = 1 + 16 + 64 + (2 if proper else 0)          # reverse read at left
        f_right = 1 + 32 + 128 + (2 if proper else 0)        # forward read at right
        a = pysam.AlignedSegment(rh); a.query_name = f"m{i}"; a.flag = f_left; a.reference_id = 0
        a.reference_start = p; a.mapping_quality = 60; a.cigarstring = "100M"
        a.query_sequence = rref[p:p + 100]; a.query_qualities = pysam.qualitystring_to_array("I" * 100)
        a.next_reference_id = 0; a.next_reference_start = right; a.template_length = ins
        b = pysam.AlignedSegment(rh); b.query_name = f"m{i}"; b.flag = f_right; b.reference_id = 0
        b.reference_start = right; b.mapping_quality = 60; b.cigarstring = "100M"
        b.query_sequence = rref[right:right + 100]; b.query_qualities = pysam.qualitystring_to_array("I" * 100)
        b.next_reference_id = 0; b.next_reference_start = p; b.template_length = -ins
        rows += [a, b]
    rows.sort(key=lambda x: x.reference_start)
    with pysam.AlignmentFile(path, "wb", header=rh) as bam:
        for r in rows:
            bam.write(r)
    pysam.index(path)
rf_write(f"{OUT}/rf.bam", True)
rf_write(f"{OUT}/rf_noproper.bam", False)

# ---------------- se.bam: 50 mapped SE + 5 unmapped
sh = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "amp", "LN": 1000}]})
rows = []
for i in range(50):
    p = 10 * i
    a = pysam.AlignedSegment(sh); a.query_name = f"s{i}"; a.flag = 0; a.reference_id = 0; a.reference_start = p
    a.mapping_quality = 60; a.cigarstring = "100M"; a.query_sequence = dref[p:p + 100]
    a.query_qualities = pysam.qualitystring_to_array("I" * 100); a.set_tag("NM", 0)
    rows.append(a)
for i in range(5):
    a = pysam.AlignedSegment(sh); a.query_name = f"u{i}"; a.flag = 4; a.reference_id = -1; a.reference_start = -1
    a.mapping_quality = 0; a.query_sequence = rseq(100); a.query_qualities = pysam.qualitystring_to_array("I" * 100)
    rows.append(a)
with pysam.AlignmentFile(f"{OUT}/se.bam", "wb", header=sh) as bam:
    for r in rows:
        bam.write(r)
pysam.index(f"{OUT}/se.bam")
shutil.copy(f"{OUT}/se.bam", f"{OUT}/noindex.bam")

# ---------------- empty.bam
with pysam.AlignmentFile(f"{OUT}/empty.bam", "wb", header=sh):
    pass
pysam.index(f"{OUT}/empty.bam")
print(json.dumps(truth, indent=1))
print("records written:", len(recs))
