"""
Re-audit 2026-09-19. Independent reconstruction of the PRE-FIX compound
hit-calling rule (per-animal FDR<0.05, not nominal p<0.05) against the
original audit's synthetic 6-animal/60-gene MAGeCK RRA output, to confirm
the fix log's claim "old rule genuinely gives 0/5 on this data" without
taking the fixer's word for it.

Input: animal_1..6.gene_summary.txt, copied unmodified from
F:\\OpenScience\\audits\\_pre-fix-20260919\\bio-crispr-screens-in-vivo-screens\\run\\mageck_out\\
"""
import pandas as pd
from statsmodels.stats.multitest import multipletests

files = {f"animal_{i}": f"animal_{i}.gene_summary.txt" for i in range(1, 7)}
dfs = {a: pd.read_csv(f, sep="\t") for a, f in files.items()}
all_r = pd.concat([d.assign(animal=a) for a, d in dfs.items()])


def add_fdr(g):
    g = g.copy()
    g["neg_fdr"] = multipletests(g["neg|p-value"], method="fdr_bh")[1]
    return g


all_r = all_r.groupby("animal", group_keys=False).apply(add_fdr)
grp = all_r.groupby("id")["neg_fdr"].apply(lambda s: (s < 0.05).sum())

print("Max animals-at-per-animal-FDR<0.05 for any of the 60 genes:", grp.max())
print(grp.sort_values(ascending=False).head(10))

# RESULT (re-audit run): max = 0 across all 60 genes, including all 5 planted
# hits (Gene000-Gene004). Independently confirms the fix log's claim that the
# pre-fix per-animal-FDR<0.05 consistency rule gave 0/5 recovered hits on this
# data -- not a cherry-picked or fabricated regression finding.
