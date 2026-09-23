"""Additional Phase 2 boundary probe for deconvolute_bystander positions.

The documented coordinate contract is 1-indexed positions within an aligned
allele. This test records whether zero or a position beyond the aligned length is
rejected rather than silently classified as an edit.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd

RUN = Path(__file__).resolve().parent
subject = RUN / "subject_scripts" / "deconvolute_bystander.py"
spec = importlib.util.spec_from_file_location("phase2_deconvolution", subject)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
allele_zip = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\base-editing-synthetic\results\CRISPResso_on_synth_cbe\Alleles_frequency_table.zip")
raw = pd.read_csv(allele_zip, sep="\t", compression="zip")
length = len(raw.iloc[0].Reference_Sequence)
valid = module.deconvolute_bystander(allele_zip, 67, [69])
assert abs(valid["%Reads"].sum() - 100.0) < 1e-9

for invalid in (0, length + 1):
    try:
        result = module.deconvolute_bystander(allele_zip, invalid, [])
    except ValueError as exc:
        print("POSITION_VALIDATION_PRESENT", invalid, str(exc))
    else:
        total_marked = float(result.loc[result.target_edited, "%Reads"].sum())
        print("POSITION_VALIDATION_MISSING", invalid, "marked_edited_pct=", total_marked)

print("INPUT13_BOUNDARY_PROBE_COMPLETED")
