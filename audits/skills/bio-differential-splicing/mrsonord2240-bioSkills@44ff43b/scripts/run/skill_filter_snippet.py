#!/usr/bin/env python3
"""SKILL.md 'rMATS-turbo Differential Analysis' python block, copied verbatim, parameterised only by input path.
Adds printed assertions on the result (audit additions are below the marker)."""
import sys
import pandas as pd
import numpy as np

path = sys.argv[1]
se = pd.read_csv(path, sep='\t')

# ---- verbatim from SKILL.md (only the read_csv path differs) ----
def min_per_rep(s):
    return s.str.split(',').apply(lambda x: min(int(v) for v in x))

se['min_inc'] = min_per_rep(se['IJC_SAMPLE_1']).combine(min_per_rep(se['IJC_SAMPLE_2']), min)
se['min_skip'] = min_per_rep(se['SJC_SAMPLE_1']).combine(min_per_rep(se['SJC_SAMPLE_2']), min)

significant = se[
    (se['FDR'] < 0.05) &
    (se['IncLevelDifference'].abs() > 0.10) &
    ((se['min_inc'] + se['min_skip']) >= 10)
].copy()

significant['score'] = -np.log10(significant['FDR']) * significant['IncLevelDifference'].abs()
top = significant.nlargest(50, 'score')
# ---- end verbatim ----

# ---- audit additions ----
print('events in file:', len(se))
print('significant after FDR<0.05, |dPSI|>0.10, min_inc+min_skip>=10:', len(significant))
print(top[['GeneID', 'exonStart_0base', 'FDR', 'IncLevelDifference', 'min_inc', 'min_skip', 'score']].head(10).to_string())
if len(sys.argv) > 2 and sys.argv[2] == 'planted':
    assert len(significant) == 1
    r = significant.iloc[0]
    assert abs(r['IncLevelDifference'] - 0.586966) < 0.002, r['IncLevelDifference']
    # min across BOTH groups: inc min is G2's 20, skip min is G1's 10 (per-replicate junction counts from expected.json)
    assert r['min_inc'] == 20 and r['min_skip'] == 10
    print('ASSERT OK: planted event recovered, dPSI %.3f (truth 0.587), min_inc %d, min_skip %d' % (r['IncLevelDifference'], r['min_inc'], r['min_skip']))
    # 'Result Prioritization' block (verbatim from SKILL.md, 'sig' = significant)
    sig = significant
    sig['exon_length'] = sig['exonEnd'] - sig['exonStart_0base']
    sig['nmd_likely'] = (sig['exon_length'] % 3 != 0)
    print('Result Prioritization block: exon_length', int(sig['exon_length'].iloc[0]), 'nmd_likely', bool(sig['nmd_likely'].iloc[0]))
