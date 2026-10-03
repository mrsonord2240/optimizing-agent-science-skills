"""OC-008: run SKILL.md's batch snippet three ways with real subprocesses (fresh interpreters). Usage: python r2_cwd.py <Skill dir>"""
import re, sys, os, subprocess, tempfile
skill = os.path.abspath(sys.argv[1])
md = open(os.path.join(skill, 'SKILL.md'), encoding='utf-8').read()
code = [b for b in re.findall(r'```python\n(.*?)```', md, re.S) if 'batch_checks' in b][0]
pre = "import numpy as np\nrng=np.random.default_rng(0);X=rng.normal(size=(300,50));y=rng.integers(0,2,300);batch_labels=rng.integers(0,3,300)\n"
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
def go(label, cwd, src):
    r = subprocess.run([sys.executable, '-W', 'error::FutureWarning', '-c', pre + src], cwd=cwd, env=env, capture_output=True, text=True, timeout=300)
    print(f'[{label}] rc={r.returncode} last stderr: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""} | stdout tail: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""}')
go('relative, cwd=Skill dir', skill, code)
go('relative, cwd=foreign', tempfile.gettempdir(), code)
go('absolute scripts path, cwd=foreign', tempfile.gettempdir(), code.replace("'scripts'", repr(os.path.join(skill, 'scripts'))))
print('comment text as shipped:', [l.strip() for l in code.splitlines() if 'sys.path.insert' in l])
