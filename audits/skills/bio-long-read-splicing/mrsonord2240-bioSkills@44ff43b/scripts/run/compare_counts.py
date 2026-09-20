#!/usr/bin/env python3
"""Compare a tool's isoform models + counts against PLANTED truth (synthetic data).
Isoforms are matched by exact intron chain (independent of the tool's IDs).
Usage: compare_counts.py <models.gtf|models.bed> <counts.tsv> <truth_counts.tsv> <read_tx.gtf> [--flair-ids]
  counts.tsv: first column = isoform id, remaining columns = samples (header row); sample names are matched to truth by prefix
  (FLAIR names 'ctrl1_ctrl_b1' -> ctrl1). Prints per-truth-isoform: truth total, matched model id, observed total, and models with no truth.
"""
import sys, re, collections

models, counts, truth, txgtf = sys.argv[1:5]


def chains_from_gtf(path):
    ex = collections.defaultdict(list)
    st = {}
    for ln in open(path):
        if ln.startswith("#"):
            continue
        f = ln.rstrip("\n").split("\t")
        if len(f) < 9 or f[2] != "exon":
            continue
        m = re.search(r'transcript_id "([^"]+)"', f[8])
        ex[m.group(1)].append((int(f[3]) - 1, int(f[4])))
        st[m.group(1)] = (f[0], f[6])
    out = {}
    for t, e in ex.items():
        e.sort()
        out[t] = (st[t][0], st[t][1], tuple((e[i][1], e[i + 1][0]) for i in range(len(e) - 1)), e[0][0], e[-1][1])
    return out


def chains_from_bed(path):
    out = {}
    for ln in open(path):
        f = ln.rstrip("\n").split("\t")
        if len(f) < 12:
            continue
        s = int(f[1])
        sizes = [int(x) for x in f[10].strip(",").split(",")]
        starts = [int(x) for x in f[11].strip(",").split(",")]
        ex = [(s + a, s + a + b) for a, b in zip(starts, sizes)]
        out[f[3]] = (f[0], f[5], tuple((ex[i][1], ex[i + 1][0]) for i in range(len(ex) - 1)), ex[0][0], ex[-1][1])
    return out


mod = chains_from_bed(models) if models.endswith(".bed") else chains_from_gtf(models)
tr = chains_from_gtf(txgtf)
tr_by_chain = {}
for t, (c, s, ch, a, b) in tr.items():
    tr_by_chain[(c, s, ch)] = t.replace(".", "")

# truth totals
tt = collections.Counter()
samples = []
for ln in list(open(truth))[1:]:
    s, t, n = ln.split()
    tt[(s, t.replace(".", ""))] += int(n)
    if s not in samples:
        samples.append(s)

# observed counts
rows = [ln.rstrip("\n").split("\t") for ln in open(counts) if not ln.startswith("#")]
hdr = rows[0]
obs = {}
colsamp = []
for h in hdr[1:]:
    colsamp.append(next((s for s in samples if h.startswith(s)), h))
for r in rows[1:]:
    try:
        obs[r[0]] = {colsamp[i]: float(r[i + 1]) for i in range(len(colsamp))}
    except ValueError:
        pass

match = collections.defaultdict(list)
unmatched = []
for mid, (c, s, ch, a, b) in mod.items():
    key = (c, s, ch)
    if key in tr_by_chain:
        match[tr_by_chain[key]].append(mid)
    else:
        unmatched.append((mid, ch))

print("%-8s %10s %10s %8s  %s" % ("truth_tx", "truth_n", "observed_n", "err%", "matched model id(s)"))
tot_truth = tot_abs = 0
for t in sorted({k[1] for k in tt}):
    tn = sum(v for (s, tx), v in tt.items() if tx == t)
    ids = match.get(t, [])
    on = sum(obs.get(i, {}).get(s, 0) for i in ids for s in samples)
    err = 100 * (on - tn) / tn if tn else float("nan")
    tot_truth += tn
    tot_abs += abs(on - tn)
    print("%-8s %10d %10.0f %+7.1f%%  %s" % (t, tn, on, err, ",".join(ids) if ids else "(NOT REPORTED)"))
print("total truth reads %d ; sum |observed-truth| per isoform %d (%.1f%% of reads misassigned or missing)" % (tot_truth, tot_abs, 100 * tot_abs / tot_truth))
print("models with intron chain absent from truth (%d): %s" % (len(unmatched), "; ".join("%s(%d introns)" % (m, len(c)) for m, c in unmatched[:10])))
