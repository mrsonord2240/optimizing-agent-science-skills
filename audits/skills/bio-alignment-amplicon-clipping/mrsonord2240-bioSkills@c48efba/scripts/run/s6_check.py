"""Input 6 checker (planted truth, SYNTHETIC HiFi-like 16S). cwd = out/i6. WSL env python.
For each final BAM compare every primary read's aligned span with the truth-derived expectation of an ideal
--both-ends --strand clip: an end that lost <= 3 bp still lies in the primer (or just upstream) -> must land exactly on the primer
boundary (left: 20, right: len-19); a deep-truncated end (>= 25 bp lost) has no primer -> must be unchanged from the alignment.
Tolerance for aligner noise: read ends may sit +-0 only after clipping (tests exact boundaries)."""
import sys, collections, pysam
D = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/data"
ref = pysam.FastaFile(f"{D}/hifi_ref.fa"); L = {c: ref.get_reference_length(c) for c in ref.references}
truth = {}
for i, l in enumerate(open(f"{D}/hifi_truth.tsv")):
    if i == 0: continue
    n, c, o, l5, l3 = l.rstrip("\n").split("\t"); truth[n] = (c, o, int(l5), int(l3))
PF, PR = 20, 19
def score(path, label, both=True):
    c = collections.Counter(); bad = []
    with pysam.AlignmentFile(path) as f:
        for r in f.fetch(until_eof=True):
            if r.is_secondary or r.is_supplementary or r.is_unmapped: c["skipped"] += 1; continue
            cont, o, lost5, lost3 = truth[r.query_name]; ln = L[cont]
            # left end of the alignment on the contig
            left_expect_clip = lost5 <= 3          # contig-left end still holds (part of) 27F primer
            right_expect_clip = lost3 <= 3
            ok_l = (r.reference_start == PF) if left_expect_clip else (r.reference_start >= lost5 - 2)
            ok_r = (r.reference_end == ln - PR) if (right_expect_clip and both) else (r.reference_end <= ln - lost3 + 2)
            if not both: ok_r = True
            c["reads"] += 1; c["left ok"] += ok_l; c["right ok"] += ok_r
            if not (ok_l and ok_r) and len(bad) < 4: bad.append((r.query_name, r.is_reverse, r.reference_start, r.reference_end, "lost", lost5, lost3, r.cigarstring[:40]))
    print(f"{label:34s} {dict(c)}"); [print("    bad:", b) for b in bad]
for path, label, both in [("m_both_strand.bam", "--both-ends --strand", True), ("ex_default_final.bam", "shipped example (default)", True)]:
    score(path, label, both)
