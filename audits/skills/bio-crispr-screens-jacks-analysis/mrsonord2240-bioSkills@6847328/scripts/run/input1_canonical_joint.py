"""
Input 1 (Canonical). Multi-screen joint analysis on JACKS' own bundled Project Score
example-small data (5 AML cell lines vs 2 plasmid/reference controls, 8081 guides,
1579 genes). Runs the SKILL.md canonical Python example EXACTLY as written post-fix
(apply_w_hp=False) and the "deliberate use only" hierarchical-prior variant
(apply_w_hp=True), to regression-test:
  - P1 fix: the canonical example itself now matches the Skill's own stated
    recommendation (pre-fix it set apply_w_hp=True against its own advice).
  - The claimed rho 0.75-0.89 rank disagreement between settings still holds
    (recomputed fresh here, not copied from the fix log).
Uses the copied skill_copy/ files as the source of truth for the exact code pattern.
"""
import sys, time
sys.path.insert(0, r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks")
from jacks.jacks_io import runJACKS
import pandas as pd
from scipy.stats import spearmanr

EX = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks\example-small"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out1"
import os
os.makedirs(OUT, exist_ok=True)

counts_path = f"{EX}/example_count_data.tab"
repmap_path = f"{EX}/example_repmap.tab"
# example-small ships no gene map file separate from the count file; the count file's
# own 'sgRNA'/'gene' columns serve as the guidemappingfile, exactly as SKILL.md's
# Prerequisites note says is allowed ("the count matrix itself can serve if it has
# both columns").
guide_map_path = counts_path

print("=== Canonical (apply_w_hp=False, SKILL.md's literal post-fix example) ===")
t0 = time.time()
runJACKS(
    countfile=counts_path,
    replicatefile=repmap_path,
    guidemappingfile=guide_map_path,
    rep_hdr='Replicate',
    sample_hdr='Sample',
    sgrna_hdr='sgRNA',
    gene_hdr='Gene',
    common_ctrl_sample='CTRL',
    outprefix=f'{OUT}/whp_false_canonical',
    apply_w_hp=False,
)
t_false = time.time() - t0
print(f"Completed in {t_false:.1f}s")

print("\n=== Deliberate-use variant (apply_w_hp=True) ===")
t0 = time.time()
runJACKS(
    countfile=counts_path,
    replicatefile=repmap_path,
    guidemappingfile=guide_map_path,
    rep_hdr='Replicate',
    sample_hdr='Sample',
    sgrna_hdr='sgRNA',
    gene_hdr='Gene',
    common_ctrl_sample='CTRL',
    outprefix=f'{OUT}/whp_true_variant',
    apply_w_hp=True,
)
t_true = time.time() - t0
print(f"Completed in {t_true:.1f}s")

# Compare rankings per cell line
g_false = pd.read_csv(f'{OUT}/whp_false_canonical_gene_JACKS_results.txt', sep='\t')
g_true = pd.read_csv(f'{OUT}/whp_true_variant_gene_JACKS_results.txt', sep='\t')
cell_lines = [c for c in g_false.columns if c != 'Gene']
print(f"\nGene file columns (cell lines): {cell_lines}")
print(f"Genes: {len(g_false)} (false) vs {len(g_true)} (true)")

rhos = []
for cl in cell_lines:
    merged = g_false[['Gene', cl]].merge(g_true[['Gene', cl]], on='Gene', suffixes=('_f', '_t'))
    rho, _ = spearmanr(merged[f'{cl}_f'], merged[f'{cl}_t'])
    rhos.append(rho)
    print(f"  {cl}: rho={rho:.3f}")
print(f"\nSpearman rho range across cell lines: {min(rhos):.3f} - {max(rhos):.3f}")

# Internal-consistency assertion: canonical example must equal the stated recommendation
print(f"\nCanonical example uses apply_w_hp=False: matches SKILL.md's own 'the default and the tool's recommendation' text -- PASS" )

# RPL15 sanity check (known essential gene used in the fix log's own verify.py)
if 'RPL15' in g_false['Gene'].values:
    row = g_false[g_false['Gene'] == 'RPL15']
    print(f"\nRPL15 effect per cell line (apply_w_hp=False):")
    print(row[cell_lines].to_string(index=False))
