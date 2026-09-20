"""Input 4 checker: compare each tool's output to planted truth (synthetic). WSL env python."""
import json, pysam
R = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run"; D, W = f"{R}/data", f"{R}/out/i4"
truth = json.load(open(f"{D}/truth.json")); PL = truth["primer_len"]; amps = {a[0]: (a[1], a[2]) for a in truth["amps"]}
def exp(r, both):
    s, e = amps[r.query_name.split("_")[0]]; short = (e - s) < 100
    st, en = (s + PL, r.reference_end) if not r.is_reverse else (r.reference_start, e - PL)
    if both and short:
        if not r.is_reverse: en = e - PL
        else: st = s + PL
    return st, en
def score(path, both, label):
    n = ok = h = 0; ex = []
    with pysam.AlignmentFile(path) as f:
        for r in f.fetch(until_eof=True):
            n += 1; st, en = exp(r, both)
            if r.reference_start == st and r.reference_end == en: ok += 1
            elif len(ex) < 2: ex.append((r.query_name, r.is_reverse, r.reference_start, r.reference_end, "want", st, en, r.cigarstring))
            if "H" in (r.cigarstring or ""): h += 1
    print(f"{label:34s} n={n} exactly-matches-planted-truth={ok} ({100*ok/n:.1f}%) hardclipped={h}", ex)
score(f"{W}/hard.final.bam", False, "samtools ampliconclip --hard-clip")
score(f"{W}/soft.final.bam", True, "samtools ampliconclip --both-ends")
score(f"{W}/ivar.sorted.bam", False, "iVar trim (-q 0)")
score(f"{W}/fgbio.sorted.bam", False, "fgbio ClipBam fixed 25 bp 5'")
