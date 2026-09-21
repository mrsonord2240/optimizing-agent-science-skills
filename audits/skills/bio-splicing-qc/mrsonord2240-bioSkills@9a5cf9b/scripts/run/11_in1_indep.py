"""Independent (no RSeQC, no Skill code) known/partial/novel junction classification with pysam + BED12, for
comparison with RSeQC junction_annotation and the SKILL.md snippet. Usage: python 11_in1_indep.py sample.bam genes.bed12 [rseqc .junction.xls]"""
import sys, collections, pysam
bam, bed = sys.argv[1], sys.argv[2]
starts, ends = collections.defaultdict(set), collections.defaultdict(set)   # known donors / acceptors (intron coords, 0-based start, end)
for line in open(bed):
    f = line.rstrip('\n').split('\t')
    if len(f) < 12: continue
    cs, n = int(f[1]), int(f[9]); sz = [int(x) for x in f[10].strip(',').split(',')]; st = [int(x) for x in f[11].strip(',').split(',')]
    for i in range(n - 1):
        starts[f[0]].add(cs + st[i] + sz[i]); ends[f[0]].add(cs + st[i + 1])
reads = collections.Counter(); juncs = collections.defaultdict(int)
for r in pysam.AlignmentFile(bam).fetch(until_eof=True):
    if r.is_unmapped or r.is_secondary or r.is_qcfail or r.is_duplicate or r.mapping_quality < 30: continue
    pos = r.reference_start
    for op, ln in r.cigartuples:
        if op == 3:
            if ln >= 50: juncs[(r.reference_name, pos, pos + ln)] += 1
            pos += ln
        elif op in (0, 2, 7, 8): pos += ln
cl = collections.Counter(); jl = collections.Counter()
for (c, s, e), n in juncs.items():
    ks, ke = s in starts[c], e in ends[c]
    k = 'annotated' if ks and ke else 'complete_novel' if not ks and not ke else 'partial_novel'
    cl[k] += n; jl[k] += 1
tot = sum(cl.values())
print('independent: reads', dict(cl), 'total', tot, '| junctions', dict(jl), 'total', sum(jl.values()))
print('independent known (reads) %.4f  known (junctions) %.4f' % (cl['annotated'] / tot, jl['annotated'] / sum(jl.values())))
if len(sys.argv) > 3:
    import pandas as pd
    x = pd.read_csv(sys.argv[3], sep='\t'); x['annotation'] = x['annotation'].str.strip()
    print('RSeQC xls  : reads', x.groupby('annotation')['read_count'].sum().to_dict(), '| junctions', x.groupby('annotation').size().to_dict())
    print('EQUAL reads:', x.groupby('annotation')['read_count'].sum().to_dict() == dict(cl), ' EQUAL junctions:', x.groupby('annotation').size().to_dict() == dict(jl))
