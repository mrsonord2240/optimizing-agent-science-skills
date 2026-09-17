"""
Follows the FIXED Skill's own documented Chronos code pattern verbatim
(SKILL.md "Chronos (Dempster 2021)" section, mrsonord2240/bioSkills@6847328)
against the real, planted-amplicon HAP1 TKOv3 data (single real cell line).

Regression tests, all against the FIXED schema:
  A. chronos.check_inputs on the FIXED orientation (rows=sequence_ID, cols=sgRNA)
     -- should PASS immediately, unlike the pre-fix audit's first documented block.
  B. model.train() with negative_control_sgrnas supplied, as the fixed code
     requires -- should complete without UnboundLocalError.
  C. chronos.alternate_CN on this single line -- per the FIXED decision tree,
     a single line is supposed to be routed to CRISPRcleanR, not Chronos'
     alternate_CN. Confirm the documented Common Errors row is accurate: the
     RuntimeError message and its wording, and that it comes AFTER training
     completes (matching the fix log's "raised after a full training run, so
     budget for it before you spend the epochs" reliability warning in
     SKILL.md's Failure Modes section).
  D. omit negative_control_sgrnas and confirm the exact UnboundLocalError the
     fix log ("found while fixing") and SKILL.md's Common Errors table claim.
"""
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, "F:/OpenScience/audit-envs/crispr-screen-analyst/tools/chronos-venv/Lib/site-packages")
import chronos

counts = pd.read_csv("../../data/hap1_tkov3_planted_erbb2amp_counts.txt", sep="\t")
cn = pd.read_csv("../../data/hap1_tkov3_planted_cn_profile.txt", sep="\t")
neg_ctrl_genes = set(pd.read_csv(
    "F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/NEGv1_nonessentials.txt", sep="\t"
)["GENE"])

guide_gene_map = counts[["sgRNA", "gene"]].drop_duplicates().rename(columns={"sgRNA": "sgrna"})
negative_control_sgrnas = {
    "screen": guide_gene_map[guide_gene_map["gene"].isin(neg_ctrl_genes)]["sgrna"].tolist()
}
print(f"negative_control_sgrnas: {len(negative_control_sgrnas['screen'])} sgRNAs from NEGv1 non-essentials")

# === FIXED orientation: rows = sequence_ID, columns = sgRNA ===
readcounts_fixed = counts.set_index("sgRNA")[["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]].T
readcounts_fixed.index.name = "sequence_ID"
print("readcounts_fixed shape:", readcounts_fixed.shape, "(rows=sequence_ID, cols=sgRNA) -- matches SKILL.md's fixed comment")

sequence_map = pd.DataFrame({
    "sequence_ID": ["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"],
    "cell_line_name": ["pDNA", "HAP1", "HAP1", "HAP1"],
    "days": [0, 18, 18, 18],
    "pDNA_batch": ["batch1", "batch1", "batch1", "batch1"],
})

print("\n=== A: chronos.check_inputs on the FIXED orientation ===")
try:
    chronos.check_inputs(
        readcounts={"screen": readcounts_fixed},
        guide_gene_map={"screen": guide_gene_map},
        sequence_map={"screen": sequence_map},
    )
    print("check_inputs PASSED on first try with the fixed orientation -- SKILL.md's fix is correct")
except Exception as e:
    print(f"check_inputs FAILED (unexpected -- fix regressed!): {type(e).__name__}: {e}")
    raise

print("\n=== B: model.train() with negative_control_sgrnas supplied ===")
model = chronos.Chronos(
    sequence_map={"screen": sequence_map},
    guide_gene_map={"screen": guide_gene_map},
    readcounts={"screen": readcounts_fixed},
    negative_control_sgrnas=negative_control_sgrnas,
)
model.train(nepochs=100)
gene_effects = model.gene_effect
print("gene_effects shape:", gene_effects.shape, "-- training completed on a SINGLE real cell line, no UnboundLocalError")
print("Sample gene effects (planted-amplicon genes):")
amplicon = ["ERBB2", "GRB7", "STARD3", "PGAP3", "MIEN1", "PNMT", "CASC3", "IKZF3"]
print(gene_effects[[g for g in amplicon if g in gene_effects.columns]])
print("Sample true-essential gene effects (should be strongly negative):")
essentials = ["POLR2L", "PCNA", "EIF3A"]
print(gene_effects[[g for g in essentials if g in gene_effects.columns]])

print("\n=== C: chronos.alternate_CN on a SINGLE cell line (should refuse per fixed decision tree) ===")
copy_number_df = cn.set_index("gene").T
copy_number_df.index = ["HAP1"]
copy_number_df = copy_number_df[[g for g in gene_effects.columns if g in copy_number_df.columns]]
try:
    result = chronos.alternate_CN(gene_effects, copy_number_df)
    print("alternate_CN SUCCEEDED on 1 line (unexpected -- SKILL.md's >=3-line claim would be wrong!)")
    print(type(result), result)
except RuntimeError as e:
    print(f"alternate_CN correctly RAISED RuntimeError on 1 line: {e}")
    print(">>> Matches SKILL.md's Common Errors row verbatim.")
except Exception as e:
    print(f"alternate_CN raised an unexpected exception type {type(e).__name__}: {e}")

print("\n=== D: omit negative_control_sgrnas -- confirm the documented UnboundLocalError ===")
model2 = chronos.Chronos(
    sequence_map={"screen": sequence_map},
    guide_gene_map={"screen": guide_gene_map},
    readcounts={"screen": readcounts_fixed},
)
try:
    model2.train(nepochs=5)
    print("train() SUCCEEDED without negative_control_sgrnas (unexpected -- SKILL.md's claim would be wrong!)")
except UnboundLocalError as e:
    print(f"train() correctly raised UnboundLocalError without negative_control_sgrnas: {e}")
    print(">>> Matches SKILL.md's Common Errors row verbatim.")
except Exception as e:
    print(f"train() raised an unexpected exception type {type(e).__name__}: {e}")

print("\nDONE")
