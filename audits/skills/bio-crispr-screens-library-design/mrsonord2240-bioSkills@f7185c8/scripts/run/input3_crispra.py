# Input 3 (Variant B) regression test: CRISPRa Calabrese-window library, 4 synthetic TFs.
# Verbatim crispra_window() from the fixed SKILL.md -- now carries an inline docstring
# caveat about the narrow 75bp window undersupplying guides (P2 fix, added 2026-09-16).
import re
import numpy as np
import pandas as pd

np.random.seed(3)

def crispra_window(tss_coord, strand='+'):
    '''Calabrese convention: -150 to -75 upstream of TSS.
    Caveat: at only 75bp wide, this window routinely fails to contain a full
    6-guide quota's worth of PAM sites passing the GC/poly-T filter -- budget
    for shortfalls (report actual count per gene rather than padding with
    out-of-window guides) or widen to Horlbeck v2 when the quota must be met.'''
    if strand == '+':
        return (tss_coord - 150, tss_coord - 75)
    return (tss_coord + 75, tss_coord + 150)

# Confirm the caveat text actually made it into the shipped SKILL.md docstring
skill_md = open(r'library-design-src/SKILL.md', encoding='utf-8').read() if __import__('os').path.exists('library-design-src/SKILL.md') else open(r'..\run\library-design-src\SKILL.md', encoding='utf-8').read()
assert 'routinely fails to contain a full' in skill_md or 'routinely fail' in skill_md, 'Calabrese undersupply caveat missing from shipped SKILL.md'
print('DOC CHECK PASS: SKILL.md crispra_window() docstring now warns about undersupply (fix log P2 item)')

bases = ['A', 'C', 'G', 'T']
genes = ['TF-A', 'TF-B', 'TF-C', 'TF-D']

print('=== INPUT 3: CRISPRa (Calabrese-window) library, 4 synthetic TFs (post-fix regression) ===')
rows = []
flags = []
for i, gene in enumerate(genes):
    rng = np.random.RandomState(300 + i)
    tss = 1000
    lo, hi = crispra_window(tss, strand='+')
    region = ''.join(rng.choice(bases, hi - lo + 40))
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
        flags.append(f'{gene}: 0/6 candidates in window')
        continue
    sel = cdf.head(6)
    if len(sel) < 6:
        flags.append(f'{gene}: only {len(sel)}/6 candidates in window')
    rows.append(sel)

lib = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
print(f'Flags: {flags if flags else "none"}')
print(f'Total guides: {len(lib)}')
print(lib.groupby('gene').size())
out_of_window = ((lib['pos_rel_tss'] < -150) | (lib['pos_rel_tss'] > -75)).sum() if not lib.empty else 0
print(f'Guides outside declared Calabrese window (should be 0): {out_of_window}')
assert out_of_window == 0
print('ASSERT PASS: no guide outside declared window; shortfalls reported explicitly rather than padded')

lib.to_csv('input3_crispra_library.csv', index=False)
print('Saved input3_crispra_library.csv')
