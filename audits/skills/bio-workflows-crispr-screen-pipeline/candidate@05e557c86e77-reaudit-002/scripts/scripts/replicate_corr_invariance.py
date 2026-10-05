import pandas as pd, numpy as np
B = 'F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline/'
for f in ['qc/hap1.count.txt', 'cn-correction/a375.count.txt']:
    t = pd.read_csv(B + f, sep='\t', index_col=0).iloc[:, 1:]
    print(f, t.shape)
    for name, tr in [('log10 raw (qc.py)', np.log10(t + 1)),
                     ('log2 raw', np.log2(t + 1)),
                     ('log2 size-factor normalized (MAGeCK count_report.Rmd style)', np.log2(t / (t.sum() / t.sum().mean()) + 1))]:
        print(name)
        print(tr.corr().round(3).to_string())
