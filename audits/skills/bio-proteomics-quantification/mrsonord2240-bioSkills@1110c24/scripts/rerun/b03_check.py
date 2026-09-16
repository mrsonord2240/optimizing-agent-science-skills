'''M4 evidence: quantification SKILL.md block b03 (median centering) executed verbatim on the SYNTHETIC MaxQuant LFQ columns.'''
import numpy as np, pandas as pd, warnings
warnings.simplefilter('always')
pg = pd.read_csv('F:/OpenScience/audits/bio-proteomics-quantification/data/proteinGroups.txt', sep='\t', low_memory=False)
intensities = pg[[c for c in pg.columns if c.startswith('LFQ intensity ')]]
ns = {'intensities': intensities}
with warnings.catch_warnings(record=True) as w:
    with open('F:/OpenScience/audits/bio-proteomics-quantification/rerun/blocks/b03_Median_center_label_free_intensities_a_n.py', encoding='utf-8') as fh:
        exec(fh.read(), ns)
    print('warnings:', [str(x.message) for x in w])
print('-inf:', int(np.isinf(ns['normalized'].values).sum()), '| medians after:', np.round(ns['normalized'].median().values, 3))
