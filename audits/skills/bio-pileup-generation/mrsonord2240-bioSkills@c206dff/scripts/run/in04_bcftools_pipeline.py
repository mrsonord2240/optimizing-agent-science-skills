#!/usr/bin/env python3
"""Input 4 (Variant B): 'Call variants with the modern bcftools mpileup -> bcftools call pipeline (single sample, BCF intermediate,
multi-sample joint, parallel by chromosome), and tell me whether the "WRONG" pipe really is wrong.'
Commands are the Skill's / usage-guide's, with only file names and contig lists substituted. Truth = planted synthetic events."""
import json, os, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

I = 4
SYN = DATA + "/syn.bam"; SF = DATA + "/syn.fa"
W = WORK + "/in04"
os.makedirs(W, exist_ok=True)
T = json.load(open(DATA + "/truth.json"))["truth"]["events"]
snp = T["snp"]

def vcf_records(path):
    rc, out, err = sh(f"bcftools view -H {path}")
    recs = []
    for l in out.splitlines():
        f = l.split("\t")
        recs.append(dict(chrom=f[0], pos=int(f[1]), ref=f[3], alt=f[4], qual=float(f[5]) if f[5] != "." else None, info=f[7], fmt=f[8] if len(f) > 8 else "", samples=f[9:]))
    return recs

# ---------------- A. SKILL.md 'Modern Germline Calling' verbatim (files substituted)
cmd = f"""cd {W} && bcftools mpileup -f {SF} -d 1000000 -q 20 -Q 20 --annotate FORMAT/AD,FORMAT/DP,FORMAT/SP,INFO/AD {SYN} | bcftools call -mv -Oz -o variants.vcf.gz && bcftools index -t variants.vcf.gz"""
rc, out, err = sh(cmd)
print("stderr:", err.strip()[-300:])
check(I, "SKILL 'Modern Germline Calling' pipeline runs and writes variants.vcf.gz + .tbi", rc == 0 and os.path.exists(W + "/variants.vcf.gz") and os.path.exists(W + "/variants.vcf.gz.tbi"), f"rc={rc}")
recs = vcf_records(W + "/variants.vcf.gz")
for r in recs:
    print(r["chrom"], r["pos"], r["ref"], r["alt"], r["qual"], r["info"][:80], r["fmt"], r["samples"])
snp_r = [r for r in recs if r["pos"] == snp["pos"]]
check(I, "planted SNP synA:100 T>C is called with the Skill's flags", len(snp_r) == 1 and snp_r[0]["ref"] == snp["ref"] and snp_r[0]["alt"].split(",")[0] == snp["alt"], snp_r)
if snp_r:
    fmt = snp_r[0]["fmt"].split(":"); sm = snp_r[0]["samples"][0].split(":")
    d = dict(zip(fmt, sm))
    check(I, "FORMAT/AD at the SNP == planted 30,10 and FORMAT/DP == 40", d.get("AD", "").startswith("30,10") and d.get("DP") == "40", d)
    check(I, "requested tags present: FORMAT/AD,DP,SP and INFO/AD", all(t in fmt for t in ("AD", "DP", "SP")) and "AD=" in snp_r[0]["info"], f"FORMAT={fmt} INFO={snp_r[0]['info'][:60]}")
ins_r = [r for r in recs if r["pos"] in (200, 199)]
del_r = [r for r in recs if 245 <= r["pos"] <= 251 and len(r["ref"]) > 1]
check(I, "planted 2 bp insertion after synA:200 is called", any(len(r["alt"]) > len(r["ref"]) for r in ins_r), [(r["pos"], r["ref"], r["alt"]) for r in ins_r])
check(I, "planted 3 bp deletion synA:251-253 is called (default BAQ + -Q 20)", bool(del_r), [(r["pos"], r["ref"], r["alt"]) for r in recs if 240 <= r["pos"] <= 260])
extra = [(r["pos"], r["ref"], r["alt"]) for r in recs if r["pos"] not in (100, 199, 200, 249, 250, 251, 930)]
check(I, "no unexplained records beyond the planted SNP/ins/del (+ synA:930, the planted conflicting-overlap site, called 2 ref/3 alt)", not extra, f"extra {extra}")

# ---------------- B. usage-guide BCF intermediate + single sample with -a FORMAT/AD,FORMAT/DP + bcftools index (csi)
rc, out, err = sh(f"""cd {W} && bcftools mpileup -f {SF} -d 1000000 -q 20 -Q 20 -a FORMAT/AD,FORMAT/DP {SYN} | bcftools call -mv -Oz -o v2.vcf.gz && bcftools index v2.vcf.gz && bcftools mpileup -f {SF} -d 1000000 -Ob -o raw.bcf {SYN} && bcftools call -mv raw.bcf -o variants.vcf""")
check(I, "usage-guide single-sample + `bcftools index` and BCF intermediate (`bcftools call -mv raw.bcf -o variants.vcf`) run", rc == 0 and os.path.exists(W + "/v2.vcf.gz.csi") and os.path.getsize(W + "/variants.vcf") > 0, f"rc={rc} {err.strip()[-150:]}")
r2 = vcf_records(W + "/variants.vcf")
print("BCF-intermediate records (no -q/-Q):", [(r["pos"], r["ref"], r["alt"]) for r in r2])
check(I, "BCF-intermediate route calls the planted SNP too", any(r["pos"] == 100 for r in r2), [(r["pos"]) for r in r2])

# ---------------- C. multi-sample joint calling (SKILL 'Multi-Sample Joint Calling'; s3.bam absent -> two samples)
rc, out, err = sh(f"""cd {W} && bcftools mpileup -f {SF} --threads 4 -d 250 -q 20 -Q 20 -a FORMAT/AD,FORMAT/DP {DATA}/s1.bam {DATA}/s2.bam | bcftools call -mv --threads 4 -Oz -o joint.vcf.gz""")
check(I, "multi-sample command (with --threads 4) runs", rc == 0 and os.path.exists(W + "/joint.vcf.gz"), f"rc={rc} {err.strip()[-150:]}")
rc, hdr, _ = sh(f"bcftools query -l {W}/joint.vcf.gz")
check(I, "joint VCF sample names come from the @RG SM tags (s1, s2)", hdr.split() == ["s1", "s2"], hdr.split())
rc, q, _ = sh(f"bcftools query -f '%POS [%AD|]\\n' {W}/joint.vcf.gz")
print("joint AD per sample:", q.strip())
check(I, "joint per-sample AD == planted (s1: 17,3  s2: 8,12)", "100 17,3|8,12|" in q, q.strip())

# ---------------- D. the 'WRONG' pipe
rc, out, err = sh(f"samtools mpileup -f {SF} {SYN} 2>/dev/null | bcftools call -mv 2>&1 | head -5; echo \"pipestatus=${{PIPESTATUS[*]}}\"")
print("WRONG pipe output:", out.strip()[:400])
check(I, "the Skill's 'WRONG' pipe (samtools mpileup | bcftools call) fails", "pipestatus=0 0" not in out, out.strip()[:200])
why_cap = ("cap" in out.lower() and "250" in out)
check(I, "the failure is due to a double depth cap (the reason the Skill gives in its comment)", why_cap, f"actual message: 'Failed to read from standard input: unknown file type' -> a text pileup is not VCF/BCF; bcftools call applies no depth cap, so the Skill's explanation is wrong")

# ---------------- E. parallel by chromosome (usage-guide loop), verbatim with contig list expanded
os.makedirs(W + "/par", exist_ok=True)
loop = f"""#!/bin/bash
set -u
cd {W}/par
rm -f chr*.vcf.gz* all.vcf.gz*
for chr in chr1 chr2 chr3 chr4 chr5 chr6 chr7 chr8 chr9 chr10 chr11; do
    bcftools mpileup -f {DATA}/multi.fa -r "$chr" -d 1000000 {DATA}/multi.bam | \\
        bcftools call -mv -Oz -o "${{chr}}.vcf.gz" &
done
wait
bcftools concat -Oz -o all.vcf.gz chr*.vcf.gz && bcftools index all.vcf.gz
echo "concat_status=$?"
"""
open(W + "/par_loop.sh", "w", newline="\n").write(loop)
rc, out, err = sh(f"bash {W}/par_loop.sh")
print("parallel loop stdout/err:", out.strip()[-200:], err.strip()[-300:])
rc, order, _ = sh(f"bcftools view -H {W}/par/all.vcf.gz | cut -f1")
got = order.split()
truth_order = [f"chr{i}" for i in range(1, 12)]
print("all.vcf.gz contig order:", got)
check(I, "each per-chromosome call has the planted SNP (11 records, pos 100)", len(got) == 11, got)
check(I, "usage-guide `bcftools concat ... chr*.vcf.gz` (shell glob = lexicographic: chr1,chr10,chr11,chr2...) preserves header contig order", got == truth_order and "concat_status=0" in out, f"order {got}; {err.strip()[-160:]}")
rc, o2, e2 = sh(f"bcftools index -f {W}/par/all.vcf.gz && echo index_ok")
print("index of concat result:", o2.strip(), e2.strip()[:200])

# ---------------- F. bcftools -a tag list & flags named in the Skill
rc, out, err = sh("bcftools mpileup -a '?' 2>&1 | head -30")
print(out[:900])
tags = ["FORMAT/AD", "FORMAT/DP", "FORMAT/SP", "INFO/AD"]
check(I, "annotate tags named in the Skill (FORMAT/AD,DP,SP, INFO/AD) all exist in this bcftools", all(t in out for t in tags), [t for t in tags if t not in out])
rc, out, err = sh("bcftools mpileup -X list 2>&1")
print("bcftools -X presets:\n", out)
check(I, "`--max-BQ 30` is the `ont` preset value (Skill's claim for ONT R10.4+)", "max-BQ 30" in out.replace("--max-BQ", "max-BQ") and "ont" in out, out[:300])

# ---------------- G. real data: human chr22 with the Skill's germline recipe
H = HUMAN + "/test.paired_end.sorted.bam"; HR = HUMAN + "/genome.fasta"
rc, out, err = sh(f"cd {W} && bcftools mpileup -f {HR} -d 1000000 -q 20 -Q 20 -a FORMAT/AD,FORMAT/DP {H} | bcftools call -mv -Oz -o real.vcf.gz && bcftools index -t real.vcf.gz && bcftools query -f '%POS\\t%REF\\t%ALT\\t%QUAL\\t[%AD]\\n' real.vcf.gz")
print("real-data calls:\n", out)
called = {int(l.split("\t")[0]): l.split("\t") for l in out.strip().splitlines()}
# independent expectation: sites where samtools mpileup (-B -Q20 -q20) shows >=30% alt of >=10 reads (strong, non-borderline)
rc, mo, _ = sh(f"samtools mpileup -B -Q 20 -q 20 -f {HR} -r chr22:1952-4617 {H}")
exp = set(); weak = {}
for r in mpileup_rows(mo):
    if r[3] == "0": continue
    n, cc = parse_bases(r[4], r[2])
    tot = sum(cc[k] for k in "ACGTacgt") + cc["ref_fwd"] + cc["ref_rev"]
    alt = sum(cc[k] for k in "ACGTacgt") - cc[r[2]] - cc[r[2].lower()]
    if tot >= 10 and alt / tot >= 0.3:
        exp.add(int(r[1]))
    elif tot >= 10 and alt / tot >= 0.1:
        weak[int(r[1])] = (alt, tot)
print("mpileup-derived strong (>=30% alt, >=10 reads) sites:", sorted(exp), "| weak 10-30% sites (informational):", weak, "| bcftools call sites:", sorted(called))
check(I, "every strong (>=30% alt, >=10 reads) site in the independent mpileup parse is called by the Skill's bcftools recipe", exp <= set(called), f"missing {sorted(exp - set(called))}")
lowq = [(p, called[p][3]) for p in sorted(called) if float(called[p][3]) < 20]
print("QUAL<20 records emitted (Skill shows no filtering step):", lowq)
snpqual = [(p, called[p][3]) for p in sorted(called)]
summary(I)
