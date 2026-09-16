import numpy as np

# Arg10/Lys8 is the common pairing (avoids overlap with the +6 isotope envelope)
SILAC_SHIFTS = {'Arg10': 10.008269, 'Lys8': 8.014199, 'Arg6': 6.020129, 'Lys6': 6.020129}

def silac_log2_ratio(heavy, light):
    '''Vectorized over arrays/Series: log2 H/L (NaN unless both channels quantified) plus a presence flag.'''
    heavy, light = np.asarray(heavy, dtype=float), np.asarray(light, dtype=float)
    h, l = heavy > 0, light > 0    # NaN compares False
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = np.where(h & l, np.log2(heavy / light), np.nan)
    presence = np.select([h & l, h, l], ['both', 'H-only', 'L-only'], default='none')    # report H-only/L-only separately
    return ratio, presence
