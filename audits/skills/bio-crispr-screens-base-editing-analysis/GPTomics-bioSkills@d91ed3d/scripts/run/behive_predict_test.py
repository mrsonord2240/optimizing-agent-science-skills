"""
Test whether an agent following the Skill's one-line BE-Hive guidance
("Python: BE-Hive (Arbab 2020) for editing-efficiency prediction; clone
maxwshen/be_predict_bystander and import via sys.path") can actually get a
usable prediction, and whether the prediction is consistent with the Skill's
own claimed editing window (positions 4-8 from PAM-distal end for BE4/CBE).

The Skill gives NO code sample and NO mention of BE-Hive's required 50-nt
substrate convention (positions -19..30, spacer at 1-20, PAM at 21-23) --
this script builds that substrate manually from BE-Hive's own README, using
this audit's synthetic guide (target C at spacer position 5, bystander C at
spacer position 7).
"""
import sys
sys.path.append(r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl")
from be_predict_bystander import predict as bystander_model

PROTOSPACER = "TGATCACGTAGCATGCACGT"  # 20nt, target C at pos5, bystander C at pos7
PAM = "TGG"
# BE-Hive wants a 50nt window: positions -19..30 (1-indexed spacer at 1-20, PAM at 21-23)
# i.e. 19nt upstream of the spacer + 20nt spacer + PAM(3) + 8nt downstream = 50nt
UPSTREAM_19 = "ATGCATGGATCGTAGCTAG"  # 19nt filler, arbitrary but fixed
DOWNSTREAM_8 = "CATGCTAG"            # 8nt filler
seq = UPSTREAM_19 + PROTOSPACER + PAM + DOWNSTREAM_8
assert len(seq) == 50, len(seq)
assert seq[19:39] == PROTOSPACER
assert seq[39:42] == PAM

bystander_model.init_model(base_editor="BE4", celltype="mES")
pred_df, stats = bystander_model.predict(seq)

print("=== stats ===")
for k, v in stats.items():
    print(f"  {k}: {v}")

print("\n=== pred_df (top 10 by predicted frequency) ===")
pred_df_sorted = pred_df.sort_values("Predicted frequency", ascending=False)
print(pred_df_sorted.head(10).to_string())

print("\nColumns:", list(pred_df.columns))
print("Sum of Predicted frequency:", pred_df["Predicted frequency"].sum())
