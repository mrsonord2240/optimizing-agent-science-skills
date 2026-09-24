"""Run the fixed chemprop prediction command against the audit's saved checkpoints."""
from pathlib import Path
import csv
import subprocess
import sys

root = Path(r"F:\OpenScience\audits\bio-qsar-modeling\run")
out_dir = Path(__file__).resolve().parent
chemprop = Path(r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\chemprop-venv\Scripts\chemprop.exe")
models = [
    root / "chemprop_model" / "replicate_0" / "model_0" / "checkpoints" / "best-epoch=4-val_loss=0.45.ckpt",
    root / "chemprop_model" / "replicate_0" / "model_1" / "checkpoints" / "best-epoch=4-val_loss=0.45.ckpt",
    root / "chemprop_model" / "replicate_1" / "model_0" / "checkpoints" / "best-epoch=1-val_loss=0.51.ckpt",
    root / "chemprop_model" / "replicate_1" / "model_1" / "checkpoints" / "best-epoch=1-val_loss=0.50.ckpt",
]
for model in models:
    assert model.is_file(), model

help_run = subprocess.run([str(chemprop), "train", "--help"], text=True, capture_output=True, timeout=180)
help_text = help_run.stdout + help_run.stderr
assert help_run.returncode == 0, help_text[-2000:]
assert "--data-seed" in help_text and "--pytorch-seed" in help_text, "chemprop 2.3.1 flags missing"

preds = out_dir / "predictions.csv"
command = [
    str(chemprop), "predict", "--test-path", str(root / "cp_test.csv"),
    "--model-paths", *(str(model) for model in models),
    "--molecule-featurizers", "rdkit_2d",
    "--uncertainty-method", "ensemble", "--preds-path", str(preds),
]
print("COMMAND:", subprocess.list2cmdline(command))
run = subprocess.run(command, text=True, capture_output=True, timeout=240)
print(run.stdout)
print(run.stderr, file=sys.stderr)
assert run.returncode == 0, f"chemprop predict exited {run.returncode}"
assert preds.is_file() and preds.stat().st_size > 0, "prediction CSV missing"
with preds.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 200, f"expected 200 predictions, got {len(rows)}"
assert "pred_0" in rows[0] and "pred_0_unc" in rows[0], rows[0].keys()
values = [float(row["pred_0_unc"]) for row in rows]
assert min(values) >= 0 and max(values) > 0, "ensemble variance must be non-negative and non-constant"
print(f"PASS: chemprop {len(rows)} predictions with rdkit_2d; pred_0_unc range={min(values):.8f}..{max(values):.8f}")
