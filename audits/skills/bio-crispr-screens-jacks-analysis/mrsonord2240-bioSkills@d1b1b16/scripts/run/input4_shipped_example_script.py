"""
Input 4 (Stress). Run the Skill's own shipped downstream-analysis code against real
JACKS output from Input 1 (Project Score example-small, apply_w_hp=False run):
  (a) examples/run_jacks.py's analyze_results(gene_file, guide_file, output_prefix) --
      P0 fix added output_prefix as a real parameter (was a NameError-raising free
      variable pre-fix).
  (b) SKILL.md's own inline efficacy_summary(grna_results_path, guidemap_path, ...) --
      P0 fix added the guidemap merge (was a KeyError('Gene') pre-fix, since the grna
      file alone has no Gene column).
Imports the copied skill_copy/examples/run_jacks.py (not the external clone, per the
audit brief) and pastes efficacy_summary() verbatim from SKILL.md's own Per-sgRNA
Efficacy Diagnostics section.
"""
import sys, os
sys.path.insert(0, r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\skill_copy\examples")
import run_jacks  # the copied Skill file, not the external clone

OUT1 = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out1"
DATA = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\data"

gene_file = f"{OUT1}/whp_false_canonical_gene_JACKS_results.txt"
grna_file = f"{OUT1}/whp_false_canonical_grna_JACKS_results.txt"

print("=== (a) examples/run_jacks.py analyze_results(gene_file, guide_file, output_prefix) ===")
try:
    genes, guides = run_jacks.analyze_results(gene_file, grna_file, f"{OUT1}/whp_false_canonical")
    print("PASS: analyze_results() ran without NameError.")
    print(f"Returned genes shape: {genes.shape}, guides shape: {guides.shape}")
except NameError as e:
    print(f"FAIL (P0 regression): NameError still present: {e}")
    raise
except Exception as e:
    print(f"Other exception: {type(e).__name__}: {e}")
    raise

print("\n=== plot_results() (uses the analyze_results() output) ===")
try:
    run_jacks.plot_results(genes, guides, f"{OUT1}/whp_false_canonical")
    png_path = f"{OUT1}/whp_false_canonical_jacks_plots.png"
    print(f"PASS: PNG written: {os.path.exists(png_path)}, size={os.path.getsize(png_path) if os.path.exists(png_path) else 'N/A'} bytes")
except Exception as e:
    print(f"FAIL: plot_results() raised {type(e).__name__}: {e}")
    raise

print("\n=== (b) SKILL.md's own inline efficacy_summary(grna_results_path, guidemap_path, ...) ===")
# Pasted verbatim from SKILL.md's "Per-sgRNA Efficacy Diagnostics" section (post-fix).
import pandas as pd

def efficacy_summary(grna_results_path, guidemap_path, low_threshold=0.3,
                     sgrna_hdr='sgRNA', gene_hdr='Gene'):
    '''Summarise per-sgRNA efficacy. The grna file has only sgrna/X1/X2, so genes come from the guide map.'''
    df = pd.read_csv(grna_results_path, sep='\t')
    guidemap = pd.read_csv(guidemap_path, sep='\t', usecols=[sgrna_hdr, gene_hdr])
    df = df.merge(guidemap, left_on='sgrna', right_on=sgrna_hdr, how='left')
    unmapped = df[gene_hdr].isna().sum()
    if unmapped:
        raise ValueError(f'{unmapped} sgRNAs in the results are absent from the guide map; check naming')
    df['low_eff'] = df['X1'] < low_threshold
    summary = {
        'total_guides': len(df),
        'low_efficacy_count': int(df['low_eff'].sum()),
        'low_efficacy_pct': df['low_eff'].mean() * 100,
        'median_efficacy': df['X1'].median(),
        'q25_q75': (df['X1'].quantile(0.25), df['X1'].quantile(0.75)),
    }
    by_gene = df.groupby(gene_hdr)['low_eff'].mean().sort_values(ascending=False)
    summary['genes_with_all_low_eff'] = int((by_gene == 1).sum())
    return summary, by_gene

# example-small's own count file doubles as the guidemap (sgRNA + Gene columns),
# matching how SKILL.md says the guidemap can come from the count matrix itself.
guidemap_path = f"{DATA}/../../../audit-envs/crispr-screen-analyst/tools/dl/JACKS/jacks/example-small/example_count_data.tab"
guidemap_path = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks\example-small\example_count_data.tab"
try:
    summary, by_gene = efficacy_summary(grna_file, guidemap_path)
    print("PASS: efficacy_summary() ran without KeyError.")
    print(summary)
except KeyError as e:
    print(f"FAIL (P0 regression): KeyError still present: {e}")
    raise

print("\n=== efficacy_summary() naming-mismatch guard (raises ValueError on unmapped guides) ===")
guidemap = pd.read_csv(guidemap_path, sep='\t', usecols=['sgRNA', 'Gene'])
guidemap_corrupt = guidemap.copy()
guidemap_corrupt.loc[0, 'sgRNA'] = 'THIS_GUIDE_DOES_NOT_EXIST'
corrupt_path = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out4_guidemap_corrupt.txt"
guidemap_corrupt.to_csv(corrupt_path, sep='\t', index=False)
try:
    efficacy_summary(grna_file, corrupt_path)
    print("FAIL: expected ValueError for an unmapped guide, none raised.")
except ValueError as e:
    print(f"PASS: raised ValueError as documented: {e}")
