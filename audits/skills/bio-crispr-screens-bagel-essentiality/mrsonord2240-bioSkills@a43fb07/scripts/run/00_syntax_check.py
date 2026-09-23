from pathlib import Path
import py_compile

for path in sorted(Path('.').glob('*.py')):
    py_compile.compile(str(path), doraise=True)
    print(f'PASS compiled {path.name}')
