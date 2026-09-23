"""
Input 7 (Variant B, NEW -- not in the pre-fix audit). Regression-tests three claims the
fix log says were internal contradictions in the pre-fix Skill:
  (1) Determinism: gene effects and guide efficacies are identical across reruns on
      identical input (Model section now states this; pre-fix text told users to "set
      a seed" for gene effects, which have none).
  (2) Iteration cap: variational inference is capped at n_iter=50 per gene (not the
      pre-fix "5000+ for publication" claim), and the documented n_iter override recipe
      in the "MCMC / variational convergence failure" Failure Mode runs.
  (3) p-value file: Python API needs BOTH ctrl_genes AND n_pseudo>0 to write a
      gene_pval file (n_pseudo Python default=0 vs CLI default=2000) -- SKILL.md's
      Python example now notes n_pseudo must be set explicitly.
"""
import sys, os, functools
sys.path.insert(0, r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks")
import jacks.infer
from jacks.jacks_io import runJACKS
import pandas as pd

EX = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks\example-small"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out7"
os.makedirs(OUT, exist_ok=True)
counts_path = f"{EX}/example_count_data.tab"
repmap_path = f"{EX}/example_repmap.tab"

common = dict(countfile=counts_path, replicatefile=repmap_path, guidemappingfile=counts_path,
              rep_hdr='Replicate', sample_hdr='Sample', common_ctrl_sample='CTRL',
              sgrna_hdr='sgRNA', gene_hdr='Gene', apply_w_hp=False)

print("=== (1) Determinism: two identical runs on identical input ===")
runJACKS(outprefix=f'{OUT}/run_a', **common)
runJACKS(outprefix=f'{OUT}/run_b', **common)
ga = pd.read_csv(f'{OUT}/run_a_gene_JACKS_results.txt', sep='\t')
gb = pd.read_csv(f'{OUT}/run_b_gene_JACKS_results.txt', sep='\t')
qa = pd.read_csv(f'{OUT}/run_a_grna_JACKS_results.txt', sep='\t')
qb = pd.read_csv(f'{OUT}/run_b_grna_JACKS_results.txt', sep='\t')
gene_identical = ga.equals(gb)
grna_identical = qa.equals(qb)
print(f"Gene effect files byte-for-byte identical across reruns: {gene_identical}")
print(f"Guide efficacy files byte-for-byte identical across reruns: {grna_identical}")
if gene_identical and grna_identical:
    print("PASS: gene effects and efficacies are deterministic (no seed needed), matching SKILL.md's corrected Model section.")
else:
    print("FAIL: outputs differ between identical reruns -- SKILL.md's determinism claim does NOT hold.")

print("\n=== (2) Iteration cap: n_iter=50 default confirmed via inferJACKS signature (see prior inspection); "
      "run the documented override recipe (MCMC / variational convergence failure Failure Mode) ===")
import inspect
sig = inspect.signature(jacks.infer.inferJACKS)
print(f"jacks.infer.inferJACKS default n_iter: {sig.parameters['n_iter'].default}")
assert sig.parameters['n_iter'].default == 50, "FAIL: SKILL.md's claimed 50-iteration cap does not match installed JACKS 0.2"
print("PASS: installed JACKS 0.2 default n_iter=50 matches SKILL.md's Quantitative Thresholds table.")

# Verbatim override recipe from SKILL.md's convergence-failure Failure Mode
import jacks.jacks_io
_default_infer = jacks.jacks_io.inferJACKS if hasattr(jacks.jacks_io, 'inferJACKS') else jacks.infer.inferJACKS
try:
    jacks.jacks_io.inferJACKS = functools.partial(jacks.infer.inferJACKS, n_iter=500)
    runJACKS(outprefix=f'{OUT}/run_it500', **common)
    print("PASS: n_iter=500 override recipe (as documented) ran to completion.")
finally:
    jacks.jacks_io.inferJACKS = _default_infer
    print("Restored jacks.jacks_io.inferJACKS to default after override.")

g500 = pd.read_csv(f'{OUT}/run_it500_gene_JACKS_results.txt', sep='\t')
cell_lines = [c for c in ga.columns if c != 'Gene']
n_changed = 0
for cl in cell_lines:
    merged = ga[['Gene', cl]].merge(g500[['Gene', cl]], on='Gene', suffixes=('_50', '_500'))
    n_changed += (merged[f'{cl}_50'].round(4) != merged[f'{cl}_500'].round(4)).sum()
print(f"Gene-effect cells changed between n_iter=50 (default) and n_iter=500 (override): {n_changed} "
      f"of {len(ga) * len(cell_lines)}")

print("\n=== (3) p-value file: Python API n_pseudo default=0 requires explicit n_pseudo>0 ===")
ctrl_genes_path = f"{OUT}/ctrl_genes.txt"
# Use a handful of real genes present in this dataset as a synthetic control-gene list
# (not claiming these are biologically validated negative controls -- purely to exercise
# the --ctrl_genes / n_pseudo code path as SKILL.md documents it).
sample_genes = ga['Gene'].sample(20, random_state=1).tolist()
pd.Series(sample_genes).to_csv(ctrl_genes_path, index=False, header=False)

runJACKS(outprefix=f'{OUT}/run_nopval', ctrl_genes=ctrl_genes_path, **common)  # n_pseudo left at Python default 0
pval_missing = not os.path.exists(f'{OUT}/run_nopval_gene_pval_JACKS_results.txt')
print(f"ctrl_genes supplied, n_pseudo left at Python default (0): pval file written = {not pval_missing}")

runJACKS(outprefix=f'{OUT}/run_withpval', ctrl_genes=ctrl_genes_path, n_pseudo=2000, **common)
pval_present = os.path.exists(f'{OUT}/run_withpval_gene_pval_JACKS_results.txt')
print(f"ctrl_genes supplied, n_pseudo=2000 (CLI default): pval file written = {pval_present}")

if pval_missing and pval_present:
    print("PASS: confirms SKILL.md's corrected note -- Python API needs n_pseudo>0 explicitly for a p-value file.")
else:
    print("FAIL: p-value file presence does not match SKILL.md's documented n_pseudo behavior.")
