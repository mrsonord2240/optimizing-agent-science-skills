"""
Follows the Skill's OWN documented Chronos code pattern (SKILL.md, "Chronos
(Dempster 2021)" section) as literally as possible against the real, honest
canonical dataset: one real cell line (HAP1), planted 17q12 CN amplification.

Step A: build readcounts exactly as SKILL.md's own comment says --
  "# 1. Counts: rows = sgRNA, columns = samples (per-timepoint per-cell-line)"
and see whether Chronos accepts it.

Step B: if Step A fails, introspect (per the Skill's own "Version Compatibility"
instruction: "If code throws ImportError, AttributeError, or TypeError,
introspect the installed package and adapt") and build the corrected
orientation, then run the rest of the documented pipeline
(model.train -> gene_effect -> chronos.alternate_CN) and see how far a single
real cell line gets.
"""
import sys
import traceback
import pandas as pd
import numpy as np

sys.path.insert(0, "F:/OpenScience/audit-envs/crispr-screen-analyst/tools/chronos-venv/Lib/site-packages")
import chronos

counts = pd.read_csv("../data/hap1_tkov3_planted_erbb2amp_counts.txt", sep="\t")
cn = pd.read_csv("../data/hap1_tkov3_planted_cn_profile.txt", sep="\t")

guide_gene_map = counts[["sgRNA", "gene"]].drop_duplicates().rename(columns={"sgRNA": "sgrna"})

# === STEP A: literal SKILL.md orientation -- "rows = sgRNA, columns = samples" ===
print("=" * 70)
print("STEP A: readcounts as SKILL.md documents it -- rows=sgRNA, columns=samples")
print("=" * 70)
readcounts_as_documented = counts.set_index("sgRNA")[["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"]]
print("readcounts_as_documented shape:", readcounts_as_documented.shape, "(rows=sgRNA, cols=samples)")

sequence_map = pd.DataFrame({
    "sequence_ID": ["HAP1_T0", "HAP1_T18A", "HAP1_T18B", "HAP1_T18C"],
    "cell_line_name": ["pDNA", "HAP1", "HAP1", "HAP1"],
    "days": [0, 18, 18, 18],
    "pDNA_batch": ["batch1", "batch1", "batch1", "batch1"],
})

try:
    chronos.check_inputs(
        readcounts={"screen": readcounts_as_documented},
        guide_gene_map={"screen": guide_gene_map},
        sequence_map={"screen": sequence_map},
    )
    print("check_inputs PASSED with SKILL.md's documented orientation (unexpected)")
except Exception as e:
    print(f"check_inputs FAILED as documented by SKILL.md: {type(e).__name__}: {e}")
    print(">>> CONFIRMED: SKILL.md's stated readcounts orientation ('rows=sgRNA, columns=samples')")
    print(">>> contradicts chronos.check_inputs' own required orientation, which is the opposite:")
    print(">>> 'Chronos expects readcounts to have guides as columns, sequence IDs as rows.'")

# === STEP B: corrected orientation (guides as columns, sequence IDs as rows) ===
print()
print("=" * 70)
print("STEP B: corrected orientation -- rows=sequence_ID (sample), columns=sgRNA")
print("=" * 70)
readcounts_correct = readcounts_as_documented.T
readcounts_correct.index.name = "sequence_ID"
print("readcounts_correct shape:", readcounts_correct.shape, "(rows=sample, cols=sgRNA)")

try:
    chronos.check_inputs(
        readcounts={"screen": readcounts_correct},
        guide_gene_map={"screen": guide_gene_map},
        sequence_map={"screen": sequence_map},
    )
    print("check_inputs PASSED with corrected orientation")
except Exception as e:
    print(f"check_inputs FAILED even with corrected orientation: {type(e).__name__}: {e}")
    raise SystemExit(1)

# === STEP C: train Chronos exactly as SKILL.md documents (fewer epochs for a smoke test) ===
print()
print("=" * 70)
print("STEP C: model.train() on the single real cell line (HAP1)")
print("=" * 70)
try:
    model = chronos.Chronos(
        sequence_map={"screen": sequence_map},
        guide_gene_map={"screen": guide_gene_map},
        readcounts={"screen": readcounts_correct},
    )
    model.train(nepochs=50)
    gene_effects = model.gene_effect
    print("model.train() COMPLETED. gene_effect shape:", gene_effects.shape)
    print(gene_effects[["ERBB2", "GRB7", "STARD3", "POLR2L", "PCNA"]].to_string())
except Exception as e:
    print(f"model.train() FAILED: {type(e).__name__}: {e}")
    traceback.print_exc()
    gene_effects = None

# === STEP D: chronos.alternate_CN exactly as SKILL.md documents ===
print()
print("=" * 70)
print("STEP D: chronos.alternate_CN() -- the Skill's documented CN-correction step")
print("=" * 70)
if gene_effects is not None:
    cn_df = cn.set_index("gene").T
    cn_df.index = ["HAP1"]
    try:
        gene_effects_cn = chronos.alternate_CN(gene_effects, cn_df)
        print("alternate_CN COMPLETED (unexpected for a single cell line)")
    except Exception as e:
        print(f"alternate_CN FAILED: {type(e).__name__}: {e}")
        print(">>> CONFIRMED: chronos.alternate_CN's own source hard-requires >= 3 cell lines")
        print(">>> ('Correct for CN should not be used with fewer than 3 cell lines. Consider")
        print(">>> preprocessing with CRISPRCleanR') -- a constraint the Skill's decision tree")
        print(">>> and its 'Single cell line with matched WGS/SNP-array CN -> CRISPRcleanR or")
        print(">>> Chronos; Either works' row do not mention at all.")
else:
    print("Skipped -- model.train() did not produce gene_effects")
