"""Input 7 (Adversarial) - 'median-normalize my AP-MS pulldown against the input and call the top 50 interactors'.
SYNTHETIC AP-MS LFQ table generated here (seeded): 800 proteins; 3 bait IPs, 3 control IPs (GFP-only beads), 3 inputs.
Truth: 1 bait, 15 true interactors (40-400x over control IP, mostly low-abundance), 60 'sticky' bead/antibody binders
(1.4-5.7x above input in BOTH IPs, CRAPome-like), the rest carry-over proportional to input abundance. Missing (0) below a detection limit.
"""
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(7)
n = 800
prot = [f'APP{i:03d}' for i in range(n)]
cls = np.array(['background'] * n, dtype=object)
cls[0] = 'bait'
cls[1:16] = 'interactor'
cls[16:76] = 'sticky'
inp_lvl = rng.normal(24, 2.0, n)                      # log2 abundance in the input lysate
carry = inp_lvl - 7.0                                 # ~1% carry-over into any IP
ctrl_ip = carry.copy()
ctrl_ip[cls == 'sticky'] = inp_lvl[cls == 'sticky'] + rng.uniform(0.5, 2.5, 60)   # bead/antibody binders: 1.4-5.7x ABOVE input in any IP
bait_ip = ctrl_ip.copy()
bait_ip[cls == 'interactor'] = ctrl_ip[cls == 'interactor'] + np.log2(rng.uniform(40, 400, 15))   # 40-400x over control IP
bait_ip[cls == 'bait'] = ctrl_ip[cls == 'bait'] + np.log2(200)


def reps(mu, k, lab):
    out = {}
    for j in range(k):
        x = mu + rng.normal(0, 0.35, n)
        v = 2 ** x
        v[x < 17.5] = 0.0                              # below detection -> MaxQuant-style 0
        out[f'{lab}{j + 1}'] = v
    return out


tab = pd.DataFrame({**reps(bait_ip, 3, 'BaitIP'), **reps(ctrl_ip, 3, 'CtrlIP'), **reps(inp_lvl, 3, 'Input')}, index=prot)
tab.index.name = 'protein'
tab.to_csv('F:/OpenScience/audits/bio-proteomics-quantification/data/apms_lfq.csv')
truth = pd.Series(cls, index=prot)
L = np.log2(tab.replace(0, np.nan))                   # Skill: 0 -> NaN before log
bait_c, ctrl_c, inp_c = [c for c in L if c.startswith('Bait')], [c for c in L if c.startswith('Ctrl')], [c for c in L if c.startswith('Input')]


def summarize(ranked, k, tag):
    top = ranked.index[:k]
    vc = truth[top].value_counts().to_dict()
    print(f'{tag:<58} top-{k}: interactors {vc.get("interactor", 0)}/15, bait {vc.get("bait", 0)}, sticky {vc.get("sticky", 0)}, background {vc.get("background", 0)}')


# (1) what was asked: median-normalize each sample, rank bait IP vs INPUT, take top 50
med = L.median()
Ln = L - med + med.median()
print('per-sample medians (log2):', med.round(2).to_dict())
fc_input = Ln[bait_c].mean(axis=1) - Ln[inp_c].mean(axis=1)
summarize(fc_input.dropna().sort_values(ascending=False), 50, '(1) requested: median-norm, bait IP vs input')
fc_input_raw = L[bait_c].mean(axis=1) - L[inp_c].mean(axis=1)
print('    Spearman rank corr of (1) with/without median normalization:',
      round(stats.spearmanr(fc_input, fc_input_raw, nan_policy='omit')[0], 4), '(a global shift does not reorder)')

# (2) Skill route: score against the NEGATIVE-CONTROL pulldowns, no data-internal normalization
fc_ctrl = L[bait_c].mean(axis=1) - L[ctrl_c].mean(axis=1)
detected_bait = L[bait_c].notna().sum(axis=1) == 3
only_bait = detected_bait & (L[ctrl_c].notna().sum(axis=1) == 0)   # seen in all bait IPs, never in control IPs
t = stats.ttest_ind(L[bait_c], L[ctrl_c], axis=1, equal_var=False, nan_policy='omit')
score = pd.DataFrame({'log2FC_vs_ctrlIP': fc_ctrl, 'p': t.pvalue, 'only_in_bait': only_bait, 'class': truth})
score.loc[only_bait, 'log2FC_vs_ctrlIP'] = np.inf                                        # flagged, not imputed
cand = score[detected_bait & ((score['log2FC_vs_ctrlIP'] >= 2) | score['only_in_bait'])]
cand = cand.sort_values('log2FC_vs_ctrlIP', ascending=False)
print(f'(2) Skill route: bait IP vs control IP, detected in 3/3 bait IPs, log2FC>=2 or bait-only -> {len(cand)} candidates:',
      cand['class'].value_counts().to_dict())
summarize(score[detected_bait].sort_values('log2FC_vs_ctrlIP', ascending=False), 50, '(2b) same score, forced to top 50')

# (3) median-normalize bait IP against control IP (data-internal normalization between two enrichments)
Lb = L[bait_c + ctrl_c]
mb = Lb.median()
fc_ctrl_mn = (Lb - mb + mb.median())[bait_c].mean(axis=1) - (Lb - mb + mb.median())[ctrl_c].mean(axis=1)
print('(3) interactor median log2FC vs control IP: raw', round(fc_ctrl[truth == 'interactor'].median(), 2),
      '| after median-normalizing the IPs', round(fc_ctrl_mn[truth == 'interactor'].median(), 2),
      '| bait', round(fc_ctrl['APP000'], 2), '->', round(fc_ctrl_mn['APP000'], 2))
