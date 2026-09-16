import numpy as np, pandas as pd

def score_vs_control_ips(ip, bait_cols, ctrl_cols, fc_cutoff=2.0, min_bait_reps=None):
    '''ip: prey x replicate RAW intensities or spectral counts; 0/NaN = not detected. Prey never
    seen in any bait IP get a NaN enrichment (nothing was measured) and are never called.'''
    L = np.log2(ip[list(bait_cols) + list(ctrl_cols)].replace(0, np.nan).astype(float))
    if min_bait_reps is None:
        min_bait_reps = len(bait_cols)          # default: every bait replicate, reproducibility first
    n_bait, n_ctrl = L[bait_cols].notna().sum(axis=1), L[ctrl_cols].notna().sum(axis=1)
    Lf = L.copy()
    Lf[ctrl_cols] = Lf[ctrl_cols].fillna(L[ctrl_cols].min())      # per-control-run detection floor
    enrich = Lf[bait_cols].mean(axis=1) - Lf[ctrl_cols].mean(axis=1)
    worst = Lf[bait_cols].min(axis=1) - Lf[ctrl_cols].max(axis=1)  # weakest bait rep vs best control
    out = pd.DataFrame({'n_bait': n_bait, 'n_ctrl': n_ctrl,
                        'log2_enrichment': enrich, 'worst_case_log2': worst})
    out['interactor'] = (n_bait >= min_bait_reps) & ((n_ctrl == 0) | (enrich >= fc_cutoff))
    return out.sort_values('log2_enrichment', ascending=False)
