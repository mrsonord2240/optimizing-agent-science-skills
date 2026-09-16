"""
Plants a real, honest focal amplification into real HAP1 TKOv3 counts.

Amplicon: the real 17q12 HER2 amplicon (ERBB2, GRB7, STARD3, PGAP3, MIEN1,
PNMT, CASC3, IKZF3 -- all genuinely co-amplified in HER2+ breast cancer,
e.g. SK-BR-3, per Aguirre 2016 / Munoz 2016, which the Skill itself cites
as its textbook example: "ERBB2 appears essential in HER2-amplified SK-BR-3").
None of these 8 genes are in CEGv2 (core essential) or NEGv1 in this dataset
check -- they are ordinary non-essential genes in HAP1 (not HER2-amplified),
so their un-planted baseline LFC should be near zero.

Planted mechanism (matches the Skill's own stated mechanism, SKILL.md lines
26-34): "multiple simultaneous cuts -> DNA-damage response -> G2 arrest ->
cells don't proliferate -> depletion proportional to number of simultaneous
cuts, not the gene's actual essentiality." We model this as a copy-number-
dependent survival-fraction multiplier applied only to the late (T18)
timepoint counts of sgRNAs targeting the amplified genes:

    survival_fraction = exp(-k * log2(CN / 2))   for CN > 2
    k = 0.6 (chosen so CN=15 gives an LFC ~ -2.5, comparable in magnitude to
        the real core-essential depletion already verified in TOOLS.md, e.g.
        POLR2L, EIF3A -- i.e. large enough to look like a genuine hit)

This is applied identically to every sgRNA of the 8 amplicon genes, which is
exactly the gene-independent (sequence/biology-independent) property the
Skill describes -- the depletion depends only on CN, not on any gene-specific
effect.
"""
import numpy as np
import pandas as pd

np.random.seed(20260916)

SRC = "F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/HAP1_TKOv3_reads.txt"
OUT_COUNTS = "F:/OpenScience/audits/bio-crispr-screens-copy-number-correction/data/hap1_tkov3_planted_erbb2amp_counts.txt"
OUT_CN = "F:/OpenScience/audits/bio-crispr-screens-copy-number-correction/data/hap1_tkov3_planted_cn_profile.txt"

AMPLICON_GENES = ["ERBB2", "GRB7", "STARD3", "PGAP3", "MIEN1", "PNMT", "CASC3", "IKZF3"]
AMPLICON_CN = 15.0
DIPLOID_CN = 2.0
K = 0.6

df = pd.read_csv(SRC, sep="\t")
assert list(df.columns) == ["SEQUENCE", "GENE", "HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"], df.columns
print(f"Loaded real HAP1 TKOv3 counts: {len(df)} sgRNAs, {df['GENE'].nunique()} genes")

# Confirm the amplicon genes are present and NOT in the essential/non-essential reference sets
ceg = set(pd.read_csv("F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/CEGv2_core_essentials.txt", sep="\t")["GENE"])
neg = set(pd.read_csv("F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/NEGv1_nonessentials.txt", sep="\t")["GENE"])
for g in AMPLICON_GENES:
    n = (df["GENE"] == g).sum()
    print(f"  {g}: {n} sgRNAs present, in_CEGv2={g in ceg}, in_NEGv1={g in neg}")
    assert n > 0, f"{g} missing from library -- pick a different amplicon gene"
    assert g not in ceg, f"{g} is a core essential -- would confound the artifact test"

survival_fraction = float(np.exp(-K * np.log2(AMPLICON_CN / DIPLOID_CN)))
print(f"\nPlanted survival_fraction for CN={AMPLICON_CN}: {survival_fraction:.4f}  "
      f"(expected LFC shift ~ {np.log2(survival_fraction):.2f})")

mask = df["GENE"].isin(AMPLICON_GENES)
print(f"Planting artifact on {mask.sum()} sgRNAs across {mask.sum()//4} genes")

planted = df.copy()
for col in ["HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]:
    planted.loc[mask, col] = planted.loc[mask, col] * survival_fraction

planted[["HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]] = planted[["HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]].round(0)

# mageck expects: sgRNA, gene, then sample count columns (integers)
mageck_df = planted.rename(columns={"SEQUENCE": "sgRNA", "GENE": "gene"})
mageck_df.to_csv(OUT_COUNTS, sep="\t", index=False)
print(f"\nWrote planted counts: {OUT_COUNTS}")

# Gene-level CN profile (matched, "known" -- exactly what a real WGS/SNP-array CN call would give)
all_genes = sorted(df["GENE"].unique())
cn_profile = pd.DataFrame({
    "gene": all_genes,
    "copy_number": [AMPLICON_CN if g in AMPLICON_GENES else DIPLOID_CN for g in all_genes],
})
cn_profile.to_csv(OUT_CN, sep="\t", index=False)
print(f"Wrote CN profile ({len(cn_profile)} genes, {mask.sum()//4} amplified at CN={AMPLICON_CN}): {OUT_CN}")

# Sanity: show raw counts before/after for one amplicon gene
print("\nSample check -- ERBB2 sgRNA counts before -> after planting:")
before = df[df["GENE"] == "ERBB2"]
after = planted[planted["GENE"] == "ERBB2"]
print(before.to_string(index=False))
print(after.to_string(index=False))
