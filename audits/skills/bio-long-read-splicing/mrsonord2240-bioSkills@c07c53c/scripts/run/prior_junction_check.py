#!/usr/bin/env python3
"""Second-method check (pysam, independent of every tool under test).

For a BAM of simulated reads (read name = <sample>_<TXID>_<n>) compare the intron chain that
each PRIMARY alignment carries (CIGAR N operations) with the planted truth transcript
(read_tx.gtf).  Reports: mapped %, spliced %, exact-chain %, contiguous-subchain % (5' fragments),
reads carrying a junction that is in NO truth transcript (false junction), strand (ts tag) accuracy.
Usage: junction_check.py <bam> <read_tx.gtf> [label]
"""
import sys, re, collections
import pysam

bam, gtf = sys.argv[1], sys.argv[2]
label = sys.argv[3] if len(sys.argv) > 3 else bam

tx = collections.defaultdict(list)
strand = {}
for ln in open(gtf):
    f = ln.rstrip("\n").split("\t")
    if len(f) < 9 or f[2] != "exon":
        continue
    tid = re.search(r'transcript_id "([^"]+)"', f[8]).group(1)
    tx[tid].append((int(f[3]) - 1, int(f[4])))  # 0-based half-open
    strand[tid] = f[6]
chain = {}
alljn = set()
for tid, ex in tx.items():
    ex.sort()
    ch = tuple((ex[i][1], ex[i + 1][0]) for i in range(len(ex) - 1))
    chain[tid.replace(".", "")] = ch
    alljn.update(ch)

st = collections.Counter()
per_tx = collections.defaultdict(lambda: collections.Counter())
sf = pysam.AlignmentFile(bam, "rb")
for r in sf.fetch(until_eof=True):
    if r.is_secondary or r.is_supplementary:
        continue
    st["reads_seen"] += 1
    if r.is_unmapped:
        st["unmapped"] += 1
        continue
    st["mapped"] += 1
    t = r.query_name.split("_")[1]
    exp = chain[t]
    obs = []
    pos = r.reference_start
    for op, ln in r.cigartuples:
        if op == 3:
            obs.append((pos, pos + ln))
            pos += ln
        elif op in (0, 2, 7, 8):
            pos += ln
    obs = tuple(obs)
    if obs:
        st["spliced"] += 1
    if any(j not in alljn for j in obs):
        st["false_junction_read"] += 1
    if obs == exp:
        st["exact_chain"] += 1
        per_tx[t]["exact"] += 1
    else:
        # contiguous subchain (5'/3' fragment)
        n = len(obs)
        ok = n > 0 and any(exp[i:i + n] == obs for i in range(len(exp) - n + 1))
        if ok:
            st["subchain"] += 1
        elif not obs and len(exp) > 0:
            st["unspliced_but_expected_spliced"] += 1
    per_tx[t]["n"] += 1
    if r.has_tag("ts"):
        want = strand[[k for k in tx if k.replace(".", "") == t][0]]
        got = r.get_tag("ts")
        # minimap2 'ts' is relative to the READ; the transcript strand on the reference is ts flipped for reverse alignments
        gene_strand = got if not r.is_reverse else ("-" if got == "+" else "+")
        st["ts_correct" if gene_strand == want else "ts_wrong"] += 1
    elif obs:
        st["spliced_no_ts_tag"] += 1
    st["rev_aligned" if r.is_reverse else "fwd_aligned"] += 1

n = max(st["mapped"], 1)
print("== %s" % label)
print("reads %d  mapped %d (%.1f%%)  spliced %d (%.1f%%)" % (st["reads_seen"], st["mapped"], 100 * st["mapped"] / max(st["reads_seen"], 1), st["spliced"], 100 * st["spliced"] / n))
print("exact intron chain %d (%.1f%%)  contiguous sub-chain(5'/3' fragment) %d (%.1f%%)  unspliced although truth spliced %d (%.1f%%)" % (
    st["exact_chain"], 100 * st["exact_chain"] / n, st["subchain"], 100 * st["subchain"] / n, st["unspliced_but_expected_spliced"], 100 * st["unspliced_but_expected_spliced"] / n))
print("reads with a junction absent from truth (false junction) %d (%.1f%%)" % (st["false_junction_read"], 100 * st["false_junction_read"] / n))
print("inferred gene strand (ts, flipped when reverse-aligned) correct %d wrong %d ; alignments fwd %d rev %d" % (st["ts_correct"], st["ts_wrong"], st["fwd_aligned"], st["rev_aligned"]))
