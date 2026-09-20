"""NEW fixtures (re-auditor's own; the first auditor and the fixer never used these).  All SYNTHETIC derivatives of REAL reads.

Family N: planted-defect BAMs the first auditor did not plant.  Base = real 1000 Genomes HG00349 chr20 slice (9601 records,
          3366-contig GRCh38 header, real bwakit alignments) -- a different base than the first audit's human chr22 slice --
          except n_nm_wrong / n_md_wrong which need a reference and use the human chr22-slice PE BAM.
Family L: threshold LADDER on real human PE reads: each file targets one Quality-Threshold band (PASS/WARN/FAIL) of one metric.
          The expected verdict is computed HERE from the records with the SKILL.md threshold table, independent of the validators.
Run in WSL: python make_new_fixtures.py <public-data-dir> <out-dir>
"""
import json
import os
import random
import sys

import pysam

PD, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
random.seed(7)
G1K = os.path.join(PD, "1000g", "HG00349.chr20_1400000-1500000.bam")
HUM = os.path.join(PD, "human", "test.paired_end.sorted.bam")
truth = {}


def reg(name, defect, expected_bad=True, **kw):
    truth[name] = {"defect": defect, "expected_bad": expected_bad, "synthetic": True, **kw}


def loadbam(p):
    with pysam.AlignmentFile(p, "rb") as b:
        return b.header.to_dict(), [r for r in b.fetch(until_eof=True)], b.header


def clone(rs, hdr):
    return [pysam.AlignedSegment.fromstring(r.to_string(), hdr) for r in rs]


def write(name, hdrdict, recs):
    p = os.path.join(OUT, name)
    with pysam.AlignmentFile(p, "wb", header=hdrdict) as o:
        for r in recs:
            o.write(r)
    return p


def sortkey(r):
    return (r.reference_id if r.reference_id >= 0 else 10**9, r.reference_start if r.reference_start >= 0 else 10**9)


# ------------------------------------------------------------------ Family N (1000G base)
gh, grecs, gH = loadbam(G1K)
fresh = lambda: clone(grecs, gH)  # noqa: E731
prim = lambda rs: [r for r in rs if not r.is_secondary and not r.is_supplementary]  # noqa: E731

write("n_ctl_valid.bam", gh, fresh())
reg("n_ctl_valid.bam", "none (control: real 1000G slice rewritten by pysam)", expected_bad=False)

rs = fresh()
dup_out = []
for i, r in enumerate(rs):
    dup_out.append(r)
    if i % 160 == 0 and not r.is_secondary:  # ~60 records duplicated verbatim, adjacent
        dup_out.append(pysam.AlignedSegment.fromstring(r.to_string(), gH))
write("n_dup_records.bam", gh, dup_out)
reg("n_dup_records.bam", f"{len(dup_out) - len(rs)} records written twice verbatim (same name/flag/pos)")

rs = fresh()
tgt = [r for r in rs if r.is_paired and r.is_proper_pair and not r.is_secondary and not r.is_supplementary][:40]
for r in tgt:
    r.next_reference_id = gH.get_tid("chr1")   # RNEXT says chr1 while flagged proper pair on chr20
write("n_mate_other_chrom.bam", gh, rs)
reg("n_mate_other_chrom.bam", "40 proper-pair reads whose RNEXT is chr1 (mate said to be on another contig)")

rs = fresh()
tgt = [r for r in rs if r.is_paired and r.is_proper_pair and r.template_length < 0 and not r.is_secondary][:40]
for r in tgt:
    r.template_length = -r.template_length      # both mates now positive TLEN
write("n_tlen_same_sign.bam", gh, rs)
reg("n_tlen_same_sign.bam", "40 reads: TLEN sign flipped so both mates of a pair have the same sign")

h2 = json.loads(json.dumps(gh))
h2["HD"]["SO"] = "queryname"
write("n_hd_queryname_but_coord.bam", h2, fresh())
reg("n_hd_queryname_but_coord.bam", "@HD SO:queryname while the records are coordinate sorted")

rs = fresh()
cnt = 0
for r in rs:
    ct = r.cigartuples
    if cnt < 30 and not r.is_unmapped and ct == [(0, 101)]:
        r.cigartuples = [(0, 40), (5, 10), (0, 61)]     # H in the middle: query length preserved
        cnt += 1
write("n_cigar_H_middle.bam", gh, rs)
reg("n_cigar_H_middle.bam", f"{cnt} reads with CIGAR 40M10H61M (hard clip inside the alignment; query length still 101)")

rs = fresh()
cnt = 0
for r in rs:
    if cnt < 30 and not r.is_unmapped and r.query_qualities is not None:
        q = list(r.query_qualities)
        q[10] = 120                                   # Phred 120 > 93, not encodable as printable ASCII
        r.query_qualities = q
        cnt += 1
write("n_qual_out_of_range.bam", gh, rs)
reg("n_qual_out_of_range.bam", f"{cnt} reads with one base quality of 120 (> Phred 93)")

rs = fresh()
for r in rs:
    r.flag |= 0x100
write("n_all_secondary.bam", gh, rs)
reg("n_all_secondary.bam", "every record flagged secondary (0x100): no primary alignment in the file")

# singleton flood: for 45% of pairs read2 becomes unmapped+unplaced, read1 keeps position with mate-unmapped
rs = fresh()
by = {}
for r in rs:
    if r.is_paired and not r.is_secondary and not r.is_supplementary:
        by.setdefault(r.query_name, {})[1 if r.is_read1 else 2] = r
names = [n for n, d in by.items() if len(d) == 2 and not d[1].is_unmapped and not d[2].is_unmapped]
random.shuffle(names)
for n in names[: int(0.45 * len(names))]:
    r1, r2 = by[n][1], by[n][2]
    r1.flag = (r1.flag & ~(0x2 | 0x20)) | 0x8
    r1.next_reference_id, r1.next_reference_start, r1.template_length = -1, -1, 0
    r2.flag = 0x1 | 0x4 | 0x80
    r2.reference_id, r2.reference_start = -1, -1
    r2.mapping_quality, r2.cigar = 0, None
    r2.next_reference_id, r2.next_reference_start, r2.template_length = -1, -1, 0
    for t in ("MC", "MQ", "XA", "XS", "AS", "MD", "NM"):
        try:
            r2.set_tag(t, None)
        except Exception:  # noqa: BLE001
            pass
rs.sort(key=sortkey)
write("n_singleton_flood.bam", gh, rs)
reg("n_singleton_flood.bam", "45% of pairs: mate 2 unmapped and unplaced, mate 1 mapped with mate-unmapped flag (poor pairing AND mapping ~77%)")

rs = fresh()
tgt = [r for r in rs if r.is_paired and not r.is_secondary][:40]
for r in tgt:
    r.flag &= ~(0x40 | 0x80)
write("n_no_mate_flags.bam", gh, rs)
reg("n_no_mate_flags.bam", "40 paired reads with neither first-of-pair (0x40) nor second-of-pair (0x80) set")

rs = fresh()
for r in rs:
    if not r.is_unmapped:
        r.mapping_quality = 255
write("n_mapq255_all.bam", gh, rs)
reg("n_mapq255_all.bam", "every mapped read has MAPQ 255 (STAR-style 'not available' sentinel; semantically a valid file)", expected_bad=False,
    note="mean-MAPQ grading is meaningless here (Skill says so for STAR); a validator PASS is the documented behaviour")

# (a header with a duplicated @SQ line was tried: samtools reheader rejects it, 'Duplicate entry chr20 in sam header', so it is not a representable file)

# ------------------------------------------------------------------ NM / MD on the human chr22-slice BAM (needs R=)
hh, hrecs, hH = loadbam(HUM)
rs = clone(hrecs, hH)
cnt = 0
for r in rs:
    if cnt < 40 and not r.is_unmapped and r.has_tag("NM"):
        r.set_tag("NM", r.get_tag("NM") + 5)
        cnt += 1
write("n_nm_wrong.bam", hh, rs)
reg("n_nm_wrong.bam", f"{cnt} reads with NM inflated by 5 (needs R= to be checked)", human_ref=True)
rs = clone(hrecs, hH)
cnt = 0
for r in rs:
    if cnt < 40 and not r.is_unmapped and r.has_tag("MD"):
        md = r.get_tag("MD")
        r.set_tag("MD", "1" + md if md[0].isdigit() else md)  # shifts every match run by one base
        cnt += 1
write("n_md_wrong.bam", hh, rs)
reg("n_md_wrong.bam", f"{cnt} reads with MD tag shifted by one base (needs R=)", human_ref=True)


# ------------------------------------------------------------------ Family L: threshold ladder (real human PE reads)
def grade_min(v, good, warn):
    return "PASS" if v > good else "WARN" if v >= warn else "FAIL"


def grade_strand(f):
    return "PASS" if 0.48 <= f <= 0.52 else "WARN" if 0.45 <= f <= 0.55 else "FAIL"


def expected(rs):
    """independent recomputation of the four graded metrics from the records; SKILL.md 'Quality Thresholds Summary' bands"""
    P = [r for r in rs if not r.is_secondary and not r.is_supplementary]
    M = [r for r in P if not r.is_unmapped]
    d = {"map": 100 * len(M) / len(P)}
    pr = [r for r in M if r.is_paired]
    if pr:
        d["pair"] = 100 * sum(1 for r in pr if r.is_proper_pair) / len(pr)
    fw = sum(1 for r in M if not r.is_reverse)
    d["strand"] = fw / len(M)
    d["mapq"] = sum(r.mapping_quality for r in M) / len(M)
    g = {"map": grade_min(d["map"], 95, 90), "strand": grade_strand(d["strand"]), "mapq": grade_min(d["mapq"], 40, 30)}
    if "pair" in d:
        g["pair"] = grade_min(d["pair"], 90, 80)
    overall = "FAIL" if "FAIL" in g.values() else "WARN" if "WARN" in g.values() else "PASS"
    return d, g, overall


def hfresh():
    return clone(hrecs, hH)


def unmap_pairs(rs, frac):
    """make `frac` of the primary mapped PROPER pairs unmapped+unplaced (both mates)"""
    by = {}
    for r in rs:
        if r.is_paired and r.is_proper_pair and not r.is_secondary and not r.is_supplementary:
            by.setdefault(r.query_name, []).append(r)
    ns = [n for n, v in by.items() if len(v) == 2]
    random.Random(1).shuffle(ns)
    for n in ns[: int(round(frac * len(ns)))]:
        for r in by[n]:
            r.flag = 0x1 | 0x4 | 0x8 | (0x40 if r.is_read1 else 0x80)
            r.reference_id = r.reference_start = -1
            r.next_reference_id = r.next_reference_start = -1
            r.mapping_quality, r.cigar, r.template_length = 0, None, 0
    rs.sort(key=sortkey)
    return rs


def strip_proper(rs, frac):
    by = {}
    for r in rs:
        if r.is_paired and r.is_proper_pair and not r.is_secondary and not r.is_supplementary:
            by.setdefault(r.query_name, []).append(r)
    ns = [n for n, v in by.items() if len(v) == 2]
    random.Random(2).shuffle(ns)
    for n in ns[: int(round(frac * len(ns)))]:
        for r in by[n]:
            r.flag &= ~0x2
    return rs


def set_forward_fraction(rs, target):
    M = [r for r in rs if not r.is_unmapped and not r.is_secondary and not r.is_supplementary]
    fw = [r for r in M if not r.is_reverse]
    rv = [r for r in M if r.is_reverse]
    want_f = int(round(target * len(M)))
    random.Random(3).shuffle(fw)
    random.Random(4).shuffle(rv)
    if want_f > len(fw):
        for r in rv[: want_f - len(fw)]:
            r.flag &= ~0x10
    else:
        for r in fw[: len(fw) - want_f]:
            r.flag |= 0x10
    return rs


def set_mapq(rs, v):
    for r in rs:
        if not r.is_unmapped:
            r.mapping_quality = v
    return rs


ladder = {
    "lad_all_pass":   (lambda: set_mapq(hfresh(), 60)),
    "lad_map_92":     (lambda: unmap_pairs(hfresh(), 0.08)),       # 92% mapped -> WARN
    "lad_map_88":     (lambda: unmap_pairs(hfresh(), 0.12)),       # 88% -> FAIL
    "lad_pair_85":    (lambda: strip_proper(hfresh(), 0.15)),      # 85% proper -> WARN
    "lad_pair_70":    (lambda: strip_proper(hfresh(), 0.30)),      # 70% -> FAIL
    "lad_strand_465": (lambda: set_forward_fraction(hfresh(), 0.465)),  # WARN
    "lad_strand_58":  (lambda: set_forward_fraction(hfresh(), 0.58)),   # FAIL (high side)
    "lad_strand_43":  (lambda: set_forward_fraction(hfresh(), 0.43)),   # FAIL (low side)
    "lad_mapq_45":    (lambda: set_mapq(hfresh(), 45)),            # PASS
    "lad_mapq_35":    (lambda: set_mapq(hfresh(), 35)),            # WARN
    "lad_mapq_25":    (lambda: set_mapq(hfresh(), 25)),            # FAIL
    "lad_warn_plus_fail": (lambda: set_forward_fraction(unmap_pairs(hfresh(), 0.08), 0.58)),  # mapping WARN + strand FAIL -> FAIL
}
ladder_truth = {}
for name, fn in ladder.items():
    rs = fn()
    d, g, ov = expected(rs)
    write(name + ".bam", hh, rs)
    ladder_truth[name] = {"metrics": {k: round(v, 4) for k, v in d.items()}, "grades": g, "overall": ov,
                          "expected_rc": 1 if ov == "FAIL" else 0}
    print(f"{name:20s} overall={ov:5s} rc={ladder_truth[name]['expected_rc']} {ladder_truth[name]['metrics']} {g}")

json.dump(truth, open(os.path.join(OUT, "fixtures_new.json"), "w"), indent=1)
json.dump(ladder_truth, open(os.path.join(OUT, "ladder_truth.json"), "w"), indent=1)
print("made", len(truth), "planted +", len(ladder_truth), "ladder")
for k in sorted(truth):
    print(f"  {k:30s} {os.path.getsize(os.path.join(OUT, k)):8d} B  bad={truth[k]['expected_bad']}  {truth[k]['defect'][:90]}")
