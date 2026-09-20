"""Input 1a: run every shipped example AS SHIPPED from a copy (cwd = examples/). Records exit + stdout/stderr tail."""
import subprocess, sys, pathlib, os
ex = pathlib.Path(__file__).parent / 'skill' / 'examples'
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
for s in ['read_alignment.py','convert_formats.py','slice_alignment.py','batch_convert.py']:
    r = subprocess.run([sys.executable, s], cwd=ex, capture_output=True, text=True, env=env, encoding='utf-8')
    print(f'=== {s} exit={r.returncode}')
    print(r.stdout.strip()[-600:])
    print('STDERR tail:', r.stderr.strip().splitlines()[-1] if r.stderr.strip() else '')
