"""Fresh reduced-draw regression of the scCODA reference workflow on the prior synthetic fixture."""
import pandas as pd
import tensorflow as tf
from sccoda.util import cell_composition_data as dat
from sccoda.util import comp_ana as mod

root = "F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples"
cells = pd.read_csv(root + "/truth_cells.csv")
cells = cells[~cells.true_doublet.astype(bool) & ~cells.true_low_quality.astype(bool)]
sample_sheet = pd.read_csv(root + "/sample_sheet.csv").set_index("sample")
cells["condition"] = cells["sample"].map(sample_sheet["condition"])
counts = pd.crosstab(cells["sample"], cells["true_cell_type"]).reset_index()
counts = counts.merge(cells[["sample", "condition"]].drop_duplicates(), on="sample")
data = dat.from_pandas(counts, covariate_columns=["sample", "condition"])
tf.random.set_seed(42)
model = mod.CompositionalAnalysis(data, formula="condition", reference_cell_type="automatic")
result = model.sample_hmc(num_results=1000, num_burnin=200)
result.set_fdr(est_fdr=0.1)
effects = result.credible_effects()
print("REFERENCE=", model.reference_cell_type, sep="")
print("CREDIBLE_EFFECTS=", ",".join(str(index) for index, value in effects.items() if bool(value)), sep="")
print("EFFECT_TABLE=", result.effect_df.to_string(), sep="\n")
