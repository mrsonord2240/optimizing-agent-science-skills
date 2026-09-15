"""Summarise MrBayes 3.2.7a output files for the audit: .pstat (ESS/PSRF), .tstat (split SDs -> ASDSF/max),
.mcmc (live ASDSF trace), .lstat (harmonic/arithmetic mean), .ss (stepping-stone). Usage: mbdiag.py <prefix>"""
import sys, os, math, glob


def table(path):
    rows, hdr = [], None
    for line in open(path, encoding='utf-8', errors='replace'):
        line = line.rstrip('\n')
        if not line.strip() or line.startswith('['):
            continue
        parts = [p for p in line.split('\t') if p.strip() != '']  # .tstat rows carry an empty field after ID
        if hdr is None:
            hdr = [p.strip() for p in parts]
            continue
        rows.append(dict(zip(hdr, [p.strip() for p in parts])))
    return hdr, rows


def main(prefix):
    out = []
    if os.path.exists(prefix + '.pstat'):
        hdr, rows = table(prefix + '.pstat')
        out.append('== .pstat (scalar diagnostics) ==')
        worst_ess, worst_psrf = None, None
        for r in rows:
            ess = float(r.get('minESS', 'nan'))
            psrf = float(r.get('PSRF', 'nan')) if r.get('PSRF', 'NA') not in ('NA', '') else float('nan')
            out.append('  %-12s mean=%-10s minESS=%8.1f avgESS=%8s PSRF=%s' % (r['Parameter'], r['Mean'], ess, r.get('avgESS'), r.get('PSRF')))
            if worst_ess is None or ess < worst_ess[1]:
                worst_ess = (r['Parameter'], ess)
            if not math.isnan(psrf) and (worst_psrf is None or abs(psrf - 1) > abs(worst_psrf[1] - 1)):
                worst_psrf = (r['Parameter'], psrf)
        out.append('  WORST minESS: %s %.1f | WORST PSRF: %s %.3f' % (worst_ess + worst_psrf))
        out.append('  GATE ESS>200 all params: %s ; PSRF<=1.01 all: %s' % (
            worst_ess[1] > 200, abs(worst_psrf[1] - 1) <= 0.01))
    if os.path.exists(prefix + '.tstat'):
        hdr, rows = table(prefix + '.tstat')
        sds = [float(r['Stddev(s)']) for r in rows if r.get('Stddev(s)') not in (None, 'NA', '')]
        if sds:
            out.append('== .tstat == informative splits=%d  ASDSF(recomputed, splits>=minpartfreq)=%.4f  max SD=%.4f' % (len(rows), sum(sds) / len(sds), max(sds)))
    if os.path.exists(prefix + '.mcmc'):
        hdr, rows = table(prefix + '.mcmc')
        col = [c for c in hdr if c in ('StdDev(s)', 'AvgStdDev(s)')]
        if col:
            trace = [(r['Gen'], r[col[0]]) for r in rows]
            shown = trace if len(trace) <= 6 else trace[:3] + ['...'] + trace[-3:]
            out.append('== .mcmc live ASDSF trace (Gen, %s) == %s' % (col[0], shown))
    if os.path.exists(prefix + '.lstat'):
        out.append('== .lstat == ' + open(prefix + '.lstat', encoding='utf-8').read().strip().replace('\n', ' | '))
    for ss in glob.glob(prefix + '.ss'):
        out.append('== .ss (last 3 lines) == ' + ' | '.join(open(ss, encoding='utf-8').read().strip().splitlines()[-3:]))
    print('\n'.join(out))


if __name__ == '__main__':
    main(sys.argv[1])
