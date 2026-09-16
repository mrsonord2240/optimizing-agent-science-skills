'''Data-import Input 2 (regression): DIA-NN 1.9 report.parquet (8 runs) -> protein x run matrix at 1% FDR. SYNTHETIC data
with 60 LOWCONF groups (pass run-level q, Global.PG.Q.Value 0.04). SKILL.md block b03 executed verbatim.'''
import os, warnings, numpy as np, pandas as pd
os.chdir('F:/OpenScience/audits/bio-proteomics-data-import/rerun/work')
warnings.simplefilter('always')
ns = {}
with warnings.catch_warnings(record=True) as w:
    with open('../blocks/b03_Loading_DIA_NN_report_parquet.py', encoding='utf-8') as fh:
        exec(fh.read(), ns)
    print('warnings:', [str(x.message) for x in w])
raw = pd.read_parquet('report.parquet'); m = ns['matrix']
print(f'report rows {len(raw)} | after filter {len(ns["report"])} | matrix {m.shape} | -inf {int(np.isinf(m.values).sum())} | NaN cells {int(m.isna().sum().sum())}')
print('LOWCONF groups in raw:', raw.loc[raw['Protein.Group'].str.startswith('LOWCONF'), 'Protein.Group'].nunique(),
      '| surviving in matrix:', int(m.index.str.startswith('LOWCONF').sum()))
print('zero PG.MaxLFQ cells among filtered rows:', int((ns['report']['PG.MaxLFQ'] == 0).sum()), '| max distinct PG.MaxLFQ per group x run:',
      int(ns['report'].groupby(['Protein.Group', 'Run'])['PG.MaxLFQ'].nunique().max()))
print('Lib.PG.Q.Value column present (1.9.x MBR alternative):', 'Lib.PG.Q.Value' in raw.columns)
