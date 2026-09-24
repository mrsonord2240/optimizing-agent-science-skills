"""Input 5 checks on the STAR 2-pass outputs (run in as-core). Independent of the Skill except junction_stats, which is the thing under test.
Usage: python 52_in5_check.py <run2 dir> <skill examples dir> <gtf>"""
import sys, glob, os, collections
d, ex, gtf = sys.argv[1:4]; sys.path.insert(0, ex)
import splicing_qc as sq, pysam
# --- merge file
merged = [l.rstrip('\n').split('\t') for l in open(f'{d}/cohort_novel_SJ.tab')]
print('merged lines', len(merged), 'columns per line', sorted({len(m) for m in merged}), 'distinct', len({tuple(m) for m in merged}))
nov = set()
for f in glob.glob(f'{d}/pass1_*_SJ.out.tab'):
    for l in open(f):
        c = l.rstrip('\n').split('\t')
        if c[5] == '0' and c[4] != '0' and int(c[6]) >= 3: nov.add((c[0], c[1], c[2], c[3]))
print('independent recomputation of the merge (pass-1 col6==0, col5>0, col7>=3):', len(nov), 'junctions; equal to merged file:', nov == {tuple(m) for m in merged})
ann = set()
for l in open(gtf):
    pass
# annotated introns from the GTF
tx = collections.defaultdict(list)
for l in open(gtf):
    f = l.split('\t')
    if len(f) > 8 and f[2] == 'exon': tx[f[8].split('transcript_id "')[1].split('"')[0]].append((int(f[3]), int(f[4])))
for t, e in tx.items():
    e.sort(); ann |= {('X', str(a[1] + 1), str(b[0] - 1)) for a, b in zip(e, e[1:])}
print('merged junctions already annotated in the GTF (should be 0 for a novel-only list):', sum(1 for m in merged if tuple(m[:3]) in ann))
for f in sorted(glob.glob(f'{d}/pass1_*_SJ.out.tab')):
    n = sum(1 for _ in open(f)); print(os.path.basename(f), n, 'lines')
# --- helper vs SJ.out.tab (unique reads, col7) on each pass-2 BAM
for bam in sorted(glob.glob(f'{d}/pass2_*_Aligned.sortedByCoord.out.bam')):
    s = os.path.basename(bam).split('_')[1]
    sj = {}
    for l in open(f'{d}/pass2_{s}_SJ.out.tab'):
        c = l.split('\t'); sj[(c[0], int(c[1]) - 1, int(c[2]))] = int(c[6])
    st = sq.junction_stats(bam, min_overhang=0)
    shared = [k for k in st if k in sj and sj[k] > 0]
    eq = sum(1 for k in shared if st[k]['reads'] == sj[k])
    sj_pos = {k for k, v in sj.items() if v > 0}
    ge10h = sum(1 for v in st.values() if v['reads'] >= 10); ge10s = sum(1 for v in sj.values() if v >= 10)
    print(f'{s}: helper junctions {len(st)}, STAR unique>0 junctions {len(sj_pos)}, shared {len(shared)}, equal counts {eq}/{len(shared)}, >=10 reads helper {ge10h} vs STAR {ge10s}; only-helper {len(set(st)-set(sj))}, only-STAR(unique>0) {len(sj_pos-set(st))}')
    h8 = sq.junction_stats(bam, min_overhang=8); print('    with --min-overhang 8: total reads counted', sum(v['reads'] for v in h8.values()), 'vs 0:', sum(v['reads'] for v in st.values()))
    xs = tot = 0
    for r in pysam.AlignmentFile(bam).fetch(until_eof=True):
        if any(op == 3 for op, _ in r.cigartuples or []): tot += 1; xs += r.has_tag('XS')
    print(f'    spliced records {tot}, with XS tag {xs}')
