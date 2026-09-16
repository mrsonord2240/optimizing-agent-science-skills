"""
Exercises chronos.alternate_CN (which hard-requires >= 3 cell lines --
confirmed in script 03) with a synthetic 3-"pseudo-line" CN dose-response
panel built from the SAME real HAP1 TKOv3 counts, so we can actually test
the claim central to this audit: does Chronos's CN correction remove the
false hits at the amplicon without erasing true essentiality signal?

This is explicitly labelled synthetic multi-line construction (NOT claimed as
real multi-cell-line biology): three pseudo-lines share the identical real T0
and T18 replicate counts, but each has the artifact planted at a different
copy number (2 = no artifact / diploid control, 8, 15), giving alternate_CN
the >=3-line CN gradient its own smoothing/interpolation procedure needs
(get_shifts fits low-CN vs gene-effect-shift per line, then a smoothed
CN-effect curve across all lines and genes).
"""
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, "F:/OpenScience/audit-envs/crispr-screen-analyst/tools/chronos-venv/Lib/site-packages")
import chronos

np.random.seed(20260916)
AMPLICON_GENES = ["ERBB2", "GRB7", "STARD3", "PGAP3", "MIEN1", "PNMT", "CASC3", "IKZF3"]
K = 0.6
LINES = {"HAP1_pseudo_CN2": 2.0, "HAP1_pseudo_CN8": 8.0, "HAP1_pseudo_CN15": 15.0}

base = pd.read_csv("F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/HAP1_TKOv3_reads.txt", sep="\t")
neg = set(pd.read_csv("F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/NEGv1_nonessentials.txt", sep="\t")["GENE"])

guide_gene_map = base[["SEQUENCE", "GENE"]].drop_duplicates().rename(columns={"SEQUENCE": "sgrna", "GENE": "gene"})
neg_sgrnas_common = guide_gene_map[guide_gene_map["gene"].isin(neg)]["sgrna"].tolist()

readcounts = {}
sequence_map_rows = []
negative_control_sgrnas = {}
cn_rows = {}

all_genes = sorted(base["GENE"].unique())

for line_name, cn_value in LINES.items():
    mask = base["GENE"].isin(AMPLICON_GENES)
    survival = float(np.exp(-K * np.log2(cn_value / 2.0))) if cn_value > 2 else 1.0
    planted = base.copy()
    for col in ["HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]:
        planted.loc[mask, col] = (planted.loc[mask, col] * survival).round(0)

    t0_id = f"{line_name}_T0"
    t18_ids = [f"{line_name}_T18A", f"{line_name}_T18B", f"{line_name}_T18C"]
    rc = planted.set_index("SEQUENCE")[["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]]
    rc.columns = [t0_id] + t18_ids
    readcounts[line_name] = rc.T
    readcounts[line_name].index.name = "sequence_ID"

    sequence_map_rows.append({"sequence_ID": t0_id, "cell_line_name": "pDNA", "days": 0, "pDNA_batch": f"batch_{line_name}"})
    for tid in t18_ids:
        sequence_map_rows.append({"sequence_ID": tid, "cell_line_name": line_name, "days": 18, "pDNA_batch": f"batch_{line_name}"})

    negative_control_sgrnas[line_name] = neg_sgrnas_common
    cn_rows[line_name] = {g: (cn_value if g in AMPLICON_GENES else 2.0) for g in all_genes}

sequence_map = pd.DataFrame(sequence_map_rows)
guide_gene_maps = {k: guide_gene_map for k in LINES}

print("Lines:", list(readcounts.keys()))
for k, v in readcounts.items():
    print(f"  {k}: readcounts shape {v.shape}")

chronos.check_inputs(readcounts=readcounts, guide_gene_map=guide_gene_maps,
                      sequence_map={k: sequence_map[sequence_map.sequence_ID.str.startswith(k)].reset_index(drop=True) for k in LINES})
print("check_inputs PASSED for 3-pseudo-line panel")

# Chronos actually wants ONE sequence_map keyed identically per library in this API version
# (each dict entry is a distinct "library"); use one shared sequence_map per named line-library.
sequence_maps = {k: sequence_map[sequence_map.sequence_ID.str.startswith(k)].reset_index(drop=True) for k in LINES}

model = chronos.Chronos(
    sequence_map=sequence_maps,
    guide_gene_map=guide_gene_maps,
    readcounts=readcounts,
    negative_control_sgrnas=negative_control_sgrnas,
)
model.train(nepochs=100)
gene_effects = model.gene_effect
print("\ngene_effect shape:", gene_effects.shape)
print(gene_effects[AMPLICON_GENES + ["POLR2L", "PCNA", "GTPBP10"]].to_string())

cn_df = pd.DataFrame(cn_rows).T  # rows = lines, columns = genes
cn_df = cn_df[gene_effects.columns]  # align gene order/coverage

print("\nRunning chronos.alternate_CN...")
gene_effects_cn, shifts = chronos.alternate_CN(gene_effects, cn_df)

print("\n=== BEFORE correction (raw Chronos gene_effect) ===")
print(gene_effects[AMPLICON_GENES + ["POLR2L", "PCNA"]].round(3).to_string())
print("\n=== AFTER chronos.alternate_CN correction ===")
print(gene_effects_cn[AMPLICON_GENES + ["POLR2L", "PCNA"]].round(3).to_string())

pre = gene_effects[AMPLICON_GENES].mean(axis=1)
post = gene_effects_cn[AMPLICON_GENES].mean(axis=1)
print("\nMean amplicon-gene effect per line, BEFORE -> AFTER correction:")
for line in LINES:
    print(f"  {line} (planted CN={LINES[line]}): {pre[line]:.3f} -> {post[line]:.3f}")

print("\nTrue essential (POLR2L, PCNA) gene effect, BEFORE -> AFTER (should remain strongly negative):")
for gene in ["POLR2L", "PCNA"]:
    print(f"  {gene}: {gene_effects[gene].round(3).to_dict()} -> {gene_effects_cn[gene].round(3).to_dict()}")

gene_effects.to_csv("chronos_out_before_correction.csv")
gene_effects_cn.to_csv("chronos_out_after_correction.csv")
