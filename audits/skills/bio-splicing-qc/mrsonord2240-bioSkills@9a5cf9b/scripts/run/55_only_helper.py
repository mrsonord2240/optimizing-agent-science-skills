"""Which junctions does junction_stats() report that STAR SJ.out.tab (pass 2) does not? Usage: python 55_only_helper.py <examples> <bam> <SJ.out.tab> <X.fa>"""
import sys, collections
sys.path.insert(0, sys.argv[1]); import splicing_qc as sq, pysam
st = sq.junction_stats(sys.argv[2], min_overhang=0); sj = {}
for l in open(sys.argv[3]):
    c = l.split('\t'); sj[(c[0], int(c[1]) - 1, int(c[2]))] = (int(c[6]), int(c[7]), c[4])
g = pysam.FastaFile(sys.argv[4]); rows = []
for k, v in st.items():
    if k not in sj:
        d = g.fetch(k[0], k[1], k[1] + 2).upper(); a = g.fetch(k[0], k[2] - 2, k[2]).upper()
        rows.append((v['reads'], d + '..' + a))
print('only in helper:', len(rows), '; motif (donor..acceptor) counts:', collections.Counter(m for _, m in rows).most_common(6), '; read counts:', sorted(r for r, _ in rows)[-5:])
print('in SJ.out.tab with unique=0 (multi-mapper only):', sum(1 for v in sj.values() if v[0] == 0))
