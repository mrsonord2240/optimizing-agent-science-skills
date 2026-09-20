"""Build PLANTED-DEFECT BAMs (SYNTHETIC derivatives of real reads) for testing validators.

Base = public-data/human/test.paired_end.sorted.bam (real Illumina reads, chr22 slice, 5644 records).
Every output is labelled synthetic; ground truth is written to data/fixtures.json.
Run in WSL:  python make_fixtures.py <public-data-dir> <out-dir>
"""
import json
import os
import random
import struct
import sys

import pysam

PD, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
SRC = os.path.join(PD, "human", "test.paired_end.sorted.bam")
random.seed(42)

truth = {}


def reg(name, defect, expected_bad=True, note=""):
    truth[name] = {"defect": defect, "expected_bad": expected_bad, "note": note, "synthetic": True}


def load():
    with pysam.AlignmentFile(SRC, "rb") as b:
        hdr = b.header.to_dict()
        recs = [r for r in b.fetch(until_eof=True)]
    return hdr, recs


def write(name, hdr, recs, index=False):
    p = os.path.join(OUT, name)
    with pysam.AlignmentFile(p, "wb", header=hdr) as o:
        for r in recs:
            o.write(r)
    if index:
        pysam.index(p)
    return p


hdr, recs = load()
mapped_pairs = [r for r in recs if r.is_paired and r.is_proper_pair and not r.is_secondary]

# 0. control: identical copy, re-written by pysam (valid)
write("ctl_valid.bam", hdr, recs, index=True)
reg("ctl_valid.bam", "none (control, pysam rewrite of real BAM)", expected_bad=False)

# ---- byte-level corruptions of the valid file -------------------------------
raw = open(os.path.join(OUT, "ctl_valid.bam"), "rb").read()
n = len(raw)
open(os.path.join(OUT, "trunc_tail.bam"), "wb").write(raw[: int(n * 0.6)])
reg("trunc_tail.bam", "file truncated at 60% (mid-block; EOF marker gone)")
open(os.path.join(OUT, "no_eof.bam"), "wb").write(raw[:-28])
reg("no_eof.bam", "28-byte BGZF EOF block removed, all data blocks intact")

# bit-flip inside a compressed block in the middle of the file
b = bytearray(raw)
for off in (n // 2, n // 2 + 7, n // 2 + 19):
    b[off] ^= 0xFF
open(os.path.join(OUT, "bitflip_mid.bam"), "wb").write(bytes(b))
reg("bitflip_mid.bam", "3 bytes flipped in the middle of the compressed stream (EOF marker intact)")


# drop one whole BGZF block from the middle (EOF marker intact)
def bgzf_blocks(buf):
    pos, out = 0, []
    while pos < len(buf):
        xlen = struct.unpack("<H", buf[pos + 10: pos + 12])[0]
        bsize = struct.unpack("<H", buf[pos + 16: pos + 18])[0] + 1
        out.append((pos, bsize))
        pos += bsize
    return out


blks = bgzf_blocks(raw)
mid = len(blks) // 2
s, l = blks[mid]
open(os.path.join(OUT, "drop_block_mid.bam"), "wb").write(raw[:s] + raw[s + l:])
reg("drop_block_mid.bam", f"one whole BGZF block (#{mid} of {len(blks)}) removed from the middle; EOF marker intact")

# ---- record-level defects (each in ONE file so attribution is exact) ---------
_HDR = pysam.AlignmentFile(SRC).header


def clone(rs):
    return [pysam.AlignedSegment.fromstring(r.to_string(), _HDR) for r in rs]


def fresh():
    return clone(recs)


# flag: proper-pair bit (0x2) on reads with the paired bit cleared
rs = fresh()
tgt = [r for r in rs if r.is_paired and r.is_proper_pair][:40]
for r in tgt:
    r.flag = (r.flag & ~0x1) | 0x2
write("flag_proper_not_paired.bam", hdr, rs, index=False)
reg("flag_proper_not_paired.bam", "40 reads carry 0x2 (proper pair) without 0x1 (paired); mate flags removed")

# flag: mate-unmapped set though mate is mapped
rs = fresh()
tgt = [r for r in rs if r.is_paired and not r.mate_is_unmapped and not r.is_unmapped][:40]
for r in tgt:
    r.flag |= 0x8
write("flag_mate_unmapped.bam", hdr, rs)
reg("flag_mate_unmapped.bam", "40 reads say mate unmapped (0x8) while the mate is mapped")

# flag: mate strand bit wrong
rs = fresh()
tgt = [r for r in rs if r.is_paired and not r.is_unmapped and not r.mate_is_unmapped][:40]
for r in tgt:
    r.flag ^= 0x20
write("flag_mate_neg_strand.bam", hdr, rs)
reg("flag_mate_neg_strand.bam", "40 reads have the mate-reverse bit (0x20) flipped vs the mate's own 0x10")

# flag: both first and second in pair
rs = fresh()
tgt = [r for r in rs if r.is_paired and r.is_read1][:40]
for r in tgt:
    r.flag |= 0x80
write("flag_first_and_second.bam", hdr, rs)
reg("flag_first_and_second.bam", "40 read1 records also carry 0x80 (read2)")

# mate pos mismatch
rs = fresh()
tgt = [r for r in rs if r.is_paired and not r.mate_is_unmapped][:50]
for r in tgt:
    r.next_reference_start = r.next_reference_start + 137
write("mate_pos_mismatch.bam", hdr, rs)
reg("mate_pos_mismatch.bam", "50 reads: PNEXT off by +137 vs the mate's real POS")

# TLEN inconsistent
rs = fresh()
tgt = [r for r in rs if r.is_paired and r.is_proper_pair and r.template_length != 0][:50]
for r in tgt:
    r.template_length = r.template_length + 500
write("tlen_mismatch.bam", hdr, rs)
reg("tlen_mismatch.bam", "50 reads: TLEN +500 vs real (does not match mate)")

# orphans: drop the mate of 60 pairs
rs = fresh()
names = []
seen = set()
for r in rs:
    if r.is_paired and r.is_proper_pair and not r.is_secondary and r.query_name not in seen:
        seen.add(r.query_name)
        names.append(r.query_name)
drop = set(names[:60])
orph = []
dropped_once = set()
for r in rs:
    if r.query_name in drop and r.is_read2 and not r.is_secondary:
        continue
    orph.append(r)
write("orphans.bam", hdr, orph)
reg("orphans.bam", "60 pairs lose read2 -> 60 orphan mates still flagged paired/proper (MATE_NOT_FOUND)")

# unsorted, header says coordinate
rs = fresh()
mapped = [r for r in rs if not r.is_unmapped]
unm = [r for r in rs if r.is_unmapped]
random.shuffle(mapped)
write("unsorted_declared_sorted.bam", hdr, mapped + unm)
reg("unsorted_declared_sorted.bam", "records shuffled, header still @HD SO:coordinate")

# hdr says queryname? not a defect. Unmapped read with MAPQ 60
rs = fresh()
tg = [r for r in rs if r.is_unmapped]
for r in tg:
    r.mapping_quality = 60
write("unmapped_mapq60.bam", hdr, rs)
reg("unmapped_mapq60.bam", f"{len(tg)} unmapped reads carry MAPQ 60")

# CIGAR length != SEQ length
rs = fresh()
cnt = 0
for r in rs:
    if cnt >= 30:
        break
    ct = r.cigartuples
    if not r.is_unmapped and ct and ct[0][0] == 0 and ct[0][1] > 60:
        ct[0] = (0, ct[0][1] - 30)  # CIGAR now consumes 30 fewer query bases than SEQ holds
        r.cigartuples = ct
        cnt += 1
write("cigar_seq_mismatch.bam", hdr, rs)
reg("cigar_seq_mismatch.bam", f"{cnt} reads: first CIGAR op shortened by 30 (query length != SEQ length)")

# alignment beyond reference end
rs = fresh()
tgt = [r for r in rs if not r.is_unmapped][:5]
for r in tgt:
    r.reference_start = 39990  # LN=40001 ; reads 143 bp
rs = sorted(rs, key=lambda r: (r.reference_id if r.reference_id >= 0 else 10**9, r.reference_start))
write("pos_beyond_ref_end.bam", hdr, rs)
reg("pos_beyond_ref_end.bam", "5 reads start at 39990 on a 40001-bp contig (CIGAR runs off the reference end)")

# read group in record not in header
rs = fresh()
for r in rs[:50]:
    r.set_tag("RG", "NOT_IN_HEADER")
write("rg_not_in_header.bam", hdr, rs)
reg("rg_not_in_header.bam", "50 reads carry RG:Z:NOT_IN_HEADER")

# missing @SQ (unmapped-only, header without @SQ)
hd2 = {"HD": {"VN": "1.6", "SO": "unsorted"}, "RG": hdr["RG"]}
with pysam.AlignmentFile(os.path.join(OUT, "no_sq_unmapped.bam"), "wb", header=hd2) as o:
    for r in recs[:200]:
        a = pysam.AlignedSegment(o.header)
        a.query_name = r.query_name
        a.query_sequence = r.query_sequence
        a.flag = 4 | (r.flag & 0xC0) | 0x1 | 0x8
        a.mapping_quality = 0
        a.set_tag("RG", "1")
        o.write(a)
reg("no_sq_unmapped.bam", "header has NO @SQ lines (unmapped-only BAM). Valid as unaligned (-u) input; a defect for an aligned BAM", expected_bad=True,
    note="ambiguous: valid for unaligned BAMs. Ground truth for an ALIGNED-BAM validator = bad")

# empty BAM (header only)
write("empty_records.bam", hdr, [], index=False)
reg("empty_records.bam", "header only, 0 records (legal file, useless for QC)", expected_bad=True, note="legal but should be flagged as 'no reads'")

# ---- low mapping rate: 30% of pairs unmapped -------------------------------------
def make_low_map(placed):
    rs = fresh()
    pairs = {}
    for r in rs:
        if r.is_paired and r.is_proper_pair and not r.is_secondary:
            pairs.setdefault(r.query_name, []).append(r)
    chosen = set(list(pairs)[: int(0.30 * len(pairs))])
    keep, unm = [], []
    for r in rs:
        if r.query_name in chosen and r.is_paired and r.is_proper_pair and not r.is_secondary:
            r.flag = 0x1 | 0x4 | 0x8 | (0x40 if r.is_read1 else 0x80)
            r.mapping_quality = 0
            r.cigar = None
            r.template_length = 0
            r.next_reference_id = -1
            r.next_reference_start = -1
            if not placed:
                r.reference_id = -1
                r.reference_start = -1
                unm.append(r)
                continue
            # placed: keep RNAME/POS of the original (standard bwa behaviour for both-unmapped is unplaced; for
            # mapped-mate case the unmapped read takes the mate's coordinates). Here both unmapped but placed.
        keep.append(r)
    out = keep + unm
    out = sorted(out, key=lambda r: (r.reference_id if r.reference_id >= 0 else 10**9, r.reference_start if r.reference_start >= 0 else 10**9))
    return out


write("lowmap_unplaced.bam", hdr, make_low_map(False), index=True)
reg("lowmap_unplaced.bam", "30% of pairs unmapped and unplaced (RNAME *) -> true mapping rate ~70% (should FAIL <90%)")
# placed variant: 60% of pairs keep read1 mapped, read2 becomes unmapped and is placed at read1's coordinates
# (the standard bwa/samtools convention for a pair with one unmapped mate) -> 30% of all reads unmapped
def make_low_map_placed():
    rs = fresh()
    by = {}
    for r in rs:
        if r.is_paired and r.is_proper_pair and not r.is_secondary and not r.is_supplementary:
            by.setdefault(r.query_name, {})[1 if r.is_read1 else 2] = r
    names = [n for n, d in by.items() if 1 in d and 2 in d]
    chosen = set(names[: int(0.6 * len(names))])
    for n in chosen:
        r1, r2 = by[n][1], by[n][2]
        r1.flag = (r1.flag & ~(0x2 | 0x20)) | 0x8
        r1.next_reference_id = r1.reference_id
        r1.next_reference_start = r1.reference_start
        r1.template_length = 0
        rev = r1.is_reverse
        r2.flag = 0x1 | 0x4 | 0x80 | (0x20 if rev else 0)
        r2.reference_id = r1.reference_id
        r2.reference_start = r1.reference_start
        r2.mapping_quality = 0
        r2.cigar = None
        r2.next_reference_id = r1.reference_id
        r2.next_reference_start = r1.reference_start
        r2.template_length = 0
    return sorted(rs, key=lambda r: (r.reference_id if r.reference_id >= 0 else 10**9, r.reference_start if r.reference_start >= 0 else 10**9))


write("lowmap_placed.bam", hdr, make_low_map_placed(), index=True)
reg("lowmap_placed.bam", "60% of pairs: read2 unmapped but PLACED at read1's position (standard convention) -> ~30% of reads unmapped, true mapping rate ~70% (should FAIL <90%)")

# ---- single-end conversion: same reads, paired flags stripped ------------------
rs = fresh()
for r in rs:
    r.flag = r.flag & 0x914  # keep reverse (0x10), unmapped (0x4), secondary (0x100), supplementary (0x800); drop all pair bits
    r.next_reference_id = -1
    r.next_reference_start = -1
    r.template_length = 0
write("single_end_like.bam", hdr, rs, index=True)
reg("single_end_like.bam", "same reads as single-end (no paired flags): VALID; tests division by paired=0 in QC scripts", expected_bad=False)

# ---- strand-imbalanced: reads all forward ------------------------------
rs = fresh()
for r in rs:
    if not r.is_unmapped and r.is_reverse:
        r.flag &= ~0x10
write("strand_all_forward.bam", hdr, rs, index=True)
reg("strand_all_forward.bam", "all reverse-strand bits cleared (mate bits left): strand balance = 1.0 (biologically bad)", expected_bad=True,
    note="flag inconsistencies too; used to test the strand-balance metric only")

json.dump(truth, open(os.path.join(OUT, "fixtures.json"), "w"), indent=1)
print("made", len(truth), "fixtures")
for k in sorted(truth):
    print(f"  {k:32s} {os.path.getsize(os.path.join(OUT, k)):8d} B  bad={truth[k]['expected_bad']}  {truth[k]['defect'][:80]}")
