"""Input 3: assert MMSplice output shape and the Skill's parse_mmsplice_csv reduction against pandas ground truth."""
import sys
sys.path.insert(0, 'skill/examples')
import pandas as pd, numpy as np
from splice_parsers import parse_mmsplice_csv, read_input_vcf, variant_key
for build, vcf in [('grch37', 'data/panel_grch37.vcf'), ('grch38', 'data/panel_grch38_auditor.vcf')]:
    df = pd.read_csv(f'out/mmsplice_{build}.csv')
    print(f'== {build}: {len(df)} rows x {df.shape[1]} cols; columns:', list(df.columns)[:8], '...')
    red = parse_mmsplice_csv(f'out/mmsplice_{build}.csv')
    inp = read_input_vcf(vcf)
    # ground truth: largest |dlp| per raw ID computed without the Skill's code
    gt = df.groupby('ID')['delta_logit_psi'].apply(lambda s: s.iloc[s.abs().argmax()])
    print('raw IDs in CSV:', sorted(df['ID'].unique()))
    print('reduced rows', len(red), 'unique keys', red['key'].nunique())
    m = red.set_index('key')['delta_logit_psi']
    ok = True
    for rid, v in gt.items():
        chrom, pos, rest = rid.split(':'); ref, alt = rest.split('>')
        k = variant_key(chrom, pos, ref, alt)
        if not (k in m.index and abs(m[k] - v) < 1e-9):
            ok = False; print('MISMATCH', rid, v, m.get(k))
    print('PASS reduction == independent per-ID argmax|dlp|' if ok else 'FAIL reduction')
    missing = inp.loc[~inp['key'].isin(set(red['key']))]
    print('input variants with no MMSplice row:', list(missing['id']))
    t = inp.set_index('key')[['id']].join(m)
    print(t.to_string())
    # direction/ground truth
    can = t[t['id'].str.contains('c.9563|c.31\+1|c.370|donor_G>A|c.386')]
    print('canonical/donor variants: all delta_logit_psi < -1?', bool((can['delta_logit_psi'] < -1).all()))
    ben = t[t['id'].str.contains('benign')]
    print('benign: |dlp| < 1 (or no row)?', bool((ben['delta_logit_psi'].abs().fillna(0) < 1).all()), list(ben['delta_logit_psi'].round(2)))
