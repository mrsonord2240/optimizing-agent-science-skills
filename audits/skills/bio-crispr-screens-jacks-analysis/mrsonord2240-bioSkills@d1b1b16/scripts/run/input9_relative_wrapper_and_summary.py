"""Input 9 (fresh Stress): run the shipped wrapper with caller-relative paths,
then execute the shipped efficacy-summary CLI and verify parseable outputs."""
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path
import pandas as pd

AUDIT = Path(r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis")
EX = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks\example-small")
JACKS_DIR = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks"
OUT = AUDIT / "run" / "out9"
OUT.mkdir(exist_ok=True)
for name in ("example_count_data.tab", "example_repmap.tab"):
    shutil.copy2(EX / name, OUT / name)
repmap = pd.read_csv(OUT / "example_repmap.tab", sep="\t")
repmap["Control"] = "CTRL"  # required by the wrapper's documented CLI contract
repmap.to_csv(OUT / "example_repmap_with_control.tab", sep="\t", index=False)

spec = importlib.util.spec_from_file_location("audit_run_jacks", AUDIT / "skill_copy" / "examples" / "run_jacks.py")
wrapper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wrapper)
old_cwd = os.getcwd()
os.chdir(OUT)
try:
    ok = wrapper.run_jacks_analysis("example_count_data.tab", "example_count_data.tab", "example_repmap_with_control.tab", "relative_out", JACKS_DIR)
finally:
    os.chdir(old_cwd)
print(f"relative-path wrapper returned={ok}")
assert ok
prefix = OUT / "relative_out"
gene_path = str(prefix) + "_gene_JACKS_results.txt"
grna_path = str(prefix) + "_grna_JACKS_results.txt"
assert Path(gene_path).exists() and len(pd.read_csv(gene_path, sep="\t")) == 1579

summary_path = OUT / "low_eff_by_gene.tsv"
cmd = [sys.executable, str(AUDIT / "skill_copy" / "scripts" / "efficacy_summary.py"), grna_path,
       str(OUT / "example_count_data.tab"), "--out", str(summary_path)]
result = subprocess.run(cmd, capture_output=True, text=True)
print(f"efficacy_summary returncode={result.returncode}")
print(result.stdout)
if result.returncode:
    print(result.stderr)
assert result.returncode == 0
by_gene = pd.read_csv(summary_path, sep="\t")
print(f"summary rows={len(by_gene)} columns={list(by_gene.columns)}")
assert len(by_gene) == 1579 and "low_eff_fraction" in by_gene.columns
