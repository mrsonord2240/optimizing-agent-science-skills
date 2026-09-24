"""Focused re-audit for bio-molecular-standardization commit 5fcd1a1.

Exercises every formerly open P1/P2 directly against the committed bundled
example, then runs the original 3,966-row hERG fixture.
"""

import importlib.util
from pathlib import Path

import pandas as pd
from rdkit import Chem, RDLogger

RDLogger.DisableLog("rdApp.*")

SOURCE = Path(
    r"F:\OpenScience\worktrees\bio-molecular-standardization-fixpass"
    r"\chemoinformatics\molecular-standardization\examples\standardize_library.py"
)
HERG = Path(
    r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst"
    r"\public-data\chembl_herg_CHEMBL240_ic50.csv"
)

spec = importlib.util.spec_from_file_location("standardize_library", SOURCE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

# P1: all-fragments-on-salt-list is flagged by default and fallback is explicit.
assert module.chembl_standardize("CC(=O)[O-].[Na+]") == (
    None,
    "multi_fragment_parent",
)
fallback, fallback_status = module.chembl_standardize(
    "CC(=O)[O-].[Na+]", multi_fragment_policy="largest_fragment"
)
assert fallback_status == "ok_largest_fragment_fallback"
assert len(Chem.GetMolFrags(Chem.MolFromSmiles(fallback))) == 1

# P1/P2: tally, replicate QC, and column validation have observable contracts.
small = pd.DataFrame(
    {
        "smiles": ["CCO", "CCO", "CC(=O)[O-].[Na+]", "not-smiles"],
        "pIC50": [5.0, 6.2, 7.0, 4.0],
    }
)
prepared, counts = module.prepare_qsar_data(small)
assert len(prepared) == 1
assert abs(prepared.loc[0, "activity_range"] - 1.2) < 1e-9
assert bool(prepared.loc[0, "replicate_disagreement"])
assert counts["ok"] == 2
assert counts["parse_failure"] == 1
assert counts["multi_fragment_parent"] == 1
assert module.prepare_qsar_data(small, replicate_policy="drop")[0].empty
try:
    module.prepare_qsar_data(small, smiles_col="typo")
except ValueError as error:
    assert "Missing required column(s): typo" in str(error)
else:
    raise AssertionError("missing-column validation did not run")

# P2: isotope retention is selected independently for each record.
tracers = pd.DataFrame(
    {
        "smiles": ["CCO", "[13CH3]CO"],
        "pIC50": [5.0, 5.1],
        "keep_isotopes": pd.Series([False, True], dtype="boolean"),
    }
)
tracer_rows, tracer_counts = module.prepare_qsar_data(
    tracers, pipeline="rdkit", keep_isotopes_col="keep_isotopes"
)
assert len(tracer_rows) == 2
assert tracer_rows["kept_isotopes"].sum() == 1
assert tracer_counts["ok"] == 2

# Regression fixture from the original audit.
herg = pd.read_csv(HERG).dropna(subset=["canonical_smiles", "pchembl_value"])
herg_rows, herg_counts = module.prepare_qsar_data(
    herg, smiles_col="canonical_smiles", activity_col="pchembl_value"
)
assert len(herg) == 3966
assert herg_counts["ok"] == 3966
assert sum(herg_counts.values()) == 3966
assert len(herg_rows) == 3208
assert int((herg_rows["n_replicates"] > 1).sum()) == 379
assert int(herg_rows["replicate_disagreement"].sum()) == 47
assert round(float(herg_rows["activity_range"].max()), 2) == 3.69

print("PASS commit=5fcd1a1 all 5 former P1/P2 findings closed")
print(f"status_counts={counts}")
print(
    "hERG rows=3966 unique=3208 replicated=379 "
    f"range_flags={int(herg_rows['replicate_disagreement'].sum())} "
    f"max_range={herg_rows['activity_range'].max():.2f}"
)
