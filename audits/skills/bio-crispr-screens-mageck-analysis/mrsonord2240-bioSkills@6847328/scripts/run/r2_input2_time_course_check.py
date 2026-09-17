import pandas as pd
import numpy as np

def time_course_consistency(mle_results, conditions=['day7', 'day14', 'day21']):
    beta_cols = [f'{c}|beta' for c in conditions]
    fdr_cols = [f'{c}|fdr' for c in conditions]
    df = mle_results[['Gene'] + beta_cols + fdr_cols].copy()
    df['all_negative'] = (df[beta_cols] < 0).all(axis=1)
    df['all_positive'] = (df[beta_cols] > 0).all(axis=1)
    df['monotone'] = df[beta_cols].apply(lambda x: (np.diff(x) <= 0).all() or (np.diff(x) >= 0).all(), axis=1)
    df['any_sig'] = (df[fdr_cols] < 0.05).any(axis=1)
    return df[df['monotone'] & df['any_sig']].sort_values(beta_cols[-1])

for f, label in [
    ("r2_input2_timecourse_mle.gene_summary.txt", "run1 (pr=2)"),
    ("r2_input2b_rerun.gene_summary.txt", "run2 (pr=2, identical cmd)"),
    ("r2_input2c_pr10.gene_summary.txt", "run3 (pr=10)"),
    ("r2_input2d_pr10b.gene_summary.txt", "run4 (pr=10, second try)"),
]:
    gs = pd.read_csv(f, sep="\t")
    hits = time_course_consistency(gs)
    dep = sorted(g for g in hits['Gene'] if g.startswith('DEP'))
    enr = sorted(g for g in hits['Gene'] if g.startswith('ENR'))
    print(label, "-> DEP recovered:", len(dep), "/10", dep, " ENR recovered:", len(enr), "/10")

gs = pd.read_csv("r2_input2_timecourse_mle.gene_summary.txt", sep="\t")
dep = gs[gs['Gene'].str.startswith('DEP')][['Gene', 'day21|beta', 'day21|fdr', 'day21|wald-fdr']]
print(dep.to_string())
