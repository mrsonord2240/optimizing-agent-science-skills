"""Independent re-audit check of parse_rmats_output (SQ-01/02/03) on fresh real rMATS 4.4.0 output.
Independent oracle: stdlib csv, no pandas, own arithmetic."""
import csv, sys, io, contextlib, math
SK = '/mnt/openscience/wt/norm-bio-splicing-quantification/skills/bio-splicing-quantification'
sys.path.insert(0, SK + '/scripts')
import quantify_splicing as q
O = '/mnt/openscience/audits/bio-splicing-quantification/run-reaudit-1/out'
types = ['SE', 'A5SS', 'A3SS', 'MXE', 'RI']


def vals(c):
    return [float(x) for x in c.split(',') if x != 'NA']


def oracle(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f, delimiter='\t'):
            a, b = vals(r['IncLevel1']), vals(r['IncLevel2'])
            reads = []
            for g in '12':
                for i, s in zip(r['IJC_SAMPLE_' + g].split(','), r['SJC_SAMPLE_' + g].split(',')):
                    reads.append(int(i) + int(s))
            rows.append(dict(ID=r['ID'], m1=sum(a) / len(a) if a else None, m2=sum(b) / len(b) if b else None,
                             m=(sum(a + b) / len(a + b)) if a + b else None, minr=min(reads)))
    return rows


def isnone(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


fail = 0
total = 0
for root, tag in [(O + '/rmats_real/out', 'real'), (O + '/rmats_planted/out', 'planted')]:
    for cnt in ['JC', 'JCEC']:
        for t in types:
            path = f'{root}/{t}.MATS.{cnt}.txt'
            ora = oracle(path)
            if not ora:
                print(f'{tag:7s}{cnt:5s}{t:5s} (empty file, skipped)')
                continue
            for N in (0, 10, 20):
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    res = q.parse_rmats_output(root, t, min_junction_reads=N, counts=cnt)
                exp = [o for o in ora if o['minr'] >= N]
                ok = sorted(res['ID'].astype(str)) == sorted(o['ID'] for o in exp)
                om = {o['ID']: o for o in exp}
                maxerr = 0.0
                mism = 0
                for _, r in res.iterrows():
                    o = om[str(r['ID'])]
                    for k, kk in (('mean_PSI', 'm'), ('mean_PSI_group1', 'm1'), ('mean_PSI_group2', 'm2')):
                        a, b = r[k], o[kk]
                        if isnone(a) and b is None:
                            continue
                        if isnone(a) or b is None:
                            mism += 1
                            continue
                        maxerr = max(maxerr, abs(a - b))
                total += 1
                good = ok and mism == 0 and maxerr < 1e-12
                fail += (not good)
                print(f'{tag:7s}{cnt:5s}{t:5s} N={N:2d} file_rows={len(ora):4d} oracle_reliable={len(exp):4d} '
                      f'skill_reliable={len(res):4d} ids_equal={ok} mism={mism} maxerr={maxerr:.2e} {"OK" if good else "FAIL"}')
print('cases', total, 'fail', fail)
