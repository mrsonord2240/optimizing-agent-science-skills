"""Input 7 (NEW): does examples/check_primer_residual.py detect planted residual primers, and does it false-positive / false-negative?
SYNTHETIC BAMs built here with pysam from data/synth.fa (contig amp1). Primers (data/synth_primers.bed, 6 col, 0-based half-open):
  A1_LEFT amp1 100-125 +   A1_RIGHT 325-350 -   A2_LEFT 300-325 +   A2_RIGHT 525-550 -   ...
Each case: build a BAM, run the shipped checker in a subprocess, record rc + stdout, compare to the expected rc AND expected counts.
cwd = out/i7 ; checker path = argv[1]. WSL env python."""
import subprocess, sys, os, pysam
CK = sys.argv[1]; D = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/data"
ref = pysam.FastaFile(f"{D}/synth.fa").fetch("amp1")
HDR = {"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "amp1", "LN": len(ref)}, {"SN": "other", "LN": 500}]}
def mk(path, reads):
    """reads: list of (name, start0, cigartuples, is_reverse, extra flags, contig id)"""
    recs = []
    for name, start, cig, rev, flagx, tid in reads:
        a = pysam.AlignedSegment(); a.query_name = name; a.reference_id = tid; a.reference_start = start
        qlen = sum(l for op, l in cig if op in (0, 1, 4)); a.flag = (16 if rev else 0) | flagx
        a.mapping_quality = 60; a.cigartuples = cig
        a.query_sequence = (ref * 2)[start:start + qlen] if qlen else ""; a.query_qualities = pysam.qualitystring_to_array("I" * qlen)
        recs.append(a)
    recs.sort(key=lambda a: (a.reference_id, a.reference_start))
    with pysam.AlignmentFile(path, "wb", header=HDR) as o:
        for a in recs: o.write(a)
def run(bam, bed, extra=()):
    p = subprocess.run([sys.executable, CK, bam, bed, *extra], capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip().replace("\n", " | ")
M = lambda n: [(0, n)]
rows = []
def case(label, reads, extra, want_rc, want_5=None, want_3=None, bed=f"{D}/synth_primers.bed"):
    bam = f"case_{len(rows):02d}.bam"; mk(bam, reads)
    rc, out = run(bam, bed, extra)
    import re
    m = re.search(r"5' end inside a primer=(\d+).*3' end inside a primer=(\d+)", out)
    g5, g3 = (int(m.group(1)), int(m.group(2))) if m else (None, None)
    ok = rc == want_rc and (want_5 is None or g5 == want_5) and (want_3 is None or g3 == want_3)
    rows.append((label, ok)); print(f"[{'PASS' if ok else 'FAIL'}] {label}: rc={rc} (want {want_rc}) 5'={g5} 3'={g3} (want {want_5}/{want_3})  <{out[:140]}>")
# A2_LEFT '+' [300,325); A1_RIGHT '-' [325,350)
case("clean: fwd read starts at primer END (325) - not residual", [("r", 325, M(50), False, 0, 0)], (), 0, 0, 0)
case("planted 5' residual: fwd read starts INSIDE '+' primer at 310", [("r", 310, M(50), False, 0, 0)], (), 1, 1, 0)
case("boundary: fwd read starts at primer START (300) -> 5' residual (its 3' end also lands in the '-' primer)", [("r", 300, M(50), False, 0, 0)], (), 1, 1, 1)
case("boundary: fwd read starts at last primer base (324) -> residual", [("r", 324, M(50), False, 0, 0)], (), 1, 1, 0)
case("boundary: fwd read starts one past primer (325) -> clean", [("r", 325, M(50), False, 0, 0)], (), 0, 0, 0)
case("planted 5' residual on a REVERSE read: read ends inside '-' primer (end=340)", [("r", 290, M(50), True, 0, 0)], (), 1, 1, 0)
case("reverse read ending exactly at primer start (325) - clean", [("r", 275, M(50), True, 0, 0)], (), 0, 0, 0)
case("planted 3' residual, --three-prime given: fwd read ends inside '-' primer (ends 340)", [("r", 250, M(90), False, 0, 0)], ("--three-prime",), 1, 0, 1)
case("same read WITHOUT --three-prime: rc 0, 3' reported but not enforced", [("r", 250, M(90), False, 0, 0)], (), 0, 0, 1)
case("soft-clipped primer: 25S45M starting at 325 - clean", [("r", 325, [(4, 25), (0, 45)], False, 0, 0)], (), 0, 0, 0)
case("hard-clipped primer: 25H45M starting at 325 - clean", [("r", 325, [(5, 25), (0, 45)], False, 0, 0)], (), 0, 0, 0)
case("soft clip but aligned start still in primer: 5S45M at 310 -> residual", [("r", 310, [(4, 5), (0, 45)], False, 0, 0)], (), 1, 1, 0)
case("read on a contig with no BED primers ('other') - ignored", [("r", 310, M(50), False, 0, 1)], (), 0, 0, 0)
case("secondary alignment inside primer is counted", [("r", 310, M(50), False, 256, 0)], (), 1, 1, 0)
case("unmapped-only BAM -> rc 2 'no mapped reads'", [("r", 0, [], False, 4, 0)], (), 2)
case("wrong-strand primer: fwd read starts in '-' primer (335) is NOT a 5' residual", [("r", 335, M(50), False, 0, 0)], (), 0, 0, 0)
# false negatives (documented limits)
case("FALSE-NEGATIVE PROBE: fwd read starts 3 bp UPSTREAM of the primer (297) and runs through it - primer bases remain",
     [("r", 297, M(60), False, 0, 0)], (), 0, 0, 0)
# bad BED input exit codes
open("b5.bed", "w").write("amp1\t300\t325\tA2_LEFT\t+\n")
bam = "case_bed.bam"; mk(bam, [("r", 325, M(50), False, 0, 0)])
rc, out = run(bam, "b5.bed"); print(f"[{'PASS' if rc == 2 else 'FAIL'}] 5-col BED: rc={rc} (docstring says 'exit 2 on bad input') <{out[:120]}>"); rows.append(("5-col BED exit code 2", rc == 2))
rc, out = run(bam, "nonexistent.bed"); print(f"[{'PASS' if rc == 2 else 'FAIL'}] missing BED: rc={rc} <{out[-100:]}>"); rows.append(("missing BED exit code 2", rc == 2))
rc, out = run("nonexistent.bam", f"{D}/synth_primers.bed"); print(f"[{'PASS' if rc == 2 else 'FAIL'}] missing BAM: rc={rc} <{out[-100:]}>"); rows.append(("missing BAM exit code 2", rc == 2))
p = subprocess.run([sys.executable, CK, bam], capture_output=True, text=True); print(f"usage (no BED): rc={p.returncode}")
print(f"\n{sum(ok for _, ok in rows)}/{len(rows)} expectations met"); [print("  UNMET:", l) for l, ok in rows if not ok]
