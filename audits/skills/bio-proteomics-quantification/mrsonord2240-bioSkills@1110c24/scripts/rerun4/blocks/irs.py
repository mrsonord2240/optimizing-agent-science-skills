import numpy as np
import pandas as pd

# protein_psm_sums: protein x channel, summed PSM reporter ions; one reference channel per plex
def sample_loading_normalize(plex):
    target = plex.sum(axis=0).mean()    # common target = mean column sum within the plex
    return plex * (target / plex.sum(axis=0))

def irs_scale(plexes, ref_cols):
    refs = pd.concat([p[ref] for p, ref in zip(plexes, ref_cols)], axis=1)
    refs = refs.where(refs > 0)    # a 0 or missing reference cannot anchor the bridge
    unbridged = refs.index[refs.isna().any(axis=1)]
    if len(unbridged):
        print(f'IRS: {len(unbridged)} proteins lack a reference in >=1 plex; set to NaN: {list(unbridged[:10])}')
    geomean = np.exp(np.log(refs).mean(axis=1, skipna=False))    # per-protein geometric mean of references
    out = []
    for i, p in enumerate(plexes):
        factor = geomean / refs.iloc[:, i]    # per-protein per-plex scaling factor
        out.append(p.mul(factor, axis=0))
    return out
