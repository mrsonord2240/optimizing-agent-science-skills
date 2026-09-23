from pathlib import Path
import ast
s=Path(r'F:\OpenScience\wt\chemoinformatics-virtual-screening\chemoinformatics\virtual-screening')
for p in [s/'scripts/prepare_receptor.py',s/'scripts/dock_single.py',s/'examples/virtual_screen.py']:ast.parse(p.read_text())
print('PARSE=PASS')
