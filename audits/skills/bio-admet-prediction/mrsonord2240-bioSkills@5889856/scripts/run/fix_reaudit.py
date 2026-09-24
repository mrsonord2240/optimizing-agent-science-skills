"""Exact-commit executable checks for the bio-admet-prediction fix pass.

Run with the shared chemoinformatics audit interpreter and the target skill root:
  python fix_reaudit.py F:\\OpenScience\\wt\\bio-admet-prediction\\chemoinformatics\\admet-prediction
"""

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

import admet_ai
import pandas as pd


skill_root = Path(sys.argv[1]).resolve()
example_path = skill_root / "examples" / "predict_admet.py"
spec = importlib.util.spec_from_file_location("predict_admet", example_path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

commit = subprocess.check_output(
    ["git", "-C", str(skill_root.parents[1]), "rev-parse", "HEAD"], text=True
).strip()
print(f"commit={commit}")
print(f"admet_ai_version={admet_ai.__version__}")

reference = [
    "CCO",
    "CC(=O)Oc1ccccc1C(=O)O",
    "Cn1cnc2n(C)c(=O)n(C)c(=O)c12",
    "CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O",
]
threshold = module.fit_similarity_threshold(reference)
gate = module.assess_applicability_domain(
    ["CCO", "[Na+].[Cl-]", "Cl[Pt](Cl)(N)N"], reference, threshold=threshold
)
print(f"similarity_threshold={threshold:.3f}")
print(gate.to_string(index=False))
assert gate.decision.tolist() == ["predict", "reject", "reject"]

with tempfile.TemporaryDirectory() as tmp_dir:
    valid_path = Path(tmp_dir) / "admetlab_results.csv"
    pd.DataFrame(
        {
            "SMILES": ["CCO"],
            "hERG_uncertainty": [0.12],
            "task_id": ["current-contract-example"],
        }
    ).to_csv(valid_path, index=False)
    valid = module.load_admetlab_results(valid_path, task_id_column="task_id")
    assert valid.shape == (1, 3)
    no_uncertainty_path = Path(tmp_dir) / "computed_properties_only.csv"
    pd.DataFrame({"SMILES": ["CCO"], "MW": [46.07]}).to_csv(
        no_uncertainty_path, index=False
    )
    try:
        module.load_admetlab_results(no_uncertainty_path)
    except ValueError as exc:
        print(f"missing_uncertainty={exc}")
    else:
        raise AssertionError("ADMETlab CSV without uncertainty did not fail validation")
    try:
        module.load_admetlab_results(Path(tmp_dir) / "missing.csv")
    except FileNotFoundError as exc:
        print(f"missing_file={exc}")
    else:
        raise AssertionError("missing ADMETlab result did not raise FileNotFoundError")

try:
    module.load_admetlab_results(
        Path(__file__).with_name("fake_admetlab.csv"), require_uncertainty=True
    )
except ValueError as exc:
    print(f"wrong_contract={exc}")
else:
    raise AssertionError("unrelated ADMETlab CSV did not fail validation")

predictions = module.predict_admet_ai(
    gate.loc[gate.decision == "predict", "smiles"].tolist(),
    endpoints=["hERG", "AMES", "DILI", "BBB_Martins"],
)
print(f"prediction_shape={predictions.shape}")
print(predictions.to_string())
assert list(predictions.columns) == ["hERG", "AMES", "DILI", "BBB_Martins"]
assert predictions.notna().all().all()

run_dir = Path(__file__).parent
truth = pd.read_csv(run_dir / "herg_300_truth.csv")
batch_smiles = truth["canonical_smiles"].tolist()
batch_threshold = module.fit_similarity_threshold(batch_smiles)
batch_gate = module.assess_applicability_domain(
    batch_smiles, batch_smiles, threshold=batch_threshold
)
assert len(batch_gate) == 300
assert batch_gate.decision.isin(["predict", "manual_review", "reject"]).all()
accepted_batch = batch_gate.loc[batch_gate.decision == "predict", "smiles"].tolist()
assert accepted_batch
endpoints = [
    "hERG", "AMES", "DILI", "BBB_Martins", "CYP1A2_Veith",
    "CYP2C19_Veith", "CYP2C9_Veith", "CYP2D6_Veith", "CYP3A4_Veith",
]
batch_predictions = module.predict_admet_ai(accepted_batch, endpoints=endpoints)
assert batch_predictions.shape == (len(accepted_batch), len(endpoints))
assert batch_predictions.notna().all().all()
print(
    "batch_300="
    f"gate_decisions={batch_gate.decision.value_counts().to_dict()} "
    f"prediction_shape={batch_predictions.shape} "
    f"hERG_range={batch_predictions.hERG.min():.3f}..{batch_predictions.hERG.max():.3f}"
)

ood = pd.read_csv(run_dir / "ood_probes_truth.csv")
ood_gate = module.assess_applicability_domain(
    ood["smiles"].tolist(), batch_smiles, threshold=batch_threshold
)
print("ood_gate=" + "; ".join(
    f"{label}: {decision}" for label, decision in zip(ood["label"], ood_gate["decision"])
))
assert ood_gate.loc[ood["label"].str.contains("sodium chloride"), "decision"].item() == "reject"
assert ood_gate.loc[ood["label"].str.contains("cisplatin"), "decision"].item() == "reject"
print("ALL_ASSERTIONS_PASSED")
