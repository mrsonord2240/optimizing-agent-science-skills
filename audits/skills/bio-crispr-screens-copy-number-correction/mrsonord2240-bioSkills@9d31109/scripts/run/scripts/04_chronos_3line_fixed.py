"""
DepMap-scale multi-cell-line panel test, per the FIXED decision tree row
">=3 cell lines, CN available -> Chronos". Regression test for two things:
  1. The original P0 (readcounts orientation) on a >=3-line panel.
  2. The "found while fixing" issue: chronos.alternate_CN returns a
     (corrected, shifts) TUPLE; the pre-fix example assigned it to one
     name. Confirm the fixed unpacking
     `gene_effects_cn, cn_shifts = chronos.alternate_CN(...)` is correct
     and that `shifts` really is a second, separate object (not part of
     the corrected matrix).

Data: SYNTHETIC, explicitly labeled. 3 pseudo-cell-lines built from the same
real HAP1 TKOv3 counts, with a CN dose-response (CN=2/8/15) planted at the
same 8 real 17q12 co-amplified genes used in Input 1/3. This is necessary
because alternate_CN hard-requires >=3 lines and no second/third real
published cell-line screen is available in this environment (see TOOLS.md
public-data -- only HAP1_TKOv3_reads.txt).
"""
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, "F:/OpenScience/audit-envs/crispr-screen-analyst/tools/chronos-venv/Lib/site-packages")
import chronos

np.random.seed(20260917)

base = pd.read_csv("F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/HAP1_TKOv3_reads.txt", sep="\t")
neg_ctrl_genes = set(pd.read_csv(
    "F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/NEGv1_nonessentials.txt", sep="\t"
)["GENE"])
AMPLICON_GENES = ["ERBB2", "GRB7", "STARD3", "PGAP3", "MIEN1", "PNMT", "CASC3", "IKZF3"]
K = 0.6

lines = {"LINE_CN2": 2.0, "LINE_CN8": 8.0, "LINE_CN15": 15.0}
readcounts_rows = []
sequence_rows = []
for line, cn_val in lines.items():
    survival = float(np.exp(-K * np.log2(cn_val / 2.0))) if cn_val > 2 else 1.0
    d = base.copy()
    mask = d["GENE"].isin(AMPLICON_GENES)
    t0_id = f"{line}_T0"
    t18_ids = [f"{line}_T18A", f"{line}_T18B", f"{line}_T18C"]
    for col_out, col_in in zip([t0_id] + t18_ids, ["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]):
        vals = d[col_in].astype(float).copy()
        if col_out != t0_id:
            vals.loc[mask] = vals.loc[mask] * survival
        readcounts_rows.append(pd.Series(vals.round(0).values, name=col_out, index=d["SEQUENCE"]))
    sequence_rows.append({"sequence_ID": t0_id, "cell_line_name": "pDNA", "days": 0, "pDNA_batch": f"{line}_batch"})
    for tid in t18_ids:
        sequence_rows.append({"sequence_ID": tid, "cell_line_name": line, "days": 18, "pDNA_batch": f"{line}_batch"})

readcounts = pd.DataFrame(readcounts_rows)
readcounts.index.name = "sequence_ID"
sequence_map = pd.DataFrame(sequence_rows)
guide_gene_map = base[["SEQUENCE", "GENE"]].drop_duplicates().rename(columns={"SEQUENCE": "sgrna", "GENE": "gene"})
negative_control_sgrnas = {"screen": guide_gene_map[guide_gene_map["gene"].isin(neg_ctrl_genes)]["sgrna"].tolist()}

print("readcounts shape:", readcounts.shape, "(rows=sequence_ID x 3 lines, cols=sgRNA)")
print("sequence_map:\n", sequence_map)

chronos.check_inputs(
    readcounts={"screen": readcounts},
    guide_gene_map={"screen": guide_gene_map},
    sequence_map={"screen": sequence_map},
)
print("check_inputs PASSED on 3-line panel")

model = chronos.Chronos(
    sequence_map={"screen": sequence_map},
    guide_gene_map={"screen": guide_gene_map},
    readcounts={"screen": readcounts},
    negative_control_sgrnas=negative_control_sgrnas,
)
model.train(nepochs=150)
gene_effects = model.gene_effect
print("\ngene_effects shape:", gene_effects.shape)
print(gene_effects[[g for g in AMPLICON_GENES if g in gene_effects.columns]])
print("\nEssentials (should stay strongly negative in all 3 lines):")
essentials = ["POLR2L", "PCNA"]
print(gene_effects[[g for g in essentials if g in gene_effects.columns]])

copy_number_df = pd.DataFrame(
    {g: [lines[ln] if g in AMPLICON_GENES else 2.0 for ln in lines] for g in gene_effects.columns},
    index=list(lines.keys()),
)

print("\n=== chronos.alternate_CN on the 3-line panel: unpack (corrected, shifts) ===")
result = chronos.alternate_CN(gene_effects, copy_number_df)
assert isinstance(result, tuple) and len(result) == 2, f"expected a 2-tuple, got {type(result)}"
gene_effects_cn, cn_shifts = result
print("gene_effects_cn shape:", gene_effects_cn.shape, "type:", type(gene_effects_cn))
print("cn_shifts shape:", getattr(cn_shifts, "shape", None), "type:", type(cn_shifts))
assert gene_effects_cn.shape == gene_effects.shape, "corrected matrix should have same shape as input"
print(">>> Confirmed: alternate_CN returns a real 2-tuple (corrected_matrix, per-gene_shifts); the pre-fix")
print(">>> example's single-name assignment would have bound the WHOLE tuple to one variable.")

print("\nAmplicon genes, before vs after alternate_CN:")
print("BEFORE:\n", gene_effects[[g for g in AMPLICON_GENES if g in gene_effects.columns]])
print("AFTER:\n", gene_effects_cn[[g for g in AMPLICON_GENES if g in gene_effects_cn.columns]])
print("\nEssentials, before vs after (should be unaffected):")
print("BEFORE:\n", gene_effects[[g for g in essentials if g in gene_effects.columns]])
print("AFTER:\n", gene_effects_cn[[g for g in essentials if g in gene_effects_cn.columns]])

gene_effects.to_csv("../chronos_3line_before.csv")
gene_effects_cn.to_csv("../chronos_3line_after.csv")
print("\nDONE")
