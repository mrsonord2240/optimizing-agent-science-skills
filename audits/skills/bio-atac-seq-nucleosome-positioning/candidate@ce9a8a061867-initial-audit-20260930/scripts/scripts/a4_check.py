import os, glob, csv, numpy as np
W = os.environ['NP'] + '/work/a4'
f = glob.glob(W + '/diff/*.positions.integrative.xls')[0]
r = list(csv.reader(open(f), delimiter='\t')); h, d = r[0], r[1:]
ix = {c: i for i, c in enumerate(h)}
def col(c): return np.array([float(x[ix[c]]) if x[ix[c]] not in ('NA', 'nan', '') else np.nan for x in d])
pos = col('center'); dis = col('treat2control_dis'); sm = col('diff_smt_loca'); fdr_pt = col('point_diff_FDR'); fdr_smt = col('smt_diff_FDR')
res = []
def chk(n, ok, i=''): res.append(bool(ok)); print('PASS' if ok else 'FAIL', n, i)
print('rows', len(d), 'columns', h[:12])
sh = pos < 12_000_000; un = pos >= 12_500_000; sh_ok = sh & (pos > 10_300_000)
print('median treat2control_dis shifted region %.1f  unshifted region %.1f' % (np.nanmedian(dis[sh_ok]), np.nanmedian(dis[un])))
print('median signed diff_smt_loca?  shifted %.1f unshifted %.1f' % (np.nanmedian(sm[sh_ok]), np.nanmedian(sm[un])))
chk('shifted region: median shift near planted 40 bp (35-45)', 35 <= np.nanmedian(dis[sh_ok]) <= 45, '%.1f' % np.nanmedian(dis[sh_ok]))
chk('unshifted region: median shift < 10 bp', np.nanmedian(dis[un]) < 10, '%.1f' % np.nanmedian(dis[un]))
call = lambda m, fdr: m & (dis >= 30) & (fdr < 0.05)
for nm, fd in [('point_diff_FDR', fdr_pt), ('smt_diff_FDR', fdr_smt)]:
    tp = call(sh_ok, fd).sum(); fp = call(un, fd).sum()
    print('Skill rule shift>=30 & %s<0.05: calls in shifted region %d / %d rows (%.1f%%); calls in unshifted region %d / %d (%.1f%%)' % (nm, tp, sh_ok.sum(), 100*tp/sh_ok.sum(), fp, un.sum(), 100*fp/un.sum()))
tp = call(sh_ok, fdr_pt).sum() / sh_ok.sum(); fp = call(un, fdr_pt).sum() / un.sum()
sens_shift_only = (sh_ok & (dis >= 30)).sum() / sh_ok.sum(); fp_shift_only = (un & (dis >= 30)).sum() / un.sum()
print('shift>=30 alone: shifted region %.1f%%, unshifted region %.1f%%' % (100*sens_shift_only, 100*fp_shift_only))
chk('shift>=30 alone recovers >=70% of planted-shift positions with <10% false calls', sens_shift_only >= 0.70 and fp_shift_only < 0.10, '%.2f / %.2f' % (sens_shift_only, fp_shift_only))
chk('Skill rule (shift>=30 AND FDR<0.05 on point_diff_FDR) recovers >=50% of planted-shift positions', tp >= 0.5, '%.3f' % tp)
print('SUMMARY', sum(res), '/', len(res))
