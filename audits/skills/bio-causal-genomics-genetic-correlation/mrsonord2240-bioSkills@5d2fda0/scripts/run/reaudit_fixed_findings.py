from pathlib import Path
p=Path(r"F:\OpenScience\worktrees\bio-causal-genomics-genetic-correlation-fixpass\causal-genomics\genetic-correlation")
s=(p/"SKILL.md").read_text()
assert "cohort-level GWAS statistic" in s and "Never use rg" in s
assert (p/"examples"/"hdl_rg.R").is_file() and (p/"examples"/"popcorn_transancestry.sh").is_file()
assert "0.3 CHP-aware" in (p/"examples"/"ldsc_crosstrait_rg.sh").read_text()
print("PASS commit=5d2fda0 scope HDL Popcorn threshold cross-reference")
