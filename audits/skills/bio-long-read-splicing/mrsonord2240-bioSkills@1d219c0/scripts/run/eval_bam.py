#!/usr/bin/env python3
"""Second method (pysam CIGAR N operations, independent of minimap2/FLAIR/IsoQuant output files).

Usage: eval_bam.py <bam> <truth_chains.tsv> [label] [--json out.json]
Read name = <sample>_<TX>_<n>. For every PRIMARY alignment compare the intron chain with the planted truth:
  exact       observed chain == truth chain of the read's own transcript
  consistent  observed chain is a contiguous sub-chain of the truth chain (5'-truncated reads) - includes exact; unspliced reads not counted
  false_junc  read carries >=1 junction that is in NO truth transcript of the annotation (incl. the novel isoforms)
  ts_plus     fraction of spliced reads with minimap2 tag ts:A:+ (orientation check from SKILL.md)
  micro       (truth column 6 'micro_idx' = i,j chain indices flanking a microexon): fraction of that transcript's reads whose chain carries both
"""
import sys, collections, json
import pysam

bam, truth = sys.argv[1], sys.argv[2]
label = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else bam
jout = None
if "--json" in sys.argv:
    jout = sys.argv[sys.argv.index("--json") + 1]

chains, micro = {}, {}
alljn = set()
for ln in list(open(truth))[1:]:
    f = ln.rstrip("\n").split("\t")
    tx, ch = f[0], f[4]
    c = tuple(tuple(int(x) for x in j.split("-")) for j in ch.split(";")) if ch else ()
    # truth is stored half-open 0-based (first intron base, first base of the next exon), the same as pysam reference_start + N length
    chains[tx] = c
    alljn.update(c)
    if len(f) > 5 and f[5]:
        micro[tx] = tuple(int(x) for x in f[5].split(","))

def is_sub(obs, full):
    if not obs:
        return False
    n = len(obs)
    return any(full[i:i + n] == obs for i in range(len(full) - n + 1))

st = collections.Counter()
per_tx = collections.defaultdict(collections.Counter)
sf = pysam.AlignmentFile(bam, "rb")
for r in sf.fetch(until_eof=True):
    if r.is_secondary or r.is_supplementary:
        continue
    st["reads"] += 1
    if r.is_unmapped:
        st["unmapped"] += 1
        continue
    st["mapped"] += 1
    tx = r.query_name.split("_")[1]
    obs, pos = [], r.reference_start
    for op, ln in r.cigartuples:
        if op == 3:
            obs.append((pos, pos + ln)); pos += ln
        elif op in (0, 2, 7, 8):
            pos += ln
    obs = tuple(obs)
    if obs:
        st["spliced"] += 1
        try:
            if r.get_tag("ts") == "+":
                st["ts_plus"] += 1
            st["ts_tagged"] += 1
        except KeyError:
            pass
    fj = any(j not in alljn for j in obs)
    if fj:
        st["false_junc"] += 1
    full = chains.get(tx)
    if full is None:
        continue
    if obs == full:
        st["exact"] += 1
    if is_sub(obs, full) or obs == full:
        st["consistent"] += 1
    if tx in micro:
        st["micro_reads"] += 1
        i, j = micro[tx]
        if full[i] in obs and full[j] in obs:
            st["micro_kept"] += 1
            per_tx[tx]["kept"] += 1
        per_tx[tx]["n"] += 1
m = max(st["mapped"], 1)
out = dict(label=label, reads=st["reads"], mapped=st["mapped"], spliced=st["spliced"],
           exact_pct=round(100 * st["exact"] / m, 1), consistent_pct=round(100 * st["consistent"] / m, 1),
           false_junc_pct=round(100 * st["false_junc"] / m, 1),
           ts_plus_frac=round(st["ts_plus"] / st["ts_tagged"], 3) if st["ts_tagged"] else None,
           micro_kept=st["micro_kept"], micro_reads=st["micro_reads"], micro_per_tx={k: dict(v) for k, v in per_tx.items()})
print("%-52s mapped %5d spliced %5d exact %5.1f%% consistent %5.1f%% false-junction-reads %5.1f%% ts:+ %s micro %s/%s %s" % (
    label[:52], st["mapped"], st["spliced"], out["exact_pct"], out["consistent_pct"], out["false_junc_pct"], out["ts_plus_frac"],
    st["micro_kept"], st["micro_reads"], {k: "%d/%d" % (v["kept"], v["n"]) for k, v in per_tx.items()} if per_tx else ""))
if jout:
    json.dump(out, open(jout, "w"), indent=1)
