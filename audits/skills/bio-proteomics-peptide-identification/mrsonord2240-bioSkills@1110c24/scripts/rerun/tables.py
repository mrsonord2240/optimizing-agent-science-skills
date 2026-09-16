# Re-audit 2026-09-15, Inputs 2, 3, 5, 6, 7: the fixed SKILL.md "FDR from a Results Table" snippet VERBATIM
# (as a function; only the read_csv is replaced by the passed frame), on SYNTHETIC tables with truth columns.
import sys
import numpy as np
import pandas as pd

D = '../data/'

def skill_snippet(psms):
    psms = psms.copy()
    psms['is_decoy'] = psms['protein'].str.startswith(('DECOY_', 'REV_', 'XXX_'))
    # one best hit per spectrum (Comet .txt writes 5 rows per scan by default)
    psms = psms.sort_values('score', ascending=False).drop_duplicates('scan').reset_index(drop=True)

    # concatenated target-decoy competition: each decoy above threshold estimates one false target
    targets = (~psms['is_decoy']).cumsum()
    decoys = psms['is_decoy'].cumsum()
    psms['fdr'] = (decoys + 1) / targets.clip(lower=1)   # +1: zero decoys is not zero FDR (OpenMS conservative default)
    psms['qvalue'] = psms['fdr'][::-1].cummin()[::-1]   # running min from the bottom -> monotone q-values

    kept = psms[(psms['qvalue'] <= 0.01) & (~psms['is_decoy'])]   # 1% list-level FDR
    return psms, kept

def rep(tag, kept):
    print(f'{tag:<60} kept={len(kept):>5} unique scans={kept["scan"].nunique():>5} true FDP={1 - kept["is_correct"].mean():.4f}')

which = sys.argv[1]
comet = pd.read_csv(D + 'comet_concat.txt', sep='\t')

if which == 'in2':
    # Input 2: Comet .txt, all 5 ranks per scan; user maps xcorr -> score as the snippet comment says
    c = comet.rename(columns={'xcorr': 'score'})
    allp, kept = skill_snippet(c)
    rep('Skill snippet on raw Comet .txt (ranks 1-5)', kept)
    print('rows in', len(c), '| scans', c.scan.nunique(), '| rows after rank-1 dedup', len(allp))
    print('XCorr at the 1% cut:', round(kept['score'].min(), 3))
    # oracle on rank-1 list
    s = allp[~allp.is_decoy].sort_values('score', ascending=False)
    f = np.cumsum(~s['is_correct'].to_numpy()) / np.arange(1, len(s) + 1)
    print('oracle largest target list with true FDP <= 1%:', int(np.max(np.where(f <= 0.01)[0]) + 1))

elif which == 'in3':
    for name in ['pulldown_nodecoy.tsv', 'pulldown_topdecoy.tsv']:
        df = pd.read_csv(D + name, sep='\t')
        allp, kept = skill_snippet(df)
        print(f'{name}: rows {len(df)} decoys {int(allp.is_decoy.sum())} false targets {int((~allp.is_decoy & ~allp.is_correct).sum())} '
              f'| kept at 1%: {len(kept)} | q min {allp.qvalue.min():.4f} max {allp.qvalue.max():.4f} | any inf: {bool(np.isinf(allp.fdr).any())}')

elif which == 'in5':
    T = pd.read_csv(D + 'separate_target.tsv', sep='\t'); Dc = pd.read_csv(D + 'separate_decoy.tsv', sep='\t')
    merged = pd.concat([T, Dc], ignore_index=True)
    allp, kept = skill_snippet(merged)   # what happens if the agent runs the concatenated snippet on a merged file
    rep('concatenated snippet on merged separate searches (dedup = TDC)', kept)
    ts = np.sort(T.score.to_numpy())[::-1]; ds = np.sort(Dc.score.to_numpy())
    corr = T.sort_values('score', ascending=False).is_correct.to_numpy()
    t = np.arange(1, len(ts) + 1); d = len(ds) - np.searchsorted(ds, ts, side='left')
    qv = lambda f: np.minimum.accumulate(f[::-1])[::-1]
    def r2(tag, q):
        k = q <= 0.01; print(f'{tag:<60} kept={int(k.sum()):>5} true FDP={1 - corr[k].mean():.4f}')
    r2('Skill separate estimator, pi0 = 1: d/t (valid, conservative)', qv(d / t))
    # pi0 estimated from the lower half of the decoy null (Storey-style, lambda = decoy median)
    lam = np.median(ds)
    pi0 = min(1.0, (T.score < lam).sum() / (0.5 * len(ds)))
    r2(f'Skill separate estimator, pi0-hat={pi0:.3f}: pi0*d/t', qv(pi0 * d / t))
    r2('Elias-Gygi 2d/(t+d) misapplied to separate searches', qv(2 * d / (t + d)))
    f = np.cumsum(~corr) / t
    print('oracle:', int(np.max(np.where(f <= 0.01)[0]) + 1))
    for n in (2600,):
        thr = ts[n - 1]; dd = int((ds >= thr).sum())
        print(f'top {n}: true FDP {1 - corr[:n].mean():.4f} | 2d/(t+d) {2*dd/(n+dd):.4f} | d/t {dd/n:.4f} | pi0*d/t {pi0*dd/n:.4f}')

elif which == 'in6':
    # NEW Input 6: FragPipe/Philosopher-style lowercase 'rev_' decoys (MSFragger psm.tsv convention)
    c = comet.rename(columns={'xcorr': 'score'}).copy()
    c['protein'] = c['protein'].str.replace('DECOY_', 'rev_', regex=False)
    allp, kept = skill_snippet(c)
    rep("snippet as written on rev_ decoys", kept)
    print('decoys detected:', int(allp.is_decoy.sum()), '| rev_ rows kept as targets:', int(kept.protein.str.startswith('rev_').sum()))
    c2 = c.copy(); c2['protein'] = c2['protein'].str.replace('rev_', 'REV_', regex=False)
    _, k2 = skill_snippet(c2)
    rep("same data with prefix upper-cased to REV_", k2)

elif which == 'in7':
    # NEW Input 7: lower-is-better engine score (E-value / SpecEValue) mapped straight to 'score'
    c = comet.rename(columns={'e-value': 'score'})
    allp, kept = skill_snippet(c)
    rep("E-value mapped to 'score' as-is (lower is better)", kept)
    c2 = comet.copy(); c2['score'] = -np.log10(comet['e-value'])
    _, k2 = skill_snippet(c2)
    rep("-log10(E-value) as score", k2)
