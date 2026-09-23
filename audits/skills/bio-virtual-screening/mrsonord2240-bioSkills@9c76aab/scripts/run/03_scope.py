from pathlib import Path
s=Path(r'F:\OpenScience\wt\chemoinformatics-virtual-screening\chemoinformatics\virtual-screening\SKILL.md').read_text()
assert 'GNINA' in s and 'validate' in s and 'PoseBusters' in s and 'Covalent inhibitor' in s
print('SCOPE_AND_GUARDRAILS=PASS')
