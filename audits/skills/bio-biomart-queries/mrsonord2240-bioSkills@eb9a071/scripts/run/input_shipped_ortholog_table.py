# Runs the SHIPPED examples/ortholog_table.py file verbatim.
import subprocess, sys, pathlib

script = pathlib.Path('skill_copy/examples/ortholog_table.py').resolve()
r = subprocess.run([sys.executable, script.name], capture_output=True, text=True, cwd=str(script.parent))
print('EXIT CODE:', r.returncode)
print('--- STDOUT ---')
print(r.stdout)
print('--- STDERR ---')
print(r.stderr)
sys.exit(r.returncode)
