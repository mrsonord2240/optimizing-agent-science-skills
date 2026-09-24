# Exact-commit re-audit input 6: shipped-file and compatibility contract checks.
# Run with: py.sh reaudit_i6_source_contract.py <skill-dir>
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
skill = (root / "SKILL.md").read_text(encoding="utf-8")
usage = (root / "usage-guide.md").read_text(encoding="utf-8")
example = root / "examples" / "raincloud_phd.R"
r_test = root / "examples" / "test_distribution_plots.R"
py_test = root / "examples" / "test_python_distribution_plots.py"
assert all(path.is_file() for path in (example, r_test, py_test))
assert "ggdist::stat_halfeye" in skill
assert "Do not make `gghalves` a required dependency" in skill
assert "position_jitter(width = 0.2, height = 0, seed = 20260923)" in skill
assert "hue=group" in skill and "legend=False" in skill
assert "safe_violin_bw" in skill and "prepare_split_violin_data" in skill
assert "N-based choice" in usage and "standalone R example" in usage
print("PASS i6: all shipped routes present; current ggdist/seeded R and hue-based Python contracts documented")
