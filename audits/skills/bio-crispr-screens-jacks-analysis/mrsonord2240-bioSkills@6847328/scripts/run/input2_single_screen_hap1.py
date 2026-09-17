"""
Input 2 (Variant A). Single-screen essentiality on real HAP1 TKOv3 data, run via the
exact CLI pattern SKILL.md documents post-fix -- from JACKS/jacks/ (regression-tests the
P1 fix: SKILL.md previously said "script at JACKS repo root", contradicting the real
layout). Benchmarks JACKS effect/std against CEGv2/NEGv1 (AUC), regression of pre-fix
Input 2 (previously AUC 0.996).
"""
import subprocess, sys, os, time
import pandas as pd
from sklearn.metrics import roc_auc_score

JACKS_DIR = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks"
DATA = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\data"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out2"
os.makedirs(OUT, exist_ok=True)

# Build a Control column since HAP1 has a single shared control (T0) for all treated
# reps, matching SKILL.md's ctrl_sample_hdr='Control' documented pattern.
repmap = pd.read_csv(f"{DATA}/hap1_repmap.txt", sep='\t')
repmap['Control'] = 'T0'  # ctrl_sample_hdr names a Sample-level id, not a Replicate id
repmap.to_csv(f"{OUT}/hap1_repmap_ctrl.txt", sep='\t', index=False)
print(repmap.to_string(index=False))

cmd = [
    sys.executable, "run_JACKS.py",
    f"{DATA}/hap1_counts.txt",
    f"{OUT}/hap1_repmap_ctrl.txt",
    f"{DATA}/hap1_guidemap.txt",
    "--rep_hdr", "Replicate",
    "--sample_hdr", "Sample",
    "--ctrl_sample_hdr", "Control",
    "--sgrna_hdr", "sgRNA",
    "--gene_hdr", "Gene",
    "--outprefix", f"{OUT}/hap1_single",
]
print("\n=== Running exactly SKILL.md's documented CLI invocation, cwd=JACKS/jacks/ ===")
print(" ".join(cmd))
t0 = time.time()
result = subprocess.run(cmd, capture_output=True, text=True, cwd=JACKS_DIR)
elapsed = time.time() - t0
print(f"\nreturncode={result.returncode}  elapsed={elapsed:.1f}s")
print("STDERR tail:\n", "\n".join(result.stderr.splitlines()[-15:]))
if result.returncode != 0:
    print("FULL STDERR:\n", result.stderr)
    sys.exit(1)

genes = pd.read_csv(f'{OUT}/hap1_single_gene_JACKS_results.txt', sep='\t')
stds = pd.read_csv(f'{OUT}/hap1_single_gene_std_JACKS_results.txt', sep='\t')
cell_line = [c for c in genes.columns if c != 'Gene'][0]
merged = genes[['Gene', cell_line]].merge(stds[['Gene', cell_line]], on='Gene', suffixes=('_effect', '_std'))
merged['z'] = merged[f'{cell_line}_effect'] / merged[f'{cell_line}_std']
print(f"\nGenes tested: {len(merged)}")

ceg = set(pd.read_csv(r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\CEGv2_core_essentials.txt", sep='\t')['GENE'])
neg = set(pd.read_csv(r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\NEGv1_nonessentials.txt", sep='\t')['GENE'])
bench = merged[merged['Gene'].isin(ceg | neg)].copy()
bench['is_essential'] = bench['Gene'].isin(ceg).astype(int)
print(f"Benchmark genes present (CEGv2 union NEGv1): {len(bench)}  (CEG={bench['is_essential'].sum()}, NEG={(1-bench['is_essential']).sum()})")

auc_effect = roc_auc_score(bench['is_essential'], -bench[f'{cell_line}_effect'])
auc_z = roc_auc_score(bench['is_essential'], -bench['z'])
print(f"AUC (effect, more negative = essential): {auc_effect:.4f}")
print(f"AUC (z=effect/std): {auc_z:.4f}")

top_hits = merged.sort_values('z').head(15)['Gene'].tolist()
known_essential = ['POLR2L', 'POLR3H', 'GTPBP10', 'PCNA', 'MRPL53', 'RRM1', 'SDHB', 'PES1', 'EIF3A']
overlap = [g for g in known_essential if g in top_hits]
print(f"Top 15 hits by z: {top_hits}")
print(f"Independently-verified essentials (MAGeCK/BAGEL2/drugZ, per public-data/README.md) present in top 15: {overlap}")
