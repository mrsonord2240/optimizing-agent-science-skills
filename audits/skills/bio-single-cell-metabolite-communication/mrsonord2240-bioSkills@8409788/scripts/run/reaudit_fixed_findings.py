"""Focused exact-commit re-audit for commit 8409788."""
import ast
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(r"F:\OpenScience\worktrees\bio-single-cell-metabolite-communication-fixpass\single-cell\metabolite-communication")
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
assert skill.count("if __name__ == '__main__':") >= 3
assert "prepare_data_for_mebocost()" in skill
assert "RuntimeError" in skill and "multiprocessing" in skill
assert (ROOT / "examples" / "mebocost.conf.example").is_file()
assert (ROOT / "examples" / "README.md").is_file()

fixture = ROOT / "examples" / "make_synthetic_fixture.py"
ast.parse(fixture.read_text(encoding="utf-8"))
with tempfile.TemporaryDirectory() as temp_dir:
    spec = importlib.util.spec_from_file_location("fixture", fixture)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    output = Path(temp_dir) / "fixture.h5ad"
    adata = module.make_fixture(output)
    assert output.is_file() and adata.shape == (24, 6)
    assert "cell_type" in adata.obs
    assert adata[adata.obs.cell_type == "Tumor", "NT5E"].X.mean() > adata[adata.obs.cell_type == "TCell", "NT5E"].X.mean()

print("PASS commit=8409788 Windows guards=3 QC_route=present fixture=24x6 config_template=present")
