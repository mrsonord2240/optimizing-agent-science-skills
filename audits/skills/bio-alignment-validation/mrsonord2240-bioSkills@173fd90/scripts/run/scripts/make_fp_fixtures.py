"""SYNTHETIC fingerprint fixtures built by the re-auditor for the Skill's Contamination/Sample-swap block.
Independent of the fixer's 40-site data: 60 sites chosen here (every k-th position with depth >= 60 in the real human PE BAM,
reference = human/genome.fasta, contig chr22 40001 bp).
  hap.txt / sites.vcf.gz : Picard haplotype database and somalier-style sites VCF over the 60 sites
  Genotypes are planted by rewriting the read bases at the 60 sites: pattern P0 (hom-ref/het/hom-alt repeating) = individual A,
  P1 = individual B, all-het = H.  Reads are the real human PE reads (5644 records).
  A.bam SM=IND_A | A2.bam SM=IND_A2 (P0 again, hets drawn independently) | B.bam SM=IND_B | H.bam SM=IND_H (all het)
  A_sameSM_as_B.bam: P0 genotypes labelled SM=IND_B | A_rg1.bam / B_rg1.bam: P0 / P1 with the nf-core read group ID:1 PU:1 LB:testN
  L.bam: only 3 reads of A overlapping 2 sites (too little data), SM=IND_A
  Each unique-RG file has its own ID, PU and LB so Picard's read-group grouping cannot merge two files.
Run in WSL: python make_fp_fixtures.py <out-dir>
"""
import gzip
import os
import random
import subprocess
import sys

import pysam

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
PD = "/mnt/openscience/audit-envs/alignment-files/public-data/human"
SRC = f"{PD}/test.paired_end.sorted.bam"
FA = f"{PD}/genome.fasta"
fa = pysam.FastaFile(FA)
LN = fa.get_reference_length("chr22")

# depth per position (real reads)
cov = {}
with pysam.AlignmentFile(SRC) as b:
    for col in b.pileup("chr22", 1900, 4700, truncate=True, min_base_quality=0, stepper="nofilter", max_depth=100000):
        cov[col.reference_pos] = col.nsegments  # 0-based
cands = [p for p in sorted(cov) if cov[p] >= 60 and fa.fetch("chr22", p, p + 1).upper() in "ACGT"]
step = max(1, len(cands) // 60)
sites = cands[::step][:60]
ti = {"A": "G", "G": "A", "C": "T", "T": "C"}
info = []
for p in sites:
    ref = fa.fetch("chr22", p, p + 1).upper()
    info.append((p, ref, ti[ref]))
print(f"{len(cands)} candidate positions with depth>=60; using {len(sites)} sites, depth range {min(cov[p] for p in sites)}-{max(cov[p] for p in sites)}")

# Picard haplotype database (tab-delimited: header lines, then CHROM POS NAME MAJOR MINOR MAF ANCHOR_SNP_NAME; one SNP per haplotype block, so the anchor is the SNP itself)
hdr = subprocess.run(["samtools", "view", "-H", SRC], capture_output=True, text=True).stdout
sq = [l for l in hdr.splitlines() if l.startswith("@SQ")]
with open(f"{OUT}/hap.txt", "w", newline="\n") as f:
    f.write("@HD\tVN:1.6\tSO:unsorted\n")
    for l in sq:
        f.write(l + "\n")
    for i, (p, ref, alt) in enumerate(info):
        f.write(f"chr22\t{p + 1}\tsite{i}\t{ref}\t{alt}\t0.30\tsite{i}\n")
# somalier-style sites VCF
vcf = "##fileformat=VCFv4.2\n" + "".join(f"##contig=<ID=chr22,length={LN}>\n" for _ in [0]) + "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
for i, (p, ref, alt) in enumerate(info):
    vcf += f"chr22\t{p + 1}\tsite{i}\t{ref}\t{alt}\t.\t.\t.\n"
open(f"{OUT}/sites.vcf", "w", newline="\n").write(vcf)
subprocess.run(["bgzip", "-f", f"{OUT}/sites.vcf"], check=True)
subprocess.run(["tabix", "-f", "-p", "vcf", f"{OUT}/sites.vcf.gz"], check=True)

with pysam.AlignmentFile(SRC) as b:
    H = b.header.to_dict()
    recs = [r for r in b.fetch(until_eof=True)]
hb = pysam.AlignmentFile(SRC).header


def with_sm(name, rgid=None):
    h = dict(H)
    h["RG"] = [dict(rg, SM=name, **({"ID": rgid, "PU": rgid, "LB": rgid} if rgid else {})) for rg in H["RG"]]
    return h


def write(name, sm, rs, rgid=None):
    """rgid=None keeps the nf-core read group (ID:1 PU:1 LB:testN); otherwise RG ID, PU and LB are rewritten to rgid (unique per file)"""
    if rgid:
        for r in rs:
            r.set_tag("RG", rgid)
    with pysam.AlignmentFile(f"{OUT}/{name}", "wb", header=with_sm(sm, rgid)) as o:
        for r in rs:
            o.write(r)
    pysam.index(f"{OUT}/{name}")


def clone():
    return [pysam.AlignedSegment.fromstring(r.to_string(), hb) for r in recs]


siteset = {p: alt for p, _, alt in info}
site_index = {p: i for i, (p, _, _) in enumerate(info)}
P0 = [0.0, 0.5, 1.0]      # genotype pattern of individual A: hom-ref, het, hom-alt repeating over the sites
P1 = [1.0, 0.0, 0.5]      # individual B: a different genotype at every site


def force(rs, pattern, seed):
    """per site, a fraction pattern[i % 3] of the reads carry the ALT base (0 = hom-ref, 0.5 = het, 1 = hom-alt)"""
    rnd = random.Random(seed)
    for r in rs:
        if r.is_unmapped or r.query_sequence is None:
            continue
        seq = list(r.query_sequence)
        qual = r.query_qualities
        ch = False
        for qpos, rpos in r.get_aligned_pairs(matches_only=True):
            if rpos in siteset and rnd.random() < pattern[site_index[rpos] % 3]:
                seq[qpos] = siteset[rpos]
                ch = True
        if ch:
            r.query_sequence = "".join(seq)
            r.query_qualities = qual
    return rs


# unique read-group IDs (rg_<SM>): the normal, well-formed case
A_recs = force(clone(), P0, 1)
write("A.bam", "IND_A", A_recs, "rg_A")
write("A2.bam", "IND_A2", force(clone(), P0, 2), "rg_A2")      # same individual, independently drawn het alleles
write("A_sameSM_as_B.bam", "IND_B", force(clone(), P0, 3), "rg_Ab")   # individual A's genotypes labelled SM=IND_B
write("B.bam", "IND_B", force(clone(), P1, 4), "rg_B")
write("H.bam", "IND_H", force(clone(), [0.5, 0.5, 0.5], 5), "rg_H")
# the same genotypes, but keeping the nf-core read group (ID:1 PU:1 LB:testN) in both files (the collision case)
write("A_rg1.bam", "IND_A", force(clone(), P0, 1))
write("B_rg1.bam", "IND_B", force(clone(), P1, 4))
site_sub = [p for p, _, _ in info][:2]
few = []
for r in A_recs:
    if not r.is_unmapped and any(r.reference_start <= p < r.reference_end for p in site_sub) and len(few) < 3:
        few.append(pysam.AlignedSegment.fromstring(r.to_string(), hb))
write("L.bam", "IND_A", few, "rg_L")
print("built", sorted(x for x in os.listdir(OUT) if x.endswith(".bam")))
