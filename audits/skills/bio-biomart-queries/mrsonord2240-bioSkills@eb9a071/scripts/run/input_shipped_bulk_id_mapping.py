# Runs the SHIPPED examples/bulk_id_mapping.py file verbatim (copied unmodified from the
# fix worktree into skill_copy/), not the SKILL.md inline pattern -- this is the "shipped
# example" gate-8 / code-usability check, and specifically re-tests the fixer's claimed
# extra fix: the groupby/NaN collapse step (pd.notna() replacing filter(None, x)).
import subprocess, sys, pathlib

script = pathlib.Path('skill_copy/examples/bulk_id_mapping.py').resolve()
r = subprocess.run([sys.executable, script.name], capture_output=True, text=True, cwd=str(script.parent))
print('EXIT CODE:', r.returncode)
print('--- STDOUT ---')
print(r.stdout)
print('--- STDERR ---')
print(r.stderr)
sys.exit(r.returncode)
