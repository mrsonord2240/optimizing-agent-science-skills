#!/usr/bin/env python3
"""NEW input 8 (second re-auditor's own design, not the fixer's 4-fold toy): synthetic Kinnex HiFi array BAM.
Adapters: the 5 sequences printed on skera.how/adapters (A-E) + 2 random 16-mers (F,G) = a 6-fold array needs 7 adapters, in array order A..G.
Each S-read = Iso-Seq 5' primer + cDNA (150-2500 nt) + polyA(25) + rc(3' primer), so lima/isoseq refine have real structure to find.
24 ZMWs: 16 full arrays (8 of them stored reverse-complemented, as a read may be), 4 with the LAST adapter missing (5 complete segments + a tail), 4 with a middle adapter missing (segments 3+4 fuse).
Writes kinnex3.bam (unaligned PacBio-style CCS BAM), adapters7.fasta, primers.fasta, truth3.tsv (zmw, expected S-read sequences in array order)."""
import pysam, random
rnd = random.Random(20260920)
comp = str.maketrans("ACGT", "TGCA"); rc = lambda s: s.translate(comp)[::-1]
ad = ["AGCTTACTTGTGAAGA", "ACTTGTAAGCTGTCTA", "ACTCTGTCAGGTCCGA", "ACCTCCTCCTCCAGAA", "AACCGGACACACTTAG"]
while len(ad) < 7: ad.append("".join(rnd.choice("ACGT") for _ in range(16)))
P5, P3 = "GCAATGAAGTCGCAGGGTTGGG", "GTACTCTGCGTTGATACCACTGCTT"
open("adapters7.fasta", "w").write("".join(">%s\n%s\n" % ("ABCDEFG"[i], a) for i, a in enumerate(ad)))
open("primers.fasta", "w").write(">IsoSeq_5p\n%s\n>IsoSeq_3p\n%s\n" % (P5, P3))
hdr = {"HD": {"VN": "1.6", "SO": "unknown", "pb": "5.0.0"},
       "RG": [{"ID": "abc123/0--0", "PL": "PACBIO", "DS": "READTYPE=CCS;BINDINGKIT=101-894-200;SEQUENCINGKIT=101-826-100;BASECALLERVERSION=5.0;FRAMERATEHZ=100", "PU": "m84039_240124_190648_s3", "PM": "REVIO"}]}
out = pysam.AlignmentFile("kinnex3.bam", "wb", header=hdr)
tr = open("truth3.tsv", "w"); tr.write("zmw\tkind\tsegments_in_array_order\n")
for hole in range(1, 25):
    segs = [P5 + "".join(rnd.choice("ACGT") for _ in range(rnd.randint(150, 2500))) + "A" * 25 + rc(P3) for _ in range(6)]
    kind = "full" if hole <= 16 else ("last_adapter_missing" if hole <= 20 else "middle_adapter_missing")
    parts = [ad[0]] + [s + ad[i + 1] for i, s in enumerate(segs)]
    if kind == "last_adapter_missing": parts[-1] = segs[-1]
    if kind == "middle_adapter_missing": parts[4] = segs[3]          # adapter between segment 3 and 4 dropped -> they fuse
    seq = "".join(parts)
    exp = list(segs) if kind == "full" else (segs[:5] + [segs[5]] if kind == "last_adapter_missing" else segs[:3] + [segs[3] + segs[4]] + segs[5:])
    if hole % 2 == 0 and kind == "full": seq = rc(seq); exp = [rc(s) for s in exp[::-1]]
    a = pysam.AlignedSegment(); a.query_name = "m84039_240124_190648_s3/%d/ccs" % hole; a.flag = 4
    a.query_sequence = seq; a.query_qualities = pysam.qualitystring_to_array("~" * len(seq))
    a.set_tag("RG", "abc123/0--0"); a.set_tag("zm", hole); a.set_tag("np", 10); a.set_tag("rq", 0.999, "f")
    out.write(a); tr.write("%d\t%s\t%s\n" % (hole, kind, ",".join(exp)))
out.close(); tr.close()
print("24 ZMWs written")
