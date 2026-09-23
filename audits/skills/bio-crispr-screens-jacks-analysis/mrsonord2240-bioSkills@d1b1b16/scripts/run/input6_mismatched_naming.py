"""
Input 6 (Adversarial). sgRNA-to-gene naming mismatch -- SKILL.md's own Common Errors
example (e.g. BRCA1_1 vs BRCA1.1). Regression of pre-fix Input 6. Builds a 2000-guide
HAP1 subset and corrupts every other guide's ID in the guidemap only (underscore -> dot),
matching SKILL.md's own example. Verifies the P2 fix: SKILL.md's Common Errors table now
says "genes missing from output entirely" (not "Many NaN gene effects").
"""
import subprocess, sys, os
import pandas as pd

JACKS_DIR = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks"
DATA = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\data"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out6"
os.makedirs(OUT, exist_ok=True)

counts = pd.read_csv(f"{DATA}/hap1_counts.txt", sep='\t')
guidemap = pd.read_csv(f"{DATA}/hap1_guidemap.txt", sep='\t')

sub_genes = counts['gene'].drop_duplicates().head(300)
counts_sub = counts[counts['gene'].isin(sub_genes)].reset_index(drop=True)
guidemap_sub = guidemap[guidemap['sgRNA'].isin(counts_sub['sgRNA'])].reset_index(drop=True)
n_genes_expected = counts_sub['gene'].nunique()
print(f"Subset: {len(counts_sub)} guides, {n_genes_expected} genes expected")

counts_sub_path = f"{OUT}/counts_sub.txt"
counts_sub.to_csv(counts_sub_path, sep='\t', index=False)

# Corrupt every other guide's ID in the guidemap only (underscore -> dot), leaving the
# count file's IDs untouched -- exactly SKILL.md's BRCA1_1 vs BRCA1.1 example.
guidemap_corrupt = guidemap_sub.copy()
mask = guidemap_corrupt.index % 2 == 0
guidemap_corrupt.loc[mask, 'sgRNA'] = guidemap_corrupt.loc[mask, 'sgRNA'].str.replace('_', '.', n=1, regex=False)
guidemap_corrupt_path = f"{OUT}/guidemap_mismatched.txt"
guidemap_corrupt.to_csv(guidemap_corrupt_path, sep='\t', index=False)
n_corrupted = mask.sum()
print(f"Corrupted {n_corrupted} of {len(guidemap_corrupt)} guide IDs in the guidemap")

repmap = pd.DataFrame({
    'Replicate': ['HAP1_T0', 'HAP1_T18A', 'HAP1_T18B', 'HAP1_T18C'],
    'Sample': ['T0', 'T18', 'T18', 'T18'],
    'Control': ['T0', 'T0', 'T0', 'T0'],
})
repmap_path = f"{OUT}/repmap.txt"
repmap.to_csv(repmap_path, sep='\t', index=False)

cmd = [
    sys.executable, "run_JACKS.py",
    counts_sub_path, repmap_path, guidemap_corrupt_path,
    "--rep_hdr", "Replicate", "--sample_hdr", "Sample", "--ctrl_sample_hdr", "Control",
    "--sgrna_hdr", "sgRNA", "--gene_hdr", "Gene",
    "--outprefix", f"{OUT}/mismatch_run",
]
result = subprocess.run(cmd, capture_output=True, text=True, cwd=JACKS_DIR)
print(f"returncode={result.returncode}")
if result.returncode != 0:
    print("FULL STDERR:\n", result.stderr)
    sys.exit(1)

genes_out = pd.read_csv(f"{OUT}/mismatch_run_gene_JACKS_results.txt", sep='\t')
n_genes_out = len(genes_out)
print(f"\nGenes returned: {n_genes_out} vs expected: {n_genes_expected}")
print(f"SKILL.md's suggested sanity check (len == n_genes_expected) detects mismatch: {n_genes_out != n_genes_expected}")

n_nan = genes_out.isna().sum().sum()
print(f"\nNaN cells in gene output: {n_nan}")
if n_nan == 0 and n_genes_out < n_genes_expected:
    print("PASS: SKILL.md's corrected symptom ('genes missing from output entirely, no NaN') matches observed behavior.")
elif n_nan > 0:
    print("FAIL: NaN values found -- SKILL.md's corrected symptom description does NOT match (would mean the P2 fix mis-describes real behavior).")
else:
    print("NOTE: gene count matches expected -- mismatch not manifesting in this subset; re-check corruption rate/coverage.")
