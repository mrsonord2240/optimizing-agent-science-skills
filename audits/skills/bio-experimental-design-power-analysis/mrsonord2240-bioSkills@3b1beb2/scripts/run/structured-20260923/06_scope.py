from pathlib import Path

skill = Path(r"F:\OpenScience\wt\p2-reaudit-bio-power-analysis\experimental-design\power-analysis\SKILL.md").read_text(encoding="utf-8")
assert "clinical-biostatistics/power-and-sample-size" in skill
assert "Clinical-trial endpoint" in skill
print("SCOPE_HANDOFF=PASS")
