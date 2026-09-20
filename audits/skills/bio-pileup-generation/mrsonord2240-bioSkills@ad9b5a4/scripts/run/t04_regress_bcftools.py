#!/usr/bin/env python3
"""Input 4 (Variant B, REGRESSION of pre-fix input 4): bcftools mpileup | bcftools call — single sample, BCF intermediate, multi-sample
joint calling (the CHANGED -d 100000 example), parallel-by-contig (the REWRITTEN block), and the corrected explanation of why
`samtools mpileup | bcftools call` fails. Bash blocks are extracted VERBATIM from the copied SKILL.md; only file names are substituted.
Truth = planted synthetic events (data/truth.json) and per-sample AD."""
import json, os, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

I = 4
W = WORK + "/t04"
os.makedirs(W, exist_ok=True)
SK = open(SKILL + "/SKILL.md", encoding="utf-8").read()
T = json.load(open(DATA + "/truth.json"))["truth"]["events"]
snp = T["snp"]
blocks = re.findall(r"```bash\n(.*?)```", SK, flags=re.S)


def blk(needle):
    hits = [b for b in blocks if needle in b]
    assert len(hits) >= 1, needle
    return hits[0]


def vcf(path):
    rc, out, err = sh(f"bcftools view -H {path}")
    return [dict(chrom=f[0], pos=int(f[1]), ref=f[3], alt=f[4], qual=f[5], info=f[7], fmt=f[8] if len(f) > 8 else "", samples=f[9:]) for f in (l.split("\t") for l in out.splitlines())]


def run_block(text, subs, cwd=W, script="blk.sh"):
    for a, b in subs.items():
        text = text.replace(a, b)
    open(f"{cwd}/{script}", "w", newline="\n").write("#!/bin/bash\ncd " + cwd + "\n" + text)
    return sh(f"bash {cwd}/{script}")


# A. Modern Germline Calling (verbatim)
b = blk("bcftools mpileup -f reference.fa -d 1000000 -q 20 -Q 20 \\\n    --annotate")
sh(f"rm -f {W}/variants.vcf.gz*")
rc, out, err = run_block(b, {"reference.fa": SYNREF, "input.bam": SYN})
check(I, "Modern Germline Calling block runs (verbatim) and writes variants.vcf.gz + .tbi", rc == 0 and os.path.exists(W + "/variants.vcf.gz") and os.path.exists(W + "/variants.vcf.gz.tbi"), f"rc={rc} {err.strip()[-120:]}")
recs = vcf(W + "/variants.vcf.gz")
print([(r["pos"], r["ref"], r["alt"], r["qual"]) for r in recs])
s = [r for r in recs if r["pos"] == 100]
d = dict(zip(s[0]["fmt"].split(":"), s[0]["samples"][0].split(":"))) if s else {}
check(I, "planted SNP synA:100 T>C called with FORMAT/AD 30,10 and FORMAT/DP 40 (planted truth), INFO/AD present", bool(s) and s[0]["ref"] == "T" and s[0]["alt"] == "C" and d.get("AD") == "30,10" and d.get("DP") == "40" and "AD=" in s[0]["info"] and "SP" in d, d)
check(I, "planted 2 bp insertion (AA>AACA at 200) and 3 bp deletion (TCGT>T at 250) are called (default BAQ + -Q 20)",
      any(r["pos"] == 200 and r["ref"] == "AA" and r["alt"] == "AACA" for r in recs) and any(r["pos"] == 250 and r["ref"] == "TCGT" and r["alt"] == "T" for r in recs), [(r["pos"], r["ref"], r["alt"]) for r in recs])
check(I, "no unexplained records (only SNP 100, ins 200, del 250, overlap-conflict site 930)", {r["pos"] for r in recs} == {100, 200, 250, 930}, [r["pos"] for r in recs])
# B. BCF intermediate (verbatim)
b = blk("-Ob -o raw.bcf")
rc, out, err = run_block(b, {"reference.fa": SYNREF, "input.bam": SYN})
r2 = vcf(W + "/variants.vcf")
check(I, "BCF Intermediate block runs; raw.bcf non-empty; calling from it gives the planted SNP/ins/del", rc == 0 and os.path.getsize(W + "/raw.bcf") > 0 and {100, 200, 250} <= {r["pos"] for r in r2}, f"rc={rc} calls={[r['pos'] for r in r2]}")
# C. multi-sample joint calling (verbatim, s3.bam absent -> two samples)
b = blk("s1.bam s2.bam s3.bam")
rc, out, err = run_block(b, {"reference.fa": SYNREF, "s1.bam s2.bam s3.bam": f"{DATA}/s1.bam {DATA}/s2.bam"})
sn = sh(f"bcftools query -l {W}/joint.vcf.gz")[1].split()
q = sh(f"bcftools query -f '%POS [%AD|]\\n' {W}/joint.vcf.gz")[1]
check(I, "Multi-Sample block (-d 100000, --threads 4) runs; samples s1,s2 from @RG SM; per-sample AD == planted (17,3 | 8,12)", rc == 0 and sn == ["s1", "s2"] and "100 17,3|8,12|" in q, f"rc={rc} samples={sn} AD={q.strip()}")
check(I, "no 'Potential memory hog' warning with the Skill's -d 100000 and 2 samples", "memory hog" not in err.lower() and "-d 100000" in err, err.strip()[-200:])
rc, out, err = sh(f"bcftools mpileup -f {SYNREF} --threads 4 -d 1000000 -a FORMAT/AD,FORMAT/DP {DATA}/s1.bam {DATA}/s2.bam 2>&1 >/dev/null | grep -i -E 'memory|Max|maximum'")
check(I, "Skill claim reproduced: -d 1000000 with 2 samples makes bcftools 1.24 warn 'Potential memory hog'", "memory hog" in out, out.strip())
rc, out, err = sh(f"bcftools mpileup -f {SYNREF} -d 1000000 -a FORMAT/DP {DATA}/s1.bam 2>&1 >/dev/null | grep -i -E 'memory|Max|maximum'")
check(I, "control: -d 1000000 with ONE sample gives no memory warning (Skill's single-sample blocks use -d 1000000)", "memory hog" not in out, out.strip())
rc, out, err = sh(f"bcftools mpileup -f {SYNREF} -d 100000 -a FORMAT/DP {DATA}/s1.bam {DATA}/s2.bam {DATA}/s1.bam {DATA}/s2.bam {DATA}/s1.bam 2>&1 >/dev/null | grep -i -E 'memory|Max|maximum'")
print("5 files at -d 100000:", out.strip()[:200])
rc, out, err = sh(f"bcftools mpileup -f {SYNREF} -d 100000 -a FORMAT/DP " + " ".join([f"{DATA}/s1.bam"] * 11) + " 2>&1 >/dev/null | grep -i -E 'memory|Max|maximum'")
print("11 files at -d 100000 (threshold check):", out.strip()[:200])
# D. WRONG pipe explanation (block extracted verbatim)
b = blk("WRONG -- samtools mpileup writes text")
check(I, "Maximum Depth block text: the WRONG comment now says text pileup is not VCF/BCF and quotes the real error; no 'double cap' rationale remains",
      "Failed to read from standard input: unknown file type" in b and "double" not in SK.lower().split("maximum depth")[1][:2500], b.split("\n")[6:9] if len(b.split("\n")) > 8 else b[:200])
rc, out, err = sh(f"bash -c 'set -o pipefail; samtools mpileup -f {SYNREF} {SYN} 2>/dev/null | bcftools call -mv 2>&1 | head -3; echo status=${{PIPESTATUS[*]}}'")
check(I, "Skill's stated error text is what bcftools 1.24 prints for the WRONG pipe and the exit status is non-zero (255)", "Failed to read from standard input: unknown file type" in out and "0 255" in out.replace("status=", ""), out.strip()[-160:])
rc, out, err = sh(f"samtools mpileup -f {SYNREF} {SYN} 2>/dev/null | bcftools call -mv > /dev/null 2>&1; echo rc=$?")
check(I, "without pipefail the pipeline's exit status is that of bcftools call: 255 (agents should not treat the pipe as success)", "rc=255" in out, out.strip())
rc, out, err = sh(f"bcftools mpileup -f {SYNREF} -d 1000000 {SYN} 2>/dev/null | bcftools call -mv 2>/dev/null | grep -vc '^#'")
check(I, "RIGHT pipe (bcftools mpileup -d 1000000 | call) returns 4 records", out.strip() == "4", out.strip())
# E. Parallel by contig block, verbatim
b = blk("xargs -a contigs.txt")
PW = W + "/par"
sh(f"rm -rf {PW}; mkdir -p {PW}")
rc, out, err = run_block(b, {"reference.fa": DATA + "/multi.fa", "input.bam": DATA + "/multi.bam"}, cwd=PW)
order = sh(f"bcftools view -H {PW}/all.vcf.gz | cut -f1")[1].split()
hdr = sh(f"bcftools view -h {PW}/all.vcf.gz | grep '^##contig' | sed 's/.*ID=\\([^,>]*\\).*/\\1/'")[1].split()
truth_order = [f"chr{i}" for i in range(1, 12)]
check(I, "Parallel-by-Contig block (verbatim): all.vcf.gz has 11 records in HEADER contig order chr1..chr11 (glob order would be chr1,chr10,chr11,chr2...)", rc == 0 and order == truth_order and hdr == truth_order, f"rc={rc} records={order}")
check(I, "Parallel block builds the index and every record is the planted pos-100 SNP", os.path.exists(PW + "/all.vcf.gz.csi") and all(x == "100" for x in sh(f"bcftools view -H {PW}/all.vcf.gz | cut -f2")[1].split()), os.listdir(PW)[:8] if os.path.isdir(PW) else "")
# failure propagation: nonexistent reference
PW2 = W + "/par_fail"
sh(f"rm -rf {PW2}; mkdir -p {PW2}")
rc, out, err = run_block(b, {"reference.fa": DATA + "/does_not_exist.fa", "input.bam": DATA + "/multi.bam"}, cwd=PW2)
check(I, "Parallel block with a missing reference: non-zero exit and no all.vcf.gz (failure not swallowed)", rc != 0 and not os.path.exists(PW2 + "/all.vcf.gz"), f"rc={rc} files={os.listdir(PW2)[:5]}")
# a partial failure: one contig with a bad region -> concat must not run
PW3 = W + "/par_partial"
sh(f"rm -rf {PW3}; mkdir -p {PW3}")
sh(f"printf 'chr1\\nchr2\\nnosuchcontig\\n' > {PW3}/contigs_bad.txt")
b_bad = b.replace("samtools idxstats input.bam | cut -f1 | grep -v '^\\*$' > contigs.txt", "cp contigs_bad.txt contigs.txt")
assert b_bad != b
rc, out, err = run_block(b_bad, {"reference.fa": DATA + "/multi.fa", "input.bam": DATA + "/multi.bam"}, cwd=PW3)
check(I, "Parallel block with one bad contig: xargs exits non-zero and concat is skipped (no all.vcf.gz)", rc != 0 and not os.path.exists(PW3 + "/all.vcf.gz"), f"rc={rc} files={sorted(os.listdir(PW3))}")
# on syn.bam (3 contigs, one read-less)
PW4 = W + "/par_syn"
sh(f"rm -rf {PW4}; mkdir -p {PW4}")
rc, out, err = run_block(b, {"reference.fa": SYNREF, "input.bam": SYN}, cwd=PW4)
rec4 = sh(f"bcftools view -H {PW4}/all.vcf.gz | cut -f1,2")[1].split()
check(I, "Parallel block on the 3-contig synthetic BAM (one contig without reads) still completes and finds the planted SNP", rc == 0 and "100" in rec4, f"rc={rc} {rec4[:8]} {err.strip()[-100:]}")
# F. flags/tags/presets named in the Skill
rc, out, err = sh("bcftools mpileup -a '?' 2>&1 | head -40")
check(I, "annotate tags named in the Skill (FORMAT/AD,DP,SP, INFO/AD) exist in bcftools 1.24", all(t in out for t in ("FORMAT/AD", "FORMAT/DP", "FORMAT/SP", "INFO/AD")), out[:100])
rc, out, err = sh("bcftools mpileup -X list 2>&1")
check(I, "`--max-BQ 30` is the `ont` preset value (Skill's ONT cheat-sheet note)", re.search(r"\nont\n\s+-B -Q5 --max-BQ 30", out) is not None and "`--max-BQ 30`" in SK, repr(out[out.index("\nont\n"):][:40]))
# G. real data
H, HR = HBAM, HREF
rc, out, err = sh(f"cd {W} && bcftools mpileup -f {HR} -d 1000000 -q 20 -Q 20 -a FORMAT/AD,FORMAT/DP {H} | bcftools call -mv -Oz -o real.vcf.gz && bcftools index -t real.vcf.gz && bcftools query -f '%POS\\t%REF\\t%ALT\\t%QUAL\\t[%AD]\\n' real.vcf.gz")
called = {int(l.split("\t")[0]): l.split("\t") for l in out.strip().splitlines()}
rc, mo, _ = sh(f"samtools mpileup -B -Q 20 -q 20 -f {HR} -r chr22:1952-4617 {H}")
exp = set()
for r in mpileup_rows(mo):
    if r[3] == "0":
        continue
    n, cc = parse_bases(r[4], r[2])
    alt = sum(cc[k] for k in "ACGTacgt") - cc[r[2]] - cc[r[2].lower()]
    tot = sum(cc[k] for k in "ACGTacgt") + cc["ref_fwd"] + cc["ref_rev"]
    if tot >= 10 and alt / tot >= 0.3:
        exp.add(int(r[1]))
print("bcftools calls on real slice:", sorted(called), "| independent strong sites:", sorted(exp))
check(I, "real chr22 slice: every strong (>=30% alt, >=10 reads) site of the independent mpileup parse is called by the Skill's germline recipe", exp <= set(called) and len(called) > 0, f"missing {sorted(exp - set(called))}")
sh(f"rm -f {W}/*.vcf.gz* {W}/raw.bcf {W}/variants.vcf")
summary(I)
