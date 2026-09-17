"""
Round-3 re-audit, Input 5 (Stress, NEW).

SKILL.md's round-3 fix added a 5th Reconciliation cause (mrsonord2240/bioSkills@9d31109,
"Reconciliation: When CN Correction Fails"): alternate_CN fits one CN-effect curve across the
whole panel, so a single extreme-CN line can retain residual signal even after correction --
"re-run detect_cn_bias per cell line, not only pooled, after alternate_CN." That sentence was
added as prose in this fix pass; it has never itself been run. This input tests it directly,
using the real 3-line post-alternate_CN gene_effect matrix already on disk from the round-2 fix
pass (chronos_3line_after.csv: LINE_CN2, LINE_CN8, LINE_CN15, real HAP1-derived counts, planted
8-gene 17q12 amplicon at per-line CN 2/8/15 respectively -- see data/hap1_tkov3_planted_cn_profile.txt
for the gene list).

Two analyses on the same real post-correction numbers:
  POOLED   -- merge all 3 lines' (gene, lfc, copy_number) rows into one table and run
              detect_cn_bias once, as an agent might do if it pools a panel's results without
              reading the per-line CN structure.
  PER-LINE -- run detect_cn_bias separately for each line, exactly as the new Reconciliation
              text instructs.

If pooling dilutes a real, still-present problem in the CN15 line that the per-line check
catches, that is direct, real-number support for the new guidance -- not just restating the fix
log's prose.
"""
import pandas as pd
from scipy.stats import spearmanr, mannwhitneyu

def detect_cn_bias(gene_lfc_df, cn_df, amplified_cn=4, diploid_cn=(1.5, 2.5), low_power_n=8):
    merged = gene_lfc_df.merge(cn_df, on='gene')
    rho, p = spearmanr(merged['copy_number'], merged['lfc'])
    amplified = merged[merged['copy_number'] > amplified_cn]['lfc']
    diploid = merged[merged['copy_number'].between(*diploid_cn)]['lfc']
    gap, p_gap = float('nan'), float('nan')
    if len(amplified) >= 3 and len(diploid) >= 3:
        gap = amplified.mean() - diploid.mean()
        p_gap = mannwhitneyu(amplified, diploid, alternative='less').pvalue
    low_power = len(amplified) < low_power_n
    return {
        'n_amplified_genes': len(amplified),
        'amplified_vs_diploid_gap': gap,
        'p_amplified_more_depleted': p_gap,
        'bias_present': bool((rho < -0.1 and p < 0.01) or (gap < -0.5 and p_gap < 0.01)),
        'low_power_floor': bool(low_power),
        'suspicious_despite_ns': bool(low_power and not pd.isna(gap) and gap < -0.5),
    }

AMPLICON_GENES = ["CASC3", "ERBB2", "GRB7", "IKZF3", "MIEN1", "PGAP3", "PNMT", "STARD3"]
LINE_CN = {"LINE_CN2": 2, "LINE_CN8": 8, "LINE_CN15": 15}

after = pd.read_csv("../chronos_3line_after.csv").set_index("cell_line_name")

# Sample a real diploid background (genes far from the amplicon, CN=2 in every line) --
# reuse a fixed random sample of 300 real genes present in the matrix, excluding the amplicon.
import numpy as np
np.random.seed(20260917)
bg_candidates = [g for g in after.columns if g not in AMPLICON_GENES]
background_genes = list(np.random.choice(bg_candidates, size=300, replace=False))

# --- Build long (gene, lfc, copy_number) tables per line, for both analyses ---
per_line_tables = {}
for line, cn in LINE_CN.items():
    rows = []
    for g in AMPLICON_GENES:
        rows.append({"gene": g, "lfc": after.loc[line, g], "copy_number": float(cn)})
    for g in background_genes:
        rows.append({"gene": g, "lfc": after.loc[line, g], "copy_number": 2.0})
    per_line_tables[line] = pd.DataFrame(rows)

print("=== PER-LINE (as the new Reconciliation cause-5 text instructs) ===")
per_line_results = {}
for line in LINE_CN:
    df = per_line_tables[line]
    r = detect_cn_bias(df[["gene", "lfc"]], df[["gene", "copy_number"]])
    per_line_results[line] = r
    print(f"  {line} (CN={LINE_CN[line]}): gap={r['amplified_vs_diploid_gap']:.3f} "
          f"p={r['p_amplified_more_depleted']:.4f} bias_present={r['bias_present']} "
          f"low_power_floor={r['low_power_floor']} suspicious_despite_ns={r['suspicious_despite_ns']}")

print("\n=== POOLED (merge all 3 lines' amplicon + background rows into one table) ===")
pooled_amp_rows = []
for line, cn in LINE_CN.items():
    for g in AMPLICON_GENES:
        pooled_amp_rows.append({"gene": f"{g}__{line}", "lfc": after.loc[line, g], "copy_number": float(cn)})
pooled_bg_rows = []
# use one line's background as the diploid reference pool (representative; all lines are CN=2 there)
for g in background_genes:
    pooled_bg_rows.append({"gene": g, "lfc": after.loc["LINE_CN2", g], "copy_number": 2.0})
pooled_df = pd.DataFrame(pooled_amp_rows + pooled_bg_rows)
r_pooled = detect_cn_bias(pooled_df[["gene", "lfc"]], pooled_df[["gene", "copy_number"]])
print(f"  pooled (n_amplified={r_pooled['n_amplified_genes']}): "
      f"gap={r_pooled['amplified_vs_diploid_gap']:.3f} p={r_pooled['p_amplified_more_depleted']:.4f} "
      f"bias_present={r_pooled['bias_present']} low_power_floor={r_pooled['low_power_floor']} "
      f"suspicious_despite_ns={r_pooled['suspicious_despite_ns']}")

print("\n=== Does pooling dilute a real per-line problem? ===")
cn15 = per_line_results["LINE_CN15"]
print(f"  LINE_CN15 alone: gap={cn15['amplified_vs_diploid_gap']:.3f} bias_present={cn15['bias_present']} "
      f"suspicious_despite_ns={cn15['suspicious_despite_ns']}")
print(f"  Pooled (all 3 lines together): gap={r_pooled['amplified_vs_diploid_gap']:.3f} "
      f"bias_present={r_pooled['bias_present']} suspicious_despite_ns={r_pooled['suspicious_despite_ns']}")
if (cn15["bias_present"] or cn15["suspicious_despite_ns"]) and not (r_pooled["bias_present"] or r_pooled["suspicious_despite_ns"]):
    print("  CONFIRMED: pooling masks a real problem visible only per-line -- supports the new "
          "Reconciliation cause-5 text with real numbers.")
else:
    print("  NOT confirmed on this real data: pooled and per-line give the same qualitative read "
          "(check numbers above -- the new prose may be overstated for this case).")

print("\nDONE")
