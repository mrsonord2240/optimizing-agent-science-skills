"""Input 4 (Variant B): motif enrichment of protein-adjusted up-regulated sites against an experiment-matched
background, then KSEA-style kinase z-scores. SYNTHETIC data; the kinase-substrate prior is SYNTHETIC too
(no PhosphoSitePlus download here, KSEAapp not installed) - it only exercises the arithmetic.

Steps follow SKILL.md: 'Motif Analysis with the Correct Background' (lines 175-198) and the KSEA row of the
Kinase-activity table (line 82: 'z-score of a kinase's substrate fold-changes'). The Skill's block only defines
position_frequencies(); background construction, the enrichment test and KSEA are agent-written.
"""
import os
from collections import Counter
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests

D = 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho'
R = 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/runs'
rng = np.random.default_rng(7)

# ---- Skill block (lines 184-195) with `confident` bound to the class-I table the expansion block produced
phospho = pd.read_csv(os.path.join(D, 'Phospho (STY)Sites.txt'), sep='\t', low_memory=False)
phospho = phospho[(phospho['Reverse'] != '+') & (phospho['Potential contaminant'] != '+')]
confident = phospho[phospho['Localization prob'] >= 0.75].copy()     # the name the Skill's motif block expects
WINDOW_HALF = 7


def position_frequencies(windows):
    counts = {i: Counter() for i in range(-WINDOW_HALF, WINDOW_HALF + 1)}
    for w in windows:
        for offset, aa in zip(range(-WINDOW_HALF, WINDOW_HALF + 1), w):
            if aa not in '_X':
                counts[offset][aa] += 1
    return counts


# ---- foreground: ADJUSTED.Model sites, significant and up in Treatment
adj = pd.read_csv(os.path.join(R, 'in1_adjusted_model.csv'))
print('contrast label in ADJUSTED.Model:', adj['Label'].unique().tolist(), '-> log2FC = Control - Treatment')
adj = adj[adj['Protein'].str.match(r'^P\d{5}_[STY]\d+$')].copy()     # singly-modified site rows only
adj['fc_T_vs_C'] = -adj['log2FC']                                     # flip to Treatment - Control
adj['acc'] = adj['Protein'].str.split('_').str[0]
adj['pos'] = adj['Protein'].str.extract(r'_[STY](\d+)$')[0].astype(int)
win = confident.set_index(['Protein', 'Position'])['Sequence window'].to_dict()
adj['window'] = [win.get((a, p)) for a, p in zip(adj['acc'], adj['pos'])]
up = adj[(adj['adj.pvalue'] < 0.05) & (adj['fc_T_vs_C'] > 0) & adj['window'].notna()]
down = adj[(adj['adj.pvalue'] < 0.05) & (adj['fc_T_vs_C'] < 0) & adj['window'].notna()]
fg = [w[15 - WINDOW_HALF: 16 + WINDOW_HALF] for w in up['window'] if isinstance(w, str) and len(w) >= 31]
print('foreground (adjusted, up, class I):', len(fg), 'sites | down:', len(down))

# ---- background A: every S/T in the identified proteins (experiment-matched, central residue preserved)
fasta, acc = {}, None
for line in open(os.path.join(D, 'synthetic.fasta'), encoding='utf-8'):
    if line.startswith('>'):
        acc = line.split('|')[1]
        fasta[acc] = ''
    else:
        fasta[acc] += line.strip()
ident = set(confident['Protein'])
bgA = []
for a in ident:
    s = fasta[a]
    for i, ch in enumerate(s):
        if ch in 'ST':
            bgA.append(''.join(s[j] if 0 <= j < len(s) else '_' for j in range(i - WINDOW_HALF, i + WINDOW_HALF + 1)))
# ---- background B: all identified class-I sites (the other 'matched dataset' reading)
bgB = [w[15 - WINDOW_HALF: 16 + WINDOW_HALF] for w in confident['Sequence window']]


def enrich(fgw, bgw, label):
    f, b = position_frequencies(fgw), position_frequencies(bgw)
    rows = []
    for off in range(-WINDOW_HALF, WINDOW_HALF + 1):
        if off == 0:
            continue
        nf, nb = sum(f[off].values()), sum(b[off].values())
        for aa in set(f[off]):
            a, c = f[off][aa], b[off][aa]
            odds, p = fisher_exact([[a, nf - a], [c, nb - c]], alternative='greater')
            rows.append((off, aa, a, nf, c, nb, p))
    t = pd.DataFrame(rows, columns=['offset', 'aa', 'fg_n', 'fg_tot', 'bg_n', 'bg_tot', 'p'])
    t['q'] = multipletests(t['p'], method='fdr_bh')[1]
    print(f'\n{label}: top positions (Fisher one-sided, BH)')
    print(t.sort_values('p').head(4).to_string(index=False))


enrich(fg, bgA, 'Background A = all S/T in identified proteins')
enrich(fg, bgB, 'Background B = all identified class-I sites')

# ---- KSEA (Casado 2013): z = (mean_substrate_FC - mean_all_FC) * sqrt(m) / sd_all_FC
# SYNTHETIC prior in PhosphoSitePlus column layout: proline-directed kinase <- S/T-P sites, basophilic <- R-x-x-S/T sites
prior = []
for _, r in confident.iterrows():
    w = r['Sequence window']
    if w[16] == 'P' and r['Amino acid'] in 'ST':
        prior.append(('SYN_PRO_KINASE', r['Protein'], f"{r['Amino acid']}{r['Position']}"))
    if w[12] == 'R' and r['Amino acid'] in 'ST':
        prior.append(('SYN_BASO_KINASE', r['Protein'], f"{r['Amino acid']}{r['Position']}"))
for _, r in confident.sample(6, random_state=3).iterrows():
    prior.append(('SYN_RANDOM_KINASE', r['Protein'], f"{r['Amino acid']}{r['Position']}"))
prior = pd.DataFrame(prior, columns=['KINASE', 'SUB_ACC_ID', 'SUB_MOD_RSD'])
prior.to_csv(os.path.join(D, 'kinase_substrate_SYNTHETIC.tsv'), sep='\t', index=False)
fcs = adj.dropna(subset=['fc_T_vs_C'])
fcs = fcs[np.isfinite(fcs['fc_T_vs_C'])]
fcs['key'] = fcs['acc'] + '_' + fcs['Protein'].str.split('_').str[1]
mu, sd = fcs['fc_T_vs_C'].mean(), fcs['fc_T_vs_C'].std()
print('\nKSEA z-scores on ADJUSTED log2FC (Treatment - Control); SYNTHETIC prior:')
for k, g in prior.groupby('KINASE'):
    keys = set(g['SUB_ACC_ID'] + '_' + g['SUB_MOD_RSD'])
    sub = fcs[fcs['key'].isin(keys)]
    m = len(sub)
    z = (sub['fc_T_vs_C'].mean() - mu) * np.sqrt(m) / sd if m else np.nan
    z_unflipped = (-sub['fc_T_vs_C'].mean() + mu) * np.sqrt(m) / sd if m else np.nan
    print(f'  {k:18s} m={m:2d}  z={z:+.2f}   (if the Label direction is not flipped: z={z_unflipped:+.2f})')
