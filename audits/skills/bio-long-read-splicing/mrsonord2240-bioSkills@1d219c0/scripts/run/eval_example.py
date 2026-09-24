#!/usr/bin/env python3
"""Assert on the CONTENT of the shipped example pipeline's outputs against the planted truth (data/plant), never on the exit code.
usage: eval_example.py <example OUTPUT_DIR> <platform hifi|ontunstr|drna> <sample> [label]
Checks: (1) BAM chains via pysam (eval_bam.py), (2) IsoQuant models+counts, (3) FLAIR isoforms+counts, (4) SQANTI3 categories, (5) filter output present.
Isoforms are matched to truth by exact intron chain (independent of the tools' own ids)."""
import sys, os, re, collections, math, subprocess, csv
import pysam
out, plat, sample = sys.argv[1:4]
label = sys.argv[4] if len(sys.argv) > 4 else out
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data", "plant")
truth = {}   # tx -> (gene, strand, annotated, chain tuple half-open)
for ln in list(open(D + "/truth_chains.tsv"))[1:]:
    f = ln.rstrip("\n").split("\t")
    truth[f[0]] = (f[1], f[2], int(f[3]), tuple(tuple(map(int, j.split("-"))) for j in f[4].split(";")))
chain2tx = {(v[3]): k for k, v in truth.items()}
tc = collections.Counter()
for ln in list(open(D + "/%s/truth_counts.tsv" % plat))[1:]:
    p, s, t, n = ln.rstrip("\n").split("\t")
    if s == sample: tc[t] += int(n)
def pear(a, b):
    n = len(a); ma, mb = sum(a) / n, sum(b) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a)); sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else float("nan")
def gtf_chains(path):
    ex = collections.defaultdict(list)
    for ln in open(path):
        if ln.startswith("#"): continue
        f = ln.rstrip("\n").split("\t")
        if len(f) < 9 or f[2] != "exon": continue
        t = re.search(r'transcript_id "([^"]+)"', f[8]).group(1)
        ex[t].append((int(f[3]) - 1, int(f[4])))
    res = {}
    for t, e in ex.items():
        e.sort(); res[t] = tuple((e[i][1], e[i + 1][0]) for i in range(len(e) - 1))
    return res
def bed_chains(path):
    res = {}
    for ln in open(path):
        f = ln.rstrip("\n").split("\t")
        st = int(f[1]); sizes = [int(x) for x in f[10].strip(",").split(",")]; starts = [int(x) for x in f[11].strip(",").split(",")]
        e = [(st + a, st + a + b) for a, b in zip(starts, sizes)]
        res[f[3]] = tuple((e[i][1], e[i + 1][0]) for i in range(len(e) - 1))
    return res
def report_counts(name, idchain, counts):
    got = collections.Counter(); unmatched = 0
    for i, c in counts.items():
        tx = chain2tx.get(idchain.get(i))
        if tx: got[tx] += c
        else: unmatched += c
    txs = sorted(tc); a = [tc[t] for t in txs]; b = [got.get(t, 0) for t in txs]
    keys = ["G055A", "G055B", "G056A", "G056B", "G057N", "G058N"]
    print("  %-8s isoforms matched to a truth chain: %d/%d ; reads in unmatched isoforms %d ; Pearson r(all %d truth tx) = %.4f ; total counted %d of %d truth reads" % (
        name, len({chain2tx.get(v) for v in idchain.values()} - {None}), len(idchain), unmatched, len(txs), pear(a, b), sum(got.values()), sum(tc.values())))
    print("  %-8s microexon/novel genes  truth->counted: %s" % (name, "  ".join("%s %d->%d" % (k, tc.get(k, 0), got.get(k, 0)) for k in keys)))
    return got
print("======== %s  (platform %s, sample %s)" % (label, plat, sample))
# 1 BAM
bam = [f for f in os.listdir(out) if f.endswith("_aligned.bam")][0]
print(subprocess.run([sys.executable, HERE + "/eval_bam.py", os.path.join(out, bam), D + "/truth_chains.tsv", "  BAM " + bam], capture_output=True, text=True).stdout.strip())
# 2 IsoQuant
iq = os.path.join(out, "isoquant", sample)
idc = gtf_chains(os.path.join(iq, sample + ".transcript_models.gtf"))
cnt = {}
for fn in (sample + ".transcript_counts.tsv", sample + ".discovered_transcript_counts.tsv"):
    p = os.path.join(iq, fn)
    if os.path.exists(p):
        for ln in open(p):
            if ln.startswith("#") or ln.startswith("feature_id"): continue
            a, b = ln.rstrip("\n").split("\t")[:2]; cnt[a] = float(b)   # discovered_* repeats ids already in transcript_counts: replace, never add
amb = {k: v for k, v in cnt.items() if k.startswith("__")}
cnt = {k: v for k, v in cnt.items() if not k.startswith("__")}
print("  IsoQuant models %d, counted features %d, __ rows %s" % (len(idc), len(cnt), amb))
report_counts("IsoQuant", idc, cnt)
# 3 FLAIR
fb = os.path.join(out, "flair_collapsed_%s.isoforms.bed" % sample)
fc = bed_chains(fb)
fcnt = {}
for ln in open(os.path.join(out, "flair_collapsed_%s.isoform.counts.txt" % sample)):
    a, b = ln.rstrip("\n").split("\t")[:2]; fcnt[a] = float(b)
print("  FLAIR isoforms %d" % len(fc))
report_counts("FLAIR", fc, fcnt)
# 4 SQANTI3
cl = list(csv.DictReader(open(os.path.join(out, "sqanti3", "sqanti3_classification.txt")), delimiter="\t"))
cat = collections.Counter(r["structural_category"] for r in cl)
print("  SQANTI3 categories (IsoQuant models):", dict(cat))
for r in cl:
    tx = chain2tx.get(idc.get(r["isoform"]))
    if tx in ("G057N", "G058N"):
        print("    novel truth isoform %s -> IsoQuant model %s -> SQANTI3 %s (%s)" % (tx, r["isoform"], r["structural_category"], r.get("subcategory")))
# 5 filter
pa = os.path.join(out, "sqanti3_filtered", "sqanti3_filtered_pass_isoforms.txt")
fg = os.path.join(out, "sqanti3_filtered", "sqanti3_filtered.filtered.gtf")
print("  filter: pass_isoforms %d lines, filtered.gtf %d lines" % (sum(1 for _ in open(pa)), sum(1 for _ in open(fg))))
