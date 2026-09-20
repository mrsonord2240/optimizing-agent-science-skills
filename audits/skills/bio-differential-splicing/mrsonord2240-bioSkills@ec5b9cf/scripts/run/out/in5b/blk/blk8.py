import pandas as pd
import numpy as np

# `significant` = the filtered rMATS table from the rMATS section
sig = significant.copy()
sig['score'] = -np.log10(sig['FDR']) * sig['IncLevelDifference'].abs()
sig['exon_length'] = sig['exonEnd'] - sig['exonStart_0base']
sig['nmd_likely'] = (sig['exon_length'] % 3 != 0)
top_events = sig.nlargest(50, 'score')
