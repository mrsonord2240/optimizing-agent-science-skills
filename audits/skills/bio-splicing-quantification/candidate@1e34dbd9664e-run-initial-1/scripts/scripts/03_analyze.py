"""Audit analysis: execute the Skill's own snippet/script on real rMATS output, recompute values, cross-check SUPPA2.
Run inside as-core: micromamba run -n as-core python 03_analyze.py <skill_dir> <out_dir>"""
import re, sys, os, json, shutil
import numpy as np, pandas as pd
skill, out = sys.argv[1], sys.argv[2]
os.chdir(out)
sys.path.insert(0, skill + '/scripts')
import quantify_splicing as q
res = {}

print('== 1. SKILL.md inline rMATS snippet, executed verbatim on real chrX rMATS output')
md = open(skill + '/SKILL.md', encoding='utf-8').read()
blocks = re.findall(r"```python\n(.*?)```", md, re.S)
snip = [b for b in blocks if 'IncLevel' in b][0]
os.makedirs('snippet_cwd', exist_ok=True)
if not os.path.exists('snippet_cwd/rmats_output'):
    shutil.copytree('rmats_real/out', 'snippet_cwd/rmats_output')
os.chdir('snippet_cwd')
try:
    exec(compile(snip, 'SKILL.md-snippet', 'exec'), {})
    print('snippet OK'); res['inline_snippet'] = 'ok'
except Exception as e:
    print('SNIPPET FAILS:', type(e).__name__, e); res['inline_snippet'] = f'{type(e).__name__}: {e}'
os.chdir('..')

print('== 2. scripts/quantify_splicing.py parse_rmats_output, five event types')
for et in ['SE', 'A5SS', 'A3SS', 'MXE', 'RI']:
    try:
        r = q.parse_rmats_output('rmats_real/out', et, 20); res[f'parse_{et}'] = f'ok rows={len(r)}'
        print(et, res[f'parse_{et}'])
    except Exception as e:
        print(et, 'FAILS:', type(e).__name__, str(e)[:120]); res[f'parse_{et}'] = type(e).__name__

print('== 3. SE: script mean_PSI vs independent mean of IncLevel1+IncLevel2 (no difference column)')
se = pd.read_csv('rmats_real/out/SE.MATS.JC.txt', sep='\t')
def vals(s):
    return [float(x) for x in str(s).split(',') if x not in ('NA', 'nan')]
se['true_mean'] = se.apply(lambda r: np.mean(vals(r.IncLevel1) + vals(r.IncLevel2)) if vals(r.IncLevel1) + vals(r.IncLevel2) else np.nan, axis=1)
r = q.parse_rmats_output('rmats_real/out', 'SE', 0)
m = se.merge(r[['ID', 'mean_PSI']], on='ID')
m['diff'] = (m.mean_PSI - m.true_mean).abs()
bad = m[(m['diff'] > 1e-9) & m.true_mean.notna()]
print('SE rows', len(m), 'script mean_PSI != true mean in', len(bad), 'rows; max abs error', round(m['diff'].max(), 3))
print('script mean_PSI outside [0,1]:', int(((m.mean_PSI < 0) | (m.mean_PSI > 1)).sum()), 'rows (min %.3f max %.3f)' % (m.mean_PSI.min(), m.mean_PSI.max()))
ex = bad.assign(absdiff=bad['diff']).sort_values('absdiff', ascending=False).head(3)[['geneSymbol', 'IncLevel1', 'IncLevel2', 'IncLevelDifference', 'true_mean', 'mean_PSI']]
print(ex.to_string())
res['SE_mean_PSI_wrong_rows'] = int(len(bad)); res['SE_mean_PSI_max_err'] = float(m['diff'].max())
res['SE_mean_PSI_outside_01'] = int(((m.mean_PSI < 0) | (m.mean_PSI > 1)).sum())
tot = lambda a, b: a.str.split(',').apply(lambda x: sum(map(int, x))) + b.str.split(',').apply(lambda x: sum(map(int, x)))
print('events with >=20 junction reads: SAMPLE_1 =', int((tot(se.IJC_SAMPLE_1, se.SJC_SAMPLE_1) >= 20).sum()), ' SAMPLE_2 =', int((tot(se.IJC_SAMPLE_2, se.SJC_SAMPLE_2) >= 20).sum()), '(script filters on SAMPLE_1 only)')

print('== 4. PSI formula and IncFormLen claims (planted + real)')
pl = pd.read_csv('rmats_planted/out/SE.MATS.JC.txt', sep='\t'); plc = pd.read_csv('rmats_planted/out/SE.MATS.JCEC.txt', sep='\t')
print('planted JC IncFormLen/SkipFormLen:', int(pl.IncFormLen[0]), int(pl.SkipFormLen[0]), '| JCEC:', int(plc.IncFormLen[0]), int(plc.SkipFormLen[0]), '(readLength 50, exon 100 nt)')
print('IJC', pl.IJC_SAMPLE_1[0], 'SJC', pl.SJC_SAMPLE_1[0], 'IncLevel1', pl.IncLevel1[0], 'IncLevel2', pl.IncLevel2[0], 'diff', pl.IncLevelDifference[0])
I, S, IL, SL = 80, 10, int(pl.IncFormLen[0]), int(pl.SkipFormLen[0])
print('Skill formula=%.4f ; naive IJC/(IJC+SJC)=%.4f ; expected 0.8' % ((I / IL) / ((I / IL) + (S / SL)), I / (I + S)))
res['planted_len_JC'] = [int(pl.IncFormLen[0]), int(pl.SkipFormLen[0])]
res['planted_len_JCEC'] = [int(plc.IncFormLen[0]), int(plc.SkipFormLen[0])]
mx = 0; n = 0
for _, r in se.iterrows():
    for ij, sj, inc in [(r.IJC_SAMPLE_1, r.SJC_SAMPLE_1, r.IncLevel1), (r.IJC_SAMPLE_2, r.SJC_SAMPLE_2, r.IncLevel2)]:
        for i, s, p in zip(str(ij).split(','), str(sj).split(','), str(inc).split(',')):
            if p == 'NA':
                continue
            a, b = int(i) / r.IncFormLen, int(s) / r.SkipFormLen
            mx = max(mx, abs(a / (a + b) - float(p))); n += 1
print('real SE JC: formula vs IncLevel on', n, 'replicate values; max abs diff', round(mx, 4))
print('real SE IncFormLen/SkipFormLen (readLength 75):', se.IncFormLen.iloc[0], se.SkipFormLen.iloc[0])
res['real_formula_maxdiff'] = mx

print('== 5. rMATS vs SUPPA2 direction (Skill: A5/A3 same convention; SE inclusion same)')
def rm_vec(r):
    return [np.nan if x == 'NA' else float(x) for x in str(r.IncLevel1).split(',') + str(r.IncLevel2).split(',')]
def corr_report(tag, pairs):
    if not pairs:
        print(tag, 'no matched events'); return None
    a = np.array([p[0] for p in pairs]).ravel(); b = np.array([p[1] for p in pairs]).ravel()
    ok = ~(np.isnan(a) | np.isnan(b))
    r_ = np.corrcoef(a[ok], b[ok])[0, 1] if ok.sum() > 2 else np.nan
    print(f'{tag}: matched events {len(pairs)}, paired values {int(ok.sum())}, Pearson r = {r_:.3f}, mean |diff| = {np.abs(a[ok]-b[ok]).mean():.3f}, mean(rMATS-SUPPA) = {(a[ok]-b[ok]).mean():.3f}')
    return float(r_)
sp = pd.read_csv('suppa/chrX_psi_SE.psi', sep='\t', index_col=0)
idx = {}
for sid in sp.index:
    mm = re.match(r'.*;SE:(\w+):(\d+)-(\d+):(\d+)-(\d+):([+-])', sid)
    if mm:
        idx[(int(mm[2]), int(mm[3]), int(mm[4]), int(mm[5]), mm[6])] = sid
pairs = []
for _, r in se.iterrows():
    k = (r.upstreamEE, r.exonStart_0base + 1, r.exonEnd, r.downstreamES + 1, r.strand)
    if k in idx:
        pairs.append((rm_vec(r), sp.loc[idx[k]].values.astype(float)))
res['SE_corr'] = corr_report('SE', pairs)
for et, tag in [('A5SS', 'A5'), ('A3SS', 'A3')]:
    df = pd.read_csv(f'rmats_real/out/{et}.MATS.JC.txt', sep='\t'); sp = pd.read_csv(f'suppa/chrX_psi_{tag}.psi', sep='\t', index_col=0)
    sd = {}
    for sid in sp.index:
        mm = re.match(r'.*;A[53]:(\w+):(\d+)-(\d+):(\d+)-(\d+):([+-])', sid)
        if mm:
            sd.setdefault(mm[6], []).append((sid, int(mm[2]), int(mm[3]), int(mm[4]), int(mm[5])))
    pairs = []; first_is_long = [0, 0]
    for _, r in df.iterrows():
        if (et == 'A5SS') == (r.strand == '+'):
            long_, short_, flank = r.longExonEnd, r.shortEE, r.flankingES + 1
        else:
            long_, short_, flank = r.longExonStart_0base + 1, r.shortES + 1, r.flankingEE
        for sid, a, b, c, d in sd.get(r.strand, []):
            if abs(a - c) <= 1 and abs(a - flank) <= 1:
                alts = [b, d]
            elif abs(b - d) <= 1 and abs(b - flank) <= 1:
                alts = [a, c]
            else:
                continue
            if sorted(alts) and abs(min(alts) - min(long_, short_)) <= 1 and abs(max(alts) - max(long_, short_)) <= 1:
                pairs.append((rm_vec(r), sp.loc[sid].values.astype(float)))
                first_is_long[0 if abs(alts[0] - long_) <= 1 else 1] += 1
                break
    print(f'{tag}: SUPPA ID first alternative equals rMATS long form in {first_is_long[0]} events, short form in {first_is_long[1]}')
    res[f'{tag}_corr'] = corr_report(f'{et} vs SUPPA2 {tag}', pairs)
json.dump(res, open('analysis_results.json', 'w'), indent=1)
