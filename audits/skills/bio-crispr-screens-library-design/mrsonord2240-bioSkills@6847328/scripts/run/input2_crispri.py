# Input 2 (Variant A) regression test: CRISPRi Dolcetto-window library, 5 synthetic lncRNAs.
# Verbatim crispri_window() from SKILL.md's "CRISPRi / CRISPRa TSS Targeting" section.
import re
import numpy as np
import pandas as pd

np.random.seed(2)

def crispri_window(tss_coord, strand='+'):
    if strand == '+':
        return (tss_coord - 50, tss_coord + 300)
    return (tss_coord - 300, tss_coord + 50)

bases = ['A', 'C', 'G', 'T']
genes = ['LINC-A1', 'LINC-B2', 'LINC-C3', 'LINC-D4', 'LINC-E5']

print('=== INPUT 2: CRISPRi (Dolcetto-window) library, 5 synthetic lncRNAs (post-fix regression) ===')
rows = []
flags = []
for i, gene in enumerate(genes):
    rng = np.random.RandomState(200 + i)
    tss = 1000  # local coordinate, TSS at 1000
    lo, hi = crispri_window(tss, strand='+')
    # build a synthetic flanking region long enough to cover the window plus PAM search
    region = ''.join(rng.choice(bases, hi - lo + 40))
    # scan for NGG PAM sites in this region, mapped back to pos_rel_tss
    candidates = []
    pam_pattern = re.compile(r'(?=([ACGT]{20}[ACGT]GG))')
    for m in pam_pattern.finditer(region):
        spacer = m.group(1)[:20]
        if 'TTTT' in spacer or spacer.count('G') + spacer.count('C') not in range(6, 15):
            continue
        abs_pos = m.start() + lo
        pos_rel_tss = abs_pos - tss
        if lo <= abs_pos <= hi:
            candidates.append({'gene': gene, 'spacer': spacer, 'pos_rel_tss': pos_rel_tss})
    cdf = pd.DataFrame(candidates)
    if cdf.empty:
        flags.append(f'{gene}: 0 candidates in window')
        continue
    # rank toward the +25..+75 Sanson optimum band
    cdf['dist_to_optimum'] = cdf['pos_rel_tss'].apply(lambda p: 0 if 25 <= p <= 75 else min(abs(p-25), abs(p-75)))
    cdf = cdf.sort_values('dist_to_optimum')
    sel = cdf.head(6)
    if len(sel) < 6:
        flags.append(f'{gene}: only {len(sel)}/6 candidates in window')
    rows.append(sel)

lib = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
print(f'Flags: {flags if flags else "none"}')
print(f'Total guides: {len(lib)}')
print(lib.groupby('gene').size())
in_optimum = lib['pos_rel_tss'].apply(lambda p: 25 <= p <= 75).sum()
print(f'Guides landing in the +25..+75 Sanson optimum: {in_optimum}/{len(lib)}')
out_of_window = ((lib['pos_rel_tss'] < -50) | (lib['pos_rel_tss'] > 300)).sum()
print(f'Guides outside the declared Dolcetto window (should be 0): {out_of_window}')
assert out_of_window == 0
print('ASSERT PASS: no guide outside declared window')

lib.to_csv('input2_crispri_library.csv', index=False)
print('Saved input2_crispri_library.csv')
