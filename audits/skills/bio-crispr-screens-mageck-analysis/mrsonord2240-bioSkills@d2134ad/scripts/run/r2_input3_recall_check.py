import pandas as pd
gt = pd.read_csv("r2_heavy_selection_ground_truth.txt", sep="\t")
depleted = set(gt[gt['truth'] == 'depleted']['Gene'])
enriched = set(gt[gt['truth'] == 'enriched']['Gene'])

for f, label in [
    ("r2_input3_median.gene_summary.txt", "median"),
    ("r2_input3_control.gene_summary.txt", "control"),
]:
    gs = pd.read_csv(f, sep="\t")
    dep_recall = gs[gs['id'].isin(depleted)]
    enr_recall = gs[gs['id'].isin(enriched)]
    dep_hit = (dep_recall['neg|fdr'] < 0.05).sum()
    enr_hit = (enr_recall['pos|fdr'] < 0.05).sum()
    print(label, "depleted recall:", dep_hit, "/", len(dep_recall),
          " enriched recall:", enr_hit, "/", len(enr_recall))
