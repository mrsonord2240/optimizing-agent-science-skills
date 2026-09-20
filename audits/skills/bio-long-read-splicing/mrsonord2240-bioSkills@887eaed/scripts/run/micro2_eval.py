#!/usr/bin/env python3
"""Two-way microexon check on data/micro2 (gen_micro2.py). For each gene: inclusion reads that carry EVERY intron of the 'inc' chain (all flanking
junctions of all microexons) / N, skipping reads whose introns equal the skip chain exactly / N, from the pysam CIGAR (N operations).
Also counts primary spliced alignments with an intron directly next to a soft clip ('dangling', the SKILL's awk done in pysam).
usage: micro2_eval.py bam truth_chains.tsv label [tsv_out_append]
prints one summary line; --genes prints the per-gene table."""
import sys, collections, pysam
bam, truth, label = sys.argv[1:4]
full = "--genes" in sys.argv
ch, mlen = {}, {}
for ln in list(open(truth))[1:]:
    f = ln.rstrip("\n").split("\t"); ch[f[0]] = tuple(tuple(map(int, j.split("-"))) for j in f[4].split(";")); mlen[f[0][:-3] if f[0].endswith("inc") else f[0][:-4]] = f[5] if f[0].endswith("inc") else mlen.get(f[0][:-4], "")
inc, skip, n_inc, n_skip = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
dang = tot = unm = 0
for r in pysam.AlignmentFile(bam).fetch(until_eof=True):
    if r.is_secondary or r.is_supplementary: continue
    tx = r.query_name.split("_")[1]; g = tx[:-3] if tx.endswith("inc") else tx[:-4]
    (n_inc if tx.endswith("inc") else n_skip)[g] += 1
    if r.is_unmapped: unm += 1; continue
    tot += 1
    cig = r.cigartuples
    if any(op == 3 for op, _ in cig) and ((cig[-1][0] == 4 and len(cig) > 1 and cig[-2][0] == 3) or (cig[0][0] == 4 and len(cig) > 1 and cig[1][0] == 3)): dang += 1
    pos = r.reference_start; obs = []
    for op, ln in cig:
        if op == 3: obs.append((pos, pos + ln)); pos += ln
        elif op in (0, 2, 7, 8): pos += ln
    obs = tuple(obs)
    if tx.endswith("inc"):
        if all(j in obs for j in ch[tx]): inc[g] += 1
    else:
        if obs == ch[tx]: skip[g] += 1
gs = sorted(n_inc, key=lambda x: (x[0] != "M", x))
pi = {g: 100.0 * inc[g] / n_inc[g] for g in gs}; ps = {g: 100.0 * skip[g] / n_skip[g] for g in gs}
if full:
    for g in gs: print("  %-4s micro %-6s inc %5.1f%%  skip %5.1f%%" % (g, mlen[g], pi[g], ps[g]))
sel = [g for g in gs if g.startswith("M")]       # 12 single-microexon genes for the means (tandem genes T1/T2 reported apart)
print("%-34s inc mean %5.1f min %5.1f (#<90: %2d/12) | skip mean %5.1f min %5.1f (#<90: %2d/12) | T1 %.0f/%.0f T2 %.0f/%.0f | dangling %d of %d aligned, unmapped %d" % (
    label, sum(pi[g] for g in sel) / len(sel), min(pi[g] for g in sel), sum(pi[g] < 90 for g in sel),
    sum(ps[g] for g in sel) / len(sel), min(ps[g] for g in sel), sum(ps[g] < 90 for g in sel),
    pi["T1"], ps["T1"], pi["T2"], ps["T2"], dang, tot, unm))
