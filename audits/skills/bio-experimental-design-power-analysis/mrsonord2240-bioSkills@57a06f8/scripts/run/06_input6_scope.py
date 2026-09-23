from pathlib import Path
skill = Path(r"F:\OpenScience\wt\experimental-design-power-analysis\experimental-design\power-analysis\SKILL.md").read_text(encoding="utf-8")
handoff = "clinical-biostatistics/power-and-sample-size"
assert handoff in skill
assert "Clinical-trial endpoint" in skill
print(f"SCOPE_HANDOFF={handoff}")
print("SCOPE_BOUNDARY_ASSERTIONS=PASS")
