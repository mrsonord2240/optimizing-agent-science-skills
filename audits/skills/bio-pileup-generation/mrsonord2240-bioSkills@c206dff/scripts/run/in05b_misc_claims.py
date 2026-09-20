#!/usr/bin/env python3
"""Input 5 supplement: remaining checkable claims in SKILL.md (BAQ cost, -E, --output-QNAME which the Skill omits)."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

I = 5
G1K = AFDATA + "/1000g/HG00349.chr20_1400000-1500000.bam"; G1KREF = AFDATA + "/1000g/chr20_padded_1500000.fa"
def timed(opts, reps=3):
    ts = []
    for _ in range(reps):
        t = time.time()
        rc, out, err = sh(f"samtools mpileup -f {G1KREF} {opts} -r chr20:1400001-1500000 {G1K} > /dev/null")
        ts.append(time.time() - t)
    return min(ts)
tb = timed(""); tn = timed("-B")
print(f"samtools mpileup default (BAQ) {tb:.2f}s vs -B {tn:.2f}s -> BAQ overhead {(tb/tn-1)*100:.0f}%")
check(I, "SKILL 'BAQ ... ~30% slower': measured overhead of default BAQ vs -B on 100 kb of 1000G is within 15-60%", 0.15 <= tb / tn - 1 <= 0.60, f"{(tb/tn-1)*100:.0f}% ({tb:.2f}s vs {tn:.2f}s, best of 3)")
rc, out, err = sh(f"samtools mpileup -f {G1KREF} -E -r chr20:1400001-1400100 {G1K} | head -2")
check(I, "-E / --redo-BAQ accepted", rc == 0 and out.startswith("chr20"), (out + err)[:80])
rc, out, err = sh(f"samtools mpileup -f {G1KREF} --no-BAQ -r chr20:1400001-1400100 {G1K} | head -2")
check(I, "--no-BAQ long form accepted", "invalid" not in err.lower() and out.startswith("chr20"), (out + err)[:80])
rc, out, err = sh(f"samtools mpileup -f {G1KREF} -B -E -r chr20:1400001-1400100 {G1K}")
check(I, "-B and -E together are rejected (Skill table lists both without saying they are exclusive)", rc != 0 and "cannot be combined" in (out + err), (out + err).strip()[:80])
H = HUMAN + "/test.paired_end.sorted.bam"; HR = HUMAN + "/genome.fasta"
def timed_h(opts, reps=3):
    ts = []
    for _ in range(reps):
        t = time.time(); sh(f"samtools mpileup -f {HR} {opts} -r chr22:1952-4617 {H} > /dev/null"); ts.append(time.time() - t)
    return min(ts)
hb, hn = timed_h(""), timed_h("-B")
print(f"human deep slice: default {hb:.2f}s vs -B {hn:.2f}s -> {(hb/hn-1)*100:.0f}% overhead")
rc, out, err = sh(f"samtools mpileup -f {G1KREF} --output-QNAME -s -r chr20:1400300-1400300 {G1K}")
r = mpileup_rows(out)
print("--output-QNAME -s columns:", [len(x) for x in r], r[0][:5] if r else None)
check(I, "undocumented-in-Skill options work: `--output-QNAME` adds read-name column with one name per read, `-s` adds MAPQ column", bool(r) and len(r[0]) == 8 and len(r[0][7].split(",")) == int(r[0][3]), f"cols={len(r[0]) if r else 0}")
json.dump([c for c in CHECKS if c[0] == I], open(os.path.join(RUN, "checks_in5b.json"), "w"), indent=1)
