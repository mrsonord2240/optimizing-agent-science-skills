from pathlib import Path
s=Path(r'F:\OpenScience\wt\experimental-design-power-analysis\experimental-design\power-analysis\SKILL.md').read_text()
assert 'clinical-biostatistics/power-and-sample-size' in s and 'Clinical-trial endpoint' in s
print('SCOPE_HANDOFF=PASS')
