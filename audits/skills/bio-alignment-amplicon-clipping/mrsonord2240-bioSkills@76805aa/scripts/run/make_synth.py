"""SYNTHETIC data (planted truth) for the amplicon-clipping audit. Run in WSL env python (pysam).
Contig amp1, 3000 bp random (seed 20260920). Four amplicons tiled with overlap. Sample genome carries SNPs at 310 and 335:
 310 lies in primer L2 [300,325) (and in amplicon 1's insert), 335 lies in primer R1 [325,350) (and in amplicon 2's insert).
Primer-derived bases carry REF; biology carries ALT. So truth VAF = 1.0 at both sites; unclipped VAF = ~0.5.
Outputs (run/data): synth.fa(+fai), synth_primers.bed (6 col, BED-0based), synth_pe.bam (coord-sorted, indexed), truth.json
"""
import random, json, os, pysam
OUT = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/data"
os.makedirs(OUT, exist_ok=True)
random.seed(20260920)
L = 3000
ref = "".join(random.choice("ACGT") for _ in range(L))
with open(f"{OUT}/synth.fa", "w") as f:
    f.write(">amp1\n")
    for i in range(0, L, 60): f.write(ref[i:i+60] + "\n")
pysam.faidx(f"{OUT}/synth.fa")
# amplicons: (name, amp_start, amp_end, primer_len)
amps = [("A1", 100, 350), ("A2", 300, 550), ("A3", 500, 750), ("A4", 900, 980)]
PL = 25
bed = []
for n, s, e in amps:
    bed.append(("amp1", s, s + PL, f"{n}_LEFT", 60, "+"))
    bed.append(("amp1", e - PL, e, f"{n}_RIGHT", 60, "-"))
with open(f"{OUT}/synth_primers.bed", "w") as f:
    for b in bed: f.write("\t".join(map(str, b)) + "\n")
snps = {310: None, 335: None}
alt = list(ref)
for p in snps:
    a = random.choice([b for b in "ACGT" if b != ref[p]]); snps[p] = a; alt[p] = a
alt = "".join(alt)
def comp(s): return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]
PLAN = {}
def primer_derived(seq, start, amp_s, amp_e):
    """sequence of a read placed at [start,start+len): primer bases (left primer [amp_s,amp_s+PL) and right primer) come from REF."""
    out = list(seq)
    for i in range(len(seq)):
        pos = start + i
        if amp_s <= pos < amp_s + PL or amp_e - PL <= pos < amp_e: out[i] = ref[pos]
    return "".join(out)
hdr = {"HD": {"VN": "1.6", "SO": "unsorted"}, "SQ": [{"SN": "amp1", "LN": L}], "RG": [{"ID": "rg1", "SM": "synth"}]}
recs = []
N = 100
for n, s, e in amps:
    short = (e - s) < 100
    rl = (e - s) if short else 100
    for k in range(N):
        j1 = 0 if random.random() < 0.8 else random.randint(1, 3)   # 5' jitter inside tolerance (5)
        j2 = 0 if random.random() < 0.8 else random.randint(1, 3)
        r1s = s + j1; r2e = e - j2; r2s = r2e - (rl - j2 if short else rl)
        if short: r1len = rl - j1; r2s = s + j1 - j1  # R2 covers [s, r2e)
        else: r1len = rl
        r1seq = primer_derived(alt[r1s:r1s + r1len], r1s, s, e)
        r2seq_f = primer_derived(alt[r2s:r2e], r2s, s, e)
        name = f"{n}_{k:03d}"
        tlen = r2e - r1s
        for is_r1 in (True, False):
            a = pysam.AlignedSegment(); a.query_name = name; a.reference_id = 0
            if is_r1:
                a.flag = 99; a.reference_start = r1s; a.query_sequence = r1seq; a.next_reference_start = r2s; a.template_length = tlen
                a.cigartuples = [(0, len(r1seq))]
            else:
                a.flag = 147; a.reference_start = r2s; a.query_sequence = r2seq_f  # BAM stores the reference-strand sequence for reverse reads
                a.next_reference_start = r1s; a.template_length = -tlen
                a.cigartuples = [(0, len(r2seq_f))]
            a.next_reference_id = 0; a.mapping_quality = 60
            a.query_qualities = pysam.qualitystring_to_array("I" * a.query_length)
            a.set_tag("RG", "rg1")
            recs.append(a)
with pysam.AlignmentFile(f"{OUT}/unsorted.bam", "wb", header=hdr) as o:
    for a in recs: o.write(a)
pysam.sort("-o", f"{OUT}/synth_pe.bam", f"{OUT}/unsorted.bam"); pysam.index(f"{OUT}/synth_pe.bam")
os.remove(f"{OUT}/unsorted.bam")
json.dump({"alt_at": {str(k): v for k, v in snps.items()}, "ref_at": {str(k): ref[k] for k in snps},
           "amps": amps, "primer_len": PL, "pairs_per_amp": N}, open(f"{OUT}/truth.json", "w"), indent=1)
print("wrote", len(recs), "records; SNPs", {k: (ref[k], v) for k, v in snps.items()})
