#!/usr/bin/env python3
"""SKILL.md 'stats: bases mapped (cigar) excludes soft-clipped bases; bases mapped includes them': check on synth.bam vs walk of CIGARs (stats-eligible reads: mapped, primary, QC-pass)."""
import pysam, subprocess
B = '/mnt/openscience/audits/bio-bam-statistics/run/data/synth.bam'
q = m = 0; sclip = ins = dele = 0
for r in pysam.AlignmentFile(B).fetch(until_eof=True):
    if r.flag & (4 | 256 | 512 | 2048) : continue
    q += r.query_length
    for op, n in r.cigartuples:
        if op in (0, 7, 8): m += n
        if op == 4: sclip += n
        if op == 1: ins += n
print('stats-eligible reads: sum(query_length)=', q, ' sum(M/=/X)=', m, ' softclip=', sclip, ' ins=', ins)
sn = {l.split('\t')[1]: l.split('\t')[2] for l in subprocess.run(['samtools', 'stats', B], capture_output=True, text=True).stdout.splitlines() if l.startswith('SN')}
print('stats bases mapped:', sn['bases mapped:'], ' bases mapped (cigar):', sn['bases mapped (cigar):'])
