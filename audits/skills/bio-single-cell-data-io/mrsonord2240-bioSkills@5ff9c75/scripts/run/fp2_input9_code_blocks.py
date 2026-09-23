"""Phase-2 Input 9: syntax-check shipped Python and extract R blocks for R parsing."""
from pathlib import Path
import ast
import re
skill = Path('F:/OpenScience/wt/single-cell-data-io/single-cell/data-io/SKILL.md')
text = skill.read_text(encoding='utf-8')
ast.parse((skill.parent/'examples/load_10x_scanpy.py').read_text(encoding='utf-8'))
py_blocks = re.findall(r'```python\n(.*?)```', text, flags=re.S)
for i, block in enumerate(py_blocks, 1): ast.parse(block, filename=f'SKILL.md python block {i}')
r_blocks = re.findall(r'```r\n(.*?)```', text, flags=re.S)
out = Path('F:/OpenScience/audits/bio-single-cell-data-io/data/fp2_r_blocks')
out.mkdir(exist_ok=True)
for i, block in enumerate(r_blocks, 1): (out / f'block_{i}.R').write_text(block, encoding='utf-8')
print('python_blocks', len(py_blocks), 'r_blocks', len(r_blocks), 'PASS input9_python')
