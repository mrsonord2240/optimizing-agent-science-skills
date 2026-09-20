"""Tiny assertion recorder: prints PASS/FAIL lines and appends them to out/results.jsonl.
Every audit claim check goes through check(); a check that is not printed did not happen."""
import json, os, subprocess, sys

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out', 'results.jsonl')
INPUT = os.environ.get('AUDIT_INPUT', '?')


def check(name, ok, detail=''):
    ok = bool(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} :: {detail}")
    with open(OUT, 'a', encoding='utf-8') as fh:
        fh.write(json.dumps({'input': INPUT, 'name': name, 'pass': ok, 'detail': str(detail)[:400]}) + '\n')
    return ok


def note(name, detail=''):
    """Informational observation (not a pass/fail)."""
    print(f"[NOTE] {name} :: {detail}")
    with open(OUT, 'a', encoding='utf-8') as fh:
        fh.write(json.dumps({'input': INPUT, 'name': name, 'pass': None, 'detail': str(detail)[:400]}) + '\n')


def sh(cmd, env=None):
    """Run a shell command, return (rc, stdout, stderr)."""
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=e, executable='/bin/bash')
    return p.returncode, p.stdout, p.stderr
