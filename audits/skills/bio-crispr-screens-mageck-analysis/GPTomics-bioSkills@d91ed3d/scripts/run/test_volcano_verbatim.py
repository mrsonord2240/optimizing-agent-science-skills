import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def volcano(gene_summary_path, direction='neg', fdr_threshold=0.05, lfc_threshold=1.0):
    '''direction: "neg" for dropout, "pos" for enrichment.'''
    df = pd.read_csv(gene_summary_path, sep='\t')
    lfc_col = f'{direction}|lfc'
    fdr_col = f'{direction}|fdr'
    fig, ax = plt.subplots(figsize=(9, 7))
    sig = (df[fdr_col] < fdr_threshold) & (np.abs(df[lfc_col]) > lfc_threshold)
    ax.scatter(df.loc[~sig, lfc_col], -np.log10(df.loc[~sig, fdr_col].clip(lower=1e-10)),
                c='lightgray', alpha=0.4, s=10)
    return fig

fig = volcano("input1_canonical.gene_summary.txt", direction="neg")
