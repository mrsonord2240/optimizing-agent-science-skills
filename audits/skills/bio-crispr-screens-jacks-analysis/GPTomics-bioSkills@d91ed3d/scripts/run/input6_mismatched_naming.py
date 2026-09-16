"""
Input 6 (Adversarial) -- SKILL.md's "sgRNA-to-gene map mismatch" Common Error: guide map
and count matrix use different sgRNA naming conventions. Deliberately corrupt half the
sgRNA IDs in the guidemap (BRCA1_1-style vs a dotted variant) relative to the countfile,
on a subset of the real HAP1 data, and check whether the actual symptom matches SKILL.md's
claim ("Many genes missing from output... NaN gene effects" / "sanity check
len(jacks_output) == n_genes_expected").
"""
import pandas as pd
from jacks.jacks_io import runJACKS

D = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\data"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out6"
import os
os.makedirs(OUT, exist_ok=True)

counts = pd.read_csv(f"{D}/hap1_counts.txt", sep='\t')
guidemap = pd.read_csv(f"{D}/hap1_guidemap.txt", sep='\t')

# Take a manageable subset: first 2000 guides
counts_sub = counts.head(2000).copy()
guidemap_sub = guidemap.head(2000).copy()

# Corrupt every other guide's ID in the guidemap only (simulate a naming-convention drift,
# e.g. underscore -> dot, exactly the BRCA1_1 vs BRCA1.1 example SKILL.md gives)
mask = guidemap_sub.index % 2 == 1
guidemap_sub.loc[mask, 'sgRNA'] = guidemap_sub.loc[mask, 'sgRNA'].str.replace('_', '.', regex=False)

counts_sub.to_csv(f"{OUT}/counts_sub.txt", sep='\t', index=False)
guidemap_sub.to_csv(f"{OUT}/guidemap_mismatched.txt", sep='\t', index=False)

n_genes_expected_correct = guidemap_sub['Gene'].nunique()  # what len(jacks_output) 'should' be per SKILL.md's own check

repmap = pd.read_csv(f"{D}/hap1_repmap.txt", sep='\t')
repmap.to_csv(f"{OUT}/repmap.txt", sep='\t', index=False)

runJACKS(
    countfile=f"{OUT}/counts_sub.txt",
    replicatefile=f"{OUT}/repmap.txt",
    guidemappingfile=f"{OUT}/guidemap_mismatched.txt",
    rep_hdr='Replicate', sample_hdr='Sample', common_ctrl_sample='T0',
    sgrna_hdr='sgRNA', gene_hdr='Gene',
    outprefix=f"{OUT}/mismatch_run",
)

genes = pd.read_csv(f"{OUT}/mismatch_run_gene_JACKS_results.txt", sep='\t')
print("n_genes_expected (unique genes in corrupted guidemap):", n_genes_expected_correct)
print("len(jacks_output) actual gene rows:", len(genes))
nan_rows = genes.drop(columns=['Gene']).isna().any(axis=1).sum()
blank_rows = (genes.drop(columns=['Gene']) == '').all(axis=1).sum() if genes.drop(columns=['Gene']).dtypes.iloc[0]==object else 'n/a(numeric dtype)'
print("Rows with NaN value:", nan_rows)
print(genes.head(5).to_string(index=False))
