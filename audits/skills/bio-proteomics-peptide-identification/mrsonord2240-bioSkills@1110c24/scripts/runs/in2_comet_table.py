# Input 2 - q-values from a Comet .txt (concatenated search) using the Skill's "FDR from a Results Table" snippet.
import pandas as pd
import numpy as np

SRC = 'F:/OpenScience/audits/bio-proteomics-peptide-identification/data/comet_concat.txt'


def skill_snippet(psms):
    # ---- SKILL.md lines 128-138, verbatim except the input frame is passed in ----
    psms['is_decoy'] = psms['protein'].str.startswith(('DECOY_', 'REV_', 'XXX_'))
    psms = psms.sort_values('score', ascending=False).reset_index(drop=True)
    targets = (~psms['is_decoy']).cumsum()
    decoys = psms['is_decoy'].cumsum()
    psms['fdr'] = decoys / targets
    psms['qvalue'] = psms['fdr'][::-1].cummin()[::-1]
    kept = psms[(psms['qvalue'] <= 0.01) & (~psms['is_decoy'])]
    return psms, kept


def report(tag, kept):
    fdp = 1 - kept['is_correct'].mean()
    print(f'{tag:<62} kept={len(kept):>5}  unique scans={kept["scan"].nunique():>5}  true FDP={fdp:.4f}')


# (0) as written: the Skill's read_csv + a 'score' column. Comet has no 'score' column.
try:
    psms = pd.read_csv(SRC, sep='\t')
    psms['is_decoy'] = psms['protein'].str.startswith(('DECOY_', 'REV_', 'XXX_'))
    psms = psms.sort_values('score', ascending=False)
except KeyError as e:
    print('as written -> KeyError:', e)

raw = pd.read_csv(SRC, sep='\t').rename(columns={'xcorr': 'score'})   # ADAPTED: map Comet xcorr -> score
print('rows', len(raw), 'scans', raw['scan'].nunique(), 'rows per scan', raw.groupby('scan').size().max())

# (a) snippet on every row of the .txt (Comet default num_output_lines = 5; the Skill never says keep rank 1)
_, kept_a = skill_snippet(raw.copy())
report('(a) Skill snippet, all Comet rows (ranks 1-5)', kept_a)

# (b) snippet after keeping the top hit per spectrum (what 'one best hit per spectrum' requires)
top1 = raw[raw['num'] == 1].copy()
all_b, kept_b = skill_snippet(top1.copy())
report('(b) Skill snippet, rank-1 only (proper TDC)', kept_b)

# (c) rank-1 with the +1 correction (Levitsky/He/Keich: (D+1)/T), as OpenMS 'conservative' default does
p = top1.copy()
p['is_decoy'] = p['protein'].str.startswith('DECOY_')
p = p.sort_values('score', ascending=False).reset_index(drop=True)
t = (~p['is_decoy']).cumsum()
d = p['is_decoy'].cumsum()
p['q'] = ((d + 1) / t.clip(lower=1))[::-1].cummin()[::-1]
report('(c) rank-1, (D+1)/T', p[(p['q'] <= 0.01) & ~p['is_decoy']])

# (d) rank-1 ranked on Comet E-value (lower = better) instead of XCorr
p = top1.copy()
p['score'] = -np.log10(p['e-value'])
_, kept_d = skill_snippet(p)
report('(d) rank-1, ranked on -log10(E-value)', kept_d)

# threshold XCorr that corresponds to q<=0.01 under (b)
print('XCorr at the 1% cut (b):', round(kept_b['score'].min(), 3))
# per-row q-value near the top: first rows of the ranked list
print(all_b[['scan', 'score', 'is_decoy', 'fdr', 'qvalue']].head(3).to_string(index=False))
