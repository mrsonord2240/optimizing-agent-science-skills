# SYNTHETIC unaligned PacBio-style HiFi BAM: 60 reads of 1.2 kb, truth: 12 planted duplicates (exact copies, different ZMW names) => 12 flagged
import pysam, random
r = random.Random(11)
hd = {"HD": {"VN": "1.6", "SO": "unknown", "pb": "5.0.0"},
      "RG": [{"ID": "ab12cd34/0--0", "PL": "PACBIO", "DS": "READTYPE=CCS;BINDINGKIT=101-894-200;SEQUENCINGKIT=101-826-100;BASECALLERVERSION=5.0.0;FRAMERATEHZ=100.000000;BarcodeFile=bc.fasta;BarcodeHash=ffff;BarcodeCount=2;BarcodeMode=Symmetric;BarcodeQuality=Score", "PU": "m84011_220902_175841_s1", "SM": "sample1", "LB": "lib1", "BC": "ACGT--ACGT"}]}
h = pysam.AlignmentHeader.from_dict(hd)
seqs = ["".join(r.choice("ACGT") for _ in range(1200)) for _ in range(48)]
allr = list(seqs) + [seqs[i] for i in range(12)]   # 12 duplicates of the first 12
o = pysam.AlignmentFile("hifi.bam", "wb", header=h)
for i, s in enumerate(allr):
    a = pysam.AlignedSegment(h); a.query_name = "m84011_220902_175841_s1/%d/ccs" % (100 + i)
    a.flag = 4; a.query_sequence = s; a.query_qualities = pysam.qualitystring_to_array("~" * len(s))
    a.set_tag("RG", "ab12cd34/0--0"); a.set_tag("zm", 100 + i); a.set_tag("np", 10); a.set_tag("rq", 0.999, "f")
    o.write(a)
o.close()
with open("hifi.fastq", "w") as f:
    for i, s in enumerate(allr):
        f.write("@m84011_220902_175841_s1/%d/ccs\n%s\n+\n%s\n" % (100 + i, s, "~" * len(s)))
print("hifi.bam / hifi.fastq: 60 reads, 12 planted duplicates")
