"""NEW input N1: usage-guide prompt 'Run junction saturation and junction annotation across all my BAMs and report samples below acceptable
thresholds' on a mixed cohort: 4 real chrX pass-2 BAMs (my STAR run) + 2 planted libraries (se_clean healthy; se_novelrich novel-rich).
Uses only the Skill's helper API (generate_qc_report) in a loop. Each library needs its own gene model (real chrX BED12 / synth.bed12).
Usage: python 81_n1_cohort.py <examples dir> <star run2 dir> <real bed12> <synthetic dir> <outdir>"""
import sys, glob, os, io, contextlib
ex, star, bed_real, syn, out = sys.argv[1:6]; sys.path.insert(0, ex)
import splicing_qc as sq
os.makedirs(out, exist_ok=True)
jobs = [(os.path.basename(b).split('_')[1], b, bed_real) for b in sorted(glob.glob(f'{star}/pass2_*_Aligned.sortedByCoord.out.bam'))]
jobs += [('planted_clean', f'{syn}/se_clean.bam', f'{syn}/synth.bed12'), ('planted_novelrich', f'{syn}/se_novelrich.bam', f'{syn}/synth.bed12')]
rows = []
for name, bam, bed in jobs:
    with contextlib.redirect_stdout(io.StringIO()):
        r = sq.generate_qc_report(bam, bed, f'{out}/{name}')
    a, s, p = r['annotation'], r['saturation'], r['support']
    flags = []
    if a['read_known'] < 0.8: flags.append('known<80%')
    if s['growth_80_100']['known'] >= 0.02: flags.append('saturation still rising')
    if p['pct_ge_min_reads'] < 30: flags.append('<30% junctions >=10 reads')
    rows.append((name, a['read_known'], a['junction_known'], s['growth_80_100']['known'], p['pct_ge_min_reads'], a['status'], flags))
print('%-18s %8s %8s %8s %8s  %-22s %s' % ('sample', 'known_rd', 'known_jn', 'growth', '%>=10rd', 'status', 'flags'))
for r in rows: print('%-18s %8.3f %8.3f %8.3f %8.1f  %-22s %s' % (r[0], r[1], r[2], r[3], r[4], r[5], '; '.join(r[6]) or '-'))
